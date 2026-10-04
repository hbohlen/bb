# 36 → 44 touch-target floor — implemented and measured

The first code change of the one-handed mobile effort. It is independent of the
reach work: reach decides *where* controls go, this decides whether a reachable
control can be hit first time. Both are needed.

## What changed

| File | Change |
|---|---|
| `packages/shared-ui/src/components/ui/coarse-pointer-sizing.ts` | Every coarse-pointer size raised to the 44px floor: `h-9` → `h-11`, `h-10` → `h-11`, `h-[36px]` → `h-11`. Glyph and icon sizes raised to `size-6` (24px), the status dot to `size-4` (16px). |
| `apps/app/src/app.css` | New `--bb-touch-target-min: 44px`. `--bb-sidebar-control-size` now resolves from it instead of hardcoding 36px, so the floor has one source. |
| `apps/app/src/components/ui/theme.css` | `--bb-sidebar-row-height-coarse` 2.5rem → 2.75rem (40 → 44px). |
| `apps/app/src/components/ui/coarse-pointer-sizing.test.ts` | New. Fails if any button-shaped constant's coarse size drops below 44px, if any glyph drops below 20px, or if either CSS token moves off the floor. |
| `apps/app/src/components/thread/timeline/MessageActionBar.tsx` | The 28px inline action cluster. `size-7` → `size-11`, `TOUCH_ACTION_WIDTH_PX` 28 → 44, and the slot height `h-7` → `h-11` so the 44px buttons are not clipped. |
| `plugins/navigation/app/ui/sidebarRowClasses.ts` | `SIDEBAR_MORE_ACTION_TRIGGER_CLASS` `h-9 w-9` → `h-11 w-11`. |
| `plugins/thread-list/app/rows/sidebarRowClasses.ts` | `SIDEBAR_CONTROL_PRIMARY_BUTTON_CLASS` `h-9 w-8` → `h-11 w-11`; `SIDEBAR_CONTROL_PAIR_SIZE_CLASS` `h-9` → `h-11` with its width widened to 5.5rem to match. |
| `NavigationPlugin.test.tsx`, `EnvironmentPicker.test.tsx` | Pre-existing assertions hardcoding the old coarse sizes, updated to the new ones. |

## Measured result on the fork's dev server

412 × 891 @ DPR 3.5, coarse-pointer emulation forced on the measuring
connection, drawer open, thread route. Same scripts, same route, same state as
the baseline in `bb-touch-target-ownership-045.md`.

| | baseline | floor only | floor + inline files |
|---|---|---|---|
| visible controls | 59 | 58 | 55 |
| **under 44px tall** | **58** | **33** | **15** |
| **44px or taller** | **1** | **25** | **40** |
| 36px cluster | 20 | 6 | 0 |
| 28px cluster | 11 | 12 | 1 |

**40 of 55 controls now meet the 44px minimum, up from 1.** Both clusters that
were supposed to be the hard part are essentially gone: the 36px group went
20 → 0 and the 28px group went 11 → 1.

## What remains, and why the floor cannot reach it

| group | n | why |
|---|---|---|
| timeline rows at 20px, full width | 7 | content-sized. No sizing utility at all, so there is no constant to raise. A product decision, not a code change. |
| composer rows at 22px, full width | 3 | content-sized, same reason. |
| sidebar group labels at 24px | 3 | content-sized, same reason. |
| `Scroll to latest event` at 32px | 1 | a single control with its own size. |
| `Collapse Threads section` at 24px | 1 | content-sized. |

Every remaining control is content-sized or bespoke. The centralized floor
covers everything that *has* a size to raise; what is left has no size.

## Layout verification

`check-compact-layout.py` asserts the compact layout survived at 412 × 891: no
horizontal overflow, nothing taller than the viewport, no vertical page scroll,
the composer inside the viewport, and the sidebar rows actually present so the
check cannot pass on an empty screen.

Result: all clear. Composer at top 778, bottom 891, height 113. Sidebar rows
measure **44 px**. No element overflows 412 px.

Two failure modes were fixed in the checker itself rather than worked around:

- It reported a clean layout on a page with five buttons and no composer,
  because it probed before the app finished mounting. It now waits 12 seconds
  and fails loudly when the composer or the sidebar rows are absent.
- A dev-server reload destroys the CDP execution context between a call and its
  reply, which surfaced as a raw `KeyError: 'result'`. The CDP helper now treats
  that as "not ready" and says so, instead of crashing.

## Verification

- `coarse-pointer-sizing.test.ts`, 5 tests, passing. Reverting one constant to
  `h-9` makes it fail and name `COARSE_POINTER_HEADER_ICON_BUTTON_CLASS = 36px`,
  so it catches the regression rather than merely describing the current state.
- **Full `apps/app` suite: 5253 tests, 572 files, 1 failure.** Four assertions
  hardcoded the old coarse sizes and failed against the new constants: two in
  `NavigationPlugin.test.tsx` (`h-9`/`w-9`) and two in
  `EnvironmentPicker.test.tsx` (`size-2`, `size-5`). All updated. That they
  existed and failed is the evidence the change propagated to the components
  the constants feed, rather than sitting inert in one file.
- **The one remaining failure is pre-existing, not mine:**
  `CommandPalette.cold-open.test.tsx` ("stays usable before its body downloads on
  first open") fails identically on a clean tree, verified by stashing every
  change and re-running it. Left alone.
- `MessageActionBar.test.tsx`, 17 tests, passing. Its layout tests pin the
  desktop action width only, so raising the touch width does not affect them.
- `pnpm exec turbo run typecheck lint` green across `bb-app`,
  `@bb/shared-ui`, `bb-plugin-thread-list`, `bb-plugin-navigation`. The 13 lint
  warnings in the two plugins are pre-existing, verified by stashing.
- `check-compact-layout.py` green.
- The measurement scripts themselves are guarded: `check-coarse-guard.py`
  proves `measure-s26.py` refuses to report a measurement taken without
  coarse-pointer emulation.

## Scope note: what is still not centralized

46 files across `apps`, `packages`, and `plugins` declare coarse sizes inline.
This change took the three that carried the largest measured groups. The rest
are not the controls that dominate a thread screen, so they are lower value
than the ones done, but the floor is a property of `coarse-pointer-sizing.ts`
and of the CSS tokens, not of every declaration in the tree.

## Open

1. **The 15 remaining controls are content-sized or bespoke.** Ten of them are
   full-width timeline and composer rows at 20 to 24px. Whether a full-width row
   is a target at all is a product decision.
2. **`Scroll to latest event` at 32px** is a single control and could simply be
   given the floor.
3. **Reach is untouched by all of this.** The header controls sit 95.3% of the
   screen height above the bottom edge, roughly twice the measured reach of
   45.6%. Every fix here is about hit size on controls that are already
   reachable. Only the arc addresses reach. Note the reach figure is a fraction
   of screen height, not an absolute pixel count, and the capture it came from
   was not the S26 Ultra. See `thumb-reach-measured.md`.