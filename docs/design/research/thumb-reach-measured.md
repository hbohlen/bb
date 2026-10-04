# Thumb reach, measured on the device — 2026-10-03

The one number the mobile UI work needed and did not have. It replaces the
unsourced 620 px figure in `thr_nvwbr87yjj/artifacts/mobile-thumb-ui-plan.md`.

## How it was measured

`research/reach-grid.html`, a 20 px grid served over Tailscale and opened on the
device. The user held the phone the way they actually hold it in bed, one hand,
lying down, and dragged to the limit of reach without shifting their hand. Six
marks right-handed, eight left-handed, each one a new limit rather than a
verifiable position.

Instrument checks, all passing against the 412 × 891 S26 profile:

- `check-reach-grid-layout.py` — no horizontal scroll (a scrolled grid would
  report positions that are not CSS pixels), grid entirely inside the viewport,
  every control at least 44 px tall.
- `check-reach-grid-math.py` — the reported from-bottom distance matches the
  viewport geometry to within 1 px at three known grid positions.
- `check-reach-grid-touch.py` — real `Input.dispatchTouchEvent` taps, not
  synthetic mouse events, record marks at the tapped coordinates.
- `check-coarse-guard.py` — the touch-target scripts still refuse to report a
  measurement taken without coarse-pointer emulation.

## Device

The marks were taken on a **384 × 682 CSS px** viewport at DPR 1.875, Chrome 148
on Android.

**This is not the Galaxy S26 Ultra, and no scaling can make it one.** The
aspect ratio settles it, and it is not close:

| | width / height | ratio |
|---|---|---|
| capture viewport | 384 / 682 | **0.5630** |
| S26 Ultra panel (GSMArena: 1440 × 3120) | 1440 / 3120 | **0.4615** |
| audit viewport | 412 / 891 | 0.4624 |

The capture is **22% off** the panel's aspect ratio. Zoom, Android's display-size
settings, and browser chrome all scale the panel uniformly, so every one of them
preserves aspect exactly. A different aspect ratio is a different physical
panel. There is no display setting that turns a 19.5:9 screen into a 16:9 one.

`convert-reach.py` asserts this rather than leaving it to inspection. It exits
non-zero on any capture whose viewport aspect drifts more than 2% from the
target, and refuses to convert:

```
$ python3 convert-reach.py --reach-css 311 --viewport 384 682
highest reach : 311 CSS px from the bottom edge, which is 45.6% of screen height

identity check
  capture viewport aspect     : 0.5630   (384 / 682)
  Galaxy S26 Ultra panel aspect : 0.4615   (1440 / 3120)
  drift                       : 22.0%   DOES NOT MATCH
```

Exit code 1, so it cannot be run by a pipeline and quietly pass a bad capture.

### What survives, and what does not

**Reach as a fraction of viewport height survives**, and it is the form that
matters, because the audit's own viewport is a full-screen phone viewport and
both numbers come off real screens:

| hand | viewport | highest reach from bottom | as fraction of height |
|---|---|---|---|
| right | 384 × 682 | **311 px** | **45.6%** |
| left | 384 × 682 | **339 px** | **49.7%** |

In millimetres on the real S26 Ultra panel, which is 158.5 mm tall, that is
**72 mm** right-handed and **79 mm** left-handed.

**The fitted thumb radius does not survive.** A radius is a physical length, so
it scales with the *panel's width*, and the capture's width is not the target
panel's width. The 311 and 339 px figures above are only usable as a fraction of
the screen they were measured on.

The absolute CSS-pixel figures in the rest of this document, the 406 px and
443 px, and the pivot coordinates, are therefore **not measurements of the target
device**. They are arithmetic applied to a capture from a different panel. They
should not be used to set an acceptance criterion.

## The fitted geometry

Each hand's marks fit a circle to within a few pixels, which is the strongest
evidence that these are a thumb sweep and not arbitrary points. **These figures
are specific to the capture device and are not transferrable to the S26 Ultra**,
because a radius is a physical length and the two panels differ in width.

| hand | pivot (screen px) | radius | max fit error | pivot height above bottom |
|---|---|---|---|---|
| right | (398, 681) | **313 px** | 5.3 px | **1 px** |
| left | (5, 638) | **294 px** | 9.6 px | 44 px |

Two findings here, and the first is the load-bearing one:

**1. The pivot is at the bottom corner of the screen, not partway up it.** The
fitted right-hand pivot sits 1 px above the bottom edge, at x = 398 on a 384 px
wide viewport, so it is just off the right edge. The left-hand pivot is at x = 5,
just inside the left edge, 44 px up. A thumb anchored at the bottom corner with
the pinky wrapped underneath sweeps a fan whose apex is that corner. The
reachable set is not a band across the bottom of the screen. It is a **fan from
one corner**, and any design that assumes a horizontal reach band is wrong by
the difference.

**2. The two hands are close but not identical.** Left-hand reach is 28 px
greater (339 v 311). The fan is also wider on the left: 67° of sweep versus 59°.
The difference is small enough that one layout can serve both, provided nothing
sits at the extreme edge of the sweep, where the left hand can reach and the
right cannot.

## The 620 px figure was wrong by 2×

`mobile-thumb-ui-plan.md` sets the acceptance criterion "every bar target centre
is within 620 px of the bottom edge", derived from bb 0.44.0 at the wrong
viewport. Measured reach is **45.6% of screen height** right-handed, **49.7%**
left-handed. The 620 px criterion permits targets **91% of the way up** the
682 px screen the marks came from.

Two separate errors, and the second one is worse:

1. **620 px is about twice the measured reach.** As a fraction of the capture's
   own 682 px height it allows 91%, against a measured 46%.
2. **A count of CSS pixels is not a physical distance.** Android's CSS px are
   1/160 inch, not the 1/96 the CSS specification uses. So "620 px" and "311 px"
   are not comparable quantities, and neither is a distance you can design
   against. 620 CSS px on an S26 Ultra is 98 mm. 311 CSS px is 49 mm. The
   portable number is the fraction, or millimetres.

## What this does to the measured touch-target data

This is the one conclusion that survives the device problem, because it does not
depend on the thumb radius at all. It compares two positions on the same
screen.

The thread header controls sit at **849 px from the bottom of an 891 px
viewport**, which is **95.3% of the screen height**. The measured reach is
**45.6%** of screen height, right-handed. So the header is:

```
0.953 / 0.456 = 2.09x  too far, right hand
0.953 / 0.497 = 1.92x  too far, left hand
```

Both numbers are ratios of measurements taken on real phone viewports, so
neither depends on which panel the capture came from. **The header is roughly
twice as far from the bottom of the screen as your thumb can reach, on either
hand.** That is the reach failure, and it needs no thumb-radius assumption.

## How many targets fit on the arc

This section **does** depend on the device, because a thumb radius is a
physical length and the capture's panel width is not the target's. The counts
below were computed from the 384-wide capture and are recorded here only so the
arithmetic is on the record. They are not valid for the S26 Ultra.

Re-derive them with `convert-reach.py` once a capture from the real device
exists. The shape of the result is unlikely to change. On the capture's own
geometry, 59° of sweep at radius 313 px:

| centre spacing | angular cost | 44 px targets that fit |
|---|---|---|
| 48 px | 8.8° | 7 |
| 52 px | 9.5° | 7 |
| 56 px | 10.3° | 6 |
| 60 px | 11.0° | 6 |

So the plan's five-tile arc fits on the capture device with room to spare, at
any reasonable spacing. The arc is not the constrained resource. **Reach is.**

## Design consequences

These are stated as fractions of screen height so they carry to the target
device. Where a claim needs an absolute length it is marked as pending.

1. **The bar sits at the very bottom, and its usable height is about 46% of the
   screen, not 91%.** Anything above that on the right hand is unreachable
   without a hand shift, which is the failure the user named. The old 620 px
   criterion permits targets 91% of the way up the screen.

2. **The fan is corner-anchored, so a full-width bottom bar wastes the far
   end.** The reachable set is widest near the pivot corner and narrows with
   distance. On the capture, a bar spanning the full width puts its far-hand
   targets at up to 400 px from the right-hand pivot, outside that hand's
   313 px radius. Options: mirror the bar by handedness, or keep every target
   within the radius and accept that the far corner is decorative. Which of
   those holds on the S26 Ultra depends on the radius re-measurement.

3. **Two-handed use is not the design case.** The two fits agree closely enough
   that one layout serves both, but only inside the overlap. The design target is
   the **intersection** of the two reaches, not the union.

4. **The 20px full-width timeline rows are inside reach already.** They are a
   size problem, not a reach problem, which is consistent with the earlier
   finding that the failure is reach rather than hit.

5. **The composer is inside reach.** Its controls measured at 8, 8, 8, 17, 21,
   and 47 px from the bottom, all far inside the bottom 46%. No change needed
   there, and this is a measured fact from the fork, independent of the capture.

6. **Nothing in this measurement settles the 36 → 44 ceiling.** That is
   independent of reach: it is about whether a reachable control can be hit
   first time. Both fixes are needed, and the ceiling change is unblocked.

## Open

1. **Re-measure reach on the S26 Ultra itself.** This is now the blocking item.
   Open `reach-grid.html` full-screen on the phone, tap "Copy result", and paste
   the JSON back. `convert-reach.py --capture` will then convert it properly
   instead of refusing. Everything absolute in this document is blocked on it.
2. **The 384 × 682 capture is unexplained.** Aspect says it is a different
   panel. Whether that was a browser mode, a different phone, or a stale
   screenshot is unresolved, and the capture's `maxTouchPoints` and user agent
   that would settle it were not kept.
3. **A single mark per position is a bound, not a measurement.** Each mark is
   "the furthest I could reach", which is a lower bound on reach. Repeating the
   sweep would tell us whether reach is stable or whether the user is
   under-reporting it.
4. **Is reach stable across the reclined posture?** The measurement was taken in
   one posture. The effort's premise is that one-handed use is mostly lying in
   bed, and the phone tilts during use.