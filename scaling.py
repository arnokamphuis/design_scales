import math
import argparse
import sys

def calculate_scaling_factors(w0, h0, p, m, dpi=300, max_coverage=100):
    """
    Calculate uniform scaling factors for terrain images on A-series paper.
    
    Parameters:
    w0, h0: Original image dimensions in pixels
    p: Pixels in original image
    m: Meters that p pixels represent
    dpi: Target DPI for printing (default 300)
    max_coverage: Maximum coverage percentage in any direction (default 100)
    
    Returns:
    Dictionary with results for different paper sizes and scales
    """
    
    # A-series paper dimensions in mm (width x height)
    a_series_mm = {
        'A0': (841, 1189),
        'A1': (594, 841),
        'A2': (420, 594),
        'A3': (297, 420)
    }
    
    # Standard map scales
    standard_scales = [100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000]
    
    # Convert mm to inches, then to pixels at target DPI
    def mm_to_pixels(mm, dpi):
        inches = mm / 25.4
        return int(inches * dpi)
    
    # Calculate original scale: pixels per meter in the original image
    original_pixels_per_meter = p / m
    
    results = {}
    
    for paper_size, (w_mm, h_mm) in a_series_mm.items():
        # Convert paper dimensions to pixels at target DPI
        w_t = mm_to_pixels(w_mm, dpi)
        h_t = mm_to_pixels(h_mm, dpi)
        
        # Calculate effective paper dimensions based on max coverage
        effective_w_t = w_t * (max_coverage / 100)
        effective_h_t = h_t * (max_coverage / 100)
        # Consider both portrait (as defined) and landscape (rotated) orientations
        # Portrait orientation (as defined)
        max_scale_portrait = min(effective_w_t / w0, effective_h_t / h0)
        # Landscape orientation (swap paper width/height)
        max_scale_landscape = min(effective_h_t / w0, effective_w_t / h0)

        if max_scale_landscape > max_scale_portrait:
            # Use landscape orientation
            orientation = 'landscape'
            used_w_t, used_h_t = h_t, w_t  # swapped for calculations/display
            effective_used_w_t, effective_used_h_t = effective_h_t, effective_w_t
            max_scale_factor = max_scale_landscape
            oriented_mm = (h_mm, w_mm)
        else:
            orientation = 'portrait'
            used_w_t, used_h_t = w_t, h_t
            effective_used_w_t, effective_used_h_t = effective_w_t, effective_h_t
            max_scale_factor = max_scale_portrait
            oriented_mm = (w_mm, h_mm)
        
        results[paper_size] = {}
        
        for scale_ratio in standard_scales:
            # Calculate what scaling factor would be needed to achieve this target map scale
            # For map scale 1:scale_ratio, 1mm on paper should represent scale_ratio mm in reality
            # At dpi DPI: (dpi/25.4) pixels per mm on paper
            # We need: (dpi/25.4) pixels per mm on paper = (original_pixels_per_meter * scale_factor) pixels per scale_ratio mm in reality
            # So: (dpi/25.4) = (original_pixels_per_meter * scale_factor) * (scale_ratio/1000)
            # Therefore: scale_factor = (dpi/25.4) * 1000 / (original_pixels_per_meter * scale_ratio)
            required_scale_factor = (dpi / 25.4) * 1000 / (original_pixels_per_meter * scale_ratio)
            
            # Use the smaller of max possible scaling or required scaling
            if required_scale_factor <= max_scale_factor:
                # Target scale is achievable - use exact scaling for target scale
                final_scale_factor = required_scale_factor
                achieves_target_scale = True
            else:
                # Target scale would be too big - use maximum possible scaling
                final_scale_factor = max_scale_factor
                achieves_target_scale = False
            
            # Calculate final dimensions
            final_w = w0 * final_scale_factor
            final_h = h0 * final_scale_factor
            
            # Calculate actual map scale achieved
            # final_scale_factor scales the original pixels_per_meter
            final_pixels_per_meter = original_pixels_per_meter * final_scale_factor
            # At dpi DPI, we have (dpi/25.4) pixels per mm on paper
            # So 1mm on paper contains (dpi/25.4) pixels, representing (dpi/25.4)/final_pixels_per_meter meters
            # Scale ratio is how many mm in reality per mm on paper
            actual_scale_ratio = ((dpi / 25.4) / final_pixels_per_meter) * 1000
            
            # Calculate coverage percentage (relative to full paper size)
            coverage_x = final_w / used_w_t * 100
            coverage_y = final_h / used_h_t * 100
            
            results[paper_size][f'1:{scale_ratio}'] = {
                'total_scaling_factor': final_scale_factor,
                'final_dimensions_px': (int(final_w), int(final_h)),
                'paper_dimensions_px': (used_w_t, used_h_t),
                'paper_dimensions_mm': oriented_mm,
                'paper_orientation': orientation,
                'actual_scale': f'1:{int(round(actual_scale_ratio))}' if actual_scale_ratio > 0 else '1:ERROR',
                'coverage_x_percent': coverage_x,
                'coverage_y_percent': coverage_y,
                'fits_on_paper': True,  # Always true since we limit to max_scale_factor
                'achieves_target_scale': achieves_target_scale
            }
    
    return results

def print_results(results, w0, h0, p, m, verbose=False):
    """Print formatted results"""
    if not verbose:
        print("=" * 80)
    
    for paper_size, scales in results.items():
        if not scales:
            continue
            
        first_entry = scales[list(scales.keys())[0]]
        paper_px = first_entry['paper_dimensions_px']
        orientation = first_entry.get('paper_orientation', 'portrait')
        paper_mm = first_entry.get('paper_dimensions_mm')
        print(f"\n{paper_size} Paper ({orientation})", end="")
        if verbose and paper_mm:
            print(f" ({paper_mm[0]} x {paper_mm[1]} mm = {paper_px[0]} x {paper_px[1]} pixels at 300 DPI)")
        else:
            print()
        print("-" * 70)
        print(f"{'Target Scale':<12} {'Scaling Factor':<15} {'Final Size (px)':<18} {'Actual Scale':<12} {'Coverage %':<12} {'Exact Scale?'}")
        print("-" * 80)
        
        for scale_name, data in scales.items():
            # Normalize coverage display so swapping image width/height yields identical formatting
            cov_x = data['coverage_x_percent']
            cov_y = data['coverage_y_percent']
            if cov_x <= cov_y:
                coverage = f"{cov_x:.1f}x{cov_y:.1f}"
            else:
                coverage = f"{cov_y:.1f}x{cov_x:.1f}"
            # Use ASCII to avoid Windows console encoding issues
            exact_scale = "YES" if data.get('achieves_target_scale', False) else "NO"
            final_size = f"{data['final_dimensions_px'][0]}x{data['final_dimensions_px'][1]}"
            print(f"{scale_name:<12} {data['total_scaling_factor']:<15.4f} {final_size:<18} {data['actual_scale']:<12} {coverage:<12} {exact_scale}")
    
    # Show a practical example if we have results
    if results:
        print("\n" + "=" * 80)
        # Find first valid result for example
        for paper_size, scales in results.items():
            if scales:
                scale_name, data = next(iter(scales.items()))
                print(f"EXAMPLE: To print on {paper_size} paper at {scale_name} scale:")
                print(f"Apply scaling factor: {data['total_scaling_factor']:.4f}")
                print(f"Final image size: {data['final_dimensions_px'][0]} x {data['final_dimensions_px'][1]} pixels")
                cov_x = data['coverage_x_percent']
                cov_y = data['coverage_y_percent']
                if cov_x <= cov_y:
                    cov_a, cov_b = cov_x, cov_y
                else:
                    cov_a, cov_b = cov_y, cov_x
                print(f"Paper coverage: {cov_a:.1f}% x {cov_b:.1f}%")
                break

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Calculate scaling factors for terrain images on A-series paper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python terrain_scaling.py --width 2500 --height 1800 --pixels 1000 --meters 50
  python terrain_scaling.py -w 3000 --height 2000 -p 500 -m 25 --dpi 600
  python terrain_scaling.py -w 1920 --height 1080 -p 100 -m 10 --paper A2 --scale 2000
  python terrain_scaling.py -w 2500 --height 1800 -p 1000 -m 50 --max-coverage 80
        """)
    
    parser.add_argument('-w', '--width', type=int, required=True,
                        help='Original image width in pixels')
    parser.add_argument('--height', type=int, required=True,
                        help='Original image height in pixels')
    parser.add_argument('-p', '--pixels', type=int, required=True,
                        help='Number of pixels in original image representing the meter distance')
    parser.add_argument('-m', '--meters', type=float, required=True,
                        help='Distance in meters that the pixel count represents')
    parser.add_argument('--dpi', type=int, default=300,
                        help='Target DPI for printing (default: 300)')
    parser.add_argument('--paper', type=str, choices=['A0', 'A1', 'A2', 'A3'],
                        help='Show results only for specific paper size (default: show all)')
    parser.add_argument('--scale', type=int,
                        help='Show results only for specific scale ratio (e.g., 2000 for 1:2000)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed information including paper dimensions')
    parser.add_argument('--max-coverage', type=float, default=100.0,
                        help='Maximum coverage percentage in any direction (default: 100)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.width <= 0 or args.height <= 0:
        print("Error: Width and height must be positive integers", file=sys.stderr)
        sys.exit(1)
    
    if args.pixels <= 0 or args.meters <= 0:
        print("Error: Pixels and meters must be positive numbers", file=sys.stderr)
        sys.exit(1)
    
    if args.dpi <= 0:
        print("Error: DPI must be a positive integer", file=sys.stderr)
        sys.exit(1)
    
    if args.max_coverage <= 0 or args.max_coverage > 100:
        print("Error: Maximum coverage must be between 0 and 100 percent", file=sys.stderr)
        sys.exit(1)
    
    print("Terrain Image Scaling Calculator")
    print("=" * 40)
    print(f"Input parameters:")
    print(f"  Image size: {args.width} x {args.height} pixels")
    print(f"  Original scale: {args.pixels} pixels = {args.meters} meters ({args.pixels/args.meters:.2f} pixels/meter)")
    print(f"  Target DPI: {args.dpi}")
    if args.max_coverage < 100:
        print(f"  Maximum coverage: {args.max_coverage}%")
    
    if args.paper:
        print(f"  Paper filter: {args.paper} only")
    if args.scale:
        print(f"  Scale filter: 1:{args.scale} only")
    
    results = calculate_scaling_factors(args.width, args.height, args.pixels, args.meters, args.dpi, args.max_coverage)
    
    # Filter results if requested
    if args.paper:
        results = {args.paper: results[args.paper]}
    
    if args.scale:
        scale_key = f'1:{args.scale}'
        filtered_results = {}
        for paper_size, scales in results.items():
            if scale_key in scales:
                filtered_results[paper_size] = {scale_key: scales[scale_key]}
        results = filtered_results
    
    if not results or all(not scales for scales in results.values()):
        print(f"No results found for the specified filters.", file=sys.stderr)
        sys.exit(1)
    
    print_results(results, args.width, args.height, args.pixels, args.meters, verbose=args.verbose)