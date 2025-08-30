import math
import argparse
import sys

def calculate_scaling_factors(w0, h0, p, m, dpi=300):
    """
    Calculate uniform scaling factors for terrain images on A-series paper.
    
    Parameters:
    w0, h0: Original image dimensions in pixels
    p: Pixels in original image
    m: Meters that p pixels represent
    dpi: Target DPI for printing (default 300)
    
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
    standard_scales = [1000, 2000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000]
    
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
        
        results[paper_size] = {}
        
        for scale_ratio in standard_scales:
            # Calculate required pixels per meter for this scale
            # Scale 1:scale_ratio means 1 unit on map = scale_ratio units in reality
            # At 300 DPI: 300 pixels per inch = 300/25.4 pixels per mm = 11.811 pixels per mm
            # For 1:scale_ratio, 1mm on paper = scale_ratio mm in reality
            # So we need (300/25.4) / (scale_ratio/1000) pixels per meter
            target_pixels_per_meter = (dpi / 25.4) * 1000 / scale_ratio
            
            # Debug print for understanding
            if scale_ratio == 1000 and paper_size == 'A3':
                print(f"DEBUG: For 1:{scale_ratio} scale:")
                print(f"  1mm on paper = {scale_ratio}mm in reality")
                print(f"  So 1m in reality = {1000/scale_ratio}mm on paper")
                print(f"  At {dpi} DPI: {dpi/25.4:.4f} pixels per mm")
                print(f"  So 1m in reality = {(dpi/25.4) * (1000/scale_ratio):.4f} pixels on paper")
                print(f"  target_pixels_per_meter: {target_pixels_per_meter:.4f}")
                print()
            
            # Calculate the scaling factor needed to achieve target scale
            scale_factor_for_map_scale = target_pixels_per_meter / original_pixels_per_meter
            
            # Apply this scaling to original image dimensions
            scaled_w0 = w0 * scale_factor_for_map_scale
            scaled_h0 = h0 * scale_factor_for_map_scale
            
            # Calculate uniform scaling to fit maximally on paper
            # This is the additional scaling to fit the scaled image on paper
            scale_x = w_t / scaled_w0
            scale_y = h_t / scaled_h0
            fit_scale = min(scale_x, scale_y)  # Uniform scaling to fit
            
            # Total scaling factor to apply to original image
            total_scale = scale_factor_for_map_scale * fit_scale
            
            # Final dimensions after all scaling
            final_w = w0 * total_scale
            final_h = h0 * total_scale
            
            # Calculate actual scale achieved (might be slightly different due to fitting)
            final_pixels_per_meter = original_pixels_per_meter * total_scale
            actual_scale_ratio = (dpi / 25.4) / final_pixels_per_meter
            
            # Debug information for troubleshooting
            if scale_ratio == 1000 and paper_size == 'A3':  # Debug first case
                print(f"DEBUG for 1:1000 on A3:")
                print(f"  original_pixels_per_meter: {original_pixels_per_meter:.4f}")
                print(f"  target_pixels_per_meter: {target_pixels_per_meter:.4f}")
                print(f"  scale_factor_for_map_scale: {scale_factor_for_map_scale:.4f}")
                print(f"  fit_scale: {fit_scale:.4f}")
                print(f"  total_scale: {total_scale:.4f}")
                print(f"  final_pixels_per_meter: {final_pixels_per_meter:.4f}")
                print(f"  dpi / 25.4: {dpi / 25.4:.4f}")
                print(f"  actual_scale_ratio: {actual_scale_ratio:.4f}")
                print(f"  target scale ratio was: {scale_ratio}")
                print()
            
            # Calculate coverage percentage
            coverage_x = final_w / w_t * 100
            coverage_y = final_h / h_t * 100
            
            results[paper_size][f'1:{scale_ratio}'] = {
                'total_scaling_factor': total_scale,
                'final_dimensions_px': (int(final_w), int(final_h)),
                'paper_dimensions_px': (w_t, h_t),
                'actual_scale': f'1:{int(round(actual_scale_ratio))}' if actual_scale_ratio > 0 else '1:ERROR',
                'coverage_x_percent': coverage_x,
                'coverage_y_percent': coverage_y,
                'fits_on_paper': final_w <= w_t and final_h <= h_t
            }
    
    return results

def print_results(results, w0, h0, p, m, verbose=False):
    """Print formatted results"""
    if not verbose:
        print("=" * 80)
    
    for paper_size, scales in results.items():
        if not scales:
            continue
            
        paper_px = results[paper_size][list(scales.keys())[0]]['paper_dimensions_px']
        print(f"\n{paper_size} Paper", end="")
        if verbose:
            paper_mm = {'A0': (841, 1189), 'A1': (594, 841), 'A2': (420, 594), 'A3': (297, 420)}[paper_size]
            print(f" ({paper_mm[0]} x {paper_mm[1]} mm = {paper_px[0]} x {paper_px[1]} pixels at 300 DPI)")
        else:
            print()
        print("-" * 70)
        print(f"{'Target Scale':<12} {'Scaling Factor':<15} {'Final Size (px)':<18} {'Actual Scale':<12} {'Coverage %':<12} {'Fits?'}")
        print("-" * 70)
        
        for scale_name, data in scales.items():
            coverage = f"{data['coverage_x_percent']:.1f}x{data['coverage_y_percent']:.1f}"
            fits = "✓" if data['fits_on_paper'] else "✗"
            final_size = f"{data['final_dimensions_px'][0]}x{data['final_dimensions_px'][1]}"
            print(f"{scale_name:<12} {data['total_scaling_factor']:<15.4f} {final_size:<18} {data['actual_scale']:<12} {coverage:<12} {fits}")
    
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
                print(f"Paper coverage: {data['coverage_x_percent']:.1f}% x {data['coverage_y_percent']:.1f}%")
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
    
    print("Terrain Image Scaling Calculator")
    print("=" * 40)
    print(f"Input parameters:")
    print(f"  Image size: {args.width} x {args.height} pixels")
    print(f"  Original scale: {args.pixels} pixels = {args.meters} meters ({args.pixels/args.meters:.2f} pixels/meter)")
    print(f"  Target DPI: {args.dpi}")
    
    if args.paper:
        print(f"  Paper filter: {args.paper} only")
    if args.scale:
        print(f"  Scale filter: 1:{args.scale} only")
    
    results = calculate_scaling_factors(args.width, args.height, args.pixels, args.meters, args.dpi)
    
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