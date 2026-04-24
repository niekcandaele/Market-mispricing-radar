# Video Recording Run Sheet

## Purpose

This is the practical one-take recording plan for the hackathon demo video.

Use it when the demo script is too broad and you need a crisp filming sequence with minimal improvisation.

If you want a more literal spoken pass during recording, pair this with `docs/video-voiceover-script.md`.

Right before the real take, run `docs/recording-preflight-checklist.md`, and on the safe local default path use `./scripts/check_safe_local_demo.sh` for the one-command final sweep.

## Target shape

- target length: 60 to 90 seconds
- tone: clear, credible, calm
- style: one strong story, not feature sprawl
- product claim: this is an explainable market-inspection radar, not a guaranteed arbitrage engine

## Before recording

- if using the safe local default, run `./scripts/check_safe_local_demo.sh`
- confirm the chosen demo entrypoint actually opens
- default to the locked safe local default path
- only switch to the live Zerve preview if it is clearly healthy right before recording
- close unrelated tabs and distractions
- pre-select a strong top-ranked market for the drilldown section, defaulting to `GTA VI released before June 2026?` on the current safe local path

## Recording order

### Beat 1, Hook and problem, 0:00 to 0:12

Screen:
- land on the Radar view
- keep the top of the page visible

Say:
Prediction markets are useful, but most interfaces still force you to scan raw odds market by market. Market Mispricing Radar turns that into an explainable workflow by ranking the markets that deserve a second look.

Do not say:
- guaranteed profit
- perfect fair value
- automated trading

## Beat 2, What the radar is showing, 0:12 to 0:28

Screen:
- stay on the Radar view
- show the top-ranked cards
- keep the QA warning and summary context visible if available

Say:
This radar surfaces markets whose pricing looks fragile, stale, extreme, or weakly supported. Instead of a flat odds list, I get ranked results with explanation headlines, category context, and visible caveats.

Point at:
- ranked market cards
- headline reason text
- category mix or reason summary if present

## Beat 3, Drill into one market, 0:28 to 0:52

Screen:
- click one strong top-ranked market into Market Detail
- keep the explanation and score-driver section in view

Say:
Now I can drill into one market and see why it was flagged, what signals are driving the score, and what caveats still apply. The score is a triage signal, not a promise of profit.

Point at:
- headline explanation
- score drivers
- observed signals
- caveats

## Beat 4, Scope honesty, 0:52 to 1:04

Screen:
- switch to Methodology
- keep the opening methodology content visible

Say:
The MVP is intentionally honest. It is Polymarket-first, explanation-rich, and designed to prioritize scrutiny, not pretend to know the exact fair value of every market.

## Beat 5, Zerve proof and close, 1:04 to 1:15

Screen:
- either stay on Methodology or briefly return to a view that still shows the product clearly
- keep the close simple

Say:
The whole workflow runs through a real Zerve notebook-to-app pipeline, so this is a real deployed workflow. It is live analysis turned into a usable product.

## Fast fallback version, under 60 seconds

Use this if time is tight:

1. Radar view, hook and problem
2. one market drilldown
3. one sentence on honest scope
4. one sentence on Zerve-native deployment proof

Suggested words:
We built a live radar for prediction markets that deserve a second look. It ranks fragile or weakly supported markets, explains why they surfaced, and lets you drill into the score drivers and caveats. The MVP is intentionally honest about scope, and the whole flow is deployed from a real Zerve notebook pipeline.

## Demo-safe market choice guidance

Prefer a market that:
- sits near the top of the Radar
- has a readable explanation headline
- shows multiple visible score drivers or caveats
- is easy to understand quickly without domain-heavy background

Avoid a market that:
- has awkward wording
- requires too much world knowledge to explain fast
- looks empty or visually weak in the detail view

## Fallback entrypoint command

```bash
./scripts/run_local_demo.sh
```

Defaults:
- refresh limit: `200`
- address: `127.0.0.1`
- port: `8768`

Override with env vars if needed, for example `MMR_SERVER_PORT=8765 ./scripts/run_local_demo.sh`.

## Final reminders

- do one clean take instead of over-explaining
- keep the story focused on inspection, explainability, and credibility
- treat the locked safe local default as the default path and only upgrade to live if it is clearly healthy
- better to sound honest and sharp than overclaiming
- if needed, use `docs/video-voiceover-script.md` to keep the spoken pass tight and consistent
- if the safe local sweep fails, stop and fix that before recording instead of improvising around it
