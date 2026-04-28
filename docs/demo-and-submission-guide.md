# Demo and Submission Guide

## Purpose

This is the single practical guide for running the demo and finishing a hackathon-style submission.

Use it instead of the older scattered runbooks, scripts, copy packs, checklists, and final-status notes.

## Demo Path

Default to the safe local demo unless a live Zerve preview is freshly verified right before presenting.

### Safe Local Demo

Run the preflight sweep:

```bash
./scripts/check_safe_local_demo.sh
```

Then launch the local app:

```bash
./scripts/run_local_demo.sh
```

Default local URL:

```text
http://127.0.0.1:8768
```

This path refreshes the Streamlit bundle and serves the mirrored app locally. It is the most reliable recording and presentation path.

### Optional Live Zerve Demo

Use the live Zerve preview only if it opens cleanly during the final check.

Public notebook link:

```text
https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4
```

Known behavior from previous checks:

- preview URLs can rotate
- a fresh host may briefly return `503` while warming up
- if it does not render within roughly a minute, switch back to the safe local demo

## Demo Flow

Keep the walkthrough short and concrete.

1. Open on the Ranked Radar.
2. Explain that the product ranks prediction markets worth inspecting, not guaranteed arbitrage.
3. Point out the score, reason, category, and refresh context.
4. Open one strong market detail page.
5. Show the explanation, score breakdown, supporting signals, and caveats.
6. Open Methodology briefly.
7. Close by saying the MVP is single-source, explainable, and Zerve-native.

Recommended drilldown if it still appears clean in the current data:

```text
Putin out as President of Russia by December 31, 2026?
```

If the ranking changes, choose a market that is understandable, has a clear reason code, and does not require niche context.

## Recording

For a short video, use this structure:

1. Problem: raw prediction-market odds are hard to triage quickly.
2. Product: Market Mispricing Radar ranks markets that look stale, fragile, extreme, or weakly supported.
3. Proof: show the Radar and one Market Detail drilldown.
4. Trust: show Methodology and the single-source MVP caveat.
5. Close: explain that Zerve handles the notebook pipeline and app deployment path.

Before recording:

- run `./scripts/check_safe_local_demo.sh`
- launch `./scripts/run_local_demo.sh`
- keep the walkthrough under the required video limit
- avoid relying on an old live preview URL
- verify the chosen market detail page before the take

## Submission Checklist

Before final submission, confirm these items:

- one demo path works
- the public Zerve notebook link opens
- the video is recorded or ready to upload
- the deck or screenshots required by the form are available
- form copy matches the real MVP scope
- no wording implies calibrated fair-value prediction or guaranteed arbitrage
- any public share post is manually approved and actually published
- final links pasted into the form open from a clean browser/session

## Suggested Form Copy

Short description:

```text
Market Mispricing Radar is an explainable Zerve app that ranks prediction markets worth inspecting because they look stale, fragile, extreme, or weakly supported.
```

Longer summary:

```text
Market Mispricing Radar ingests Polymarket data, normalizes market records, computes interpretable fragility signals, and presents the highest-priority markets in a Streamlit app. The score is intentionally framed as an inspection signal rather than a claim of true fair value. Judges can move from a ranked radar view into a market detail page that explains the main reason, supporting signals, score components, and caveats.

The MVP is single-source and deliberately scoped. Its goal is to show a clean Zerve-native workflow: notebook-style ingestion and scoring, explicit intermediate outputs, explanation assembly, and a judge-facing app over prepared results.
```

Built with:

```text
Zerve, Streamlit, Python, Polymarket market data, and a local Git mirror for portable snippets, docs, and submission artifacts.
```

Scope caveat:

```text
This MVP does not claim guaranteed arbitrage or calibrated fair value. It surfaces markets that deserve human inspection based on transparent heuristics.
```

## Share Post

If the submission requires a public post, use the verified notebook link:

```text
https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4
```

Draft:

```text
I built Market Mispricing Radar for ZerveHack: an explainable app that ranks prediction markets worth inspecting because they look stale, fragile, extreme, or weakly supported.

It uses a Zerve-native workflow for ingestion, scoring, explanation assembly, and a Streamlit app over prepared notebook outputs.

Project: https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4
```

Only publish after choosing the platform and confirming the required tag from the current submission instructions.

## Optional Agentic Report

An optional Zerve Agentic Report was generated:

```text
https://app.zerve.ai/report/4b2bcec4-48d2-4960-b051-cd465aa18a56
```

Use it only as a bonus if it opens cleanly in the intended viewing context. Keep the public notebook URL as the main project link.
