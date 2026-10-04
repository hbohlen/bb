import json
import urllib.request

import websocket


PAGE_LIST = "http://127.0.0.1:40673/json"


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
  const canvas = document.getElementById('canvas');
  const rect = canvas.getBoundingClientRect();
  const readout = document.getElementById('readout');

  const tap = (gridX, gridY) => {
    const x = rect.left + gridX, y = rect.top + gridY;
    const opts = { bubbles: true, cancelable: true, clientX: x, clientY: y,
                   pointerId: 1, pointerType: 'touch', isPrimary: true };
    canvas.dispatchEvent(new MouseEvent('mousedown', opts));
    window.dispatchEvent(new MouseEvent('mousemove', opts));
    window.dispatchEvent(new MouseEvent('mouseup', opts));
  };

  // The grid's own bottom-left corner is the anchor the user cares about: it is
  // the point at the very bottom of the grid area. Its distance from the screen
  // bottom must equal the gap between the grid bottom and the viewport bottom,
  // not the grid height.
  const cases = [[0, 0], [0, rect.height], [0, rect.height / 2]];
  const got = [];
  for (const [x, y] of cases) {
    document.getElementById('reset').click();
    tap(x, y);
    const m = readout.textContent.match(/highest reach = (\d+) px/);
    got.push({ grid: [Math.round(x), Math.round(y)],
               reported: m ? Number(m[1]) : null });
  }

  const bottomGap = Math.round(innerHeight - rect.bottom);
  const topGap = Math.round(rect.top);
  return JSON.stringify({
    viewport: { w: innerWidth, h: innerHeight },
    grid: { top: topGap, height: Math.round(rect.height) },
    gapBelowGrid: bottomGap,
    cases: got,
    // Expected for each case, computed from the geometry rather than the page.
    expected: [
      { grid: [0, 0], fromBottom: innerHeight - rect.top },
      { grid: [0, rect.height], fromBottom: innerHeight - rect.bottom },
      { grid: [0, rect.height / 2], fromBottom: innerHeight - (rect.top + rect.height / 2) },
    ],
  }, null, 1);
})()
"""


def main() -> None:
    cdp = CDP(page_ws())
    cdp.send("Emulation.setDeviceMetricsOverride",
             {"width": 412, "height": 891, "deviceScaleFactor": 3.5, "mobile": True})
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.eval("location.reload()")
    cdp.eval("new Promise(r => setTimeout(r, 1500))")
    result = json.loads(cdp.eval(PROBE))
    print(json.dumps(result, indent=1))

    mismatches = [
        (c, e) for c, e in zip(result["cases"], result["expected"])
        if abs(c["reported"] - e["fromBottom"]) > 1
    ]
    if mismatches:
        raise SystemExit(f"geometry disagrees with the viewport: {mismatches}")
    print("\nfrom-bottom maths matches the viewport geometry")


if __name__ == "__main__":
    main()