# Presenter Cheat Sheet

## Purpose

This is the compact live-pitch and judge-Q&A aid.

Use it when the longer docs are too much and you need the sharpest version of the story in one place.

## 15-second pitch

Market Mispricing Radar is a live inspection tool for prediction markets. It ranks markets whose pricing looks fragile, stale, extreme, or weakly supported, then explains why they surfaced.

## 30-second pitch

Prediction markets are useful, but most interfaces still make you scan raw odds market by market. Market Mispricing Radar turns that into an explainable workflow by ranking the markets that deserve a second look, showing the score drivers, and exposing caveats instead of hiding them.

## 60-second pitch

Prediction markets are information-dense, but raw market lists do not tell you what to inspect first. Market Mispricing Radar ingests live market data, scores fragility signals like staleness, weak support, extremeness, and instability, then surfaces the markets that deserve scrutiny in a deployed app with explanation headlines, drilldown detail, and methodology notes. The key design choice is honesty: this is not pretending to know the perfect fair value of every market, it is helping someone prioritize where to look next.

## Strongest proof points

- real Zerve notebook pipeline is live end to end
- the demo app flow is verified and presentation-safe through the local fallback path
- the product is explainable, not a black-box score dump
- the app exposes caveats and QA context instead of pretending certainty
- the MVP is narrow on purpose and honest about single-source scope

## Best one-line differentiators

- This is a market-inspection radar, not a generic dashboard.
- The score is for prioritizing scrutiny, not claiming perfect fair value.
- The whole flow runs through a real Zerve notebook-to-app pipeline.

## Honest scope framing

Say this if needed:
- The MVP is Polymarket-first.
- The score is a triage signal, not a promise of profit.
- This is strongest today as an explainable inspection tool, not an automated trading system.

## Likely judge questions

### What exactly is the score measuring?
Suggested answer:
It measures how much evidence there is that a market deserves extra scrutiny, using signals like staleness, extremeness, weak support, and instability. It is not a claim that we know the exact true price.

### Why is this better than just browsing Polymarket directly?
Suggested answer:
Browsing raw markets gives you data, but not triage. This product ranks what is most worth inspecting first and explains why, which is a much better inspection workflow.

### Why does Zerve matter here?
Suggested answer:
Because this is not just a notebook or just a front-end mockup. The same Zerve environment handles ingestion, scoring, explanation generation, and the deployed app can actually be inspected and used.

### What is the current MVP scope?
Suggested answer:
It is intentionally Polymarket-first and explanation-first. We wanted a credible, honest MVP that proves the workflow end to end before expanding to multi-source comparison.

### What would you build next?
Suggested answer:
Cross-source comparison, stronger confidence calibration, and richer supporting context where it actually improves explainability instead of just adding noise.

### Why should judges trust this if it is heuristic?
Suggested answer:
Because we are honest about that. The app exposes score drivers, caveats, and QA warnings, so the output is inspectable instead of pretending to be magically correct.

## If you need to sound more technical

Use this:
The current pipeline fetches live Polymarket data, normalizes and categorizes markets, builds feature signals, scores fragility-oriented heuristics, generates explanation rows, and feeds those outputs into a deployed Streamlit app inside Zerve.

## If you need to sound more product-focused

Use this:
The value is not just finding odd-looking markets. It is giving someone a usable, explainable triage surface instead of an endless list of raw odds.

## Demo-path note

For the final presentation, treat the verified local fallback as the safe default. Only switch to a live Zerve preview if it opens cleanly right before use.

## Good closing line

We built something people can actually inspect and understand, not just a flashy score or a notebook screenshot.
