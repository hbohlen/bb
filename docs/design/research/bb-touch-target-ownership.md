# BB-5 — Which bb layer draws the sub-44px controls?

**Resolved by measurement, 2026-10-03.** Two passes: a live DOM audit against the
running app, then a source read of `github.com/get-bb/bb` with `codegraph`.

- **Device:** Samsung Galaxy S26 Ultra. 1440 × 3120 native, 500 PPI → Android's
  560dpi density bucket → Chrome DPR **3.5** → CSS viewport **412 × 891**.
- **Installed app:** bb 0.44.0 at `http://127.0.0.1:38886`.
- **Source read:** `get-bb/bb` @ `c201f649`, which is version **0.45.0** — one
  minor version ahead of the installed app. Source findings are therefore
  *indicative*, and flagged as such below.

Scripts, all rerunnable:
`.bb/chats/thr_5685rvuhj9/tmp/measure-s26.py`, `group-s26.py`, `owner-s26.py`.

---

## Corrections to the first pass

Three of this ticket's earlier conclusions were wrong and are replaced here.

**1. The device was wrong.** The first pass used a Pixel 7 profile. The device is
a Galaxy S26 Ultra, viewport **412 × 891**, not 412 × 915. Sources conflict on the
CSS viewport — `whatismyscreensize.com` says 480 × 1040, others say 412 × 891 —
so it is resolved from the panel spec instead: 1440 ÷ 3.5 = 411.4 → **412**,
3120 ÷ 3.5 = 891.4 → **891**. The 480 figure assumes DPR 3, which no Samsung
density bucket produces for this panel. Confirmed against `yesviz.com`, which
lists the S25 Ultra — same 6.9″ 1440×3120 panel — at DPR 3.5 / 412 × 891.

**2. "The 28 px controls are hardcoded and unreachable by a theme" was wrong, and
badly wrong.** The first pass read `h-[28px] w-[28px]` off the class list and
concluded no theme could move it. The class list actually reads:

```
h-[28px] w-[28px] rounded-md p-0 max-md:pointer-coarse:h-[36px] max-md:pointer-coarse:w-[36px]
```

There is an explicit coarse-pointer override **in the same class string**. The
first pass filtered the class list down to `h-`/`w-`/`p-` prefixed tokens and threw
the `max-md:pointer-coarse:` variants away. On the S26 Ultra those buttons measure
**36 × 36**.

The source confirms this is systematic.
`packages/shared-ui/src/components/ui/coarse-pointer-sizing.ts` is a dedicated
module of 23 exported sizing constants, used by **73 files**, each pairing a
compact value with a `max-md:pointer-coarse:` bump:

```ts
const HEADER_ICON_BUTTON_BOX_CLASS =
  "h-[28px] w-[28px] rounded-md p-0 max-md:pointer-coarse:h-[36px] max-md:pointer-coarse:w-[36px]";

export const COARSE_POINTER_ROW_HEIGHT_CLASS =
  "h-[var(--bb-sidebar-row-height)] max-md:pointer-coarse:h-[var(--bb-sidebar-row-height-coarse)]";
```

**3. Plugin attribution was incomplete.** The first pass counted 2 plugin controls
and concluded the plugin layer owns almost nothing. That missed the thread list.
`plugins/thread-list` is a **bundled plugin** and it draws the 46 sidebar thread
rows — more than half the undersized controls. `data-testid` prefixed `plugin-`
does **not** mark them; only the two footer items carry it. So that marker
identifies *some* plugin UI, not plugin UI in general.

---

## What the source reveals that the DOM could not

### bb has a deliberate, centralised coarse-pointer sizing system

| Layer | Mechanism | Location |
|---|---|---|
| Buttons, rows, icons | 23 `COARSE_POINTER_*` class constants | `packages/shared-ui/src/components/ui/coarse-pointer-sizing.ts`, 73 consumers |
| Sidebar control size | `--bb-sidebar-control-size: 28px` → `36px` | `apps/app/src/app.css:33-41`, under `@media (width < 48rem) and (pointer: coarse)` |
| Sidebar row height | `--bb-sidebar-row-height: 1.75rem` → `--bb-sidebar-row-height-coarse: 2.5rem` | `apps/app/src/components/ui/theme.css:597-598` |
| Type scale | `text-sm max-md:pointer-coarse:text-base` and similar | same module |
| Touch detection | `use-pointer-coarse.ts`, `"(pointer: coarse)"` | `packages/shared-ui/src/components/ui/hooks/` |

**The 36 px ceiling is the finding.** Every coarse-pointer bump in the codebase
tops out at **36 px**. There is no 44 px anywhere in the system. The bump is
thorough and deliberate — and it stops 8 px short of the target.

### `--bb-sidebar-row-height-coarse` does not fire

`--bb-sidebar-row-height` measured **1.75rem** under forced touch emulation, not
the 2.5rem coarse value, even though `--bb-sidebar-control-size` in the *same*
media block correctly resolved to 36px. This is a live inconsistency between two
tokens in the same query and is worth reporting upstream.

### No thumb bar exists

`codegraph query "thumb-bar OR thumbbar OR reachability OR thumb-zone"` returns
one unrelated hit (`pruneUnreferencedChunks`). There is **no reachability
affordance in bb today**. Safe-area insets are already plumbed —
`pb-[var(--bb-safe-area-bottom,env(safe-area-inset-bottom))]` in
`AppLayout.tsx:804` — so a bottom bar has a place to live, but
`--bb-safe-area-bottom` computed **empty** on the S26 profile.

---

## Measured state on the Galaxy S26 Ultra

412 × 891, DPR 3.5, `pointer: coarse` true, `maxTouchPoints` 5. 83 visible
controls on the thread screen.

| | count |
|---|---|
| visible controls | 83 |
| under 44 px tall | **82 (99%)** |
| 44 px or taller | **1** — the feedback-mode button, at exactly 44×44 |
| theme can move (token-driven) | 78 |
| theme blocked (px literal, no override) | 0 |
| bare, no sizing class | 46 |
| bundled-plugin-drawn (thread list) | 46 |
| shell-drawn | 35 |
| plugin-marked (`data-testid="plugin-*"`) | 2, both already 36 px |

**Top band, 849 px from the bottom edge:**

| control | size |
|---|---|
| Go back · Go forward · Show right panel · Toggle sidebar | 36 × 36 |
| panel rows (New thread, Plugins, Skills, Automations, Agentation, Jujutsu, Tasks, Theme Preview) | 296 × 40 |
| each row's "options" disclosure | 36 × 36 |

**Composer band, 8–65 px from the bottom edge** — inside reach:

| control | size |
|---|---|
| Start feedback mode | 44 × 44 |
| Prompt actions · Start voice input | 40 × 40 |
| Remote access · Provider usage · Report a bug | 36 × 36 |
| Provider/model chip · Permission mode · Projects & Sections | 32 tall |
| **Chat actions (per thread row)** | **28 × 28** |
| inline status glyphs | 14 × 14 |

The pattern is unambiguous: **size increases as you move toward the bottom of the
screen.** 36 px at the top, 40 px in the composer, 44 px at the very bottom. The
one genuinely undersized cluster is the 28 × 28 `Chat actions` button on every
thread row, plus 14 px glyphs.

---

## Ownership, resolved

| group | n | owner | theme can fix? |
|---|---|---|---|
| Sidebar thread rows + `Chat actions` | 46 | **`plugins/thread-list`** (bundled plugin) | Partly — row height reads a token; the 28 px button is fixed |
| Header icon buttons | 4 | shell (`AppPageHeader.tsx`) | No — px literals, though a coarse override exists |
| Panel rows + disclosures | 23 | shell | Yes — token-driven |
| Composer controls | 10 | shell | Yes — token-driven |
| Sidebar footer items | 3 | shell + 2 bundled plugins | Yes |

**`Chat actions` at 28 × 28 is the highest-value target in the whole audit.** It
sits inside the user's reach, in the bundled `thread-list` plugin, and it is the
only frequently-used control that got no coarse-pointer bump at all — it has no
`max-md:pointer-coarse:` variant in its class string.

---

## What this means for the map

1. **The reach fix and the size fix are both upstream work, and neither is a
   theme.** Corrected from the first pass: 78 of 82 undersized controls are
   token-driven, so a theme can move most of them. But a theme cannot change
   *which layer draws what*, cannot add a thumb bar, and cannot lift the 36 px
   ceiling, because 36 px is hardcoded in `coarse-pointer-sizing.ts` as
   `max-md:pointer-coarse:h-[36px]` rather than expressed as a token.
2. **The single highest-leverage upstream change is one number:** the
   coarse-pointer ceiling, 36 → 44. One constant in one file, 73 consumers, and it
   lifts the header buttons, row actions and toolbar buttons together.
3. **Second: `Chat actions` at 28 px needs the bump it never got.** It is the most
   reachable and most repeated undersized control.
4. **BB-9 (plugin vs upstream) is largely answered.** The bundled `thread-list`
   plugin owns the largest single group of undersized controls, and it is in-repo,
   so it is patchable without forking. Everything else is the app shell. An
   external plugin can add a thumb bar; it cannot resize what the shell draws.
5. **A theme still has real work**, just not the work the first pass claimed:
   `--bb-sidebar-row-height-coarse`, `--spacing`, and the type scale are all
   theme-settable, and BB-6's AAA 7:1 body text is achievable there.

---

## Could not be determined

- Whether the 14 × 14 glyphs have expanded hit areas. `getComputedStyle` shows
  `pointer-events: auto` on the button itself, and no pseudo-element or overlaying
  sibling was found, but a DOM measurement cannot prove absence.
- **Version skew.** Source is 0.45.0; the installed app is 0.44.0. The
  coarse-pointer system may have changed between them. Every source claim should be
  re-checked against 0.44.0 before being relied on for a patch.
- Screens other than the thread screen. Only the thread screen was measured.
- The sidebar drawer was never opened. It is host-drawn and may size differently.
- Whether `--bb-safe-area-bottom` being empty is a bug or simply unset by default.
- **Whether a 44 px bump breaks layout.** Raising row heights by 8 px changes
  information density in a list view. That needs a visual check, not a
  measurement.