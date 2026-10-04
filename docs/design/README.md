# Design record

This directory holds the design and research record for this fork. It is not part
of upstream bb and is never expected to merge cleanly — that is the point of
keeping it namespaced here rather than at the repository root.

The fork itself is `github.com/hbohlen/bb`, forked from `get-bb/bb`. Upstream
changes arrive with:

```bash
git fetch upstream && git merge upstream/main
```

Anything under `docs/design/` is ours and will conflict only if upstream starts
shipping a file of the same path.

## What is here

| File | What it settles |
|---|---|
| `PRODUCT.md` | What bb is, who it is for, and the constraints future work must preserve. Authored with `/impeccable init`. |
| `GLOSSARY.md` | The reach / hit / reachability distinction the whole effort depends on. |
| `research/adhd-ui-design.md` | Evidence review for UI and typography for ADHD. Peer-reviewed and standard sources, with folklore flagged. |
| `research/adhd-ui-design-short.md` | Three-minute decision companion to the above. |
| `research/bb-theming-capabilities.md` | Verified token reference: every bb CSS custom property, its derivation, and what a theme cannot change. |
| `research/bb-touch-target-ownership.md` | Which bb layer draws the sub-44px controls, measured on a Galaxy S26 Ultra. |
| `research/bb-touch-target-ownership-045.md` | The same measurement re-run against the fork's own 0.45.0 dev server. Corrects two measurement bugs and records the fork baseline. |
| `research/thumb-reach-measured.md` | Thumb reach measured on the device, both hands, as a fraction of screen height. Replaces the unsourced 620 px figure. Flags that the capture was not the S26 Ultra and which figures therefore do not transfer. |
| `research/touch-target-floor-44.md` | The 36 → 44 touch-target floor, implemented and measured. Controls meeting 44px went from 1 to 40 of 55. |
| `research/reach-grid.html` | The 20 px grid used to measure it. Open it on the device, drag to the limit of reach without shifting your hand, then Copy result. |
| `agents/` | The issue-tracker, triage-label, and domain-doc conventions this effort uses. |
| `scripts/` | The measurement scripts that produced `research/bb-touch-target-ownership.md`, plus their captured output. All are rerunnable against a running bb. |

## Reproducing the touch-target audit

The audit needs a running bb and a CDP websocket. Start bb, note the port, then
edit the `PAGE_LIST` constant at the top of each script to match:

```bash
cd docs/design/scripts
./launch-s26.sh                                   # headless Chrome, CDP on :40673
python open-thread-s26.py /projects/<proj>/threads/<thr>
python measure-s26.py > s26.json                   # viewport, tokens, per-control sizes
python short-s26.py > short-s26.json               # the under-44 list, grouped
python group-s26.py                                # buckets the undersized controls by cause
python owner-s26.py                                # locates the controls with no sizing class
```

Every script sets `Emulation.setDeviceMetricsOverride` and
`Emulation.setTouchEmulationEnabled` on the connection it measures through, and
every script aborts if `(pointer: coarse)` is false at measurement time. That
abort is not paranoia. Touch emulation is per CDP session state, so a probe on a
fresh websocket measures a desktop size wearing a mobile user agent, and two
earlier passes recorded exactly that. See
`research/bb-touch-target-ownership-045.md`.

`measure-s26.py` forces touch emulation through `Emulation.setTouchEmulationEnabled`
because a device profile alone leaves `navigator.maxTouchPoints` at 0, which
makes `(pointer: coarse)` false and every measurement a desktop size wearing a
mobile user agent. The CDP websocket needs `suppress_origin=True` or Chrome
rejects the connection with a 403, and the browser needs
`--remote-allow-origins='*'` for the same reason.

## Converting a reach capture

`convert-reach.py` turns the JSON from `reach-grid.html` into millimetres, and
refuses any capture it cannot honestly convert:

```bash
python convert-reach.py --capture reach-capture.json
```

It exits 1 when the capture's viewport aspect does not match the target panel,
because zoom and display-size settings scale a panel uniformly and preserve its
aspect, so a mismatch means different hardware. It exits 2 when the capture has
no DPR, because the physical panel is then unknown.

**Reach is a fraction of screen height, not a count of CSS pixels.** Android CSS
px are 1/160 inch, not the 1/96 the CSS specification uses, so pixel counts are
not physical distances and are not comparable between devices.

`check-reach-conversion.py` guards the conversions in `convert-reach.py`
against the GSMArena panel spec, and confirms the tool rejects the bad capture.
Run it after touching either file:

```bash
python check-reach-conversion.py
```

## Where the decisions live

Open decision tickets are tracked on the BB Tasks board under the `BB` project,
not in this repository. The design record explains what was decided and why; the
board tracks what is still open.

## The finding that shapes everything

The user's failure mode is **reach**, not hit. Hand anchored at the bottom of the
phone, lying on their stomach, reaching a top-of-screen control means tilting the
phone and shifting the hand up and back down. Re-gripping is the correct remedy
for a reach failure and the useless remedy for a hit failure, which is how the
failure mode was identified.

Two consequences follow:

1. Distance and effective hit size degrade **together** at the top of the screen,
   because tilting the phone both moves the screen away from the hand and
   foreshortens it. Reach and target size must be fixed in one change.
2. bb's coarse-pointer sizing tops out at 36px and stops 8px short of 44. One
   constant in `packages/shared-ui/src/components/ui/coarse-pointer-sizing.ts`
   is the highest-leverage change available.
