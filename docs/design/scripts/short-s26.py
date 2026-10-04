"""List the controls that stay under 44px on a coarse pointer, and why.

The `max-md:pointer-coarse:` overrides in `coarse-pointer-sizing.ts` raise a
control to its coarse size, so any control still under 44px on a phone is a
control that either carries no override or overrides to something short. This
names them, because the 36px ceiling is a change to that one file and this is
the list it would have to cover.

Run: python docs/design/scripts/short-s26.py
"""

import json
import urllib.request

import websocket


PAGE_LIST = "http://127.0.0.1:40673/json"
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
  const groups = {};
  for (const b of document.querySelectorAll("button,[role=button]")) {
    const r = b.getBoundingClientRect();
    if (r.width === 0 || r.height === 0 || r.height >= 44) continue;
    const cls = (b.className || "").split(/\s+/).filter(Boolean);
    const coarse = cls.filter(c => c.startsWith("max-md:pointer-coarse:"));
    const key = (b.getAttribute("aria-label") || b.getAttribute("title") || "(unlabelled)")
                  .replace(/\s+/g, " ").slice(0, 30)
                + " | " + Math.round(r.width) + "x" + Math.round(r.height)
                + " | coarse=" + (coarse.join(" ") || "none");
    groups[key] = groups[key] || {
      n: 0, fb: Math.round(innerHeight - r.bottom),
      tid: b.getAttribute("data-testid") || "-",
    };
    groups[key].n++;
  }
  return JSON.stringify({
    coarseActive: matchMedia("(pointer: coarse)").matches,
    under44: Object.values(groups).reduce((a, g) => a + g.n, 0),
    groups: Object.entries(groups).sort((a, b) => b[1].n - a[1].n),
  }, null, 1);
})()
"""


def main() -> None:
    cdp = CDP(page_ws())
    cdp.send("Emulation.setDeviceMetricsOverride", DEVICE)
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.eval("new Promise(r => setTimeout(r, 800))")
    report = json.loads(cdp.eval(PROBE))
    if not report["coarseActive"]:
        raise SystemExit("pointer:coarse is false; run measure-s26.py first")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()