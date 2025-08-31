class TerrainScalingCalculator {
    constructor() {
        this.aSeries = {
            'A0': [841, 1189],
            'A1': [594, 841],
            'A2': [420, 594],
            'A3': [297, 420]
        };
        
        this.standardScales = [100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000];
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const calculateBtn = document.getElementById('calculateBtn');
        const clearBtn = document.getElementById('clearBtn');
        const inputs = document.querySelectorAll('input, select');

        calculateBtn.addEventListener('click', () => this.handleCalculate());
        clearBtn.addEventListener('click', () => this.handleClear());

        // Real-time validation
        inputs.forEach(input => {
            input.addEventListener('input', () => this.validateForm());
        });

        // Initialize form validation
        this.validateForm();
    }

    mmToPixels(mm, dpi) {
        const inches = mm / 25.4;
        return Math.floor(inches * dpi);
    }

    calculateScalingFactors(w0, h0, p, m, dpi = 300, maxCoverage = 100) {
        const originalPixelsPerMeter = p / m;
        const results = {};

        for (const [paperSize, [wMm, hMm]] of Object.entries(this.aSeries)) {
            const wT = this.mmToPixels(wMm, dpi);
            const hT = this.mmToPixels(hMm, dpi);

            const effectiveWT = wT * (maxCoverage / 100);
            const effectiveHT = hT * (maxCoverage / 100);

            // Portrait (as defined) max uniform scale
            const maxScalePortrait = Math.min(effectiveWT / w0, effectiveHT / h0);
            // Landscape (swap paper dimensions) max uniform scale
            const maxScaleLandscape = Math.min(effectiveHT / w0, effectiveWT / h0);

            let orientation, usedWT, usedHT, paperDimsMm;
            let maxScaleFactor;
            if (maxScaleLandscape > maxScalePortrait) {
                orientation = 'landscape';
                usedWT = hT; // swapped
                usedHT = wT;
                maxScaleFactor = maxScaleLandscape;
                paperDimsMm = [hMm, wMm];
            } else {
                orientation = 'portrait';
                usedWT = wT;
                usedHT = hT;
                maxScaleFactor = maxScalePortrait;
                paperDimsMm = [wMm, hMm];
            }
            
            results[paperSize] = {};
            
            for (const scaleRatio of this.standardScales) {
                const requiredScaleFactor = (dpi / 25.4) * 1000 / (originalPixelsPerMeter * scaleRatio);
                
                let finalScaleFactor, achievesTargetScale;
                if (requiredScaleFactor <= maxScaleFactor) {
                    finalScaleFactor = requiredScaleFactor;
                    achievesTargetScale = true;
                } else {
                    finalScaleFactor = maxScaleFactor;
                    achievesTargetScale = false;
                }
                
                const finalW = w0 * finalScaleFactor;
                const finalH = h0 * finalScaleFactor;
                
                const finalPixelsPerMeter = originalPixelsPerMeter * finalScaleFactor;
                const actualScaleRatio = ((dpi / 25.4) / finalPixelsPerMeter) * 1000;
                
                const coverageX = (finalW / usedWT) * 100;
                const coverageY = (finalH / usedHT) * 100;
                
                results[paperSize][`1:${scaleRatio}`] = {
                    totalScalingFactor: finalScaleFactor,
                    finalDimensionsPx: [Math.floor(finalW), Math.floor(finalH)],
                    paperDimensionsPx: [usedWT, usedHT],
                    paperOrientation: orientation,
                    paperDimensionsMm: paperDimsMm,
                    actualScale: `1:${Math.round(actualScaleRatio)}`,
                    coverageXPercent: coverageX,
                    coverageYPercent: coverageY,
                    fitsOnPaper: true,
                    achievesTargetScale: achievesTargetScale,
                    paperSizeMm: [wMm, hMm]
                };
            }
        }
        
        return results;
    }

    validateForm() {
        const width = document.getElementById('width').value;
        const height = document.getElementById('height').value;
        const pixels = document.getElementById('pixels').value;
        const meters = document.getElementById('meters').value;
        const dpi = document.getElementById('dpi').value;
        const maxCoverage = document.getElementById('maxCoverage').value;
        
        const calculateBtn = document.getElementById('calculateBtn');
        
        const isValid = width > 0 && height > 0 && pixels > 0 && meters > 0 && 
                       dpi >= 72 && maxCoverage > 0 && maxCoverage <= 100;
        
        calculateBtn.disabled = !isValid;
        calculateBtn.style.opacity = isValid ? '1' : '0.5';
    }

    handleCalculate() {
        try {
            const width = parseInt(document.getElementById('width').value);
            const height = parseInt(document.getElementById('height').value);
            const pixels = parseInt(document.getElementById('pixels').value);
            const meters = parseFloat(document.getElementById('meters').value);
            const dpi = parseInt(document.getElementById('dpi').value);
            const maxCoverage = parseFloat(document.getElementById('maxCoverage').value);
            const paperFilter = document.getElementById('paperFilter').value;
            const scaleFilter = document.getElementById('scaleFilter').value;

            // Validate inputs
            if (!this.validateInputs(width, height, pixels, meters, dpi, maxCoverage)) {
                return;
            }

            // Calculate results
            let results = this.calculateScalingFactors(width, height, pixels, meters, dpi, maxCoverage);
            
            // Apply filters
            results = this.applyFilters(results, paperFilter, scaleFilter);
            
            // Display results
            this.displayResults(results, { width, height, pixels, meters, dpi, maxCoverage, paperFilter, scaleFilter });
            
        } catch (error) {
            console.error('Calculation error:', error);
            this.showError('An error occurred during calculation. Please check your inputs.');
        }
    }

    validateInputs(width, height, pixels, meters, dpi, maxCoverage) {
        if (width <= 0 || height <= 0) {
            this.showError('Width and height must be positive integers');
            return false;
        }
        
        if (pixels <= 0 || meters <= 0) {
            this.showError('Pixels and meters must be positive numbers');
            return false;
        }
        
        if (dpi <= 0) {
            this.showError('DPI must be a positive integer');
            return false;
        }
        
        if (maxCoverage <= 0 || maxCoverage > 100) {
            this.showError('Maximum coverage must be between 0 and 100 percent');
            return false;
        }
        
        return true;
    }

    applyFilters(results, paperFilter, scaleFilter) {
        let filteredResults = { ...results };
        
        if (paperFilter) {
            filteredResults = { [paperFilter]: results[paperFilter] };
        }
        
        if (scaleFilter) {
            const scaleKey = `1:${scaleFilter}`;
            const newResults = {};
            for (const [paperSize, scales] of Object.entries(filteredResults)) {
                if (scales[scaleKey]) {
                    newResults[paperSize] = { [scaleKey]: scales[scaleKey] };
                }
            }
            filteredResults = newResults;
        }
        
        return filteredResults;
    }

    displayResults(results, inputParams) {
        const resultsCard = document.getElementById('resultsCard');
        const inputSummary = document.getElementById('inputSummary');
        const resultsContainer = document.getElementById('resultsContainer');
        const exampleCard = document.getElementById('exampleCard');

        // Show input summary
        this.displayInputSummary(inputSummary, inputParams);
        
        // Clear previous results
        resultsContainer.innerHTML = '';
        
        // Check if we have results
        const hasResults = Object.keys(results).length > 0 && 
                          Object.values(results).some(scales => Object.keys(scales).length > 0);
        
        if (!hasResults) {
            resultsContainer.innerHTML = '<p style="text-align: center; color: var(--text-secondary); padding: 2rem;">No results found for the specified filters.</p>';
            resultsCard.style.display = 'block';
            resultsCard.classList.add('fade-in');
            return;
        }

        // Display results for each paper size
        for (const [paperSize, scales] of Object.entries(results)) {
            if (Object.keys(scales).length === 0) continue;
            
            const paperSection = this.createPaperSection(paperSize, scales, inputParams.dpi);
            resultsContainer.appendChild(paperSection);
        }
        
        // Generate and display example
        this.generateExample(results, exampleCard);
        
        // Show results with animation
        resultsCard.style.display = 'block';
        resultsCard.classList.add('fade-in');
        exampleCard.style.display = 'block';
        exampleCard.classList.add('fade-in');
    }

    displayInputSummary(container, params) {
        const pixelsPerMeter = (params.pixels / params.meters).toFixed(2);
        
        container.innerHTML = `
            <h3><i class="fas fa-info-circle"></i> Input Parameters</h3>
            <p><strong>Image size:</strong> ${params.width} × ${params.height} pixels</p>
            <p><strong>Original scale:</strong> ${params.pixels} pixels = ${params.meters} meters (${pixelsPerMeter} pixels/meter)</p>
            <p><strong>Target DPI:</strong> ${params.dpi}</p>
            ${params.maxCoverage < 100 ? `<p><strong>Maximum coverage:</strong> ${params.maxCoverage}%</p>` : ''}
            ${params.paperFilter ? `<p><strong>Paper filter:</strong> ${params.paperFilter} only</p>` : ''}
            ${params.scaleFilter ? `<p><strong>Scale filter:</strong> 1:${params.scaleFilter} only</p>` : ''}
        `;
    }

    createPaperSection(paperSize, scales, dpi) {
        const section = document.createElement('div');
        section.className = 'paper-section';
        
        // Get paper dimensions for header
        const firstScale = Object.values(scales)[0];
    const [paperW, paperH] = firstScale.paperDimensionsMm || firstScale.paperSizeMm;
    const [pixelsW, pixelsH] = firstScale.paperDimensionsPx;
    const orientation = firstScale.paperOrientation || 'portrait';
        
        section.innerHTML = `
            <h3>${paperSize} Paper (${orientation})</h3>
            <p style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 1rem;">
                ${paperW} × ${paperH} mm = ${pixelsW} × ${pixelsH} pixels at ${dpi} DPI
            </p>
            <div class="results-table-container">
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Target Scale</th>
                            <th>Scaling Factor</th>
                            <th>Final Size (px)</th>
                            <th>Actual Scale</th>
                            <th>Coverage %</th>
                            <th>Exact Scale?</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.generateTableRows(scales)}
                    </tbody>
                </table>
            </div>
        `;
        
        return section;
    }

    generateTableRows(scales) {
        return Object.entries(scales).map(([scaleName, data]) => {
            // Normalize coverage order (smallest first) for rotation invariance
            const c1 = data.coverageXPercent;
            const c2 = data.coverageYPercent;
            const coverage = c1 <= c2
                ? `${c1.toFixed(1)}×${c2.toFixed(1)}`
                : `${c2.toFixed(1)}×${c1.toFixed(1)}`;
            const exactScale = data.achievesTargetScale ? 
                '<span class="scale-exact">✓</span>' : 
                '<span class="scale-approximate">✗</span>';
            const finalSize = `${data.finalDimensionsPx[0]}×${data.finalDimensionsPx[1]}`;
            
            return `
                <tr>
                    <td><strong>${scaleName}</strong></td>
                    <td>${data.totalScalingFactor.toFixed(4)}</td>
                    <td>${finalSize}</td>
                    <td><span class="${data.achievesTargetScale ? 'scale-exact' : 'scale-approximate'}">${data.actualScale}</span></td>
                    <td><span class="coverage-badge">${coverage}</span></td>
                    <td>${exactScale}</td>
                </tr>
            `;
        }).join('');
    }

    generateExample(results, exampleCard) {
        // Find first valid result for example
        for (const [paperSize, scales] of Object.entries(results)) {
            if (Object.keys(scales).length > 0) {
                const [scaleName, data] = Object.entries(scales)[0];
                
                document.getElementById('exampleContent').innerHTML = `
                    <div class="example-content">
                        <h4><i class="fas fa-print"></i> Example: Printing on ${paperSize} paper at ${scaleName} scale</h4>
                        <p><span class="example-highlight">Apply scaling factor:</span> ${data.totalScalingFactor.toFixed(4)}</p>
                        <p><span class="example-highlight">Final image size:</span> ${data.finalDimensionsPx[0]} × ${data.finalDimensionsPx[1]} pixels</p>
                        <p><span class="example-highlight">Paper coverage:</span> ${(Math.min(data.coverageXPercent, data.coverageYPercent)).toFixed(1)}% × ${(Math.max(data.coverageXPercent, data.coverageYPercent)).toFixed(1)}%</p>
                        <p><span class="example-highlight">Actual scale achieved:</span> ${data.actualScale}</p>
                        ${!data.achievesTargetScale ? 
                            '<p style="color: var(--warning-color); font-weight: 500; margin-top: 0.5rem;"><i class="fas fa-exclamation-triangle"></i> Note: Target scale could not be achieved due to paper size constraints.</p>' : 
                            '<p style="color: var(--success-color); font-weight: 500; margin-top: 0.5rem;"><i class="fas fa-check-circle"></i> Exact target scale achieved!</p>'
                        }
                    </div>
                `;
                break;
            }
        }
    }

    handleClear() {
        // Clear form inputs
        document.getElementById('width').value = '';
        document.getElementById('height').value = '';
        document.getElementById('pixels').value = '';
        document.getElementById('meters').value = '';
        document.getElementById('dpi').value = '300';
        document.getElementById('maxCoverage').value = '100';
        document.getElementById('paperFilter').value = '';
        document.getElementById('scaleFilter').value = '';
        
        // Hide results
        document.getElementById('resultsCard').style.display = 'none';
        document.getElementById('exampleCard').style.display = 'none';
        
        // Validate form
        this.validateForm();
    }

    showError(message) {
        // Create a simple error display
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--error-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            max-width: 400px;
            font-size: 0.875rem;
            line-height: 1.4;
        `;
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
        
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

// Initialize the calculator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new TerrainScalingCalculator();
});