"""Drive reach-grid.html with real touch events and report what it captures.

Synthetic MouseEvents prove the handlers run; they do not prove a finger works.
This dispatches Input.dispatchTouchEvent at the S26 profile, which is the same
path a real tap takes through the browser's input pipeline, and reads back the
mark the page recorded.

Run: python docs/design/scripts/check-reach-grid-touch.py
"""

import json
import urllib.request

import websocket


PAGE_LIST = "http://127.0.0.1:40673/json"
GRID = "http://127.0.0.1:8901/reach-grid.html"


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


def tap(cdp: CDP, x: float, y: float) -> None:
    for kind in ("touchStart", "touchEnd"):
        cdp.send("Input.dispatchTouchEvent", {
            "type": kind,
            "touchPoints": [] if kind == "touchEnd" else
                [{"x": x, "y": y, "radiusX": 12, "radiusY": 12, "force": 1}],
        })


def main() -> None:
    cdp = CDP(page_ws())
    cdp.send("Emulation.setDeviceMetricsOverride",
             {"width": 412, "height": 891, "deviceScaleFactor": 3.5, "mobile": True})
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.send("Emulation.setEmitTouchEventsForMouse",
             {"enabled": False, "configuration": "mobile"})
    cdp.eval(f"location.assign('{GRID}')")
    cdp.eval("new Promise(r => { addEventListener('load', () => r(1), {once: true});"
             " setTimeout(() => r(0), 8000); })")
    cdp.eval("new Promise(r => setTimeout(r, 1200))")

    geom = json.loads(cdp.eval(
        "(() => { const r = document.getElementById('canvas').getBoundingClientRect();"
        " return JSON.stringify({left: r.left, top: r.top, w: r.width, h: r.height}); })()"
    ))

    cdp.eval("document.getElementById('reset').click()")
    for gx, gy in ((60, 120), (180, 400)):
        tap(cdp, geom["left"] + gx, geom["top"] + gy)
        cdp.eval("new Promise(r => setTimeout(r, 150))")

    result = json.loads(cdp.eval(
        "JSON.stringify({"
        " marks: [...document.querySelectorAll('#marks .mark')]"
        "   .map(m => ({left: parseFloat(m.style.left), top: parseFloat(m.style.top)})),"
        " readout: document.getElementById('readout').textContent.trim(),"
        " status: document.getElementById('status').textContent.trim()"
        "})"
    ))

    print(json.dumps({"geometry": geom, "result": result}, indent=1))

    captured = sorted((m["left"], m["top"]) for m in result["marks"])
    expected = sorted([(60, 120), (180, 400)])
    if captured != expected:
        raise SystemExit(f"touch marks {captured}, expected {expected}")
    print("\nreal touch events record marks at the tapped grid coordinates")


if __name__ == "__main__":
    main()