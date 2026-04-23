# Slide Build Kit

## Purpose

This is the bridge between the deck outline and the actual slide build.

Use it when turning the submission story into Google Slides so the visual choices are mostly pre-made instead of improvised.

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

Default: compact 6-slide deck.

Only expand beyond that if a fuller version becomes clearly stronger.

Use a clean, visual deck. Prefer one strong screenshot plus a few bullets over dense text blocks.

## Expanded 8-slide build notes

### Slide 1, Title / hook
Use:
- `artifacts/submission/slide-ready/local-radar-view-16x9.png`

On-slide emphasis:
- product name
- one-line value proposition
- one strong phrase about explainable market inspection

Avoid:
- too many bullets
- technical implementation details

### Slide 2, Problem
Use:
- `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- or a clean text slide with light visual support if the screenshot makes the slide too repetitive

On-slide emphasis:
- too many markets
- too little prioritization
- raw odds do not tell you what to inspect first

Speaker note reminder:
- frame this as a triage problem, not just a data problem

### Slide 3, Solution
Use:
- `artifacts/submission/slide-ready/local-radar-view-16x9.png`

On-slide emphasis:
- ranks markets that deserve scrutiny
- explanation headlines
- visible caveats and context

Best visual reason:
- this screenshot makes the product immediately legible

### Slide 4, Product drilldown / explainability
Use:
- `artifacts/submission/slide-ready/local-market-detail-view-16x9.png`

On-slide emphasis:
- score drivers
- observed signals
- caveats
- drilldown clarity

Speaker note reminder:
- say the score is a triage signal, not a profit promise

### Slide 5, Methodology / honest scope
Use:
- `artifacts/submission/slide-ready/local-methodology-view-16x9.png`

On-slide emphasis:
- Polymarket-first MVP
- explainable fragility scoring
- honest scope and limitations

Best reason to include:
- it signals credibility because the product explains what it does not claim

### Slide 6, Why Zerve matters
Use:
- either a lighter screenshot reuse or a clean text slide

On-slide emphasis:
- notebook pipeline and deployed app live in one environment
- analysis becomes a usable product
- not a notebook-only project or a fake mockup

### Slide 7, Proof / accomplishments
Use:
- optional reuse of `local-radar-view-16x9.png` or `local-market-detail-view-16x9.png`
- fall back to the uncropped proof captures only if a taller crop is genuinely more readable

On-slide emphasis:
- real notebook-to-app pipeline
- deployed Streamlit product
- explanation-rich ranking
- product-facing polish completed against live deployment

### Slide 8, Next steps
Use:
- simple text-first slide

On-slide emphasis:
- cross-source comparison
- stronger calibration
- richer context where it improves explainability

Keep it short:
- this is a close, not a roadmap lecture

## Default compact 6-slide version

This is the current default deck path.

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
1. keep the compact 6-slide deck as the default unless a fuller version clearly improves the story
2. use this kit for screenshot/layout refinement
3. copy speaker notes from `docs/submission-deck-outline.md` and `docs/judge-demo-script.md`
4. do one final readability and alignment pass before recording or submitting
