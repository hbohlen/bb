# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

One bundle serves every viewport. bb's "mobile app" is a responsive view of the
same single-page app, gated by the `mobileApp` experiment flag
(`bb settings show` → `experiments`) — not a native target. Verified in
`docs/research/bb-theming-capabilities.md` §6.

## Users

A single user, working solo. The primary device is a Samsung Galaxy S26 Ultra,
held and operated one-handed. ADHD makes typography a first-order accessibility
concern rather than a polish item: text size, line height and letter spacing
are load-bearing requirements, not styling preferences.

Secondary context: the same person also uses bb on a desktop viewport, in a
slightly wider screen. One product serves both; the phone case is the harder
one and sets the constraints.

## Product Purpose

bb is an agentic IDE: projects, threads, and environments in which coding agents
do work. The user runs it as their primary working surface, not an occasional
review tool.

This repo's product is not a fork of bb. It is a **design and specification
record for an installed bb**, authored from the outside. The work is
[docs/agents/issue-tracker.md] and [GLOSSARY.md] plus a research corpus, and it
aims at a destination recorded as BB-2: a verified, buildable specification for
reworking bb's mobile UI for one-handed use, covering thumb reach, minimum
touch-target size, and a deep-black + purple visual system — every claim traced
to a measurement or a cited source, and each element assigned to the layer that
can actually deliver it (bb app shell, bundled bb plugin, or external plugin).

Success means the route is unambiguous enough to build from, and nothing in it
is asserted without a source.

## Positioning

The differentiator is a **verification standard**, not a design style. Reach and
hit are separated because conflating them hides the user's actual failure mode;
every figure is a measurement or a citation, and every UI element is assigned to
the layer with the authority to change it. A neighbouring product could copy a
thumb bar; it could not copy a claim it never measured.

## Operating Context

- **Agent orchestration goes through BB Tasks.** Work is dispatched to agents as
  bb threads from the board, capped at 3 concurrent. A `wayfinder:map` parent
  (BB-2) carries decision tickets as children.
- **jj is the source of truth for local history**; this repo is colocated
  (`jj git init --colocate`), so `land` writes the git ref and `git push` ships.
- **Themes are authored as CSS files on disk** at `~/.bb/theme/<id>/theme.css`
  and activated with `bb theme set <id>`. bb serves no theme files over HTTP, so
  any web font must be embedded (base64 `@font-face` or a fetch that succeeds)
  or named as a system font.
- **Live measurement uses `agent-browser`** (v0.27.0), which reaches the local
  bb at `http://127.0.0.1:38886` already authenticated. The Hermes browser tool
  cannot: it blocks private addresses and would need a getbb.app sign-in.
- The user views bb remotely at `https://hbo.getbb.app`; `bb connect expose
  <port>` gives a thread's server a reachable URL.

## Capabilities and Constraints

**Confirmed constraints on what a theme can do** (full detail in
`docs/research/bb-theming-capabilities.md`):

- A theme is a stylesheet of custom properties, injected last. It **cannot**
  change component layout, add or reorder DOM, or alter what is rendered.
  Density is global: `--spacing` scales the whole 0.25rem grid at once, so the
  composer cannot be roomy while the sidebar stays cramped.
- `:root, .light` and `.dark` are the only blocks with a guaranteed cascade
  position. Anything finer is element scoping and is fragile.
- **All three secondary text tiers must be set** (`--muted-foreground`,
  `--subtle-foreground`, `--readback-foreground`). bb's defaults are light-mode
  greys; a dark canvas with only `--canvas`/`--ink` set is unusable.
- **The whole type scale must be set, not just `--text-base`.** bb's own
  coarse-pointer media query re-sets `--text-2xs/xs/sm/base` on small touch
  screens, and a theme value in `:root, .light` only wins by cascade order.
- `--text-*--line-height` companions are absolute lengths, not ratios. Raise a
  size and its companion together, or text gets bigger at the same leading.
- Three sizes are hardcoded literals in bb's CSS (`text-[9px]`,
  `text-[10px]`, `text-[11px]`) and cannot be rescaled by a theme. The residual
  small text is a **code fix in bb's components**, not a theme fix. Do not chase
  it with selectors against hashed class names.
- Size cap: 256,000 bytes safe for `theme.css` (measured 256,018 accepted /
  256,019 rejected). An embedded base64 font consumes most of that budget.
- Malformed CSS is accepted silently. There is no validation pass; correctness is
  only observable in the rendered app. `bb theme show --css` proves storage, not
  application.
- A theme cannot control the PWA splash or OS status bar — `manifest.webmanifest`
  hardcodes `#ffffff`. Favicon colour is a separate 9-value setting.
- Light/dark mode is per-client; the palette is global and server-stored. One
  theme serves every window.

**Measured standing constraints** (BB-2, established by measurement):

- At 412×915, header controls sit 877 px from the bottom edge at 28×28 px; 147
  of 148 buttons on the thread screen are under 44 px tall.
- The composer ends 16 px from the bottom edge, so a permanent bottom bar has no
  free space without displacing it.
- bb ships a sidebar drawer (24 px start zone, 24–72 px drag, ≥450 px/s fling) —
  host-owned, not a plugin opportunity.
- The header does not collapse on compact viewports. `isCompactViewport` re-wires
  state, not layout.

**Explicitly undecided:** whether the user's failure mode is reach-rate or
hit-rate; how much of bb should be changed upstream versus by plugin; whether
distraction reduction conflicts with a wider action surface; and the final token
values for the deep-black + purple theme. These are live decision tickets, not
gaps to be filled by assumption.

**How work is delivered: delegated.** The user left the choice of mechanism to
the design work — theme CSS, plugin, or upstream patch, and whether the result is
a one-off or a reusable system — to be decided per task and recorded where it
matters. The choice was offered and explicitly delegated.

## Brand Commitments

None binding. "Deep black + purple" is a colour direction recorded in
[GLOSSARY.md], justified by WCAG contrast arithmetic in the research corpus
rather than colour-meaning folklore. The active custom theme is
`nocturne-purple`; `focus` and `linear-precision` also exist in
`~/.bb/theme/`. None of these is a brand commitment, and the user has not named
a tone of voice for bb's UI copy.

## Evidence on Hand

- `docs/research/bb-theming-capabilities.md` — verified token reference for bb
  0.44.0: all 354 custom properties, derivation percentages, the mobile
  question, and every limit listed above. Claims tagged `[exec]` or `[read]`.
- `docs/research/adhd-ui-design.md` and `adhd-ui-design-short.md` — evidence
  review on UI and typography for ADHD, with a verification pass.
- `GLOSSARY.md` — the reach / hit / reachability distinction and the vocabulary
  the effort depends on.
- Live app: bb 0.44.0 packaged install, server on `http://127.0.0.1:38886`.
  Measurement is available, not merely documented.

**Must not be fabricated:** any further contrast ratio, reach figure, touch-target
size, or research claim. Every new number needs a source, and
**distraction budget** is explicitly still undefined in [GLOSSARY.md] — do not
present it as a measurable quantity.

## Product Principles

1. **Measure, never assume.** A figure without a source does not enter the
   record. This applies to the user as much as to the agent.
2. **Reach and hit are independent failures with independent fixes.** Never
   propose a reach fix that leaves target size unaddressed, and never let one
   metric stand in for the other.
3. **Assign every element to the layer that can change it.** App shell, bundled
   plugin, or external plugin — a proposal that names none of them is not
   actionable.
4. **A theme is a real but limited instrument.** Respect its boundaries
   (no layout, no DOM, no rescaling hardcoded sizes) instead of fighting them
   with brittle selectors.
5. **Never ask the user for a fact obtainable by measurement or by running a
   command.**

## Accessibility & Inclusion

No formal conformance target has been set. Established requirements:

- Typography — size, line height, and letter spacing — is a first-order
  requirement driven by ADHD, not a preference.
- Touch targets must meet the minimum touch-target size; 147 of 148 buttons
  currently fail this on the thread screen at 412×915.
- On a pure-black canvas, WCAG SC 1.4.11 (3:1 for non-text UI boundaries) cannot
  be met by a quiet divider colour. **Split the borders:** `--border` /
  `--border-hairline` stay decorative, and `--input` and `--ring` carry the
  load-bearing 3:1. Anything interactive takes its visibility from those two,
  never from `--border`.
- Full keyboard operability and focus visibility are expected of an IDE, though
  no audit has established the current state.
