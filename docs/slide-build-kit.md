# Slide Build Kit

## Purpose

This is the bridge between the deck outline and the actual slide build.

Use it when turning the submission story into the current slides-generator HTML deck or any future presentation rebuild so the visual choices are mostly pre-made instead of improvised.

## Source inputs

Narrative sources:
- `docs/submission-deck-outline.md`
- `docs/judge-demo-script.md`
- `docs/presenter-cheat-sheet.md`

Visual sources:
- `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- `artifacts/submission/slide-ready/local-market-detail-view-16x9.png`
- `artifacts/submission/slide-ready/local-methodology-view-16x9.png`
- `artifacts/submission/local-radar-view.png`
- `artifacts/submission/local-market-detail-view.png`
- `artifacts/submission/local-methodology-view.png`
- `docs/submission-visual-assets.md`

## Recommended deck shape

Current default: rebuilt 9-slide `slides-generator` HTML deck at `artifacts/submission/slides-generator-deck/slides.html`.

The older compact 6-slide shape below is retained as source structure only. Do not treat it as the active deck artifact.

Use a clean, visual deck. Prefer one strong screenshot or generated visual plus a few bullets over dense text blocks.

## Current 9-slide build mapping

Use this mapping for the rebuilt `slides-generator` deck and any low-risk visual polish pass.

### Slide 1, Title / hook
Use:
- generated hero visual: `artifacts/submission/slides-generator-deck/images/hero.png`

On-slide emphasis:
- product name
- live prediction-market radar
- fragile, stale, extreme, or weakly supported prices
- Zerve notebook-to-app workflow

Speaker note reminder:
- open with the inspection problem: dense markets, weak triage.

### Slide 2, Raw odds are not enough
Use:
- generated inspection visual: `artifacts/submission/slides-generator-deck/images/inspection.png`

On-slide emphasis:
- too many markets compete for attention
- fragile pricing can hide in plain sight
- users need reasons, not just ranks

Speaker note reminder:
- frame this as inspection and prioritization, not guaranteed arbitrage.

### Slide 3, Explainable triage surface
Use:
- text-first layout with strong hierarchy

On-slide emphasis:
- live Polymarket data
- staleness, extremeness, weak support, and instability
- inspection-priority ranking
- explanations and caveats

Best visual reason:
- this slide sets up the product model before the screenshots prove it.

### Slide 4, Radar view proof
Use:
- `artifacts/submission/slides-generator-deck/images/radar.png`

On-slide emphasis:
- ranked cards
- explanation headlines
- category context
- visible caveats

Speaker note reminder:
- point out the default GTA VI drilldown path.

### Slide 5, Detail view proof
Use:
- `artifacts/submission/slides-generator-deck/images/detail.png`

On-slide emphasis:
- score drivers
- observed signals
- caveats
- auditability

Speaker note reminder:
- say the score is inspection evidence, not a profit promise.

### Slide 6, Methodology honesty
Use:
- `artifacts/submission/slides-generator-deck/images/methodology.png`

On-slide emphasis:
- Polymarket-first MVP
- explanation-first ranking
- clear limitations
- triage signal, not financial advice

Best reason to include:
- it makes the project more credible by showing what the score does not claim.

### Slide 7, Why Zerve matters
Use:
- generated pipeline visual: `artifacts/submission/slides-generator-deck/images/pipeline.png`

On-slide emphasis:
- notebook blocks produce the live analysis pipeline
- outputs flow into a deployed Streamlit product
- judges can inspect a real workflow, not static screenshots

### Slide 8, Final-mile truth
Use:
- stats/card layout

On-slide emphasis:
- ready: locked safe local demo path
- ready: submission copy and notes
- blocked: public Zerve share link

Speaker note reminder:
- be explicit that the remaining blocker is public sharing, not the product demo.

### Slide 9, Close
Use:
- clean closing card

On-slide emphasis:
- fast triage
- explainable evidence
- honest scope
- default demo: locked safe local path
- drilldown: GTA VI released before June 2026?

Keep it short:
- this is the close, not a roadmap lecture.

## Legacy compact 6-slide version

This is retained as source structure only. The current deck artifact is the rebuilt 9-slide `slides-generator` HTML deck at `artifacts/submission/slides-generator-deck/slides.html`.

1. title / hook with `local-radar-view-16x9.png`
2. problem and solution with either light radar reuse or a text-first slide
3. product flow as a text-first slide
4. explainable product proof with `local-market-detail-view-16x9.png`
5. why Zerve matters as a text-first slide or very light radar reuse
6. live now / honest room to grow with `local-methodology-view-16x9.png` only if the slide needs visual support

Use these sources for the compact path:
- on-slide copy: `docs/slide-copy-pack.md`
- speaker notes: `docs/submission-deck-outline.md`

### Compact path visual mapping

#### Compact slide 1
Use:
- `artifacts/submission/slide-ready/local-radar-view-16x9.png`

#### Compact slide 2
Use one of:
- a light reuse of `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- or no screenshot if the problem/solution slide reads cleaner as text

#### Compact slide 3
Use:
- no screenshot by default
- keep this as a clean workflow slide unless the final deck feels too text-heavy

#### Compact slide 4
Use:
- `artifacts/submission/slide-ready/local-market-detail-view-16x9.png`

#### Compact slide 5
Use one of:
- no screenshot by default
- or a very light reuse of `artifacts/submission/slide-ready/local-radar-view-16x9.png` if the slide needs visual continuity

#### Compact slide 6
Use one of:
- no screenshot by default
- or `artifacts/submission/slide-ready/local-methodology-view-16x9.png` if the close benefits from visible MVP honesty and scope framing

## Visual rules

- do not put all three screenshots on one slide
- prefer one large screenshot over multiple tiny ones
- prefer the 16:9 slide-ready screenshots as the default deck assets
- keep the uncropped PNGs as backup proof captures, not the first-choice slide visuals
- keep text short enough that the screenshot still matters
- use screenshots to support the spoken story, not replace it

## Best current screenshot-to-slide matches

- strongest product hero: `local-radar-view-16x9.png`
- strongest explainability proof: `local-market-detail-view-16x9.png`
- strongest credibility / scope proof: `local-methodology-view-16x9.png`

## Final build reminder

Use this order:
1. treat `artifacts/submission/slides-generator-deck/slides.html` as the current deck artifact
2. use this kit for screenshot/layout refinement only when it clearly improves the rebuilt deck
3. keep speaker notes aligned with `docs/submission-deck-outline.md` and `docs/judge-demo-script.md`
4. do one final readability and alignment pass before recording or submitting
