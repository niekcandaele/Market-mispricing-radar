# Hackathon Submission Copy Draft

## Project name

Market Mispricing Radar

## Tagline

A live prediction-market radar that surfaces markets whose prices look fragile, stale, extreme, or weakly supported.

## Short description

Market Mispricing Radar helps an operator find prediction markets that deserve a second look. Instead of scanning raw odds market by market, the app ranks fragile, stale, extreme, or weakly supported markets and explains why each one surfaced.

## Longer project summary

Prediction markets are information-dense, but most interfaces still leave the user to do the triage manually. Market Mispricing Radar turns that into an explainable workflow. It ingests live market data, scores markets whose pricing looks stale, extreme, unstable, or weakly supported, and presents the results in a deployed radar app with clear headlines, drilldown detail, and explicit caveats.

The key design choice is honesty. This project does not pretend to know the perfect fair value of every market, and it does not promise arbitrage. Instead, it prioritizes which markets look most worth inspecting right now and shows the evidence behind that prioritization.

## The problem

Prediction markets can be useful signals, but the operator experience is weak when the goal is inspection rather than casual browsing.

Current interfaces tend to show raw market lists and prices, which creates three problems:
- there are too many markets to inspect manually
- fragile or suspicious pricing can hide in plain sight
- raw odds alone do not explain which markets deserve attention first

## The solution

Market Mispricing Radar is an explainable triage surface for prediction markets.

It:
- ingests live market data
- computes an anomaly or fragility-oriented score
- ranks the markets that deserve the most scrutiny
- explains why each market surfaced
- exposes caveats instead of hiding them

The result is a live decision-support radar, not just a notebook or a static dashboard.

## How it works

The current MVP flow is:
1. fetch live Polymarket market data
2. normalize and categorize markets
3. build market features
4. score fragility signals such as staleness, extremeness, weak support, and recent instability
5. generate market-level explanations
6. deploy the results into a Streamlit app inside Zerve

The app includes:
- a Radar view for ranked inspection
- a Market Detail view for score drivers, observed signals, peers, and caveats
- a Methodology view that explains what the score means and what it does not mean

## Why this is a strong hackathon project

- it solves a real inspection problem instead of making a shallow demo
- it turns analysis into a usable deployed product
- it keeps the scope honest and explainable
- it is built around a real notebook-to-app workflow inside Zerve
- it balances technical depth with a clear product surface

## Built with

- Zerve notebooks and Streamlit deployment
- Python
- Polymarket live market data

## Challenges we ran into

- Polymarket ingestion inside Zerve initially hit request-shape and header issues
- Zerve notebook and deploy automation was brittle through raw UI interaction, so the workflow had to be hardened into a more reliable execution and validation path
- live deployment previews could fall into misleading or stale UI states, which required verification against actual preview output rather than trusting the interface
- turning the project into something presentation-ready took multiple rounds of product-copy and app-flow polish beyond the initial technical proof

## Accomplishments we are proud of

- proving a real end-to-end Zerve pipeline from notebook blocks to deployed Streamlit app
- building an explainable ranking flow rather than an opaque score dump
- shipping a polished Radar / Detail / Methodology product flow
- improving live category quality and fixing false-positive labeling in the deployed app
- turning the project into something judges can inspect and understand instead of stopping at code completion

## What we learned

- the most credible MVP was not “predict fair value perfectly,” it was “rank what deserves scrutiny and explain why”
- deployment validation has to check real rendered output, not just click logs or editor state
- for hackathons, product clarity and narrative polish matter almost as much as the underlying technical proof

## Current MVP scope

- Polymarket-first
- single-source anomaly or fragility scoring
- explainable component-based ranking
- deployed app inside Zerve

## What is next

- add cross-source comparison with other prediction platforms
- improve confidence calibration and richer supporting signals
- add contextual event/news inputs where they genuinely improve explainability

## Honest caveat section

This MVP is intentionally scoped.

It is:
- not a guaranteed arbitrage engine
- not a perfect fair-value model
- not financial advice
- currently strongest as an explainable market-inspection tool rather than an automated trading system

## One-minute spoken version

We built Market Mispricing Radar, a live inspection tool for prediction markets. Instead of forcing someone to scan raw odds market by market, it ranks the markets whose pricing looks fragile, stale, extreme, or weakly supported and explains why they surfaced. The whole workflow is live inside Zerve, from notebook ingestion and scoring to the deployed Streamlit app. The key idea is honesty: this is not pretending to know perfect fair value, it is helping an operator prioritize which markets deserve a second look right now.
