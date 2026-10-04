"""Re-measure bb's compact-viewport controls on the Galaxy S26 Ultra.

The device is a Samsung Galaxy S26 Ultra: 1440 x 3120 native, 500 PPI, which
Android maps to a 560dpi bucket, so Chrome reports devicePixelRatio 3.5 and a CSS
viewport of 412 x 891. The previous pass used 412 x 915, which is 24 px too tall,
and had no source to check the hardcoded sizes against.

Touch emulation is forced rather than relying on a device profile, because a
profile alone leaves navigator.maxTouchPoints at 0 and bb's own
`(width<48rem) and (pointer:coarse)` query never fires. Without that query the
measurement is a desktop size wearing a mobile user agent.

Run: python docs/design/scripts/measure-s26.py
"""

import json
import urllib.request

import websocket


BROWSER_CDP = "ws://127.0.0.1:40673/devtools/browser/20e7bf83-d0a3-4289-bbfd-9044bddf76a0"
PAGE_LIST = "ws://127.0.0.1:40673/json"

# Native panel divided by the DPR Chrome derives from the 560dpi density bucket.
DEVICE = {"width": 412, "height": 891, "deviceScaleFactor": 3.5, "mobile": True}


def page_ws() -> str:
    with urllib.request.urlopen(PAGE_LIST.replace("ws://", "http://")) as resp:
        for t in json.load(resp):
            if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                return t["webSocketDebuggerUrl"]
    raise SystemExit("no page target found")


class CDP:
    def __init__(self, url: str):
        # suppress_origin: Chrome's CDP rejects a websocket carrying an Origin
        # header unless the browser was launched with --remote-allow-origins.
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
      literal: cls.filter(c => /\[/.test(c)).join(" "),
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
    # Wait for the load event rather than reloading blindly: a bare
    # location.reload() destroys the execution context the next evaluate()
    # targets, so the probe lands before the app has mounted.
    cdp.eval("new Promise(r => { if (document.readyState === 'complete') r(1);"
             " else addEventListener('load', () => r(1), {once: true});"
             " setTimeout(() => r(0), 8000); })")
    cdp.eval("new Promise(r => setTimeout(r, 4000))")
    print(cdp.eval(PROBE))
    print(f"\nBROWSER_CDP was {BROWSER_CDP}", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()