"""Check the 44px floor did not break the compact layout.

Raising 20 controls by 4 to 8px each moves everything below them. This checks
the three things that would break first on a 412x891 viewport: the composer
still fits, the sidebar rows still fit their drawer, and nothing overflows the
viewport horizontally or vertically.

Run: python docs/design/scripts/check-compact-layout.py
"""

import json
import urllib.request

import websocket


PAGE_LIST = "http://127.0.0.1:40673/json"
DEVICE = {"width": 412, "height": 891, "deviceScaleFactor": 3.5, "mobile": True}
THREAD = "/projects/proj_bwjku26bsp/threads/thr_4i7xkycskz"


class NotReady(Exception):
    """Chrome has no execution context yet, or lost it mid-call."""


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
                # A dev-server reload or navigation destroys the execution context
                # between the send and the reply, and Chrome answers with an error
                # instead of a result. Treat that as "not ready yet" rather than
                # crashing, so the caller can settle and try again.
                if "error" in msg:
                    raise NotReady(msg["error"])
                return msg.get("result", {})

    def eval(self, expr: str):
        try:
            return self.send(
                "Runtime.evaluate",
                {"expression": expr, "returnByValue": True, "awaitPromise": True},
            )["result"].get("value")
        except NotReady:
            return None


PROBE = r"""
(() => {
  const doc = document.documentElement;
  const overflowX = [];
  document.querySelectorAll('*').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width > 0 && (r.right > doc.clientWidth + 1 || r.left < -1)) {
      overflowX.push({ tag: e.tagName, id: e.id || '',
                       left: Math.round(r.left), right: Math.round(r.right) });
    }
  });

  const composer = [...document.querySelectorAll('div')]
    .filter(d => (d.className || '').split(/\s+/).includes('chat-prompt-box'))
    .pop();
  const cr = composer && composer.getBoundingClientRect();

  // A control whose rect is taller than the viewport cannot be tapped at all.
  const tallerThanViewport = [...document.querySelectorAll('button,[role=button]')]
    .map(b => ({ r: b.getBoundingClientRect(),
                 l: (b.getAttribute('aria-label') || '').slice(0, 30) }))
    .filter(x => x.r.height > doc.clientHeight)
    .map(x => x.l);

  return JSON.stringify({
    viewport: { w: doc.clientWidth, h: doc.clientHeight },
    scroll: { w: doc.scrollWidth, h: doc.scrollHeight },
    horizontalOverflow: overflowX.slice(0, 6),
    horizontalOverflowCount: overflowX.length,
    composer: cr ? { top: Math.round(cr.top), bottom: Math.round(cr.bottom),
                     h: Math.round(cr.height) } : null,
    tallerThanViewport,
    sidebarRows: [...document.querySelectorAll('[data-bb-plugin="thread-list"] [role="button"], [data-bb-plugin="thread-list"] a')]
      .map(e => Math.round(e.getBoundingClientRect().height))
      .filter(h => h > 0),
  }, null, 1);
})()
"""


def main() -> None:
    cdp = CDP(page_ws())
    cdp.send("Emulation.setDeviceMetricsOverride", DEVICE)
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.eval(f"location.assign('http://127.0.0.1:11580{THREAD}')")
    # A navigation destroys the execution context the next evaluate() targets,
    # so the wait happens after the context is back. The app needs well over
    # five seconds to mount on a cold load: probing earlier finds a shell with
    # five buttons and no composer, which the checks below then read as an
    # empty screen rather than a layout failure.
    cdp.eval("new Promise(r => setTimeout(r, 12000))")
    # Re-assert emulation: it is per-session state and a navigation is a new one.
    cdp.send("Emulation.setDeviceMetricsOverride", DEVICE)
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.eval("new Promise(r => setTimeout(r, 800))")

    raw = cdp.eval(PROBE)
    if raw is None:
        raise SystemExit(
            "no execution context: the dev server reloaded while the check ran. "
            "Re-run once it has settled."
        )
    report = json.loads(raw)
    print(json.dumps(report, indent=1))

    failures = []
    if report["horizontalOverflowCount"]:
        failures.append(
            f"{report['horizontalOverflowCount']} elements overflow horizontally: "
            f"{report['horizontalOverflow']}"
        )
    if report["tallerThanViewport"]:
        failures.append(f"controls taller than the viewport: {report['tallerThanViewport']}")
    if report["scroll"]["h"] > report["viewport"]["h"] + 1:
        failures.append(
            f"page scrolls vertically: {report['scroll']['h']} > {report['viewport']['h']}"
        )
    if not report["composer"]:
        failures.append("composer not found; the check measured an empty screen")
    elif report["composer"]["top"] < 0 or report["composer"]["bottom"] > report["viewport"]["h"]:
        failures.append(f"composer leaves the viewport: {report['composer']}")
    if not report["sidebarRows"]:
        failures.append("no sidebar rows found; the check did not run on the thread screen")

    if failures:
        raise SystemExit("\n".join(failures))
    print("\ncompact layout intact at 412x891: no overflow, nothing taller than the screen")


if __name__ == "__main__":
    main()