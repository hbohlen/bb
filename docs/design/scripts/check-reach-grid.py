import json
import subprocess
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
  const status = document.getElementById('status');
  const marks = document.getElementById('marks');

  const tap = (x, y) => {
    const opts = { bubbles: true, cancelable: true, clientX: x, clientY: y,
                   pointerId: 1, pointerType: 'touch', isPrimary: true };
    canvas.dispatchEvent(new MouseEvent('mousedown', opts));
    window.dispatchEvent(new MouseEvent('mousemove', opts));
    window.dispatchEvent(new MouseEvent('mouseup', opts));
  };

  const before = { readout: readout.textContent.trim(), marks: marks.children.length };
  tap(rect.left + 30, rect.top + 30);
  tap(rect.left + 30, rect.top + 30);
  tap(rect.left + 30, rect.top + 30);
  tap(rect.left + 30, rect.top + 30);

  return JSON.stringify({
    viewport: { width: innerWidth, height: innerHeight, dpr: devicePixelRatio,
                maxTouchPoints: navigator.maxTouchPoints,
                pointerCoarse: matchMedia('(pointer: coarse)').matches },
    canvasRect: { w: Math.round(rect.width), h: Math.round(rect.height),
                  top: Math.round(rect.top) },
    topTicks: [...document.querySelectorAll('#top .tick')].length,
    leftTicks: [...document.querySelectorAll('#left .tick')].length,
    firstTickTopX: document.querySelector('#top .tick')?.textContent,
    firstTickLeftY: document.querySelector('#left .tick')?.textContent,
    before,
    after: { readout: readout.textContent.trim(), marks: marks.children.length },
  }, null, 1);
})()
"""


def main() -> None:
    cdp = CDP(page_ws())
    cdp.send("Emulation.setDeviceMetricsOverride",
             {"width": 412, "height": 891, "deviceScaleFactor": 3.5, "mobile": True})
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.eval("location.assign('http://127.0.0.1:8901/reach-grid.html')")
    cdp.eval("new Promise(r => { addEventListener('load', () => r(1), {once: true});"
             " setTimeout(() => r(0), 8000); })")
    cdp.eval("new Promise(r => setTimeout(r, 1200))")
    print(cdp.eval(PROBE))
    probe = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                            "http://127.0.0.1:8901/reach-grid.html"], capture_output=True)
    print(f"\nserver responds {probe.stdout}")


if __name__ == "__main__":
    main()