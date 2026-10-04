"""Group bb's still-undersized controls on the Galaxy S26 Ultra, by cause.

Runs against the live app with touch emulation forced on, then buckets every
control under 44px by the reason it stayed small:

  token-literal  the class list hardcodes a px value, so no theme token can move it
  token-driven   it reads a CSS var or a spacing utility, so a theme CAN move it
  bare           no sizing class at all; size comes from content or a parent

The point is to answer one question for BB-5: which of the undersized controls
are fixable by a theme, and which need a bb source change.

Run: python docs/design/scripts/group-s26.py
"""

import json
import re
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
  const VAR = /var\(--/;
  const PX_UTIL = /\b(h|w)-\[(\d+)px\]/;
  const SPACING_UTIL = /\b(h|w)-(\d+(?:\.\d+)?)\b/;

  const rows = [...document.querySelectorAll("button,[role=button]")].map(b => {
    const r = b.getBoundingClientRect();
    const cls = (b.className || "").split(/\s+/).filter(Boolean);
    const sizes = cls.filter(c => /^(h-|w-|size-|p[xytblr]?-)/.test(c));
    return {
      l: (b.getAttribute("aria-label") || b.getAttribute("title") || "")
           .replace(/\s+/g, " ").slice(0, 30),
      tid: b.getAttribute("data-testid") || "-",
      w: Math.round(r.width), h: Math.round(r.height),
      fb: Math.round(innerHeight - r.bottom),
      sizes,
    };
  }).filter(x => x.w > 0 && x.h > 0);

  const cause = x => {
    const px = x.sizes.filter(c => PX_UTIL.test(c));
    if (px.length) return "token-literal:" + px.join(" ");
    if (x.sizes.some(c => VAR.test(c))) return "token-driven:var";
    if (x.sizes.some(c => SPACING_UTIL.test(c))) return "token-driven:spacing";
    return "bare";
  };

  const small = rows.filter(x => x.h < 44);
  const buckets = {};
  small.forEach(x => {
    const k = cause(x);
    buckets[k] = buckets[k] || {n: 0, sizes: {}, samples: [], maxFb: 0};
    buckets[k].n++;
    const s = x.h + "x" + x.w;
    buckets[k].sizes[s] = (buckets[k].sizes[s] || 0) + 1;
    if (buckets[k].samples.length < 3) buckets[k].samples.push(x.l || "(unlabelled)");
    buckets[k].maxFb = Math.max(buckets[k].maxFb, x.fb);
  });

  return JSON.stringify({
    total: rows.length,
    under44: small.length,
    atLeast44: rows.filter(x => x.h >= 44).length,
    themeFixable: small.filter(x => !cause(x).startsWith("token-literal")).length,
    themeBlocked: small.filter(x => cause(x).startsWith("token-literal")).length,
    buckets,
  }, null, 1);
})()
"""


def main() -> None:
    cdp = CDP(page_ws())
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.eval("new Promise(r => setTimeout(r, 600))")
    print(cdp.eval(PROBE))


if __name__ == "__main__":
    main()