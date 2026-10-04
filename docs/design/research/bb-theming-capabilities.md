# bb theming capabilities — verified reference

**Purpose:** establish exactly what bb 0.44.0's theme system exposes, so an
ADHD-oriented theme is authored against real capability instead of assumption.

**Scope note.** This is interface-design evidence, not branding. There is no
"purple means X" component here: the accent is a contrast and distinctness
decision, justified by WCAG ratios in §7, not by colour psychology. Nothing in
this document cites colour-meaning folklore.

**Install inspected:** bb `0.44.0`, packaged app at
`~/.local/share/mise/installs/node/22.23.1/lib/node_modules/bb-app`,
server on `http://127.0.0.1:38886`, data dir `~/.bb`.

**Verification legend.** Claims are tagged:

- **[exec]** — verified by running a command or driving the live app.
- **[read]** — read from bb's own documentation or bundled source, not executed.

---

## 1. Where themes live, and their structure

**[exec]**

```console
$ bb theme dir
/home/hbohlen/.bb/theme

$ bb theme list
Built-in:
  default, nord, dracula, solarized, gruvbox, catppuccin
Custom (/home/hbohlen/.bb/theme):
  claude-terracotta, focus, linear-precision, * nocturne-purple,
  notion-warm, supabase-emerald, vercel-ink
Plugins:
  (none)
Active: Custom theme 'nocturne-purple' (56808 bytes)
Code theme: github-dark / github-light
```

**[exec]** A theme is a **folder whose name is the theme id**, containing
`theme.css`:

```
~/.bb/theme/<id>/theme.css                     # required
~/.bb/theme/<id>/pierre-dark.json              # optional code colours
~/.bb/theme/<id>/pierre-light.json             # optional
~/.bb/theme/<id>/theme.json                    # optional codeTheme map
```

`theme.json` form **[read]** (`references/theming.md`):

```json
{ "codeTheme": { "dark": "pierre-dark.json", "light": "github-light" } }
```

If a custom theme ships no code colours, bb falls back to `pierre-dark` /
`pierre-light`. **[exec]** confirmed this: a custom theme with only `theme.css`
resolved to `"dark": "pierre-dark", "light": "pierre-light"`.

Built-in palettes use a matching Shiki pair (`nord` → nord dark/light, etc.).
**[exec]** `nocturne-purple`, a custom theme, ships its own
`pierre-dark.json`/`pierre-light.json` and reports `github-dark / github-light`.
There is **no separate code-theme setting**; the code theme follows the UI palette
**[read]**.

---

## 2. Light/dark: a separate, per-client axis

**[read]** The palette is global and server-stored. Light/dark **mode** is a
per-client setting that the palette layers on top of. One stylesheet handles both
modes.

**[exec]** Confirmed in the bundled base stylesheet
`app/dist/assets/index-C5-8cYca.css`: two parallel token blocks, `:root, .light`
and `.dark`. Both also set `color-scheme`, which drives native form controls and
scrollbars.

**[exec]** Both selectors are required, and `:root` matches in *both* modes — so
anything left only in `:root, .light` leaks into dark mode. This is the single
most common authoring mistake. Put mode-independent values (fonts, ANSI palette,
`color-mix` text tiers) in the first block; re-set only anchors, accent and
semantics in `.dark`.

**[exec]** No theme CSS was observed setting `color-scheme`; bb's own block
supplies it. Do not fight it.

---

## 3. The real token list

**[exec]** Extracted from the bundled stylesheet: **354 distinct `--*` custom
properties**, of which the following are the *design* tokens (the rest are
Tailwind's `@property` machinery — `--tw-*` — and internal layout metrics).

### 3.1 Anchors (set first; almost everything derives from these)

| token | drives |
|---|---|
| `--canvas` | base surface: page, cards, popovers, sidebar, and via mixes every neutral fill/border |
| `--ink` | base text colour, and the strength of every derived neutral |

### 3.2 Text tiers (do **not** auto-derive — set explicitly)

| token | default (light) | default (dark) | role |
|---|---|---|---|
| `--foreground` | `= --ink` | `= --ink` | body text; leave alone |
| `--muted-foreground` | `oklch(44% 0 0)` | `oklch(78% 0 0)` | metadata, timestamps, labels — highest-contrast secondary tier |
| `--subtle-foreground` | `oklch(50% 0 0)` | `oklch(68% 0 0)` | captions, hints, placeholders — lowest tier |
| `--readback-foreground` | `oklch(47% 0 0)` | `oklch(71.5% 0 0)` | settled/closed-turn machinery, recedes between the two above |

The three secondary tiers are **hardcoded literals in bb's own CSS**, not mixes.
A theme that changes `--canvas`/`--ink` without also setting them gets bb's grey
defaults on a black canvas. **[exec]** verified: setting only
`--canvas: #101014; --ink: #f0eef5` left `--muted-foreground: oklch(44% 0 0)` —
dark grey on near-black, unusable. **Always set all three.**

### 3.3 Accent

| token | derives | drives |
|---|---|---|
| `--primary` | **set** | primary buttons, active/accent states, links, focus ring, selection |
| `--primary-foreground` | **set** | text/icons on a `--primary` fill |
| `--ring` | `= --primary` | keyboard focus outline |
| `--sidebar-ring` | `= --primary` | focus outline in the sidebar |
| `--file-accent` | **set** | file-path titles in the timeline |
| `--timeline-accent` | **set** | timeline accent; `--file-accent` defaults to it |

### 3.4 Surfaces & chrome (auto-derive — the actual percentages)

All percentages are **[exec]**, read out of the bundled CSS:

| token | light derivation | dark derivation |
|---|---|---|
| `--background`, `--card`, `--popover` | `= --canvas` | `= --canvas` |
| `--secondary`, `--accent` | ink **8%** | ink **13%** |
| `--muted` | ink **11%** | ink **16%** |
| `--border` | ink **14%** | ink **19.4%** |
| `--border-hairline` | ink **14.7%** | ink **21%** |
| `--border-seam` | ink **9.5%** | ink **11%** |
| `--input` | ink **29.5%** | ink **32.6%** |
| `--surface-recessed` | translucent ink 6% | translucent ink 6% |
| `--surface-recessed-solid` | ink 6% | ink 6% |
| `--surface-recessed-soft-solid` | ink 4.2% | ink 4.2% |
| `--surface-raised` | translucent ink 2.5% | translucent ink 2.5% |
| `--surface-raised-solid` | ink 2.5% | ink 2.5% |
| `--surface-scrim` | canvas 92% | canvas 92% |
| `--state-hover` | translucent ink 5.9% | translucent ink 13.8% |
| `--state-active` | translucent ink 11.8% | translucent ink 22.5% |
| `--sidebar` | ink 2.2% | ink 4.3% |
| `--sidebar-foreground` | `= --ink` | `= --ink` |
| `--sidebar-accent` | ink 8% | ink 12% |
| `--sidebar-accent-foreground` | `= --ink` | `= --ink` |
| `--sidebar-border` | ink 14% | ink 18.1% |
| `--surface-destructive` | destructive 6% | destructive 8% |
| `--surface-destructive-border` | destructive 25% | destructive 30% |
| `--surface-attention` | attention 14% | attention 12% |
| `--surface-selected` | primary 16% | primary 12% |
| `--surface-selected-border` | primary 35% | primary 35% |

**The derivation model in one sentence:** the neutral ramp is `--ink` mixed into
`--canvas` at increasing percentages. Higher percentage = further from the
surface. **[read]** this matches `references/theming.md` exactly.

### 3.5 Semantic / status (set explicitly; these carry meaning)

| token | light default | dark default |
|---|---|---|
| `--destructive` | `oklch(45% .19 25.86)` | `oklch(56% .19 22.17)` |
| `--destructive-foreground` | `oklch(100% 0 0)` | `oklch(100% 0 0)` |
| `--destructive-text` | `oklch(45% .19 25.86)` | `oklch(65% .16 22)` |
| `--warning` | `oklch(70% .16 50)` | `oklch(75% .16 50)` |
| `--warning-text` | `oklch(55% .14 50)` | `oklch(75% .16 50)` |
| `--attention` | `oklch(74% .15 80)` | `oklch(80% .15 80)` |
| `--success` | `oklch(70% .15 155)` | `oklch(74% .15 155)` |
| `--success-foreground` | success 45% into ink | success 45% into ink |
| `--diff-added` | `oklch(40% .13 163)` | `oklch(77% .17 163)` |
| `--diff-removed` | `oklch(40% .17 28)` | `oklch(72% .19 22)` |
| `--pr-merged` | `oklch(53% .2 295)` | `oklch(68% .18 295)` |
| `--brand-discord` | `oklch(57.74% .2091 273.85)` | `= --foreground` |
| `--version-upgrade` | ink 96% | ink 96% |
| `--sidebar-search-match` | amber 80% .13 88 mixed into canvas | same, more canvas |
| `--sidebar-search-match-border` | same family | same family |

### 3.6 Terminal

`--ansi-0` … `--ansi-15` and `--ansi-bg-fg-0` … `--ansi-bg-fg-15` **[exec]**.
Full light and dark hex sets are present in the bundled CSS. If you remap an ANSI
colour you must also remap its `-bg-fg` companion — that is the readable text
drawn on top when the colour is used as a background. **[read]**

### 3.7 Non-colour tokens — **the ADHD-relevant set**

These are the real levers. A theme can change far more than colour.

**[exec]**

| token | default | what it actually drives |
|---|---|---|
| `--font-sans` | `"Inter Variable", Inter, sans-serif` | **entire UI / body text** (`html` uses `--default-font-family`, which is `var(--font-sans)`) |
| `--font-mono` | `ui-monospace, SFMono-Regular, Menlo, …` | code blocks, diffs, file paths, previews |
| `--font-serif` | `Georgia, serif` | serif prose (rarely used in UI) |
| `--font-terminal` | `"JetBrainsMono Nerd Font Mono", …` | **the integrated terminal's xterm renderer, independent of `--font-mono`** |
| `--radius` | `.5rem` | base corner rounding; `--radius-md` is `calc(var(--radius) - 2px)`, `--radius-lg` is `= --radius` |
| `--spacing` | `.25rem` | **Tailwind v4 spacing unit.** Every `p-4`, `gap-2`, `m-1.5` is `calc(var(--spacing) * N)` — verified in CSS and in the live DOM |
| `--text-2xs` … `--text-2xl` | `.625rem`…`1.5rem` | the whole type scale, each with a paired `--text-*--line-height` |
| `--leading-tight/snug/normal/relaxed` | 1.25 / 1.375 / 1.5 / 1.625 | line-height utilities |
| `--tracking-tight/normal/wide/wider/widest` | `-.025em` … `.1em` | letter-spacing utilities |
| `--font-weight-light/normal/medium/semibold` | 300/400/500/600 | weight utilities |
| `--icon-stroke-width` | `1.75` | Lucide icon stroke — a direct, legitimate legibility knob |
| `--shadow-*` | full scale | `--shadow-2xs/xs/sm/md/lg/xl/2xl`, plus `--shadow-x/y/blur/spread/opacity/color` and `--shadow-lift` |
| `--bb-sidebar-row-height` | `1.75rem` | sidebar row height (hit-target size) |
| `--bb-sidebar-control-size` | `28px` → `36px` under `@media ((width<48rem)) and (pointer:coarse)` | sidebar control hit-target |
| `--secondary-panel-width-mobile` | `min(76vw, 320px)` | mobile side-panel width |
| `--sidebar-width` / `--sidebar-width-mobile` | present in CSS | sidebar width |
| `--pill-surface`, `--pill-foreground`, `--pill-icon`, `--pill-shadow`, `--pill-surface-selected`, `--pill-surface-selected-border` | present | prompt-mention chips; documented as fixed literals, override only if needed **[read]** |
| `--diffs-light-bg`/`--diffs-dark-bg` and `-addition-color`/`-deletion-color` | `= --background` / `= --diff-added` / `= --diff-removed` | diff viewer surfaces |

---

## 4. Typography: what a theme can and cannot change

### 4.1 Font family — **4 tokens, confirmed**

`--font-sans`, `--font-mono`, `--font-serif`, `--font-terminal`. **[exec]**
Verified all four are honoured: a probe theme setting all four to `Sora`
produced `getComputedStyle(document.body).fontFamily === "Sora, sans-serif"`,
and `--default-font-family` / `--default-mono-font-family` resolved through to
the theme's values. This matches `bb guide customization`: *"Theme CSS can
override typography as well as colors. `--font-terminal` controls the
integrated terminal's font family independently of `--font-mono`."*

Note the chain: `html { font-family: var(--default-font-family, …) }`, and
`--default-font-family: var(--font-sans)`. **Setting `--font-sans` is enough to
re-face the whole app.** **[exec]**

### 4.2 Font size, line height, letter spacing — **yes, via the Tailwind scale tokens**

This is the finding most likely to be assumed absent. bb builds on **Tailwind
CSS v4.3.0** **[exec]**, whose utilities are thin wrappers over custom
properties:

```css
.text-base { font-size: var(--text-base);
             line-height: var(--tw-leading, var(--text-base--line-height)) }
.leading-normal  { --tw-leading: var(--leading-normal);  line-height: var(--leading-normal) }
.tracking-wide   { --tw-tracking: var(--tracking-wide); letter-spacing: var(--tracking-wide) }
.p-4   { padding: calc(var(--spacing) * 4) }
.gap-2 { gap: calc(var(--spacing) * 2) }
```

So overriding `--text-base`, `--text-base--line-height`, `--leading-normal`,
`--tracking-wide` and `--spacing` rescales the entire UI.

**[exec]** A probe theme setting `--text-base: 1.25rem`, `--leading-normal: 1.9`,
`--tracking-wide: .06em`, `--spacing: .375rem` changed the computed values of
every one of those tokens on `document.documentElement`, and rendered body text
moved from bb's stock 15px to 20px. `getComputedStyle` on real text nodes
confirmed the new sizes painting.

### 4.3 The limit: a handful of sizes are hardcoded

**[exec]** Scanning all four bundled CSS files for literal `font-size` values
outside `em`/`rem` reveals exactly three hardcoded utilities in the app shell:

```css
.text-\[9px\]  { font-size: 9px }
.text-\[10px\] { font-size: 10px }
.text-\[11px\] { font-size: 11px }
```

Referenced twice each from JS (`text-[10px]`, `text-[11px]`, `text-[0.9em]`).
These are compact chrome — small counters and icons. **A theme cannot rescale
them without element-scoped CSS rules targeting hashed class names**, which is
fragile across upgrades.

**[exec]** Live measurement on a Pixel 7 viewport confirmed the practical effect:
with `--text-base` raised to 20px, most text rescaled, but a visible cluster
remained at 13px / 12px / 10px — the hardcoded utilities plus `em`-relative rules
that inherit from an unscaled ancestor.

**Consequence for an ADHD-oriented theme:** a global type-scale bump gets you ~90%
of the way. The residual small text is a *code* fix in bb's components, not a
theme fix. Do not attempt to chase it with arbitrary class selectors.

### 4.4 Line-height subtlety

**[exec]** The `--text-*--line-height` companions are paired with the sizes
(`--text-base--line-height: 1.375rem`, an absolute length, not a ratio). Raising
`--text-base` without raising its `--line-height` companion gives you bigger text
at the same absolute leading — cramped. **Raise both together.**

Also note bb ships a coarse-pointer media query:

```css
@media ((width<48rem)) and (pointer:coarse) {
  :root { --bb-sidebar-control-size: 36px; --bb-sidebar-control-icon-size: 20px }
}
@media (width<=767px) and (pointer:coarse) {
  :root { --text-2xs: .6875rem; --text-xs: .875rem;
          --text-sm: .9375rem; --text-base: 1rem;
          --text-base--line-height: 1.5rem }
}
```

**[exec]** Confirmed live: on a Pixel 7 profile, `--text-sm` computed to
`.9375rem` and `--text-2xs` to `.6875rem` — i.e. **bb already enlarges the type
scale on small touch screens**, and a theme value in `:root, .light` still wins
(cascade order: later sheet, same specificity), but a theme that sets only
`--text-base` will find `--text-sm` silently bumped by the media query. **Set the
whole scale, not just `--text-base`.**

### 4.5 Loading a font the browser does not have

Three documented routes **[read]**:

1. **A system or bundled font** — just name it. Inter is always bundled.
2. **`@import url(...)`** — must be the **very first statement** in the file, or it
   is ignored. Then reference the family.
3. **`@font-face`** with a `src` URL or a `data:` URI.

**[exec]** `@import` with Google Fonts worked: the theme loaded, `Sora`
registered in `document.fonts`, and `body` computed to `Sora, sans-serif`.

**[exec]** The existing `nocturne-purple` theme embeds its font as a base64
`@font-face` data URI, with the comment *"bb serves no theme files over HTTP"* —
a self-contained approach that removes a network dependency but pushes the file
toward the 256 KB ceiling (§5).

Always end the stack with a generic family (`sans-serif` / `monospace` / `serif`)
so text still renders if the font fails **[read]**.

---

## 5. Authoring and activation: the real command surface

**[exec]**

```console
$ bb theme set does-not-exist
Error: HTTP 404: Custom theme 'does-not-exist' not found.
  Create /home/hbohlen/.bb/theme/does-not-exist/theme.css first.

$ bb theme set ../etc
Error: HTTP 400: Invalid theme id '../etc'.

$ bb theme set 'bad name'
Error: HTTP 400: Invalid theme id 'bad name'.

$ bb theme set A<x70 chars>
Error: HTTP 400: Invalid theme id 'A<x70 chars>'.
```

**[exec]** A folder with **no `theme.css`** is invisible — `bb theme set` 404s and
`bb theme list` omits it. The CSS file is what makes a theme exist.

**[exec]** **Invalid CSS is accepted silently.**
`:root, .light { --canvas: ; --ink: notacolor; @@@ }` was reported as
`Theme set to Custom theme 'zz-broken' (51 bytes)` with no error. The browser
discards the malformed declarations. **There is no validation pass — a broken
theme fails quietly in the UI.** Check the result visually; `bb theme show --json`
returning your CSS verbatim only proves storage, not application.

**[exec]** **Size cap, measured by bisection.** Largest accepted `theme.css`:
**256,018 bytes**. First rejected: **256,019 bytes**. Note this is *not*
`256 × 1024` (262,144) and *not* `256 × 1000` (256,000) — it is close to but above
the decimal-KB figure, so `references/theming.md`'s "*capped at ~256 KB*" is
accurate as an approximation only. If you need an exact bound, budget **256,000
bytes**. The cap is on file size, so an embedded base64 font eats a large share
of it.

### Commands **[exec]**

| command | effect |
|---|---|
| `bb theme dir` | print the custom-theme directory |
| `bb theme list` | built-in + custom + plugin themes, marks the active one |
| `bb theme set <id> [--favicon-color <c>]` | activate; preserves favicon unless the flag replaces the selection |
| `bb theme show [id] [--css]` | print active theme, or resolve `<id>` without activating |
| `bb theme reset` | back to Default, preserving favicon |
| `bb theme favicon set <c>` / `reset` | favicon only, theme preserved |
| `--json` on any of the above | machine-readable |

Favicon colours: `default`, `red`, `orange`, `yellow`, `green`, `teal`, `blue`,
`purple`, `pink` **[read]**.

**[exec]** Theme id rules: must start with a letter or digit; at most 64 letters,
digits, dots, underscores or hyphens; no slashes, no spaces.

**[read]** Hovering a palette in Settings → Appearance previews it live in that
window without saving; `bb theme show <id>` is the CLI counterpart. Changes apply
live to every open window — **no reload needed**.

**[read]** `bb theme set` is **global and app-wide**. If the user is mid-session,
restore the previous theme when done.

### Persistence **[exec]**

`bb settings show` exposes the resolved state under an `appearance` key:

```json
"appearance": {
  "themeId": "nocturne-purple",
  "customCss": "@import url(...)…",
  "faviconColor": "default",
  "resolvedCodeTheme": { "dark": "github-dark", "light": "github-light", "files": {} }
}
```

So the palette — including the full CSS text — lives in the server-side settings
store, mirrored under `~/.bb`; the file on disk is the source you author.

---

## 6. Does a theme reach the mobile UI?

**Yes. bb has one web bundle; there is no separate mobile app.**

**[exec]** With the default-off `mobileApp` experiment enabled
(`bb settings experiment mobileApp true`), the server still serves the *same*
single-page app: the injected stylesheets were unchanged
(`index-C5-8cYca.css`, `markdown-preview-*.css`, `app.css`), and every theme
token computed identically on a Pixel 7 emulation profile and on desktop. Turning
the experiment back off changed nothing structural.

**[exec]** There is exactly one `index.html` and one set of JS chunks under
`app/dist/`. The "mobile app" is a responsive view of the same bundle, gated by
an experiment flag (`mobileApp` in `bb settings show` → `experiments`).

**[exec]** Both a narrow/coarse viewport and a desktop viewport read the same
theme. So a theme written for desktop is automatically a theme on mobile — with
two caveats, both live-verified:

1. **Media queries in bb's own CSS override some of your type scale.** The
   coarse-pointer block re-sets `--text-2xs/xs/sm/base`. A theme must set the full
   scale to survive on mobile (§4.4).
2. **Mobile layout metrics are themeable and separate from desktop.** Set them
   explicitly if the goal is bigger touch targets:
   `--secondary-panel-width-mobile` (default `min(76vw, 320px)`),
   `--sidebar-width-mobile`, `--bb-safe-area-bottom` (safe-area inset),
   `--bb-sidebar-row-height` (default `1.75rem` desktop, `2.5rem` coarse),
   `--bb-sidebar-control-size` (28px → 36px on coarse pointers).

**[exec]** Also note the PWA `manifest.webmanifest` hardcodes
`"background_color": "#ffffff"` and `"theme_color": "#ffffff"`. A theme does
**not** control the installed-app splash or the OS status-bar colour; those come
from the favicon colour selection and the manifest.

---

## 7. Deep black + purple: a starting point, not a design

The requested direction is **deep black canvas, purple accent**. This section is
a *documented starting point* with its contrast arithmetic shown, so the real
design work can start from checked numbers.

### 7.1 The pure-black constraint, stated plainly

On `#000000`, WCAG SC 1.4.11 (3:1 for non-text UI boundaries) is only cleared at
roughly `#5c5c60` and above — which is far too light to use as a quiet divider.
**[exec]** verified that when only `--canvas`/`--ink` are set, bb's derived
`--input` is ink-32.6% into canvas, which on pure black lands below 3:1.

**Therefore: split the borders.** `--border` / `--border-hairline` stay quiet and
decorative; `--input` and `--ring` carry the load-bearing 3:1. Anything
interactive takes its visibility from `--input` or `--ring`, never `--border`.

### 7.2 Starting-point CSS

**This is scaffolding.** Every value needs re-derivation against real rendered
elements before it is a theme — see §8. Ratios below are arithmetic against these
hex values, not measurements of bb's rendered output.

```css
/* Deep-black + purple STARTING POINT — not a finished design.
 * Values are computed placeholders; verify each against the live app.
 * Rule: --border* are decorative; --input and --ring carry the 3:1.
 */

:root,
.light {
  --canvas: #0a0a0f;
  --ink: #eae7f2;

  --primary: #7c5cff;
  --primary-foreground: #ffffff;

  /* MUST be set: bb's defaults are light-mode greys and will not survive
     a dark canvas. Derive from the anchors so contrast tracks the theme. */
  --muted-foreground:    color-mix(in oklch, var(--ink) 72%, var(--canvas));
  --subtle-foreground:   color-mix(in oklch, var(--ink) 60%, var(--canvas));
  --readback-foreground: color-mix(in oklch, var(--ink) 66%, var(--canvas));

  /* Split borders: quiet vs load-bearing (SC 1.4.11 needs 3:1). */
  --border: #1e1d26;          /* decorative dividers only */
  --border-hairline: #141319;
  --border-seam: #0e0e13;
  --input: #55555e;           /* must clear 3:1 against its surface */
  --ring: #7c5cff;            /* focus outline */

  --sidebar: #050508;
  --sidebar-border: #16151c;
  --sidebar-accent: #141020;

  --success: #3fb950;
  --warning: #d29922;
  --warning-text: #0a0a0f;
  --destructive: #f85149;
  --destructive-text: #ff7b72;
  --attention: #d29922;
  --diff-added: #3fb950;
  --diff-removed: #f85149;
  --pr-merged: #a371f7;
  --file-accent: #a371f7;

  /* Typography. Mode-independent, so :root, .light only.
     The web font must be embedded or fetched — bb serves no theme files. */
  --font-sans: "Atkinson Hyperlegible", ui-sans-serif, system-ui, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, monospace;
  --font-terminal: ui-monospace, SFMono-Regular, Menlo, monospace;

  /* ADHD-relevant scale. Set the WHOLE scale: bb's coarse-pointer media
     query re-sets --text-2xs/xs/sm/base and will otherwise override you. */
  --text-2xs: 0.8125rem;  --text-2xs--line-height: 1.125rem;
  --text-xs:  0.9375rem;  --text-xs--line-height:  1.3125rem;
  --text-sm:  1.0625rem;  --text-sm--line-height:  1.4375rem;
  --text-base: 1.1875rem; --text-base--line-height: 1.625rem;
  --text-lg:  1.375rem;   --text-lg--line-height:  1.75rem;
  --leading-normal: 1.65;
  --tracking-wide: 0.03em;

  /* Density + legibility */
  --spacing: 0.3125rem;
  --radius: 0.625rem;
  --icon-stroke-width: 2;
  --bb-sidebar-row-height: 2.25rem;
  --secondary-panel-width-mobile: min(88vw, 400px);
}

.dark {
  --canvas: #000000;
  --ink: #ece9f2;

  --primary: #a78bfa;
  --primary-foreground: #0a0a0d;

  --border: #1c1b22;
  --border-hairline: #131318;
  --border-seam: #0c0c10;
  --input: #5c5c64;         /* verify >=3:1 on #000000 */
  --ring: #a78bfa;

  --sidebar: #040406;
  --sidebar-border: #17161d;
  --sidebar-accent: #12101c;

  --success: #4ade80;
  --warning: #fbbf24;
  --warning-text: #0a0a0d;
  --destructive: #f87171;
  --destructive-text: #fca5a5;
  --attention: #fbbf24;
  --diff-added: #4ade80;
  --diff-removed: #f87171;
  --pr-merged: #a78bfa;
  --file-accent: #a78bfa;
}
```

### 7.3 Numbers behind the accent choice

**[read]** `references/theming.md` recommends keeping dark ink under ~12:1 on
near-black, because light-on-dark text blooms on OLED. Pure white is not
required. These ratios are arithmetic on the hex values above:

| pairing | ratio | verdict |
|---|---|---|
| `#ece9f2` on `#000000` | ~17.6:1 | AAA, no bloom of pure white |
| `#a78bfa` on `#000000` (accent as text) | ~7.7:1 | AAA |
| `#a855f7` on `#000000` (rejected purple-500) | ~5.3:1 | AAA-normal only; reads heavier |
| `#0a0a0d` on `#a78bfa` (button label) | ~10:1 | AAA |
| `#5c5c64` on `#000000` (`--input`) | ~3.3:1 | clears SC 1.4.11 |

These are **computed, not measured on bb's rendered output.** The theme skill's
own rule applies: measure the DOM, not the token file.

---

## 8. What a theme CANNOT do

Verified limits, each tagged.

**Cannot change component layout or structure.** A theme is a stylesheet of custom
properties injected as the last sheet. It cannot add, remove or reorder DOM,
change a component's spacing *between* elements, or alter what is rendered.
Density changes only via `--spacing`, which scales the whole 0.25rem grid at once
— you cannot make the composer roomy and the sidebar cramped.

**Cannot rescale the ~3 hardcoded tiny sizes.** `text-[9px]`, `text-[10px]`,
`text-[11px]` are literal `font-size` declarations in bb's CSS **[exec]**. The
only workaround is element-scoped CSS against hashed class names, which breaks
across bb upgrades. The existing `nocturne-purple` theme does not attempt it, and
neither should a new one.

**Cannot express per-element preferences.** `:root, .light` and `.dark` are the
only two blocks with a guaranteed cascade position. Anything finer is element
scoping, which is fragile. **[read]** palette values belong in those two blocks so
tooling can read them.

**Cannot exceed 256,000 bytes safely.** Measured cap 256,018 bytes accepted /
256,019 rejected **[exec]**. An embedded base64 web font consumes most of that
budget — `nocturne-purple` is 56,808 bytes for exactly this reason.

**Cannot be validated by the CLI.** Malformed CSS is accepted without error
**[exec]**. There is no lint step. Correctness is only observable in the rendered
app.

**Cannot control the PWA splash or OS status bar.** `manifest.webmanifest`
hardcodes `background_color`/`theme_color` as `#ffffff` **[exec]**, independent of
theme CSS. Favicon colour is a separate 9-value setting.

**Cannot change the terminal's colours independently of its font.**
`--font-terminal` is settable **[exec]**, but the terminal's *colour* scheme is
governed by `--ansi-*`, shared with anything else using the ANSI palette.

**Cannot set a colour-scheme the theme does not name.** bb's own `:root, .light` /
`.dark` blocks set `color-scheme: light|dark` **[exec]**; a theme that wants native
scrollbars and form controls to match must not fight it.

**Cannot affect other clients' mode.** The palette is server-global; light/dark
mode is per-client **[read]**. One theme serves every window; each window chooses
its own mode.

**Cannot be scoped to a window or thread.** Activation is app-wide.

---

## 9. Verification performed

Everything below was executed on the live bb 0.44.0 install, then **state was
restored**: active theme back to `nocturne-purple`, `mobileApp` experiment back to
`false`, and all 40+ temporary `zz-*` probe theme folders deleted from
`~/.bb/theme`.

- **[exec]** `bb theme dir` / `list` / `show` / `show --json` / `set` — output quoted
  verbatim above.
- **[exec]** `bb settings show` — inspected the `appearance` block and the
  `experiments` block.
- **[exec]** Token extraction: 354 `--*` properties parsed from
  `app/dist/assets/index-C5-8cYca.css`; every derivation percentage in §3 read
  from the actual `:root, .light` and `.dark` blocks.
- **[exec]** Live computed-style probes via Playwright + Chromium against
  `http://127.0.0.1:38886` (no auth): confirmed the four `--font-*` tokens, the
  Tailwind scale tokens, `--spacing`, `--radius`, `--icon-stroke-width`, and the
  mobile-specific metrics all resolve from theme CSS onto
  `document.documentElement`.
- **[exec]** A probe theme that rescaled the type scale was loaded and real text
  nodes were measured: body text moved from bb's stock 15px to 20px, while a
  residual cluster at 13/12/10px confirmed the hardcoded-utility limit.
- **[exec]** Failure modes: id validation (400s), missing `theme.css` (404),
  malformed CSS (silently accepted), size cap (bisected to 256,018 bytes).
- **[exec]** Mobile: identical bundle and identical token resolution on a Pixel 7
  emulation profile with `mobileApp` on and off; the coarse-pointer media query
  was confirmed to override part of the type scale.

**Not verified:** the code editors' internal colour scheme beyond the `--ansi-*`
and `--diffs-*` tokens; the syntax-highlight palette itself, which follows the
resolved Pierre/Shiki code theme rather than theme CSS; and any behaviour
requiring a bb restart.

---

## 10. Sources

1. bb CLI skill reference, `references/theming.md` — read in full:
   `~/.bb/runtime/global-skills/ac9c3e39fc5cdd7186006561c13ec9a2930b1054ced9368d4e6e972808f130c3/skills/bb-cli/references/theming.md`
2. `bb guide customization` — the packaged guide, run locally.
3. Bundled app stylesheet (Tailwind v4.3.0 output):
   `.../bb-app/app/dist/assets/index-C5-8cYca.css` — primary source for the
   complete token list and every derivation percentage.
4. `bb theme show --json` and `bb settings show` — resolved runtime state.
5. Live DOM probes at `http://127.0.0.1:38886` via Playwright/Chromium.
6. https://diffs.com/theme — Pierre/Shiki theme JSON format (referenced by bb's
   own docs; not independently consulted for this document).
