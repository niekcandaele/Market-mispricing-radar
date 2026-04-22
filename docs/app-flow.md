# Judge-Facing App Flow

## Purpose

This document turns the MVP app idea into a concrete Zerve Streamlit flow.

The app should help a judge understand three things quickly:
- what the product found
- why those markets are interesting
- why the result is credible enough to inspect further

## Primary design rule

The app is not a full trading terminal.

It is a fast inspection surface for the top flagged markets.
A judge should understand the product in under a minute and complete the happy-path demo in under three.

## Core app structure

The MVP should use three main screens or sections:
1. ranked radar
2. market detail
3. methodology

These can be implemented as sidebar navigation, tabs, or a top-level page switch.

## Screen 1: Ranked Radar

This is the landing view and the most important screen.

### Goal

Show the top suspicious or fragile markets immediately.

### Main content

A ranked table or card list with one row per market.

### Required columns or fields

- rank
- market title
- source
- category
- current probability
- final score
- headline reason
- last refresh or last update age

### Required widgets

- source filter
- category filter
- minimum score threshold
- sort control, defaulting to highest score
- result count selector, for example top 10, 25, 50
- refresh metadata badge or panel

### Recommended row actions

- click market to open detail view
- open source link in a new tab

### Output this screen must support

The user should be able to answer:
- what are the top flagged markets right now
- which source they came from
- the one-line reason each market is interesting

## Screen 2: Market Detail

This is where the product earns trust.

### Goal

Explain exactly why one market was flagged.

### Header section

Show:
- market title
- source name
- source link
- current probability
- final score
- refresh timestamp
- market status
- resolution time if available

### Explanation section

Show:
- headline reason
- short explanation
- detailed explanation
- primary reason code
- caveats

### Score breakdown section

Show component-level values such as:
- staleness component
- event-horizon component
- extremeness component
- liquidity component
- volatility component
- data-quality adjustment if present

Use a simple bar chart, stacked chart, or labeled score cards.

### Supporting signals section

Show the raw or lightly processed fields that explain the score:
- time since update
- time to resolution
- volume
- liquidity
- distance from midpoint
- any recent movement metric available in MVP

### Optional comparison section

If easy, include:
- similar markets from the same category
- a small table showing why this market ranked above nearby peers

This is optional. Do not hold MVP hostage for it.

### Output this screen must support

The user should be able to answer:
- why did this market get flagged
- which signals drove the score
- what caveats should reduce confidence

## Screen 3: Methodology

This is a short trust-building screen, not a research paper.

### Goal

Explain what the score means and what it does not mean.

### Required sections

#### What the product does
- ranks markets that look stale, fragile, extreme, or weakly supported
- surfaces interpretable reasons for inspection

#### What the product does not claim
- not guaranteed arbitrage
- not a perfect fair-value model
- not financial advice

#### Current MVP scope
- Polymarket-first
- single-source anomaly scoring
- explainable component-based ranking

#### Score ingredients
- staleness
- time to resolution
- price extremeness
- liquidity support
- volatility or movement anomaly when available

#### Caveats
- single-source MVP
- some market structures may be simplified or excluded
- quality depends on source freshness and available metadata

### Output this screen must support

The user should be able to answer:
- why this app is useful
- why the approach is honest
- why the MVP is intentionally scoped

## Shared app elements

These should appear globally or nearly globally.

### Refresh trust panel

Always show:
- last refresh timestamp
- market count processed
- source count
- score version

### Navigation

Keep navigation dead simple.

Preferred pattern:
- `Radar`
- `Market Detail`
- `Methodology`

### Empty and error states

Handle these explicitly.

#### No results after filtering
Show:
- a short message
- reset filters button

#### Missing detail fields
Show:
- available data first
- a brief note when a metric is unavailable

#### Pipeline not refreshed yet
Show:
- an honest loading or unavailable message
- the last successful refresh if known

## Recommended happy-path demo

This is the recommended demo flow.

### Step 1
Open the app on the Ranked Radar screen.

Narration:
- this tool scans active markets and ranks the ones that look most worth inspecting

### Step 2
Point to the top-ranked market.

Narration:
- the app does not just rank markets, it also gives a reason summary up front

### Step 3
Open the Market Detail screen for one top result.

Narration:
- here is the score breakdown, the raw supporting signals, and the caveats

### Step 4
Open Methodology.

Narration:
- the score is deliberately interpretable and modest in its claims

### Step 5
Return to the radar and mention refresh metadata.

Narration:
- the outputs are tied to a concrete refresh cycle, not hand-wavy analysis

## Implementation notes for Zerve

### Upstream variables the app should consume
- `ranked_markets`
- `market_explanations`
- `refresh_metadata`
- optionally `market_features`

### App logic rule

The app should mostly present precomputed outputs.
Do not move core ingestion, normalization, or scoring logic into the Streamlit layer.

Current mirrored scaffold:
- `zerve/app/streamlit_app.py`

### MVP cutoff rule

If time is short, ship:
- a strong radar screen
- a strong detail screen
- a short methodology section

That is enough for a credible demo.
