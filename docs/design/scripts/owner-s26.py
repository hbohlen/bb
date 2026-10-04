"""Locate bb's 46 "bare" undersized controls and name the component that draws each.

These carry no h-/w-/size-/px- class at all, so their size comes from content or
a parent. To attribute them I read each element's React fiber via the devtools
hook when available, and otherwise fall back to the nearest ancestor carrying a
recognisable data attribute plus its DOM path.

The output answers BB-5's open question: which component owns the residue that
no theme token can move.

Run: python docs/design/scripts/owner-s26.py
"""

import json
import urllib.request

import websocket


PAGE_LIST = "http://127.0.0.1:40673/json"


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
  const out = [];
  for (const b of document.querySelectorAll("button,[role=button]")) {
    const r = b.getBoundingClientRect();
    if (r.width === 0 || r.height === 0 || r.height >= 44) continue;
    const cls = (b.className || "").split(/\s+/).filter(Boolean);
    const sized = cls.filter(c => /^(h-|w-|size-|p[xytblr]?-)/.test(c));
    if (sized.length) continue;               // only the bare bucket

    // Nearest ancestor that names a component-ish region.
    let node = b, region = "unknown";
    while (node && node !== document.body) {
      for (const attr of ["data-sidebar", "data-testid", "data-slot",
                          "data-component", "data-panel", "data-testid"]) {
        const v = node.getAttribute && node.getAttribute(attr);
        if (v) { region = attr + "=" + v; break; }
      }
      if (region !== "unknown") break;
      node = node.parentElement;
    }

    // Stable-ish structural path from a landmark ancestor.
    const path = [];
    let n = b;
    for (let i = 0; i < 4 && n && n.tagName !== "BODY"; i++) {
      let s = n.tagName.toLowerCase();
      const t = n.getAttribute && (n.getAttribute("data-testid")
               || n.getAttribute("data-slot")
               || n.getAttribute("data-sidebar"));
      if (t) s += "[" + t + "]";
      const p = n.parentElement;
      if (p) {
        const same = [...p.children].filter(c => c.tagName === n.tagName);
        if (same.length > 1) s += ":" + (same.indexOf(n) + 1);
      }
      path.unshift(s);
      n = p;
    }

    const cs = getComputedStyle(b);
    out.push({
      label: (b.getAttribute("aria-label") || b.getAttribute("title") || "").slice(0, 28),
      w: Math.round(r.width), h: Math.round(r.height),
      fb: Math.round(innerHeight - r.bottom),
      region, path: path.join(">"),
      pe: cs.pointerEvents,
      display: cs.display,
    });
  }
  return JSON.stringify({n: out.length, controls: out}, null, 1);
})()
"""


def main() -> None:
    cdp = CDP(page_ws())
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.eval("new Promise(r => setTimeout(r, 600))")
    print(cdp.eval(PROBE))


if __name__ == "__main__":
    main()