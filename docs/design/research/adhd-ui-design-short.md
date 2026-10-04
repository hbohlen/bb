# ADHD and UI design: the short version

**Read time: 3 minutes.** The full evidence is in `adhd-ui-design.md`. This page
gives you the decisions. Every claim there links to a study, a standard, or the
font maker.

**Your job is to rule on the table in section 1.** The rest follows from it.

---

## 1. What the evidence says about your five beliefs

| Your belief | Verdict | Base this on |
|---|---|---|
| High contrast helps ADHD | Partly. Real but weak | Low vision, not ADHD |
| Better type helps ADHD | Weak. The evidence is about dyslexia | Dyslexia studies |
| Dyslexia fonts help ADHD | **No.** Refuted for dyslexia too | One meta-analysis |
| Fewer distractions help ADHD | **Yes, and reversed.** A busy screen can protect attention | Load Theory |
| Lexend or Atkinson helps ADHD | **No evidence either way** | Neither has been tested on ADHD |
| WCAG contrast numbers | Settled | W3C, no debate |

---

## 2. The one result that changes your plan

Your brief asks for a stripped, calm, deep-black screen.

The strongest ADHD study found the opposite. Forster, Robertson, Jennings,
Asherson and Lavie 2013 show that a **demanding foreground task removes
distraction.** Attention stops wandering when the task is hard enough. In that
study the ADHD group started worse than controls, and raising the task load
removed the difference.

**Low load is not protection.** A calm screen with a weak task can let attention
drift. A busy screen with one clear task can hold it.

**What to do.** Remove noise. Add one clear, demanding task. Those are different
actions.

---

## 3. What to build on

These hold up.

1. Body text at **7:1** contrast. This is the AAA level.
2. Controls and states at **3:1**. Add a visible border to each control.
3. Increase **letter spacing and word spacing together.** Zorzi raised word and
   line spacing as well. Letter spacing on its own makes reading worse.
4. Use **heavier** weights. W3C says thin strokes fade on screen.
5. Remove **unsolicited** input. No badges, no animation, no autoplay.
6. Keep one clearly demanding task in front.

## 4. What to build on, honestly

Build these. Do not call them ADHD findings.

7. Line height near 1.5. Lines of 50 to 75 characters.
8. A plain sans-serif face.
9. Lexend or Atkinson Hyperlegible. Choose on design grounds, not health claims.

---

## 5. Never put these in the design doc

Each of these is false or unsourced.

- **Atkinson Hyperlegible: 27% better recall, 39% fewer refixations, 12 studies.**
  The cited 2022 paper does not exist. These numbers are invented.
- **Lexend: validated at Vanderbilt.** No such study exists. It comes from SEO
  sites.
- **Any contrast number described as what ADHD needs.** No study set one.
- **Any dyslexia font claimed to help ADHD.** Refuted at the source.
- **Any figure of the form "line spacing of 1.5x raises readability by 15%."**
  These circulate with no study behind them.

---

## 6. The font choice, in one line

Neither font has been tested on ADHD. Both are free.

- **Atkinson Hyperlegible** if low vision matters to your users.
- **Lexend** if long reading matters to your users.
- Either way, **the spacing is the part with real evidence behind it.**

---

## 7. Contrast numbers you can use

All from W3C WCAG 2.2.

| Level | Normal text | Large text |
|---|---|---|
| AA | 4.5:1 | 3:1 |
| AAA | 7:1 | 4.5:1 |

- Large text means 18pt, or 14pt bold.
- **Do not round.** A value of 4.499 to 1 fails the 4.5 to 1 rule.
- Controls and states need 3:1 against their background.
- A brand rule does not excuse low contrast.

---

## 8. What you must decide

Answer these four. The work cannot start until you do.

1. **Keep the calm screen, or put one demanding task in front?** Section 2 says
   the second. Your brief says the first.
2. **Lexend or Atkinson?** Both are fine. Pick one.
3. **Is 7:1 the floor, or is 4.5:1 enough?** The evidence supports 7:1 for low
   vision.
4. **Do you keep the premise that this is an ADHD project, or a low-vision
   project that also helps you?** The evidence supports the second.

---

**Next step after you decide.** Ticket BB-4 asks whether your problem is reach or
hit. Ticket BB-5 asks which part of bb draws the small buttons. Both change the
plan. Neither has an answer yet.
