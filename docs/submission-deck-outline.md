# Submission Deck Outline and Speaker Notes

## Purpose

This document is the source outline for the hackathon deck, speaker notes, and short demo/video flow.

It is designed so Niek or Cata can present the project quickly without having to reconstruct the story from implementation notes.

## Submission-state checklist

- [x] default demo entrypoint locked to the safe local default path
- [x] safe local default demo entrypoint confirmed
- [x] slide deck created from this outline
- [x] speaker notes copied into the final deck and companion notes doc
- [ ] short demo video recorded on the same story arc
- [ ] final submission links checked

## Demo entrypoints

### Safe default demo
```bash
./scripts/run_local_demo.sh
```

### Optional live upgrade
- active Zerve Streamlit preview from the deploy tab
- current working preview URLs can rotate, so reopen from Zerve if needed
- only switch to this path if it opens cleanly at the final check

## Slide 1, Title / Hook

### Slide title
Market Mispricing Radar

### On-slide content
- A live prediction-market radar for fragile, stale, extreme, or weakly supported prices
- Explainable ranking, not a black-box score dump
- Built and deployed through a real Zerve notebook-to-app pipeline

### Speaker notes
Open with the inspection problem: prediction markets are dense, but most interfaces leave triage to the user.

## Slide 2, Raw odds are not enough

### Slide title
Raw odds are not enough

### On-slide content
- too many markets compete for attention
- fragile pricing can hide in plain sight
- users need reasons, not just ranks

### Speaker notes
Frame the problem as inspection and prioritization, not guaranteed arbitrage.

## Slide 3, Explainable triage surface

### Slide title
The product is an explainable triage surface

### On-slide content
- fetch live Polymarket market data
- score staleness, extremeness, weak support, and instability
- rank markets by inspection priority
- explain why each market surfaced
- expose caveats instead of hiding them

### Speaker notes
Keep this as a product story: the app helps decide what deserves a second look.

## Slide 4, Radar view proof

### Slide title
Radar view proof

### On-slide content
- ranked cards
- explanation headlines
- category context
- visible caveats

### Speaker notes
Show the top-ranked markets and point out the default Putin drilldown path.

## Slide 5, Detail view proof

### Slide title
The score is inspection evidence, not a profit promise

### On-slide content
- score drivers show what moved the market up the radar
- observed signals make the ranking auditable
- caveats keep the MVP honest

### Speaker notes
Use Putin as the refreshed locked default drilldown example.

## Slide 6, Methodology honesty

### Slide title
Methodology honesty

### On-slide content
- Polymarket-first MVP
- explanation-first ranking
- clear limitations
- triage signal, not financial advice

### Speaker notes
This is the honesty beat. Say what the score does and does not claim.

## Slide 7, Why Zerve matters

### Slide title
Why this fits ZerveHack

### On-slide content
- notebook blocks produce the live analysis pipeline
- outputs flow into a deployed Streamlit product
- the workflow turns analysis into something judges can inspect

### Speaker notes
Close the loop from Zerve notebook to deployed app. Mention the safe local default only if needed for recording reliability.

## Slide 8, Submission status

### Slide title
Submission status is near-ready, not pretend-complete

### On-slide content
- ready: locked safe local demo path
- ready: submission copy and notes
- blocked: public Zerve share link

### Speaker notes
Be explicit: the remaining blocker is public sharing, not the product demo.

## Slide 9, Close

### Slide title
A usable radar for markets worth a second look

### On-slide content
- fast triage
- explainable evidence
- honest scope
- default demo: locked safe local path
- drilldown: Putin out as President of Russia by December 31, 2026?

### Speaker notes
End on the value: fast triage, explainable evidence, honest scope.

## Legacy compact 6-slide deck

This is retained as source structure. The current deck artifact is the rebuilt 9-slide `slides-generator` HTML deck at `artifacts/submission/slides-generator-deck/slides.html`.

### Slide 1, Title / hook
Speaker notes:
This is a live inspection radar for prediction markets. The key value is not another market list, it is helping people see which markets deserve a second look right now.

### Slide 2, Problem + solution
Speaker notes:
Most market interfaces give you raw odds but not triage. We turn that into one workflow that ranks the markets most worth inspecting and explains why they surfaced.

### Slide 3, Product flow
Speaker notes:
The workflow is real end to end. We fetch live Polymarket data, normalize it, score fragility signals, generate explanations, and feed a deployed app.

### Slide 4, Explainable product proof
Speaker notes:
This is the strongest demo slide. Start on the Radar, then drill into one market, then briefly reinforce that the Methodology view stays honest about what the score does and does not claim.

### Slide 5, Why Zerve matters
Speaker notes:
This is a strong ZerveHack fit because the notebook pipeline and deployed product live in one environment. It turns live notebook analysis into a usable deployed product.

### Slide 6, Live now / honest room to grow
Speaker notes:
The MVP is intentionally Polymarket-first and explanation-rich. The score is a triage signal, not a profit promise. Next comes cross-source comparison and stronger calibration, but the current version already proves a credible notebook-to-product workflow.

## Short video flow

Target: 60 to 90 seconds.

1. title hook and problem, 10 to 15 seconds
2. Radar view, 20 seconds
3. one market drilldown, 25 seconds
4. Methodology and why the score is honest, 10 to 15 seconds
5. close on Zerve-native proof and next steps, 10 seconds

## Strongest one-line talking points

- This is a live inspection radar for prediction markets built for active inspection.
- The score is designed to prioritize scrutiny, not pretend we know true fair value.
- Every surfaced market comes with an explanation path, not just a rank.
- The deployed app is wired to the real Zerve notebook pipeline end to end.

## If the demo is under one minute

Use this compressed story:

- prediction markets produce too many raw odds and not enough prioritization
- Market Mispricing Radar ranks the markets most worth inspecting right now
- each market has an explanation trail, score drivers, and caveats
- the whole flow is deployed from a real Zerve notebook pipeline
