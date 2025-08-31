# Terrain Image Scaling Calculator (CLI & Web)

Comprehensive tooling (Python CLI + modern web app) to determine optimal uniform scaling factors for terrain (or any raster) images when printing on A-series paper at common cartographic map scales. Includes automatic portrait vs. landscape orientation optimization to maximize usable scaling while honoring a configurable maximum paper coverage.

## Key Features

### Algorithm / Core Logic
* Supports A0, A1, A2, A3 paper sizes (easily extendable)
* Evaluates both portrait and landscape orientations and automatically selects the one permitting the larger uniform scale factor (while respecting max coverage)
* 14 standard map scales: 1:100 through 1:500,000
* Precise conversion using target DPI (default 300; any positive integer)
* `--max-coverage` lets you restrict usage to a percentage of paper width & height (e.g. leave margins)
* Reports whether target map scale is exactly achieved or approximated due to physical paper limits
* Coverage percentages (width × height) relative to the chosen orientation

### CLI & Web Parity
The Python script (`scaling.py`) and the web UI (`webapp/js/calculator.js`) implement the same orientation-aware algorithm so that results stay consistent between command line and browser.

### Windows-Friendly Output
The CLI deliberately uses ASCII `YES` / `NO` instead of Unicode check marks to avoid Windows console encoding issues.

## How the Orientation Optimization Works

For each paper size:
1. Convert nominal paper dimensions (mm) to pixels at the target DPI.
2. Apply max coverage factor (percentage) to obtain effective usable width & height.
3. Compute potential uniform scaling factors for:
   * Portrait: `min(effective_width / image_width, effective_height / image_height)`
   * Landscape (swap paper sides): `min(effective_height / image_width, effective_width / image_height)`
4. Choose the orientation that yields the larger scaling factor.
5. For every requested map scale, compute the required scale factor. If it is <= the max possible factor (from step 4), it is achievable exactly; otherwise the algorithm falls back to the maximum possible, reporting the actual resulting scale.

## CLI Usage

```bash
python scaling.py -w <IMAGE_WIDTH_PX> --height <IMAGE_HEIGHT_PX> -p <REFERENCE_PIXELS> -m <REFERENCE_METERS> [--dpi <DPI>] [--paper A2] [--scale 2000] [--max-coverage 90] [-v]
```

Arguments:
* `-w, --width` (int, required) – original image width in pixels
* `--height` (int, required) – original image height in pixels
* `-p, --pixels` (int, required) – number of pixels in the image that correspond to the measured distance
* `-m, --meters` (float, required) – real-world meters represented by the pixel count
* `--dpi` (int, default 300) – target print DPI
* `--paper {A0,A1,A2,A3}` – filter to a single paper size
* `--scale <ratio>` – filter to a single target scale (e.g. 2000 for 1:2000)
* `--max-coverage` (float 0–100, default 100) – limit usable paper dimension percentage
* `-v, --verbose` – include paper mm & pixel dimensions

Example:
```bash
python scaling.py -w 2769 --height 3253 -p 2498 -m 114.21 --paper A3 --scale 2000
```

Sample (truncated) output:
```
Terrain Image Scaling Calculator
================================
Input parameters:
  Image size: 2769 x 3253 pixels
  Original scale: 2498 pixels = 114.21 meters (21.88 pixels/meter)
  Target DPI: 300
  Paper filter: A3 only
  Scale filter: 1:2000 only

A3 Paper (landscape)
----------------------------------------------------------------------
Target Scale  Scaling Factor  Final Size (px)    Actual Scale  Coverage %   Exact Scale?
--------------------------------------------------------------------------------
1:2000        0.2700          746x879            1:2000        21.3x17.7    YES
```

## Interpreting Results
* `Scaling Factor` – multiply original pixel dimensions by this factor to get the printed pixel dimensions (at target DPI).
* `Actual Scale` – the resulting map scale after applying the chosen scaling factor.
* `Coverage %` – percentage of paper width × height occupied (after orientation selection and coverage limit). When both percentages are below your max coverage, desired margins are maintained.
* `Exact Scale?` – `YES` means the requested map scale was feasible at or below the max orientation scaling; `NO` means it was capped by the paper constraints.

## Web Application
The browser-based interface (in `webapp/`) mirrors the logic and adds a responsive, monochrome UI with branding. Open `webapp/index.html` directly or serve it through any static server.

### Quick Run (Static)
```bash
cd webapp
python -m http.server 8000
# Open http://localhost:8000
```

### Result Sections
Each paper size section title includes the selected orientation, e.g. `A2 Paper (portrait)` or `A1 Paper (landscape)`.

## Docker / Podman Deployment

An Nginx-based container (port 4375) serves the static web application.

Build & run with Docker:
```bash
docker build -t terrain-scaling-web .
docker run --rm -p 4375:80 terrain-scaling-web
# Open http://localhost:4375
```

Using Podman (rootless example):
```bash
podman build -t terrain-scaling-web .
podman run --rm -p 4375:80 terrain-scaling-web
```

## Extending
* Add more paper sizes: extend the `a_series_mm` dict (and optionally UI dropdown logic).
* Add custom scale ratios: append to `standard_scales` in `scaling.py` and mirrored JS array.
* Add export features (PDF/CSV): hook into the webapp after results generation.

## Known Differences (CLI vs Web)
| Aspect              | CLI                               | Web UI                              |
|---------------------|------------------------------------|--------------------------------------|
| Exact indicator     | YES / NO (ASCII)                  | ✓ / ✗ (Unicode)                      |
| Orientation display | In section header                 | In section header                    |
| Filters             | Flags `--paper`, `--scale`        | Form dropdowns                       |
| Output format       | Plain text table                  | Styled HTML tables                   |

## License
See `LICENSE` for details.

## Attribution
Branding assets and logo used with permission of the author.

---
Built for precision printing workflows where maximizing map scale within physical constraints matters.
