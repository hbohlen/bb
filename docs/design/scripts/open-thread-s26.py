"""Put the CDP browser in a known state before measuring.

The fork's fresh profile lands on an unauthenticated shell with no thread
selected, which measures 14 controls instead of the ~57 a real screen has.
Measuring an empty screen would understate the problem, so this navigates to the
thread route the design record was written against.

The sidebar drawer is the other half of the state, because the thread-list rows
only exist when it is open. Without an explicit choice here the control count
drifts between runs and every comparison against a previous figure is
meaningless, so the drawer is set deliberately and the resulting state is
printed.

Run: python docs/design/scripts/open-thread-s26.py <thread-url> [open|closed]
"""

import json
import sys
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


def drawer_state(cdp) -> str:
    return cdp.eval(
        "document.querySelector('[data-sidebar=\"panel\"]')"
        "?.getAttribute('data-state') || 'absent'"
    )


def set_drawer(cdp, want: str) -> str:
    if drawer_state(cdp) == want:
        return want
    cdp.eval("document.querySelector('[data-sidebar=\"trigger\"]')?.click()")
    cdp.eval("new Promise(r => setTimeout(r, 1200))")
    return drawer_state(cdp)


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "/"
    want = sys.argv[2] if len(sys.argv) > 2 else "closed"
    if want not in ("open", "closed"):
        raise SystemExit(f"drawer must be open or closed, got {want!r}")

    cdp = CDP(page_ws())
    cdp.eval(f"location.assign({json.dumps(target)})")
    cdp.eval(
        "new Promise(r => { if (document.readyState === 'complete') r(1);"
        " else addEventListener('load', () => r(1), {once: true});"
        " setTimeout(() => r(0), 10000); })"
    )
    cdp.eval("new Promise(r => setTimeout(r, 5000))")
    state = set_drawer(cdp, want)
    if state != want:
        raise SystemExit(f"asked for the drawer {want}, browser reports {state}")
    count = cdp.eval("document.querySelectorAll('button,[role=button]').length")
    print(f"route    {cdp.eval('location.pathname')}")
    print(f"drawer   {state}")
    print(f"controls {count}")


if __name__ == "__main__":
    main()