#!/usr/bin/env python3
"""Convert a thumb-reach capture to millimetres, then to any target panel.

Two things make raw CSS pixels unusable as a reach budget, and this script
exists to catch both.

1. **A CSS pixel is not a physical size.** Android's are 1/160 inch, not the
   1/96 the CSS spec says, so the same count of CSS px is 1.67x smaller
   physically on Android than on a desktop. This is the mistake that makes a
   measured 406 px look like a reach figure when it is only 64 mm.

2. **A capture from the wrong panel cannot be converted at all.** Zoom and
   display-size settings scale a panel uniformly and preserve its aspect ratio,
   so a viewport whose aspect does not match the panel came from different
   hardware. No amount of arithmetic repairs that.

Usage:
    convert-reach.py --capture reach-capture.json
    convert-reach.py --reach-css 311 --viewport 384 682
"""

from __future__ import annotations

import argparse
import json
import sys

MM_PER_INCH = 25.4

# Android's CSS px are 1/160 inch. Verified against the S26 Ultra: a 412x891
# viewport at DPR 3.5 is 1442x3118 device px, which at 1/160 inch reconstructs
# the GSMArena panel of 1440x3120 at 500 PPI. The 1/96 CSS-spec convention would
# imply 382 PPI, which is wrong.
CSS_PX_PER_INCH = 160.0

# The device this effort is designed for. GSMArena: 1440 x 3120, 500 PPI, 6.9in.
TARGET = {"name": "Galaxy S26 Ultra", "w_px": 1440, "h_px": 3120, "ppi": 500.0}


def panel_mm(px: float, ppi: float) -> float:
    """A panel dimension in millimetres from its device pixels and density."""
    return px / ppi * MM_PER_INCH


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", help="reach-grid Copy result JSON")
    ap.add_argument("--reach-css", type=float, help="highest reach from bottom, CSS px")
    ap.add_argument("--viewport", nargs=2, type=float, metavar=("W", "H"), help="capture viewport, CSS px")
    ap.add_argument("--dpr", type=float, help="capture DPR; without it the physical panel is unknown")
    args = ap.parse_args()

    dpr = args.dpr
    if args.capture:
        data = json.load(open(args.capture))
        reach_css = float(data["highestFromBottom"])
        vw, vh = float(data["viewport"]["width"]), float(data["viewport"]["height"])
        dpr = dpr if dpr is not None else data["viewport"].get("dpr")
        print(f"capture       : {vw:g} x {vh:g} CSS px, dpr {dpr}, "
              f"maxTouchPoints {data['viewport'].get('maxTouchPoints')}")
        print(f"user agent    : {data.get('device', '')[:100]}")
    elif args.reach_css is not None and args.viewport:
        reach_css, (vw, vh) = args.reach_css, args.viewport
    else:
        ap.error("give --capture, or both --reach-css and --viewport")

    print(f"highest reach : {reach_css:g} CSS px from the bottom edge, "
          f"which is {reach_css / vh * 100:.1f}% of screen height")

    capture_aspect = vw / vh
    target_aspect = TARGET["w_px"] / TARGET["h_px"]
    drift = abs(capture_aspect - target_aspect) / target_aspect
    print()
    print("identity check")
    print(f"  capture viewport aspect     : {capture_aspect:.4f}   ({vw:g} / {vh:g})")
    print(f"  {TARGET['name']} panel aspect : {target_aspect:.4f}   ({TARGET['w_px']} / {TARGET['h_px']})")
    print(f"  drift                       : {drift * 100:.1f}%   "
          f"{'MATCHES' if drift < 0.02 else 'DOES NOT MATCH'}")
    if drift >= 0.02:
        print()
        print("  Zoom, display-size settings and browser insets all scale a panel uniformly and")
        print("  preserve its aspect. A different aspect is a different physical panel, so this")
        print("  capture cannot be converted to the target. Re-measure on the target device.")
        return 1

    if dpr:
        dev_w, dev_h = vw * dpr, vh * dpr
        # Compare device pixels against the panel, not PPI against PPI. A browser
        # rounds its CSS viewport, so 412 stands for the 411.4 the panel actually
        # gives, and a PPI comparison reports that rounding as a 12% density error.
        w_drift = abs(dev_w - TARGET["w_px"]) / TARGET["w_px"]
        h_drift = abs(dev_h - TARGET["h_px"]) / TARGET["h_px"]
        print(f"  at dpr {dpr:g} this is a {dev_w:.0f} x {dev_h:.0f} device-px panel; "
              f"{TARGET['name']} is {TARGET['w_px']} x {TARGET['h_px']}")
        print(f"  panel drift: {w_drift * 100:.1f}% wide, {h_drift * 100:.1f}% tall")
        if max(w_drift, h_drift) < 0.02:
            print(f"  -> that is the {TARGET['name']} panel. Capture is valid.")
        else:
            print(f"  -> NOT the {TARGET['name']} panel, despite the aspect matching.")

    if not dpr:
        print()
        print("  No DPR, so the physical panel size is unknown and no mm conversion is possible.")
        print("  The height fraction above is still valid, because it does not depend on DPR.")
        return 2

    frac = reach_css / vh
    target_h_mm = panel_mm(TARGET["h_px"], TARGET["ppi"])
    target_h_css = target_h_mm / MM_PER_INCH * CSS_PX_PER_INCH
    reach_on_target_css = frac * target_h_css

    print()
    print(f"target panel : {TARGET['h_px']} px at {TARGET['ppi']:.0f} PPI = {target_h_mm:.1f} mm tall, "
          f"about {target_h_css:.0f} CSS px at 1/{CSS_PX_PER_INCH:.0f} inch")
    print(f"reach        : {frac * 100:.1f}% of height = {frac * target_h_mm:.0f} mm "
          f"= {reach_on_target_css:.0f} CSS px")

    header_frac = 849 / 891
    print()
    print("against the thread header, which sits 849/891 = "
          f"{header_frac * 100:.1f}% of screen height up")
    print(f"  header is {header_frac / frac:.2f}x too far, right hand at {0.456 / frac * 100:.0f}% reach")
    return 0


if __name__ == "__main__":
    sys.exit(main())
