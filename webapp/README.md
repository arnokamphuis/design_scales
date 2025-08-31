# Terrain Image Scaling Calculator - Web Application

A modern, responsive web application for calculating optimal scaling factors when printing terrain images on A-series paper at various map scales.

![Terrain Scaling Calculator](https://img.shields.io/badge/Status-Active-brightgreen) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

## Features

### 🎯 **Core Functionality**
- Calculate scaling factors for terrain images on A0, A1, A2, and A3 paper sizes
- Automatic orientation optimization (chooses portrait vs. landscape for maximum feasible scale)
- Support for 15 standard map scales (1:100 to 1:500,000, now including 1:150)
- Customizable print DPI (72-1200 DPI)
- Maximum coverage control (1-100%)
- Real-time calculation and validation

### 🎨 **Modern Interface**
- Clean, responsive design that works on all devices
- Interactive form with real-time validation
- Professional results tables with clear indicators
- Example usage generation
- Smooth animations and transitions

### 📊 **Detailed Results**
- Scaling factors for each paper size and map scale combination
- Final image dimensions in pixels
- Actual scale achieved (when target scale isn't possible)
- Paper coverage percentages (after orientation selection)
- Orientation shown in each paper section header (e.g. "A3 Paper (landscape)")
- Clear indication of exact vs. approximate scales

### ⚡ **User Experience**
- No installation required - runs in any modern web browser
- Instant calculations with client-side processing
- Form validation with helpful error messages
- Responsive design for desktop, tablet, and mobile use

## How to Use

### 1. **Input Image Parameters**
- **Image Width/Height**: Enter the dimensions of your original terrain image in pixels
- **Reference Pixels**: Number of pixels in your image that represent a known distance
- **Reference Distance**: The real-world distance (in meters) that those pixels represent

### 2. **Configure Print Settings**
- **Print DPI**: Target resolution for printing (default: 300 DPI)
- **Max Coverage**: Maximum percentage of paper to use (default: 100%)
- **Paper Size Filter**: Optionally show results for specific paper size only
- **Scale Filter**: Optionally show results for specific map scale only

### 3. **Calculate and Review Results**
- Click "Calculate Scaling Factors" to generate results
- Review the results table showing scaling factors, final dimensions, and coverage
- Check the example usage section for practical application instructions
- Look for ✓ (exact scale achieved) or ✗ (approximate scale due to paper constraints)

## Understanding the Results

### Results Table Columns
- **Target Scale**: The desired map scale (e.g., 1:2000)
- **Scaling Factor**: Multiplication factor to apply when printing
- **Final Size (px)**: Resulting image dimensions after scaling
- **Actual Scale**: The map scale actually achieved (may differ from target)
- **Coverage %**: Percentage of the selected orientation's usable paper used (width × height)
- **Exact Scale?**: Whether the exact target scale was achieved

### Color Coding
- **Green ✓**: Target scale achieved exactly
- **Orange ✗**: Target scale not achievable, maximum possible scaling used

## Technical Details

### Browser Compatibility
- Modern browsers with ES6+ support
- Chrome 60+, Firefox 55+, Safari 12+, Edge 79+
- Responsive design works on mobile devices

### Technologies Used
- **HTML5**: Semantic markup with modern form elements
- **CSS3**: Grid/Flexbox layouts, custom properties, animations
- **JavaScript ES6+**: Classes, arrow functions, destructuring
- **Font Awesome**: Icons for better visual hierarchy
- **Google Fonts**: Inter font family for professional typography

### Performance
- Client-side calculations (no server required)
- Lightweight (~50KB total including assets)
- Responsive design optimized for all screen sizes

## Installation

### Option 1: Direct Usage
1. Download or clone the repository
2. Open `webapp/index.html` in any modern web browser
3. Start using the calculator immediately

### Option 2: Local Web Server (Recommended)
```bash
# Using Python 3
cd webapp
python -m http.server 8000

# Using Node.js
cd webapp
npx serve .

# Then open http://localhost:8000 in your browser
```

### Option 3: Deploy to Web Server
1. Upload the entire `webapp` folder to your web server
2. Access via your domain/webapp URL
3. No server-side processing required

## Example Usage

### Scenario: Printing a 2769×3253 pixel terrain image
- **Reference**: 2498 pixels = 114.21 meters in the real world
- **Goal**: Print at 1:2000 scale on A3 paper
- **Orientation Chosen**: Landscape (automatically selected to maximize scaling)

**Result**: Apply scaling factor 0.2700 to achieve exact 1:2000 scale with 21.3% × 17.7% paper coverage.

## File Structure

```
webapp/
├── index.html          # Main application page
├── css/
│   └── style.css      # Modern styling and responsive design
├── js/
│   └── calculator.js  # Calculation logic and UI interactions
└── README.md          # This documentation
```

## Advantages Over Command Line

- **User-Friendly**: No command line knowledge required
- **Visual**: Clear, formatted results with color coding
- **Interactive**: Real-time validation and immediate feedback
- **Accessible**: Works on any device with a web browser
- **Responsive**: Optimized for mobile and tablet use

## Future Enhancements

- [ ] Export results to PDF or CSV
- [ ] Save/load calculation presets
- [ ] Additional paper sizes (A4, custom sizes)
- [ ] Imperial units support
- [ ] Batch processing for multiple images
- [ ] Integration with image editing software
- [ ] Custom orientation lock (force portrait or landscape override)

## Support

For issues or questions:
1. Check the input validation messages for common problems
2. Ensure all required fields are filled with valid values
3. Verify that your image dimensions and reference measurements are accurate
4. Try different paper sizes or scales if current settings don't fit

---

**Built with ❤️ for cartographers, surveyors, and terrain visualization professionals.**