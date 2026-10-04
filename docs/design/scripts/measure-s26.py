"""Measure bb's compact-viewport controls on the Galaxy S26 Ultra, in one pass.

Sets device metrics and touch emulation on the same connection it measures
through. That ordering is the whole point of this script: Chrome's
`Emulation.setTouchEmulationEnabled` is per CDP session state that a later
connection does not inherit, so a probe on a fresh connection measures
`(pointer: coarse)` as false, bb's coarse-pointer overrides never fire, and every
control reports its desktop size. Two earlier passes produced 28x28 and 20x20
from exactly that mistake.

Run: python docs/design/scripts/measure-s26.py
"""

import json
import sys
import urllib.request

import websocket


PAGE_LIST = "http://127.0.0.1:40673/json"

# Native panel 1440x3120 at 500 PPI lands in Android's 560dpi bucket, so Chrome
# derives devicePixelRatio 3.5 and a CSS viewport of 412x891.
DEVICE = {"width": 412, "height": 891, "deviceScaleFactor": 3.5, "mobile": True}


def page_ws() -> str:
    with urllib.request.urlopen(PAGE_LIST) as resp:
        for t in json.load(resp):
            if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                return t["webSocketDebuggerUrl"]
    raise SystemExit("no page target found")


class CDP:
    def __init__(self, url: str):
        self.ws = websocket.create_connection(url, timeout=30, suppress_origin=True)
        self.n = 0

    def send(self, method: str, params: dict | None = None) -> dict:
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                return msg.get("result", {})

    def eval(self, expr: str):
        return self.send(
            "Runtime.evaluate",
            {"expression": expr, "returnByValue": True, "awaitPromise": True},
        )["result"].get("value")


PROBE = r"""
(() => {
  const cs = getComputedStyle(document.documentElement);
  const rows = [...document.querySelectorAll("button,[role=button]")].map(b => {
    const r = b.getBoundingClientRect();
    const cls = (b.className || "").split(/\s+/).filter(Boolean);
    return {
      l: (b.getAttribute("aria-label") || b.getAttribute("title") || "")
           .replace(/\s+/g, " ").slice(0, 34),
      tid: b.getAttribute("data-testid") || "-",
      w: Math.round(r.width), h: Math.round(r.height),
      fb: Math.round(innerHeight - r.bottom),
      coarseOverride: cls.some(c => /pointer-coarse/.test(c)),
      literal: cls.filter(c => /\[/.test(c) && !/pointer-coarse/.test(c)).join(" "),
    };
  }).filter(x => x.w > 0 && x.h > 0);

  const tally = arr => { const o = {}; arr.forEach(x => {
      const k = x.h + "x" + x.w; o[k] = (o[k] || 0) + 1; }); return o; };
  const shell = rows.filter(x => !x.tid.startsWith("plugin-"));
  const plugin = rows.filter(x => x.tid.startsWith("plugin-"));

  return JSON.stringify({
    viewport: {w: innerWidth, h: innerHeight,
               dpr: devicePixelRatio,
               maxTouchPoints: navigator.maxTouchPoints,
               pointerCoarse: matchMedia("(pointer:coarse)").matches,
               widthUnder48rem: matchMedia("(width<48rem)").matches},
    tokens: {sidebarControl: cs.getPropertyValue("--bb-sidebar-control-size").trim(),
             sidebarRowHeight: cs.getPropertyValue("--bb-sidebar-row-height").trim(),
             textBase: cs.getPropertyValue("--text-base").trim(),
             textSm: cs.getPropertyValue("--text-sm").trim(),
             textXs: cs.getPropertyValue("--text-xs").trim(),
             text2xs: cs.getPropertyValue("--text-2xs").trim(),
             spacing: cs.getPropertyValue("--spacing").trim(),
             iconStrokeWidth: cs.getPropertyValue("--icon-stroke-width").trim(),
             safeAreaBottom: cs.getPropertyValue("--bb-safe-area-bottom").trim()},
    counts: {visible: rows.length,
             under44: rows.filter(x => x.h < 44).length,
             atLeast44: rows.filter(x => x.h >= 44).length,
             shell: shell.length, shellUnder44: shell.filter(x => x.h < 44).length,
             plugin: plugin.length, pluginUnder44: plugin.filter(x => x.h < 44).length,
             hasCoarseOverride: rows.filter(x => x.coarseOverride).length,
             hardcodedLiteral: rows.filter(x => x.literal).length},
    shellSizes: tally(shell),
    topBand: rows.filter(x => x.fb > 600).map(x => [x.l, x.w + "x" + x.h, x.fb]),
    composer: rows.filter(x => x.fb > 0 && x.fb <= 70)
                   .map(x => [x.l, x.w + "x" + x.h, x.fb]),
    literalGroups: rows.filter(x => x.literal)
      .reduce((o, x) => { const k = x.literal;
        o[k] = o[k] || {n: 0, size: x.w + "x" + x.h, sample: x.l, fb: x.fb};
        o[k].n++; return o; }, {}),
    pluginRows: plugin.map(x => [x.l, x.w + "x" + x.h, x.fb]),
  }, null, 1);
})()
"""


def main() -> None:
    cdp = CDP(page_ws())
    cdp.send("Emulation.setDeviceMetricsOverride", DEVICE)
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.send("Emulation.setEmitTouchEventsForMouse",
             {"enabled": True, "configuration": "mobile"})
    cdp.eval("new Promise(r => setTimeout(r, 800))")
    report = json.loads(cdp.eval(PROBE))
    if not report["viewport"]["pointerCoarse"]:
        raise SystemExit("pointer:coarse is false; the measurement would be a "
                         "desktop size wearing a mobile user agent")
    print(json.dumps(report, indent=1))
    print(f"\nmeasured {report['viewport']}", file=sys.stderr)


if __name__ == "__main__":
    main()