#!/usr/bin/env python3
"""Guard the unit conversions in convert-reach.py.

Two conversion errors cost real time in this effort. Both were invisible in the
output because the numbers still looked plausible.

1. Treating a CSS pixel as 1/96 inch. Android's are 1/160 inch, so a reach
   figure in CSS px read as a physical distance is wrong by 1.67x.
2. Double-applying the DPR when deriving density from a device-pixel panel,
   which reported the S26 Ultra as a 65920 PPI device.

This asserts the conversions against the GSMArena panel spec, and asserts that
the tool refuses the wrong-panel capture rather than converting it.

Run: python3 check-reach-conversion.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent / "convert-reach.py"
MM_PER_INCH = 25.4
CSS_PX_PER_INCH = 160.0  # Android, not the CSS spec's 96
PANEL_W, PANEL_H, PANEL_PPI = 1440.0, 3120.0, 500.0

failures: list[str] = []


def check(name: str, got, want, tol: float = 0.005) -> None:
    ok = abs(got - want) <= tol
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: got {got}, want {want}")
    if not ok:
        failures.append(name)


def run(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True
    )


def tool_constant(name: str) -> float:
    """Read a constant out of the tool, so the guard tests the tool and not a copy."""
    src = SCRIPT.read_text()
    m = re.search(rf"^{name}\s*=\s*([0-9.]+)", src, re.MULTILINE)
    if not m:
        failures.append(f"{name} not found in {SCRIPT.name}")
        return float("nan")
    return float(m.group(1))


print("the tool's own CSS-px constant, not a copy of it")
css_in = tool_constant("CSS_PX_PER_INCH")
check("CSS_PX_PER_INCH", css_in, CSS_PX_PER_INCH)
if css_in == 96.0:
    failures.append("tool uses the 1/96 CSS-spec value, wrong on Android")
    print("  FAIL  1/96 is the CSS spec value; Android CSS px are 1/160 inch")

print()
print("the tool's own target panel, not a copy of it")
m = re.search(r'"h_px":\s*(\d+)', SCRIPT.read_text())
if not m:
    failures.append("target panel height not found in tool")
    print("  FAIL  target panel height not found in tool")
else:
    check("target panel height", float(m.group(1)), PANEL_H, tol=1)


print("panel geometry in millimetres")
panel_h_mm = PANEL_H / PANEL_PPI * MM_PER_INCH
panel_w_mm = PANEL_W / PANEL_PPI * MM_PER_INCH
check("panel height mm", panel_h_mm, 158.5, tol=0.2)
check("panel width mm", panel_w_mm, 73.2, tol=0.2)

print()
print("CSS px are 1/160 inch on Android, not 1/96")
check(
    "406 CSS px in mm",
    406 / CSS_PX_PER_INCH * MM_PER_INCH,
    64.4,
    tol=0.2,
)
# The 1/96 error is the one that produced the bogus "406 px is a reach figure".
check(
    "406 CSS px would be mm under 1/96 (the bug)",
    406 / 96 * MM_PER_INCH,
    107.4,
    tol=0.2,
)

print()
print("the audit viewport really is the S26 Ultra panel")
dev_w, dev_h = 412 * 3.5, 891 * 3.5
check("device width vs panel", dev_w, PANEL_W, tol=PANEL_W * 0.02)
check("device height vs panel", dev_h, PANEL_H, tol=PANEL_H * 0.02)

print()
print("reach survives as a height fraction")
# 311/682 from the capture, and the S26's own 426/891 from a valid capture.
check("capture fraction", 311 / 682, 0.4560, tol=0.001)
check("s26 fraction", 426 / 891, 0.4781, tol=0.001)

print()
print("tool refuses a capture from the wrong panel")
r = run("--reach-css", "311", "--viewport", "384", "682", "--dpr", "1.875")
check("exit code is 1", r.returncode, 1)
if "DOES NOT MATCH" not in r.stdout:
    failures.append("refusal message missing")
    print("  FAIL  refusal message missing")
else:
    print("  PASS  refusal message present")

print()
print("tool accepts a valid S26 capture and reports the right reach")
with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "cap.json"
    p.write_text(
        json.dumps(
            {
                "device": "SM-S948B Chrome/148 Mobile",
                "viewport": {"width": 412, "height": 891, "dpr": 3.5, "maxTouchPoints": 5},
                "marks": [{"x": 300, "y": 450, "fromBottom": 406}],
                "highestFromBottom": 426,
            }
        )
    )
    r = run("--capture", str(p))
    check("exit code is 0", r.returncode, 0)
    if "Capture is valid" not in r.stdout:
        failures.append("valid capture rejected")
        print("  FAIL  valid capture rejected")
    else:
        print("  PASS  valid capture accepted")
    if "76 mm" not in r.stdout:
        failures.append("reach mm missing or wrong")
        print("  FAIL  reach in mm missing from output")
    else:
        print("  PASS  reach reported in mm")

print()
print("tool reports density in a plausible range, not double-applied")
r = run("--reach-css", "426", "--viewport", "412", "891", "--dpr", "3.5")
density = re.findall(r"(\d+(?:\.\d+)?)\s*PPI", r.stdout)
print(f"  PPI values in output: {density}")
if not density:
    failures.append("no density reported at all")
    print("  FAIL  tool reported no density")
for val in density:
    v = float(val)
    if not 150 <= v <= 900:
        failures.append(f"density {v} outside 150-900 PPI")
        print(f"  FAIL  {v} PPI is not a real phone panel density")
    else:
        print(f"  PASS  {v} PPI is a plausible phone density")

print()
if failures:
    print(f"{len(failures)} FAILED: {failures}")
    sys.exit(1)
print("all reach-conversion guards passed")
