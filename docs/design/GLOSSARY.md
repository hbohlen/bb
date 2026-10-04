# Glossary

Terms the bb mobile-UI effort uses. Implementation detail deliberately excluded.

## Reach

The distance a user's thumb can comfortably span from the bottom edge of the
screen without the hand re-gripping. A property of the user and their grip, not
of the device. Measured in pixels from the bottom edge.

## Hit

Whether a control can be reliably pressed on the first attempt. Governed mainly
by its size relative to the minimum touch-target size, and by competing
neighbours.

A control can be within **reach** and still be hard to **hit**. The two failures
are independent and have independent fixes.

## Reachability

How much of the interface a user can operate with one hand, without stretching
or re-gripping. The gap between the controls they need and the controls inside
their **reach**. A property of the whole interface, not of one control.

## Compact viewport

A viewport the host marks as phone-shaped: narrow enough to qualify under the
host's breakpoint, or presenting a coarse pointer. The host's own term and the
host's own decision, passed to plugins as `isCompactViewport`.

## Thumb bar

A fixed strip of controls along the bottom edge of a compact viewport, above the
composer, sized so its targets sit inside the user's **reach** and meet the
minimum touch-target size.

## Thumb arc

A fan of controls opening upward from a single pivot near the bottom of a
compact viewport. Named for the path a thumb sweeps, not for its geometry: every
target lands on the sweep the thumb already makes.

Not a **radial menu** — see below for why.

## Radial menu

A menu whose items are arranged around a centre at varying angles, requiring the
finger to travel an angular distance and land inside a sector.

## Sidebar drawer

The host-drawn, overlay-style presentation of the sidebar used on compact
viewports. Slides over content; closed by backdrop tap or by swipe. Distinct
from the persistent sidebar rail of wide viewports.

## Distraction budget

The amount of simultaneous visual and interactive attention a surface may demand
before it stops supporting a single focus of attention.

Proposed, not yet measurable. Still being defined.

## Deep-black + purple theme

The effort's colour direction: a near-black background with purple as the
accent, and a supporting palette chosen around it. Distinct from a **theme** in
the host's sense — see below.

## Theme

A named palette plus typography override, authored as CSS against the host's
design tokens, applied live to every open window. The host's own term.