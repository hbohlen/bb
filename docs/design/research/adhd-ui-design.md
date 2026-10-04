# ADHD and UI/typography/contrast: what the evidence supports

Research notes for the interface redesign. Every claim below is labelled by evidence tier:

- **[PEER-REVIEWED]** — primary study, systematic review or meta-analysis
- **[STANDARD]** — W3C / official body (WCAG, NICE)
- **[FIRST-PARTY]** — designer's own claim (font vendor, foundry, agency); not independent evidence
- **[FOLKLORE]** — SEO/blog/agency content with no traceable study behind it

Where no evidence exists, this document says so rather than filling the gap.

---

## 0. TL;DR verdict on the five premises

| Premise | Verdict | One line |
|---|---|---|
| 1. High contrast is better for ADHD | **Partly supported, weaker than assumed** | Reduced contrast sensitivity in ADHD is real but inconsistent across studies; nothing establishes an ADHD-specific contrast threshold. Target AAA, do it for low-vision reasons. |
| 2. Better typography is better for ADHD | **Supported by analogy, not by ADHD trials** | The spacing/legibility evidence is all dyslexia-based. ADHD gets higher letter-spacing and clean layout on a borrowed warrant. |
| 2b. Dyslexia fonts transfer to ADHD | **Refuted as a mechanism; fine as a heuristic** | Font-specific benefits are null even *in dyslexia* (Azzarello meta-analysis, g = −0.04). |
| 3. Minimising distractions helps | **Supported, and is the strongest of the three** | But the strongest ADHD-specific evidence points the *other* way: a demanding task suppresses distraction (Forster & Lavie). |
| 4. Lexend / Atkinson Hyperlegible help ADHD | **No evidence found for either** | Both are defensible on generic legibility grounds; neither has been tested against ADHD. |
| 5. WCAG contrast minimums | **Settled, unambiguous** | AA 4.5:1 / 3:1 large; AAA 7:1 / 4.5:1 large. |

---

## 1. Contrast

### 1.1 Does ADHD reduce contrast sensitivity?

**Yes, on average, but the literature is genuinely inconsistent — and this matters for how much confidence a redesign can claim.**

- **[PEER-REVIEWED]** Bellato, A., Perna, J., Ganapathy, P.S. et al. (2023). *Association between ADHD and vision problems. A systematic review and meta-analysis.* Molecular Psychiatry 28, 410–422. <https://doi.org/10.1038/s41380-022-01699-0>
  - Pre-registered (PROSPERO CRD42021256352), 42 studies in narrative synthesis, 35 in meta-analyses, ~3.25M participants.
  - Finds increased risk of **astigmatism (OR 1.79)**, **hyperopia (OR 1.79)**, **strabismus (OR 1.93)**, **reduced near point of convergence (OR 5.02)**, increased accommodative lag (Hedge's g = 0.63), and **self-reported vision problems (g = 0.63)**.
  - Notably **no** difference in retinal nerve fibre layer thickness or refractive error — i.e. **functional, not structural**, findings.
  - The paper reports reduced contrast sensitivity in ADHD (Hedge's g = −2.82, 95% CI [−4.89, −0.75], p = 0.012), but the wide CI means a lot rests on few studies — **and, checked in the full text, the authors' own trim-and-fill sensitivity analyses on contrast sensitivity dropped the model to non-significance (p > 0.05)**. Verified against the article body, not just the abstract. Treat the contrast-sensitivity result as exploratory, not established.
  - Also in the same paper: reduced **colour** discrimination, Hedge's g = 0.51, 95% CI [0.04, 0.99]. Relevant to picking accent colours in a purple theme — the accent should not be the only thing carrying state.
  - Authors' own framing: "ADHD is associated with some self-reported and objectively ascertained functional vision problems, but not with structural alterations of the eye."

- **[PEER-REVIEWED]** Fuermaier, A.B.M., Hüpen, P., De Vries, S.M. et al. (2018). *Perception in attention deficit hyperactivity disorder.* ADHD Attention Deficit and Hyperactivity Disorders 10, 21–47. <https://doi.org/10.1007/s12402-017-0230-0>
  - Systematic review of 36 studies (1996–2016), psychophysical and self/informant report.
  - On contrast sensitivity specifically: **"Results concerning contrast sensitivity were inconsistent."** One study found medium deficits (d = 0.63–0.73), two found none (d = 0.10–0.38).
  - Also found ADHD individuals "experience discomfort to sensory stimuli at a lower level than typically developing individuals" — i.e. hypersensitivity at *lower* intensity, which is the more directly relevant finding for UI.

- **[PEER-REVIEWED]** Ulucan Atas, P.B., Ceylan, O.M., Dönmez, Y.E. et al. (2020). *Ocular findings in patients with attention deficit and hyperactivity.* Int Ophthalmol 40, 3105–3113. <https://doi.org/10.1007/s10792-020-01497-z>
  - n = 37 children with combined ADHD vs 37 controls. **Contrast sensitivity significantly lower at 4 of 5 spatial frequencies** (1.5, 3, 12, 18 cpd). No differences in colour vision, convergence, or acuity.
  - This is the study that actually pushes a design conclusion: *"the level of contrast in the tools used by ADHD patients in daily life settings should be enhanced."*
  - **Caveat to state plainly: n = 74, single study, no replication found.** The recommendation is one author's inference from a small cross-sectional design, not a validated guideline.

- **[PEER-REVIEWED]** Colour vision / contrast discrimination in adults with ADHD (Guillamon & Amado 2014, parts 1 & 2) found colour-saturation discrimination differences **only in females**, and **no difference in contrast sensitivity** between ADHD and control groups. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4219036/>
- **[PEER-REVIEWED]** *Normal visual acuity and electrophysiological contrast…* found no change in retinal contrast gain or background noise in ADHD. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4549567/>
- **[PEER-REVIEWED]** Spatke et al. (2018) found covert spatial attention effects were **indistinguishable** between adult ADHD and controls — a useful counterweight to any claim that ADHD is fundamentally a visual-attention deficit. <https://pmc.ncbi.nlm.nih.gov/articles/PMC5971124/>

**Verdict on premise 1.** "ADHD brains need high contrast" is *directionally defensible but overstated as stated.* There is meta-analytic support for a group-level association between ADHD and reduced contrast sensitivity, plus replicated single-study findings, but also well-powered nulls. Critically: **no study identified here establishes an ADHD-specific contrast threshold.** Nobody has measured "ADHD users need 8:1" or similar. Any such number in a design doc is invented.

**What this means for the redesign:** ship **WCAG AAA (7:1)** for body text rather than the AA floor. Justification must be *low vision + reduced contrast sensitivity subgroup*, not "ADHD brains." That is an honest, defensible reason that happens to also serve ADHD users.

---

## 2. Typography

### 2.1 Letter spacing — the strongest typography evidence, but it is dyslexia evidence

- **[PEER-REVIEWED]** Zorzi, M., Barbiero, C., Facoetti, A. et al. (2012). *Extra-large letter spacing improves reading in dyslexia.* PNAS 109(28), 11455–11459. <https://doi.org/10.1073/pnas.1205566109> (open access: <https://pmc.ncbi.nlm.nih.gov/articles/PMC3396504/>)
  - Purely typographic manipulation, no training. Widened inter-letter spacing on 14pt body text (~2.5pt extra, ≈18% increase) produced ~20% faster reading and roughly halved errors in dyslexic children aged ~8–14.
  - **Verified on re-read 2026-10-03: Zorzi did not change letter spacing alone.** The full text states that "space between words and interline spacing were also increased to maintain a proportionate appearance of the overall text." The word-spacing co-adjustment is part of the intervention, not an afterthought — which is why the counter-evidence below lands where it does.
  - **Critically: this is a dyslexia sample.** The PNAS comment thread (<https://www.pnas.org/doi/10.1073/pnas.1212877109>) and the reply (<https://www.pnas.org/doi/10.1073/pnas.1213265109>) debate whether the effect is dyslexia-*specific*; the authors' position is that the group × spacing **interaction** matters, not the null control result.
  - Zorzi also notes that "the standard letter spacing for text seems to be optimal in skilled adult readers," and that both reduction and increase in spacing harm reading performance in skilled readers. So this is **not** a licence to widen tracking on every surface indiscriminately.
- **[PEER-REVIEWED]** Counter-evidence on spacing: <https://link.springer.com/article/10.1007/s11881-020-00194-x> found that **increasing inter-letter spacing *without* a matching increase in inter-word spacing impaired reading speed**. Letter spacing and word spacing must move together. This is a real design constraint that most "increase tracking" advice omits.

**Practical takeaway:** increase letter spacing **and** word spacing proportionally. Lexend and Atkinson both do this naturally.

### 2.2 Do dyslexia-specific typefaces work? The strongest evidence says no.

- **[PEER-REVIEWED]** Azzarello, C., Paek, S., Hodge, C., Lewis, J. (2026). *Does font improve reading in dyslexic children?: meta-analysis of dyslexia-friendly fonts and dyslexic children's reading performance.* Annals of Dyslexia. <https://doi.org/10.1007/s11881-026-00389-8>
  - 15 studies, 91 effect sizes, **N = 688**, random-effects.
  - Result: **g = −0.04, 95% CI [−0.15, 0.07], p = 0.5** — "no consistent or reliable effect on reading performance in terms of speed or accuracy."
  - This is the single most decisive source in this document. It refutes the marketing claim *for dyslexia itself*. Transferring a dyslexic claim to ADHD is therefore transferring a claim that the source population does not support.
- **[PEER-REVIEWED]** Rello, L. & Baeza-Yates, R. (2013). *Good fonts for dyslexia.* ASSETS '13. <https://dyslexiahelp.umich.edu/wp-content/uploads/2014/02/good_fonts_for_dyslexia_study.pdf> — eye-tracking, n = 48, 12 fonts: **sans-serif, monospaced and roman styles significantly outperformed serif, proportional and italic.** OpenDyslexic itself did not significantly improve reading time or shorten fixations.
- **[PEER-REVIEWED]** *The effect of a specialized dyslexia font, OpenDyslexic, on reading rate and accuracy.* Annals of Dyslexia (2016). Alternating-treatment design: **no improvement in reading rate or accuracy**, individually or as a group. <https://link.springer.com/article/10.1007/s11881-016-0127-1>
- **[PEER-REVIEWED]** *Dyslexie font does not benefit reading in children with or without dyslexia.* Annals of Dyslexia (2017). <https://link.springer.com/article/10.1007/s11881-017-0154-6>

**Verdict on premise 2b.** **Refuted as a mechanism.** Specialised dyslexia fonts have no measurable reading benefit even for dyslexic readers. That said, the *underlying properties* they implement — plain sans-serif, generous spacing, high x-height, low stroke contrast, unambiguous letterforms — do have independent support. Prefer them **for those properties**, and say so.

### 2.3 Is there any ADHD-specific typography evidence?

- **[PEER-REVIEWED, WEAK]** Pytel, C.A.L. et al. *Providing accommodating formats in psychological reports for adults with ADHD to increase client accessibility of information* — examines font styles and textual emphasisers in assessment report summaries/recommendations for adults with ADHD. Proportionate; not a controlled trial. <https://openresearch.okstate.edu/entities/publication/e42bbc4b-ea90-4471-97a0-4fac356de952>
- **[PEER-REVIEWED, DESCRIPTIVE]** *How do adults with neurodevelopmental disorders prefer information being presented?* (2025), Behaviour Research Methods / Taylor & Francis. <https://doi.org/10.1080/09523987.2025.2544118>
  - n = 204 adults with diagnosed ADHD, autism, dyslexia, dyscalculia or dyspraxia, surveyed on preferred font style, font size, character spacing, line spacing, title design, background colour, reward icon and instruction layout.
  - **Important limitation: this is a preference survey, not a performance study.** Preference ≠ benefit. Also groups ADHD with four other diagnoses, so ADHD-specific conclusions cannot be isolated from it.
- **[PEER-REVIEWED]** Phalke, S.S., Shrivastava, A., & Sahgal, P. — series of papers on visual design guidelines for digital content for children with ADHD, covering font size, font type, line spacing, background colour and illustrations. A nine-month experimental study is in preprint. Low visibility; treat as suggestive, not settled. <https://gyan.iitg.ac.in/items/5c91501f-5fde-41ff-b7dd-ba62e2f96b22>
- **[PEER-REVIEWED]** Fuermaier et al. (2018), above, establishes that ADHD participants report sensory discomfort at *lower* stimulus levels than controls. This is the most defensible ADHD-specific bridge to typographic generosity: lower tolerance for sensory intensity supports more whitespace, not specifically wider tracking.

**Verdict.** **No evidence found** that any particular typographic setting is superior for a clinically diagnosed ADHD population. Line height ~1.5, shorter line length, and chunking are **defensible defaults**, but they are conventions adopted from dyslexia practice and general readability literature, not ADHD findings. Do not attribute them to ADHD research.

**Flag as [FOLKLORE]:** every source encountered claiming quantified typography benefits for ADHD specifically — e.g. `designyourway.net/blog/best-fonts-for-adhd`, `neurolaunch.com`, `academync.com`, `focusflowapp.in`. Several cite invented-looking statistics ("line spacing of 1.5x increases readability by 15%, per the National Center for …" from `worldmetrics.org`) with no traceable study. None should be cited in a design doc.

---

## 3. Distraction: both sides

### 3.1 Side A — reducing distractions and notifications helps

- **[PEER-REVIEWED]** Kushlev, K., Proulx, J.D.E., & Dunn, E.W. (2016). *"Silence Your Phones": Smartphone Notifications Increase Inattention and Hyperactivity Symptoms.* CHI '16, 1011–1020. **Correct DOI: <https://doi.org/10.1145/2858036.2858359>** — an earlier draft of this document cited `10.1145/2858036.2858223`, which resolves to an unrelated paper ("Expressy", a wrist-worn IMU paper). Corrected on re-verification 2026-10-03.
  - Two-week within-subject experiment, n = 221 from the general population (not clinically diagnosed). Alerts-on vs alerts-off weeks.
  - Participants reported **significantly higher inattention and hyperactivity with alerts on**; higher inattention in turn predicted lower productivity and psychological wellbeing.
  - Scope limit: measures *ADHD-associated symptoms in the general population*, not diagnosed ADHD. Direction is relevant; magnitude is not transferable.
- **[PEER-REVIEWED]** *Blocking mobile internet on smartphones improves sustained attention…* PNAS Nexus 4(2), pgaf017. Two-week experiment: reduced smartphone use improved subjective wellbeing, mental health, and **objectively measured sustained attention**; 91% improved on at least one outcome. <https://academic.oup.com/pnasnexus/article/4/2/pgaf017/8016017>
- **[PEER-REVIEWED]** Irvine, B., Elise, F., Brinkert, J. et al. (2024). *'A storm of post-it notes': Experiences of perceptual capacity in autism and ADHD.* Neurodiversity. <https://doi.org/10.1177/27546330241229004>
  - n = 312 (108 autistic, 40 ADHD, 79 autistic+ADHD, 85 neurotypical), thematic analysis of survey data.
  - Neurodivergent participants across all groups report a "barrage of information." **The ADHD-specific distinction is valuable and non-obvious:** autistic participants describe this as *overwhelming* (they take in more), whereas ADHD participants describe it as *overload* (they cannot select what to attend to). Different mechanism, same felt experience. For an ADHD interface this argues against a maximalist "show everything" layout.
- **[PREPRINT, VERIFIED]** *AttentionGuard* (arXiv 2602.07865, submitted 8 Feb 2026; Wizard-of-Oz pilot, **n = 11** adults self-reporting ADHD or ASRS ≥ 4; NASA-TLX 47.2 vs 62.8, d = 1.21; comprehension 78.4% vs 61.2%; two participants abandoned baseline sessions). Verified against the abstract — but note the headline result is **not** distraction reduction. Its central claim is **bi-directional scaffolding**: the adaptive condition responds to *overstimulation* by reducing complexity and **to understimulation by injecting novelty, curiosity hooks and gamified elements**. That is direct support for §3.2 below: ADHD users need scaffolding added in both directions, not a uniformly calmer screen. Two abandoned baseline sessions is a small but real threat to the comparison.
- **[PREPRINT, VERIFIED]** *FocusView* (arXiv 2507.13309, **n = 12** adults with ADHD, informational-video customisation) reports reduced-distraction controls improved *perceived* viewability (self-report, not a performance measure), and found **participants for whom background music was a distraction in one context and a stimulation boost in another** — i.e. distraction is partly user-specific, which argues for **user-configurable** rather than imposed simplification. Also surfaced a practical constraint worth stealing: *reduce the number of customisation options, because the options themselves distract.* Preprint tier; do not lean on it.

### 3.2 Side B — ADHD users often need *more* external structure, not less

This is the part most redesign guidance gets backwards.

- **[STANDARD]** NICE NG87, *Attention deficit hyperactivity disorder: diagnosis and management* (2018, updated 2019). <https://www.nice.org.uk/guidance/ng87/chapter/recommendations>
  - The guideline's own definition of **environmental modifications** explicitly includes **adding** structure, not only removing clutter:
    > "Examples may include changes to seating arrangements, changes to lighting and noise, **reducing distractions (for example, using headphones)**, optimising work or education to have **shorter periods of focus with movement breaks (including the use of 'I need a break' cards)**, **reinforcing verbal requests with written instructions** and, for children, the appropriate use of teaching assistants at school."
  - NICE also advises parents/carers on "structure in the child or young person's day" and clear, consistent rules.
  - **Read that list closely: three of the six examples ADD external aids** (break cards, written instructions, teaching assistants). Only one is about reduction.
  - For adults, NICE recommends medication only **after** environmental modifications have been implemented *and reviewed* — i.e. the environment is a first-line intervention, not a consolation prize. <https://primarycare.northeastlondon.icb.nhs.uk/wp-content/uploads/2023/08/Methylphenidate-lisdexamfetamine-dexamfetamine-and-atomoxetine-adult-ADHD-SCG_07.2023.pdf>
- **[PEER-REVIEWED]** Jurek, L., Duchier, A., Gauld, C. et al. (2025). *Sensory Processing in Individuals With ADHD Compared With Control Populations: A Systematic Review and Meta-analysis.* J Am Acad Child Adolesc Psychiatry. PROSPERO CRD42022325271. <https://sensoryproject.org/wp-content/uploads/2025/04/Jurek-et-al-2025.pdf>
  - 30 studies, **N = 5,374** (23 child, 7 adult studies). ADHD participants show significantly more severe atypical sensory processing across **every quadrant**: sensory sensitivity (SMD 1.17), sensory avoiding (1.15), low registration (1.22), seeking (1.23).
  - Heterogeneity very high (I² 87–97%); only 9 studies at low risk of bias. Authors note **ADHD clinical guidelines do not currently include assessment of sensory processing** and argue it should be.
  - Reading for design: this supports reducing *unintentional* sensory input, and equally supports not stripping the interface of legitimate external structure.
- **[PEER-REVIEWED]** Forster, S., Robertson, D.J., Jennings, A., Asherson, P., & Lavie, N. (2013). *Plugging the Attention Deficit: Perceptual Load Counters Increased Distraction in ADHD.* Neuropsychology 28(1), 91–97. <https://doi.org/10.1037/neu0000020> (open access: <https://pmc.ncbi.nlm.nih.gov/articles/PMC3906797/>; abstract verified at <https://discovery.ucl.ac.uk/id/eprint/1425379/>)
  - **This is the most important finding in the whole document for redesign purposes.** Per **Load Theory** (Lavie), raising perceptual load of the attended task *eliminates* distractor processing. In this study, perceptual load **significantly reduced distractor interference for the ADHD group as effectively as for controls**.
  - **Verified verbatim on re-verification 2026-10-03.** Adults with ADHD showed significantly greater distractor interference than age- and IQ-matched controls, **p = .005, ηp2 = .231**. The load manipulation then "significantly reduced distractor interference for the ADHD group and was as effective in reducing the elevated distractor interference in ADHD as it was for controls." Task was a letter-search with load varied by set size; distractors were salient irrelevant cartoon images on 10% of trials.
  - Note the author list: **Forster, Robertson, Jennings, Asherson & Lavie** — Asherson is a clinical ADHD researcher, which is why this counts as a diagnosed-sample study rather than the general-population symptom survey of §3.1. An earlier draft attributed this to "Forster & Lavie 2013" generically, which obscured that it is the ADHD-specific study.
  - **Design implication, stated carefully:** a plain, low-stimulation "single-focus" interface is not obviously the right target. It is arguable that a *demanding* foreground task is what protects attention — which argues for one clearly-demanding primary task, not an empty screen. Load ≠ clutter. A screen with high perceptual load and zero competing items can protect attention better than a "calm" screen with a weak foreground.

**Verdict on premise 3.** **Confirmed for distraction and notification reduction; contested for visual simplification.** Both effects are real and they point in different directions. NICE's own list puts both in the same paragraph. The defensible synthesis for this redesign:

- Remove *unsolicited* input: notifications, badges, animations, autoplay, non-essential chrome.
- *Add* *solicited* structure: explicit written instructions, visible state, clear single next action, save/resume, no time pressure.
- Keep one clearly-demanding foreground task (Load Theory) rather than a sparse, ambiguous screen.

---

## 4. The two typefaces

### 4.1 Lexend

| Field | Finding | Tier |
|---|---|---|
| Origin | Conceived 1999–2000 by **Dr Bonnie Shaver-Troup**, EdD, an educational therapist in Silicon Valley | [FIRST-PARTY] |
| Digital cut | **2004**, commissioned to type designer **Linnea Lundquist** | [FIRST-PARTY] |
| Current form | **2018**, digitised for Google Fonts by **Thomas Jockin**, derived from Andrew Paglinawan's Quicksand; variable weight axis added by Font Bureau March 2021; Arabic expansion 2021 | [FIRST-PARTY] |
| Licence | OFL-1.1 (free, all commercial use) | [FIRST-PARTY] |
| Designed for | Readers whose reading performance is limited by **visual crowding and masking** — targeting dyslexia and struggling readers | [FIRST-PARTY] |

Sources: <https://design.google/library/lexend-readability>, <https://github.com/googlefonts/lexend> (repo archived April 2026, read-only), <https://www.lexend.com/>

**Evidence quality — this is the part to be careful about.**

- **[FIRST-PARTY, WEAK]** The headline "empirically shown to significantly improve reading-proficiency" claim on lexend.com rests on **one study of 20 third-graders** reading aloud in five fonts at 16pt, set two grade levels above their level. N = 20. No peer-reviewed journal. No reported effect sizes, CIs, or statistics in the public description. Two grade levels above grade level means the floor of the task is controlled, but the design is far too small to establish a general claim.
- **[FIRST-PARTY, UNVERIFIABLE]** The claim of "validated studies at Vanderbilt University" appears **only** on third-party SEO sites (`focusflowapp.in`, `homeschoolpicks.com`). I found **no trace of a Vanderbilt study in any primary source.** Do not repeat this claim. It is an SEO artefact.
- **[PEER-REVIEWED, INDIRECT]** Lexend implements, consistently: sans-serif form, high x-height, low stroke contrast, generous letter *and* word spacing, unambiguous `i`/`l`/`j`. Each of those properties has independent support — including the spacing evidence that is the actual causal mechanism (Zorzi 2012). So Lexend is defensible **by construction**, not by any test of Lexend itself.
- **ADHD-specific evidence: none found.** No study of Lexend with a diagnosed ADHD sample.

### 4.2 Atkinson Hyperlegible

| Field | Finding | Tier |
|---|---|---|
| Commissioned by | **Braille Institute of America** | [FIRST-PARTY] |
| Designed by | **Applied Design Works**, 2019 | [FIRST-PARTY] |
| Named after | J. Robert Atkinson, founder of the Braille Institute | [FIRST-PARTY] |
| **Designed for** | **Readers with low vision / partial sight** — explicitly *not* dyslexia, explicitly *not* ADHD | [FIRST-PARTY] |
| Design principle | Maximise pairwise character distinctness | [FIRST-PARTY] |
| Licence | Free for personal and all commercial use | [FIRST-PARTY] |

Sources: <https://www.brailleinstitute.org/freefont/>, <https://accessibility.tools/docs/dyslexia/font-atkinson-hyperlegible>

Specific design features (Braille Institute, [FIRST-PARTY]): unambiguous letterforms (`B`/`8`, `O`/`0`); clear uprights (`1`/`I`/`i`/`l`); distinct pairs (`E`/`F`, `p`/`q`); open counters (`e`/`b`/`g`/`s`); spurs and tails (`g`/`m`/`n`/`r`); special circular forms for `Å`/`9`/`%`/`.`. Recognition: Fast Company Innovation by Design Award (2019); Cooper Hewitt, Smithsonian Design Museum permanent collection (2024). Current family: Atkinson Hyperlegible (2019), Hyperlegible Next (2025, 7 weights, 150+ languages), Hyperlegible Mono (2025).

**Evidence quality.**

- **[GAP, INDEPENDENTLY DOCUMENTED]** accessibility.tools: *"there is currently no independent, published research specifically testing Atkinson Hyperlegible"* — for dyslexia *or* ADHD. Its claims rest on typographical theory and internal qualitative user testing. <https://accessibility.tools/docs/dyslexia/font-atkinson-hyperlegible>
- **[FOLKLORE — high reach, actively harmful]** The widely circulated claim that Atkinson Hyperlegible is "validated across 12 peer-reviewed studies," "increases immediate recall by 27%," and "reduces saccadic refixation errors by 39%" cites *"Journal of Cognitive Engineering, 2022."* **I could not locate that paper.** Searching that journal's 2022 volume turned up unrelated human–AI trust research. The claim appears on content-farm pages (e.g. `lifetips.alibaba.com`) that also assert reductions in "visual fatigue metrics (pupil dilation)". **Do not put these numbers in a design document.** They are almost certainly fabricated.
- **ADHD-specific evidence: none found.**

### 4.3 Head-to-head conclusion

Neither font has been tested against ADHD. Both are defensible choices on generic legibility grounds, and both are free/OFL. The decision between them is a design-values decision, not an evidence decision:

- **Atkinson Hyperlegible** — better if the audience includes low vision or older users; distinctness-first design.
- **Lexend** — better if the goal is reading fluency at length; spacing-first design.
- Either way, the **spacing** is the part with actual mechanism behind it.

---

## 5. WCAG contrast numbers (settled)

All from W3C WCAG 2.2 Understanding docs — **[STANDARD]**.

### 5.1 Text

| Criterion | Level | Normal text | Large text |
|---|---|---|---|
| **1.4.3 Contrast (Minimum)** | AA | **4.5:1** | **3:1** |
| **1.4.6 Contrast (Enhanced)** | AAA | **7:1** | **4.5:1** |

- 1.4.3: <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html>
- 1.4.6: <https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced>

**"Enhanced" is AAA, and the number is 7:1 for normal text / 4.5:1 for large text.** That is the whole of it — AAA is not a different formula, only a higher threshold.

### 5.2 Large text definition

Large-scale text = **18pt, or 14pt bold**, i.e. approximately **24px, or ~18.5px bold** (1pt = 1.333px). WCAG 2.2 adds a note: these general measures are used *except for very thin or unusual fonts*, where the thin strokes need more.

### 5.3 Thresholds are thresholds — do not round

W3C is explicit, in both documents: *"The 3:1 and 4.5:1 contrast ratios … are intended to be treated as threshold values. When comparing the computed contrast ratio to the Success Criterion ratio, the computed values should not be rounded (e.g., 4.499:1 would not meet the 4.5:1 threshold)."*

### 5.4 Anti-aliasing note — directly relevant to type choice

WCAG: *"Due to anti-aliasing, particularly thin or unusual fonts may be rendered by user agents with a much fainter color than the actual text color defined in the underlying CSS. This can lead to situations where text has a contrast ratio that nominally passes the Success Criterion, but has a much lower contrast in practice."* Best practice per W3C: choose a font with stronger/thicker lines, or exceed the requirement.

This is a *standards body's* own reason to prefer heavier weights over thin ones — useful in an ADHD redesign, and citable, unlike a blog post.

### 5.5 Non-text contrast

**SC 1.4.11 Non-text Contrast (Level AA): 3:1** against adjacent colours for (a) visual information needed to identify UI components and their states, and (b) parts of graphics required to understand the content. <https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast>

Directly quoted, and worth quoting in the design doc:

> "For people with cognitive disabilities, it is a best practice to delineate the boundary of all controls, even those that have visible content, to aid in the recognition of controls and the completion of activities."

Also: 3:1 applies to state indicators (focus, selected, checked) but *not* to states that never appear adjacent to each other. And note the anti-aliasing caution here too — avoid thin lines and shapes.

### 5.6 Exemptions (all of 1.4.3 / 1.4.6)

Incidental text (inactive components, pure decoration, not visible, or part of a picture containing significant other visual content); logotypes. **Brand guidelines do not exempt low contrast** — W3C: *"Beyond logos and logotypes, text that has insufficient contrast due to corporate identity or brand guidelines is not exempted."*

---

## 6. What to do, and what to write down

### Well-evidenced — safe to build on

1. **Body text at AAA 7:1** (light and dark). Justify as low-vision/reduced-contrast-sensitivity, not "ADHD brains".
2. **UI components and states at 3:1**, with visible control boundaries — W3C explicitly recommends boundaries for cognitive disabilities.
3. **Letter spacing AND word spacing increased together.** Zorzi 2012 (dyslexia) raised both, plus line spacing — verified in the full text this pass — plus the Springer 2020 finding that letter spacing without word spacing *hurts*.
4. **Prefer heavier weights.** W3C's own anti-aliasing guidance.
5. **No unsolicited input**: no badges, no autoplay, no ambient animation. Kushlev 2016, PNAS Nexus 2025.
6. **One clearly-demanding foreground task**, not a sparse screen. Forster, Robertson, Jennings, Asherson & Lavie 2013 (*Plugging the Attention Deficit*, p = .005, ηp2 = .231).

### Reasonable but not ADHD-evidenced — build it, attribute it honestly

7. Line height ~1.5, line length 50–75 characters, chunked content. Typography and general readability literature, not ADHD research.
8. A well-drawn sans-serif. Rello & Baeza-Yates 2013 (dyslexia) and the null meta-analysis both support plain sans over serif/italic.
9. Atkinson Hyperlegible or Lexend. Chosen for implemented legibility properties, not for any proven ADHD or even dyslexia benefit.

### Do not write in the design doc

- Any contrast threshold described as "what ADHD needs" — no such threshold exists.
- Atkinson Hyperlegible's "27% recall / 39% refixation / 12 peer-reviewed studies / *Journal of Cognitive Engineering* 2022" — source unlocatable, almost certainly fabricated.
- Lexend's "validated at Vanderbilt" — appears only on SEO sites; no primary source.
- Lexend's "empirically shown to significantly improve reading proficiency" without the N = 20 qualifier.
- Any figure of the form "line spacing 1.5x increases readability by 15% per …" — these circulate without traceable studies.
- Any statement that a dyslexia font helps ADHD. The Azzarello 2026 meta-analysis refutes the dyslexia claim at source.

---

## 7. Verification pass (parent agent, this ticket)

The five load-bearing sources were fetched and read directly rather than trusted from the subagent's summary:

| Source | Status |
|---|---|
| Azzarello 2026 meta-analysis (Springer, `s11881-026-00389-8`) | **Confirmed.** Abstract matches the report verbatim: 15 studies, 91 effect sizes, N = 688, g = −0.04, 95% CI [−0.15, 0.07], p = 0.5. Published 31 July 2026. |
| Bellato 2023 (Mol Psychiatry, `s41380-022-01699-0`) | **Confirmed with added detail.** Contrast sensitivity g = −2.8191, CI [−4.8895, −0.7486], p = 0.0118 — but the authors' own trim-and-fill sensitivity analyses **knocked this to non-significance**. §1.1 has been corrected to say so; the earlier draft understated the fragility. Colour-discrimination g = 0.5136 added. |
| AttentionGuard (arXiv 2602.07865) | **Corrected.** Real paper, n = 11, self-report ADHD or ASRS ≥ 4 — not a clinical sample. Its actual headline is *bi-directional* scaffolding (responds to understimulation by **adding** novelty), which strengthens §3.2 rather than §3.1. Re-labelled from PEER-REVIEWED to PREPRINT. |
| FocusView (arXiv 2507.13309) | **Confirmed.** n = 12, exactly as reported; "music as distraction vs. stimulation boost" quote verified in the abstract. |
| Zorzi 2012 PNAS, Forster & Lavie 2013, Kushlev 2016 CHI | **Resolve** to the correct papers via DOI; claims consistent with the abstracts. Not full-text checked — they are not doing load-bearing work beyond direction of effect. |
| Atkinson "27% recall / 39% refixation / *J Cognitive Engineering* 2022" | **Confirmed absent.** Searches for that journal + those figures return only content-farm pages (e.g. `lifetips.alibaba.com`) and unrelated 2022 papers in the journal. Treat the figures as fabricated; the report's warning stands. |

**Net effect on the conclusions: none.** The verdicts in §0 survive verification. What changed is confidence labelling on the contrast-sensitivity premise (weaker than drafted) and a stronger reading of the preprint evidence for §3.2.

---

## 7b. Second verification pass — independent re-fetch, 2026-10-03

Every source below was **re-fetched from its primary URL** and the load-bearing
sentences read in the fetched text, not from the first pass's summary. Verbatim
evidence is attached per source in `## Sources` at the end of this
document.

| Source | Result of independent re-fetch |
|---|---|
| W3C SC 1.4.3 | **Confirmed verbatim.** "The visual presentation of text and images of text has a contrast ratio of at least 4.5:1"; large-scale text "at least 3:1"; and "the computed values should not be rounded (e.g., 4.499:1 would not meet the 4.5:1 threshold)." |
| W3C SC 1.4.6 | **Confirmed verbatim.** Normal text "of at least 7:1"; large-scale text "at least 4.5:1". |
| W3C SC 1.4.11 | **Confirmed verbatim.** "Ensure meaningful visual cues achieve 3:1 against the background", extending to "any visual information necessary to indicate state, such as whether a component is selected or focused". |
| NICE NG87 | **Confirmed verbatim.** Full environmental-modifications sentence, including all three structure-*adding* examples and the one reducing example. The "3 add vs. 1 reduces" reading in §3.2 holds. |
| Azzarello 2026 | **Confirmed from abstract** (Springer gated the body). "dyslexia-friendly fonts have no consistent or reliable effect on reading performance in terms of speed or accuracy", 15 studies / 91 effect sizes / N = 688, g = −0.04, 95% CI [−0.15, 0.07], p = 0.5. |
| Bellato 2023 | **Confirmed, and the first pass's correction is upheld.** Trim-and-fill for contrast sensitivity: "in both cases, no studies were estimated as missing, but the uni-level meta-analytic models became non-significant". Publication bias was detected for both colour vision and contrast sensitivity. |
| Zorzi 2012 | **Confirmed from full text — and one material omission found.** "Space between words and interline spacing were also increased to maintain a proportionate appearance of the overall text." §2.1 has been amended: Zorzi raised word and line spacing too, so letter spacing alone is not the finding. |
| Forster et al. 2013 | **Confirmed with full author list and effect sizes, which the first pass lacked.** Forster, Robertson, Jennings, **Asherson**, & Lavie. Abstract read verbatim: p = .005, ηp2 = .231. The first pass cited this as "Forster & Lavie 2013" generically, which hid that it is the diagnosed-sample ADHD study. |
| Kushlev et al. 2016 | **DOI in the document was WRONG and is now fixed.** `10.1145/2858036.2858223` resolves to "Expressy", an unrelated wrist-worn IMU paper. Correct DOI is `10.1145/2858036.2858359`. Abstract confirmed: n = 221 general population, "Participants reported higher levels of inattention and hyperactivity when alerts were on than when alerts were off", and the scope limit "even in people not clinically diagnosed with ADHD" is the authors' own wording. |
| Atkinson folklore figures | **Confirmed absent from both first-party sources.** The Braille Institute Atkinson page and the official `googlefonts/atkinson-hyperlegible` repository were both searched for "27%", "39%" and "refixat*" — **zero hits in either.** Absence from the maker's own pages is stronger evidence of unsourcing than the first pass's journal-volume search. |
| Lexend | **Confirmed first-party.** "Lexend is a variable typeface designed by Bonnie Shaver-Troup and Thomas Jockin in 2018", designed for "improving reading fluency in low-proficiency readers (including those with dyslexia.)" — a first-party design claim, explicitly not an ADHD claim. No "Vanderbilt" mention present. |

### Dead-URL finding

The Atkinson page most commonly cited for the folklore figures,
`brailleinstitute.org/freefont/why-atkinson-hyperlegible/`, returns **HTTP 404**.
The live equivalent is `brailleinstitute.org/freefont/`. Citations should use the
live URL.

### What this pass did *not* verify

- Azzarello's results tables (paywalled) — abstract only.
- Whether any *other* Atkinson study exists anywhere. Absence on two first-party
  pages is evidence of unsourcing, not proof of absence.
- The negative result on ADHD-specific typography is a **search that found
  nothing**, not a proof that none exists.

---

## Source list by tier

**[STANDARD]**
- W3C, *Understanding SC 1.4.3 Contrast (Minimum)* — <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html>
- W3C, *Understanding SC 1.4.6 Contrast (Enhanced)* — <https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced>
- W3C, *Understanding SC 1.4.11 Non-text Contrast* — <https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast>
- NICE NG87, *ADHD: diagnosis and management*, recommendations + glossary — <https://www.nice.org.uk/guidance/ng87/chapter/recommendations>

**[PEER-REVIEWED]**
- Bellato et al. 2023, *Mol Psychiatry* 28:410–22 — <https://doi.org/10.1038/s41380-022-01699-0>
- Fuermaier et al. 2018, *ADHD Atten Def Hyp Disord* 10:21–47 — <https://doi.org/10.1007/s12402-017-0230-0>
- Ulucan Atas et al. 2020, *Int Ophthalmol* 40:3105–13 — <https://doi.org/10.1007/s10792-020-01497-z>
- Jurek et al. 2025, *J Am Acad Child Adolesc Psychiatry* — <https://sensoryproject.org/wp-content/uploads/2025/04/Jurek-et-al-2025.pdf>
- Forster, Robertson & Jennings 2013, *Neuropsychology* 28(1):91–97 — <https://doi.org/10.1037/neu0000020>
- Irvine et al. 2024, *Neurodiversity* — <https://doi.org/10.1177/27546330241229004>
- Kushlev, Proulx & Dunn 2016, *CHI '16* 1011–20 — <https://doi.org/10.1145/2858036.2858359> (corrected; the `…2858223` DOI in earlier drafts points at an unrelated paper)
- *Blocking mobile internet…* 2025, *PNAS Nexus* 4(2):pgaf017 — <https://academic.oup.com/pnasnexus/article/4/2/pgaf017/8016017>
- Zorzi et al. 2012, *PNAS* 109(28):11455–9 — <https://doi.org/10.1073/pnas.1205566109>
- Azzarello, Paek, Hodge & Lewis 2026, *Annals of Dyslexia* — <https://doi.org/10.1007/s11881-026-00389-8>
- Rello & Baeza-Yates 2013, *ASSETS '13* — <https://dyslexiahelp.umich.edu/wp-content/uploads/2014/02/good_fonts_for_dyslexia_study.pdf>
- *OpenDyslexic reading rate and accuracy*, *Ann Dyslexia* 2016 — <https://link.springer.com/article/10.1007/s11881-016-0127-1>
- *Dyslexie font does not benefit reading…*, *Ann Dyslexia* 2017 — <https://link.springer.com/article/10.1007/s11881-017-0154-6>
- Letter/word spacing interaction — <https://link.springer.com/article/10.1007/s11881-020-00194-x>
- Neurodevelopmental formatting preferences (n = 204, survey) — <https://doi.org/10.1080/09523987.2025.2544118>

**[FIRST-PARTY]**
- Braille Institute, Atkinson Hyperlegible — <https://www.brailleinstitute.org/freefont/>
- Google Design, *Clean and clear: making reading easier with Lexend* — <https://design.google/library/lexend-readability>
- googlefonts/lexend repo (archived) — <https://github.com/googlefonts/lexend>
- Lexend.com — <https://www.lexend.com/>

**[DOCUMENTED GAPS]**
- accessibility.tools on Atkinson Hyperlegible — <https://accessibility.tools/docs/dyslexia/font-atkinson-hyperlegible>

---

## Sources

Every source above, with the verbatim sentence each claim rests on. Quotes were
attached only after the text appeared literally in the fetched page — a
paraphrase is rejected by the ledger.

[1] https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — WCAG 2.2 SC 1.4.3 Contrast (Minimum)
    > "text and images of large-scale text have a contrast ratio of at least 3:1;"
    > "the computed values should not be rounded (e.g., 4.499:1 would not meet the 4.5:1 threshold)."
    > "The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following:"
[2] https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html — WCAG 2.2 SC 1.4.6 Contrast (Enhanced)
    > "of at least 7:1, except for the following:"
    > "text and images of large-scale text have a contrast ratio of at least 4.5:1;"
    > "The visual presentation of text and images of text has a contrast ratio of at least 7:1, except for the following:"
[3] https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — WCAG 2.2 SC 1.4.11 Non-text Contrast
    > "Ensure meaningful visual cues achieve 3:1 against the background."
    > "any visual information necessary to indicate state, such as whether a component is selected or focused must also ensure that the information used to identify the control in that state has a minimum 3:1 contrast ratio."
[4] https://www.nice.org.uk/guidance/ng87/chapter/recommendations — NICE NG87: ADHD — diagnosis and management (recommendations)
    > "Examples may include changes to seating arrangements, changes to lighting and noise, reducing distractions (for example, using headphones), optimising work or education to have shorter periods of focus with movement breaks (including the use of 'I need a break' cards), reinforcing verbal requests with written instructions and, for children, the appropriate use of teaching assistants at school."
[5] https://link.springer.com/article/10.1007/s11881-026-00389-8 — Azzarello et al. (2026) meta-analysis: dyslexia-friendly fonts, Annals of Dyslexia
    > "Using a random-effects model, the results indicate that dyslexia-friendly fonts have no consistent or reliable effect on reading performance in terms of speed or accuracy."
    > "This meta-analysis synthesizes data from 15 empirical studies (91 effect sizes;"
    > "p = 0.5."
[6] https://pmc.ncbi.nlm.nih.gov/articles/PMC3396504 — Zorzi et al. (2012) Extra-large letter spacing improves reading in dyslexia, PNAS
    > "Here, we show that a simple manipulation of letter spacing substantially improved text reading performance on the fly (without any training) in a large, unselected sample of Italian and French dyslexic children."
    > "Space between words and interline spacing were also increased to maintain a proportionate appearance of the overall text"
[7] https://www.nature.com/articles/s41380-022-01699-0 — Bellato et al. (2023) ADHD and vision problems, systematic review + meta-analysis, Mol Psychiatry
    > "in both cases, no studies were estimated as missing, but the uni-level meta-analytic models became non-significant (both"
    > "publication bias was detected for the meta-analyses of studies on color vision and contrast sensitivity"
[8] https://www.brailleinstitute.org/freefont — Braille Institute: Atkinson Hyperlegible (first-party)
    > "Atkinson Hyperlegible is the first font originally developed in 2019 for low vision readers."
    > "fonts designed to improve legibility and readability for individuals with low vision."
[9] https://github.com/googlefonts/lexend — Lexend, official repository (first-party design claim)
    > "Lexend is a variable typeface designed by Bonnie Shaver-Troup and Thomas Jockin in 2018."
    > "Thomas modified Quicksand for the specialized task of improving reading fluency in low-proficiency readers (including those with dyslexia.)"
[10] https://dl.acm.org/doi/10.1145/2858036.2858359 — Kushlev, Proulx & Dunn (2016) 'Silence Your Phones', CHI '16 — correct DOI
    > "We recruited a sample of 221 participants from the general population."
    > "Participants reported higher levels of inattention and hyperactivity when alerts were on than when alerts were off."
    > "even in people not clinically diagnosed with ADHD"
[11] https://discovery.ucl.ac.uk/id/eprint/1425379 — Forster, Lavie et al. (2013) Plugging the Attention Deficit: Perceptual Load Counters Increased Distraction in ADHD
    > "The presence of these distractors produced a significantly greater interference effect on the search RTs for the adults with ADHD compared with controls, p = .005, ηp2 = .231."
    > "Perceptual load, however, significantly reduced distractor interference for the ADHD group and was as effective in reducing the elevated distractor interference in ADHD as it was for controls."
    > "We tested adults with ADHD and age- and IQ-matched controls on a novel measure of irrelevant distraction under load, designed to parallel the form of distraction that is symptomatic of ADHD."
    > "increased perceptual load as a means of improving the ability to focus attention and avoid distraction"
