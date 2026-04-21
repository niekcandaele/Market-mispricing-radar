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
- `artifacts/submission/local-radar-view.png`
- `artifacts/submission/local-market-detail-view.png`
- `artifacts/submission/local-methodology-view.png`
- `docs/submission-visual-assets.md`

## Recommended deck shape

Target: 6 to 8 slides.

Use a clean, visual deck. Prefer one strong screenshot plus a few bullets over dense text blocks.

## Slide-by-slide build notes

### Slide 1, Title / hook
Use:
- `artifacts/submission/local-radar-view.png`

On-slide emphasis:
- product name
- one-line value proposition
- one strong phrase about explainable market inspection

Avoid:
- too many bullets
- technical implementation details

### Slide 2, Problem
Use:
- either a cropped version of `local-radar-view.png` or a clean text slide with light visual support

On-slide emphasis:
- too many markets
- too little prioritization
- raw odds do not tell you what to inspect first

Speaker note reminder:
- frame this as a triage problem, not just a data problem

### Slide 3, Solution
Use:
- `artifacts/submission/local-radar-view.png`

On-slide emphasis:
- ranks markets that deserve scrutiny
- explanation headlines
- visible caveats and context

Best visual reason:
- this screenshot makes the product immediately legible

### Slide 4, Product drilldown / explainability
Use:
- `artifacts/submission/local-market-detail-view.png`

On-slide emphasis:
- score drivers
- observed signals
- caveats
- drilldown clarity

Speaker note reminder:
- say the score is a triage signal, not a profit promise

### Slide 5, Methodology / honest scope
Use:
- `artifacts/submission/local-methodology-view.png`

On-slide emphasis:
- Polymarket-first MVP
- explainable component-based scoring
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
- optional reuse of `local-radar-view.png` or `local-market-detail-view.png`

On-slide emphasis:
- real notebook-to-app pipeline
- deployed Streamlit product
- explanation-rich ranking
- judge-facing polish completed against live deployment

### Slide 8, Next steps
Use:
- simple text-first slide

On-slide emphasis:
- cross-source comparison
- stronger calibration
- richer context where it improves explainability

Keep it short:
- this is a close, not a roadmap lecture

## Simplified 6-slide version

If the deck should be tighter, use:
1. title / hook with radar screenshot
2. problem and solution
3. product drilldown with detail screenshot
4. methodology / honest scope with methodology screenshot
5. why Zerve matters
6. next steps / close

## Visual rules

- do not put all three screenshots on one slide
- prefer one large screenshot over multiple tiny ones
- crop screenshots only if readability improves
- keep text short enough that the screenshot still matters
- use screenshots to support the spoken story, not replace it

## Best current screenshot-to-slide matches

- strongest product hero: `local-radar-view.png`
- strongest explainability proof: `local-market-detail-view.png`
- strongest credibility / scope proof: `local-methodology-view.png`

## Final build reminder

Once the Google/browser blocker is gone, use this order:
1. build the deck from this kit
2. copy speaker notes from `docs/submission-deck-outline.md` and `docs/judge-demo-script.md`
3. do one readability pass before recording or submitting
