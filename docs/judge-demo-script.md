# Judge Demo Script

## One-line pitch

Market Mispricing Radar is a live inspection tool for prediction markets that look stale, fragile, extreme, or weakly supported.

It does not claim certain arbitrage or perfect fair value. It helps people find the markets most worth a second look.

## What to say in the first 20 seconds

Prediction markets are useful, but most interfaces still force you to scan raw odds market by market.

This project turns that into a ranked radar. It pulls live market data, scores markets whose pricing looks fragile, stale, extreme, or weakly supported, and explains why each one surfaced.

## Demo goal

By the end of the demo, a judge should understand:
- what problem the product solves
- what the score means
- why the result is credible enough to inspect further
- why building it inside Zerve matters

## Recommended 90-second demo flow

### 1. Open on the Radar view

Say:

"This landing view shows the live markets that currently deserve the most scrutiny. Instead of a flat list of odds, I get a ranked radar with explanation headlines, filtering, and category context."

Point out:
- top ranked markets
- headline reason on each card
- filters and sort controls
- QA warning summary
- category mix and reason summary tables

### 2. Click into one market

Use a top-ranked example.

Say:

"Now I can drill into a single market and see why it was flagged, what signals are driving the score, and what caveats still apply."

Point out:
- headline explanation
- score drivers
- observed signals
- comparable markets
- caveats

Important framing:

"The score is a triage signal. Higher does not mean guaranteed profit. It means more evidence that the market deserves inspection."

### 3. Show Methodology briefly

Say:

"This page makes the scope honest. It explains what the product does, what it does not claim, and how the current MVP is intentionally conservative."

Point out:
- Polymarket-first MVP scope
- explainable fragility scoring
- single-source caveat
- no fake promise of perfect pricing

### 4. Close with the Zerve proof

Say:

"This is a real deployed workflow. The deployed Streamlit app is reading live notebook outputs from the real Zerve pipeline end to end."

## Strongest proof points to mention

- real Zerve notebook pipeline is live end to end
- deployed Streamlit app reads notebook outputs through Zerve variable loading
- markets are ranked with explanations, not just scores
- category inference was improved and validated in live deployment
- presentation copy, drilldowns, and tables were polished directly against the deployed preview

## What the score means

Use this wording if needed:

"The score combines signals like staleness, time to resolution, price extremeness, liquidity support, and movement or volatility proxies when available. It is designed to surface fragile pricing situations, not to pretend we know the true fair value of every market."

## What makes this a strong hackathon project

- clear problem, fast to understand
- live deployed product, not just analysis notebooks
- honest scope and methodology
- explainable outputs instead of black-box ranking
- strong Zerve-native story: ingestion, notebook pipeline, and deployed app all connected

## If time is very short

Use this compressed version:

1. "We built a live radar for prediction markets that deserve a second look."
2. "It ranks fragile or weakly supported markets and explains why they surfaced."
3. "This detail view shows the score drivers and caveats for one market."
4. "It is running through a real Zerve notebook-to-Streamlit deployment, not a mockup."

## Demo safety notes

- default to the verified local Streamlit mirror for recording or presentation if there is any uncertainty
- only switch to the live preview if the freshest deploy-tab preview opens cleanly right before use
- keep the story focused on inspection, explainability, and live proof, not on claiming perfect mispricing detection

## Local fallback command

This is now the safe default demo path.

```bash
./scripts/run_local_demo.sh
```

If needed, override the default port with `MMR_SERVER_PORT=<port> ./scripts/run_local_demo.sh`.
