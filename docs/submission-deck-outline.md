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
- Find prediction markets whose pricing looks fragile, stale, or weakly supported
- Explainable ranking, not a black-box score dump
- Built and deployed through a real Zerve notebook-to-app pipeline

### Speaker notes
Prediction markets are powerful, but most interfaces still make you scan one market at a time. We built a live radar that surfaces which markets deserve a second look right now, and explains why they surfaced.

## Slide 2, Problem

### Slide title
The problem with raw market interfaces

### On-slide content
- too many markets, too little prioritization
- fragile or weakly supported pricing can hide in plain sight
- raw odds alone do not explain which markets deserve inspection first

### Speaker notes
The problem is not a lack of market data, it is a lack of triage. If you want to inspect market quality, you should not need to manually browse endless raw odds and guess what looks unstable or stale.

## Slide 3, Solution

### Slide title
A ranked radar for markets that deserve scrutiny

### On-slide content
- ranks markets that look stale, fragile, extreme, or weakly supported
- surfaces explanation headlines and drilldown detail
- keeps the MVP honest about scope and confidence

### Speaker notes
The product claim is intentionally tight. We are not saying we know the true fair value of every market. We are saying we can rank which markets look most worthy of inspection and explain the reasons behind that ranking.

## Slide 4, Product flow

### Slide title
How the product works

### On-slide content
1. ingest live Polymarket markets
2. normalize and categorize markets
3. build market features and score fragility signals
4. generate explanations and a deployed radar app

### Speaker notes
This is a real end-to-end flow. The notebook ingests live market data, normalizes it, builds features, scores markets, generates explanations, and feeds the deployed Streamlit app.

## Slide 5, Live product proof

### Slide title
Live demo proof

### On-slide content
- Radar view ranks live markets with explanation headlines
- Detail view shows score drivers, signals, and caveats
- Methodology view explains what the score means and what it does not mean

### Speaker notes
This is the strongest demo section. Start on the Radar view, click into a top market, and show that the score is interpretable. Then briefly show the Methodology page to reinforce that the scope is honest and deliberate.

## Slide 6, Why this is credible

### Slide title
Why the output is worth trusting

### On-slide content
- explainable fragility scoring
- visible QA warnings and caveats
- product surfaces evidence, not just a rank
- deployed app connected to the live notebook pipeline

### Speaker notes
We tried hard not to build a flashy but dishonest project. The app exposes caveats, shows QA warnings, and explains why a market surfaced instead of hiding behind an opaque score.

## Slide 7, Why Zerve matters

### Slide title
Why this fits ZerveHack

### On-slide content
- notebook pipeline and deployed app are connected in one environment
- analysis becomes a usable product with a real app surface
- real deployment with a usable app, not static screenshots

### Speaker notes
The Zerve story matters here. This project turns live notebook analysis into a usable deployed product. The same environment handles ingestion, scoring, explanation generation, and deployment.

## Slide 8, MVP honesty and next steps

### Slide title
What is live now, and what comes next

### On-slide content
Live now:
- Polymarket-first MVP
- deployed radar, detail, and methodology views
- explanation-rich market ranking

Next:
- add cross-source comparison
- strengthen confidence calibration
- expand richer event/news context

### Speaker notes
The MVP is intentionally single-source and honest about that. The obvious next step is cross-source confirmation, but the current version already demonstrates a strong explainable workflow end to end.

## Default compact 6-slide deck

This is the current default deck path.

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
