# Architecture

## Purpose

This document describes the intended system architecture for the MVP of Market Mispricing Radar.

The design is explicitly based on how Zerve works:
- development happens in a DAG-like canvas or notebook workflow
- outputs are passed and stored between stages
- app deployment should consume prepared upstream variables
- scheduled jobs and API deployment are secondary layers, not the starting point

## Architectural principle

Build the product as a staged analytical pipeline first, then expose the results through a simple app.

That means:
- do not put heavy logic directly in the app
- do not make the Streamlit layer responsible for raw data ingestion
- keep scoring outputs stable and reusable
- treat the app as a presentation layer over prepared data

## System split

### Git / Forgejo side

Purpose:
- planning
- project management
- backup of important artifacts
- portable docs and notes
- exported code snippets from Zerve

Main artifacts:
- PRD
- project plan
- architecture and schema docs
- scoring notes
- demo copy
- sample payloads and schemas

### Zerve side

Purpose:
- primary execution environment
- data ingestion
- transformation
- feature engineering
- scoring
- explanation assembly
- app deployment
- optional API and scheduled jobs

## High-level system diagram

```text
External sources
  -> source fetch blocks
  -> raw snapshot outputs
  -> normalization layer
  -> feature engineering layer
  -> scoring layer
  -> explanation layer
  -> ranked outputs
  -> Streamlit app deployment
```

Optional later path:

```text
ranked outputs
  -> FastAPI deployment
  -> scheduled refresh
```

## Zerve layer design

## 1. Development layer

This is the heart of the product.

The development layer should own all core business logic and produce explicit named outputs for downstream use.

### Recommended block groups

#### A. Source config and helpers

Responsibilities:
- define source selection
- define fetch limits
- define category filters if needed
- import reusable helper functions or constants

Likely outputs:
- `source_config`

#### B. Source ingestion

Responsibilities:
- fetch raw market data from Polymarket
- preserve identifiers, titles, timestamps, prices, and status
- optionally keep a raw JSON snapshot for debugging

Likely outputs:
- `polymarket_raw_markets`
- `ingestion_metadata`

#### C. Normalization

Responsibilities:
- convert raw source payloads into one internal schema
- derive common fields
- clean titles and timestamps
- calculate freshness and event timing fields

Likely outputs:
- `normalized_markets`

Current local mirror:
- `zerve/snippets/polymarket_normalization_block.py`

#### D. Feature engineering

Responsibilities:
- create derived signals used by the score
- compute staleness, volatility, structural, and event-related features
- keep features interpretable

Likely outputs:
- `market_features`

Current local mirror:
- `zerve/snippets/polymarket_feature_block.py`

#### E. Scoring

Responsibilities:
- combine features into a single ranking score
- retain sub-scores
- preserve enough detail for explanation

Likely outputs:
- `ranked_markets`
- `score_components`

Current local mirror:
- `zerve/snippets/polymarket_scoring_block.py`

#### F. Explanation assembly

Responsibilities:
- translate explicit score components into readable reasons
- create short and detailed explanations
- attach caveats or confidence notes

Likely outputs:
- `market_explanations`

#### G. Validation and QA

Responsibilities:
- inspect top-ranked results
- catch obviously bad outputs
- provide sanity-check summaries

Likely outputs:
- `qa_summary`
- `refresh_metadata`

## 2. Deployment layer

Primary deployment target:
- Streamlit app

The app should read prepared variables from the development layer using Zerve variable references.

### Streamlit responsibilities
- display top ranked markets
- allow selection or filtering of markets
- show score breakdowns and explanations
- show refresh timestamp and source metadata
- include a short methodology section

### Streamlit should not do
- primary raw data fetching
- heavy recomputation of score logic
- source normalization logic
- fragile on-the-fly transformations that belong upstream

## 3. Optional API deployment layer

Use only if the app is already solid.

### Possible endpoints
- `GET /markets/top`
- `GET /markets/{id}`
- `GET /meta/refresh`

### API design principle
The API should expose already-computed outputs, not recreate the whole pipeline on every request.

## 4. Scheduled jobs layer

Use only when the development pipeline is stable.

Responsibilities:
- periodic re-ingestion
- periodic re-scoring
- update the outputs consumed by the app

Important Zerve note:
- active scheduled layers become read-only, so they should be introduced after the pipeline is mature enough

## Assets strategy

### Functions & classes
Use when logic becomes reused or messy, for example:
- raw source parsing
- title cleanup helpers
- score helper functions
- explanation templating helpers

### Constants & secrets
Use for:
- API keys if needed later
- source-specific settings
- thresholds or tuned values

### Requirements
Keep dependencies modest.

Likely packages:
- requests or httpx
- pandas
- numpy
- streamlit in deployment context if needed by Zerve deployment setup
- minimal helper libraries only if they clearly pay off

## Data persistence approach

Zerve already stores block outputs and passes them downstream.

So for MVP we should rely primarily on:
- explicit block outputs
- source snapshots where useful for debugging
- small QA tables for sanity checks

We do not need to introduce a separate database for MVP.

## MVP architecture decision

The MVP should be:
- single source at first
- one clear normalization path
- one feature layer
- one scoring layer
- one app deployment

This is enough to prove the concept and keeps the architecture coherent.

## Expansion path

### Expansion 1
- add second market source
- add cross-source comparison layer
- update normalized schema to support source-aware comparisons

### Expansion 2
- add Metaculus or external forecasting signals
- add optional context features

### Expansion 3
- add scheduled refresh and lightweight API
- add richer history views or change tracking

## Failure modes to avoid

- app owns too much logic
- too many blocks with unclear responsibilities
- no stable named outputs for downstream deployment
- multi-source matching before single-source ranking works
- black-box score with no explanation path

## Recommended MVP build order

1. raw ingestion
2. normalized schema
3. feature table
4. ranked table
5. explanations
6. Streamlit app
7. polish
8. only then optional API or scheduler
