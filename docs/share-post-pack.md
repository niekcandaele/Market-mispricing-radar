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
- use the final public Zerve project/share link if that is the expected hackathon proof link
- after the notebook is made public, recheck the notebook share route at `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`
- treat a bare `200` as insufficient if the route only serves the generic Zerve shell instead of the actual public project page
- do not substitute the gallery/community route unless the submission flow explicitly wants the gallery page instead
- if the submission-day choice is the locked safe local default for demo reliability, keep the public post about the project itself, not about local-only launch commands

Current blocker:
- no verified public Zerve project/share URL yet for the required share post. The latest retained authenticated metadata baseline still says `canvas.is_public: false`, and the public-share gate is still red.
- do not guess the link from notebook ids, preview hosts, or repo notes
- the next action is explicit: make the notebook public in Zerve via the share/privacy control, then recheck the resulting public project/share URL
- the known privacy seam is the notebook public toggle backed by `PATCH /canvas/<canvas_id>` with `is_public`, so the blocker is no longer a vague search problem
- the first recheck target after the toggle is the notebook share route `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`
- the gallery/community path is separate and should not be assumed to be the required project link
- current baseline check confirms that this route can return the generic Zerve shell with `200`, so success must mean the actual public project page renders, not just that the route responds
- reusable recheck helper: `python3 scripts/check_zerve_public_share.py`
- it can use `--bearer`, `ZERVE_BEARER`, or a best-effort Chromium token extraction path for the authenticated check
- only treat the link as ready when that checker reports `summary.ready_for_share_post_link: true`
- the checker now emits a `summary` block and exits non-zero until the share-post link is actually ready
- latest route baseline: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260424T194951Z.json`
- if the project is already public by the time this is used, still reverify the exact final link before posting
- evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-status-20260423T055107Z.json`

## Tagging note

The live Devpost page says to tag:
- `@Zerve AI` on LinkedIn
- `@Zerve_AI` on X

Check the exact platform autocomplete before posting in case branding changed.

## LinkedIn draft

Built for ZerveHack: **Market Mispricing Radar**.

Prediction markets are information-dense, but raw market lists still make you do the triage manually. I built Market Mispricing Radar to surface the markets whose pricing looks fragile, stale, extreme, or weakly supported, then explain why they deserve a second look.

The project runs as a real Zerve notebook-to-app workflow: live market ingestion, scoring, explanation generation, and a deployed product people can inspect.

The key design choice was honesty. This is not claiming perfect fair value or guaranteed arbitrage. It is a triage tool for figuring out which markets are most worth inspecting right now.

Built with Zerve, Python, Streamlit, and live Polymarket data.

#ZerveHack #DataScience #PredictionMarkets #AI

## Shorter LinkedIn variant

Built for ZerveHack: **Market Mispricing Radar**.

It turns live prediction-market data into an explainable radar that surfaces the markets most worth inspecting, then shows why they were flagged. The full workflow runs inside Zerve, from notebook analysis to a deployed app.

Built with Zerve, Python, Streamlit, and live Polymarket data.

#ZerveHack #AI #DataScience

## X draft

Built for #ZerveHack: Market Mispricing Radar.

It ranks prediction markets whose pricing looks fragile, stale, extreme, or weakly supported, then explains why they surfaced. Real Zerve notebook-to-app workflow, not just a static demo.

Built with Zerve, Python, Streamlit, and live Polymarket data. @Zerve_AI

## Ultra-short X fallback

Built for #ZerveHack: Market Mispricing Radar, an explainable prediction-market radar built in Zerve that surfaces markets worth a second look and shows why. @Zerve_AI

## Post checklist

Before posting:
- confirm which platform to use
- confirm exact tag on that platform
- confirm the public project link to include
- if the project is still not public in Zerve, first flip the Zerve share/privacy toggle and then check the notebook share route for this project
- if the notebook route only returns the generic Zerve shell, do not treat that as a valid public-link success
- if the project is public but the URL is still unresolved, stop and reverify the exact final link before posting
- do not silently swap in the gallery/community route unless that exact route has been consciously chosen and verified
- use one clean screenshot only
- keep the tone product-facing, not overly technical
- do not mention safe local default launch commands in the public post

## Approval boundary

This pack is draft-only.

Do not post from here without an explicit human go-ahead.
