# Share Post Pack

## Purpose

ZerveHack currently lists a public share post as a required submission item.

This document prepares the draft copy and asset choices without posting anything automatically.

Use it when Niek or Cata decides which platform to use.

## Recommendation

Default to **one simple LinkedIn post**.

Why:
- lowest-risk public surface
- easiest to make sound credible without over-compressing the project
- easiest place to attach one strong screenshot plus the project link

Fallback:
- an X post if a shorter public proof is more practical

## Safe attachment choice

Default screenshot:
- `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- Google Drive copy: `Market Mispricing Radar - local-radar-view-16x9.png`

Default link choice:
- use the verified public Zerve notebook link: `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`
- latest retained checker evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260426T0503Z.json`
- the checker reports `summary.ready_for_share_post_link: true`
- do not substitute the gallery/community route unless the submission flow explicitly wants the gallery page instead
- because the demo recording path remains the locked safe local default, keep the public post about the project itself, not about local-only launch commands

Current share-post status:
- verified public Zerve notebook URL is available for the required share post: `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`. The latest retained checker reports `summary.ready_for_share_post_link: true`.
- do not guess alternate links from notebook ids, preview hosts, or repo notes
- the next action is now the human-approved public post itself, not more link discovery
- the gallery/community path is separate and should not be assumed to be the required project link unless the submission flow explicitly asks for it
- reusable recheck helper: `python3 scripts/check_zerve_public_share.py`
- it can use `--bearer`, `ZERVE_BEARER`, or best-effort Chromium token extraction for the authenticated check, and browser-rendered route verification for the client-side notebook page
- only treat the link as ready while that checker reports `summary.ready_for_share_post_link: true`
- latest route evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260426T0503Z.json`
- still reverify the exact final link before posting

## Tagging note

The live Devpost page was rechecked again on 2026-04-26 and says to tag:
- `@Zerve AI` on LinkedIn
- `@Zerve_AI` on X

Evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/devpost-requirements-check-20260426T1253Z.json`. Still check the exact platform autocomplete before posting in case branding display differs.

## LinkedIn draft

Built for ZerveHack: **Market Mispricing Radar**.

Prediction markets are information-dense, but raw market lists still make you do the triage manually. I built Market Mispricing Radar to surface the markets whose pricing looks fragile, stale, extreme, or weakly supported, then explain why they deserve a second look.

The project runs as a real Zerve notebook-to-app workflow: live market ingestion, scoring, explanation generation, and a deployed product people can inspect.

The key design choice was honesty. This is not claiming perfect fair value or guaranteed arbitrage. It is a triage tool for figuring out which markets are most worth inspecting right now.

Public notebook: https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4

Built with Zerve, Python, Streamlit, and live Polymarket data.

@Zerve AI

#ZerveHack #DataScience #PredictionMarkets #AI

## Shorter LinkedIn variant

Built for ZerveHack: **Market Mispricing Radar**.

It turns live prediction-market data into an explainable radar that surfaces the markets most worth inspecting, then shows why they were flagged. The full workflow runs inside Zerve, from notebook analysis to a deployed app.

Public notebook: https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4

Built with Zerve, Python, Streamlit, and live Polymarket data.

@Zerve AI

#ZerveHack #AI #DataScience

## X draft

Built for #ZerveHack: Market Mispricing Radar.

It ranks prediction markets that look fragile, stale, extreme, or weakly supported, then explains why they surfaced. Real Zerve notebook-to-app workflow.

https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4

@Zerve_AI

## Ultra-short X fallback

Built for #ZerveHack: Market Mispricing Radar, an explainable prediction-market radar built in Zerve that surfaces markets worth a second look and shows why.

https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4 @Zerve_AI

## Post checklist

Before posting:
- confirm which platform to use
- confirm exact tag on that platform
- keep the public project link as `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4` unless the submission flow explicitly requests another verified route
- optionally rerun `python3 scripts/check_zerve_public_share.py` as a final sanity check; require `summary.ready_for_share_post_link: true`
- do not silently swap in the gallery/community route unless that exact route has been consciously chosen and verified
- use one clean screenshot only
- keep the tone product-facing, not overly technical
- do not mention safe local default launch commands in the public post

## Approval boundary

This pack is draft-only.

Do not post from here without an explicit human go-ahead.
