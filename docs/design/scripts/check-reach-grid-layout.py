"""Check the reach grid is a sound measuring instrument at the S26 profile.

Three properties have to hold before any number it reports can be trusted:
no horizontal scroll (a scrolled grid reports positions that are not CSS
pixels), the grid fully inside the viewport, and every control at least 44px
tall. The last one matters because the instrument must not commit the defect
it is measuring.

Run: python docs/design/scripts/check-reach-grid-layout.py
"""

import json
import urllib.request

import websocket


PAGE_LIST = "http://127.0.0.1:40673/json"
GRID = "http://127.0.0.1:8901/reach-grid.html"
MIN_TARGET = 44


def page_ws() -> str:
    with urllib.request.urlopen(PAGE_LIST) as resp:
        for t in json.load(resp):
            if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                return t["webSocketDebuggerUrl"]
    raise SystemExit("no page target")


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
  const doc = document.documentElement;
  const canvas = document.getElementById('canvas').getBoundingClientRect();
  const offenders = [];
  document.querySelectorAll('*').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width > 0 && r.right > doc.clientWidth + 1) {
      offenders.push({ tag: e.tagName, id: e.id || '', right: Math.round(r.right) });
    }
  });
  return JSON.stringify({
    clientWidth: doc.clientWidth,
    scrollWidth: doc.scrollWidth,
    overflowX: doc.scrollWidth > doc.clientWidth,
    overflowing: offenders.slice(0, 5),
    grid: { top: Math.round(canvas.top), bottom: Math.round(canvas.bottom),
            w: Math.round(canvas.width), h: Math.round(canvas.height) },
    gridInsideViewport: canvas.bottom <= doc.clientHeight && canvas.top >= 0,
    buttons: [...document.querySelectorAll('button')].map(b => {
      const r = b.getBoundingClientRect();
      return { label: b.textContent.trim(), h: Math.round(r.height), w: Math.round(r.width) };
    }),
  }, null, 1);
})()
"""


def main() -> None:
    cdp = CDP(page_ws())
    cdp.send("Emulation.setDeviceMetricsOverride",
             {"width": 412, "height": 891, "deviceScaleFactor": 3.5, "mobile": True})
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.eval(f"location.assign('{GRID}')")
    cdp.eval("new Promise(r => { addEventListener('load', () => r(1), {once: true});"
             " setTimeout(() => r(0), 8000); })")
    cdp.eval("new Promise(r => setTimeout(r, 1200))")

    report = json.loads(cdp.eval(PROBE))
    print(json.dumps(report, indent=1))

    failures = []
    if report["overflowX"]:
        failures.append(f"horizontal scroll: {report['scrollWidth']} > {report['clientWidth']}, "
                        f"overflowing {report['overflowing']}")
    if not report["gridInsideViewport"]:
        failures.append(f"grid not inside the viewport: {report['grid']}")
    for b in report["buttons"]:
        if b["h"] < MIN_TARGET:
            failures.append(f"button {b['label']!r} is {b['h']}px tall, under {MIN_TARGET}")

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"\ninstrument is sound: no scroll, grid inside viewport, "
          f"every control at least {MIN_TARGET}px")


if __name__ == "__main__":
    main()