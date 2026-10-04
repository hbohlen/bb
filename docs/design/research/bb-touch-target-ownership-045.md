# Re-measurement on the fork — 2026-10-03

Every number in `bb-touch-target-ownership.md` came from bb 0.44.0's installed
DOM. This is the same measurement against the fork's own dev server, so the
36px-ceiling change starts from a baseline that is actually the code being
changed.

- **App under test:** the fork's dev server at `http://127.0.0.1:11580`, bb
  **0.45.0**, source `get-bb/bb` @ `c201f649`.
- **Route:** `/projects/proj_bwjku26bsp/threads/thr_4i7xkycskz`, the same thread
  screen the first pass measured.
- **Device:** Galaxy S26 Ultra profile, 412 × 891 @ DPR 3.5, touch emulation
  forced.

## A measurement bug that invalidated two earlier passes

Chrome's `Emulation.setTouchEmulationEnabled` is per CDP **session** state. A
probe on a new websocket does not inherit it, so `(pointer: coarse)` measures
false, bb's `max-md:pointer-coarse:` overrides never fire, and every control
reports its **desktop** size. Both earlier passes hit this: the first recorded
28 × 28 for the header buttons that the source says are `h-[28px] w-[28px]
max-md:pointer-coarse:h-[36px] max-md:pointer-coarse:w-[36px]`, and the second
recorded 28 × 28 while asserting coarse was true.

`measure-s26.py` now sets device metrics and touch emulation on the same
connection it measures through, and exits non-zero if `pointer: coarse` is false
at measurement time. Verified: with the override active, `Go back` computes
`36px` and its rect is 36 × 36.

The generated CSS was always correct. The rules
`.max-md\:pointer-coarse\:h-\[36px\] { height: 36px; }` exist inside
`@layer utilities` under `@media (width < 48rem) { @media (pointer: coarse) }`.

## Corrected figures

Measured with the drawer **open** on the fork instance, which holds a single
thread.

| | first pass (0.44.0) | this pass (0.45.0 fork) |
|---|---|---|
| visible controls | 83 | 59 |
| under 44 px tall | 82 | 58 |
| 44 px or taller | 1 | 1 |
| shell-drawn | 35 | 58 |
| plugin-marked (`data-testid="plugin-*"` buttons) | 2 | 1 |

**The 83-control pass is not reproducible on the fork, and the difference is
thread count, not a regression.** The fork instance has exactly one thread, so
the sidebar renders 3 thread-list rows where the 0.44.0 instance rendered 46.
The 0.44.0 figure therefore mixes a control-size problem with a
how-many-threads-are-in-the-sidebar problem, and the two should not be compared
directly. What carries over is the shape of the distribution, not the counts.

Drawer state is explicitly set by `open-thread-s26.py` and printed, because it
silently changes the DOM. With this instance's single thread it moves the count
by 0; on an instance with many threads it moves it by the row count.

**The ceiling is 36 px, and it is uniform.** Every shell control that carries a
coarse override lands on one of 36 (header and sidebar icon buttons), 40
(composer prompt actions), or 44 (feedback mode). Height distribution of the 58
still under 44:

| height | n |
|---|---|
| 20 | 9 |
| 22 | 3 |
| 24 | 2 |
| 28 | 11 |
| 32 | 2 |
| **36** | **20** |
| 40 | 9 |

So the 36px ceiling in `coarse-pointer-sizing.ts` is exactly the modal target
and covers 20 of 58 undersized controls on its own. The 28px cluster is
`Message actions` plus `Copy message` and `Reply in side chat`, and the 20/22px
items are timeline **rows**, not controls: they are full-width
`button.items-center` elements with `overflow-hidden text-left text-sm`, sized
by their content.

## What a theme can and cannot move, on the fork

From `group-s26.py`:

| bucket | n |
|---|---|
| `token-driven:spacing` | 16 |
| `bare` (content-sized) | 30 |
| `token-literal: h-[28px] w-[28px]` | 6 |
| `token-driven:var` | 6 |

A theme moves the 22 token-driven controls and none of the 36 others. Raising
the ceiling is upstream source work in one file,
`packages/shared-ui/src/components/ui/coarse-pointer-sizing.ts`, which has **77
consumers** across `apps`, `packages`, and `plugins` and exports 25
`COARSE_POINTER_*` constants. The sidebar row height is a separate token pair
(`--bb-sidebar-row-height` / `--bb-sidebar-row-height-coarse`) with 14
consumers, currently 1.75rem / 2.5rem, and its coarse value is 40px.

## Attribution of the bare bucket

`owner-s26.py` previously reported zero bare controls while `group-s26.py`
counted 25. Its filter skipped anything matching `^(h-|w-|size-|p-)`, which
swept up `size-5` and `px-2` rows. Fixed to use the same `cause()` test as
`group-s26.py`; it now reports 29, of which 27 sit under
`data-testid="app-layout-content-shell"` (the message timeline) and 2 under
`data-sidebar="group-label"`.

## Scripts

Run in this order from `docs/design/scripts/`:

```bash
./launch-s26.sh                                   # headless Chrome + CDP on :40673
python open-thread-s26.py /projects/<proj>/threads/<thr>
python measure-s26.py > s26.json                  # viewport, tokens, counts, sizes
python short-s26.py > short-s26.json              # the under-44 list, grouped
python group-s26.py > groups-s26.json             # by cause
python owner-s26.py > owner-s26.json              # bare bucket attribution
```

`launch-s26.sh` and `open-thread-s26.py` are new. Without them the measurement
runs against an empty shell that reports 14 controls, because a fresh profile
has no thread selected.

## Scripts changed

- `measure-s26.py` rewritten. Sets emulation and measures on one connection,
  fails loudly when coarse is false, reports which controls carry a coarse
  override, and excludes coarse-variant classes from the `literal` grouping so
  the cause buckets do not double-count a control that has both a desktop
  literal and a coarse override.
- `owner-s26.py` filter corrected to match `group-s26.py`'s `cause()`.
- `short-s26.py` added: the under-44 controls grouped by size and by the
  coarse override each one carries.

## Still open

1. **The 46-row sidebar case is untested on the fork.** The fork instance has
   one thread, so the largest single group of undersized controls in the 0.44.0
   audit never appeared here. Seed a few threads, or point the measurement at
   the 0.44.0 instance, before treating the distribution as the whole picture.
   That group is the one most likely to change when the ceiling moves, since
   thread rows read `--bb-sidebar-row-height-coarse`, not the header constants.
2. **The 20px timeline rows.** They are buttons, so they are tappable, but they
   are 20px tall and full width. Whether they are a control or a row is a
   product call, not a measurement.
3. **Safe area.** `--bb-safe-area-bottom` computes empty on the S26 profile,
   so nothing in the app is adding bottom inset for a home-indicator bar.