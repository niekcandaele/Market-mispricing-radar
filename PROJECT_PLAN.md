# Market Mispricing Radar

## Status

Chosen concept for ZerveHack.

This repository is the support layer for planning, backup, project management, and portable artifacts. The core analysis and deployment are expected to happen in Zerve, with selected assets copied between this repo and Zerve as needed.

Primary planning document:
- `PRD.md`

This file is the execution-oriented plan.

## Executive direction

We are building a prediction-market intelligence product in Zerve that ranks potentially mispriced or fragile markets and explains why they are flagged.

The intended final artifact is:
- a public Zerve project
- a deployed Streamlit app in Zerve
- optionally a FastAPI endpoint if it is low-friction after the app works

## What the Zerve docs change in our plan

After reviewing the Zerve docs, a few things are now clear:

- Zerve is not just a notebook. It is a DAG-style block environment with durable stored outputs between blocks.
- The cleanest hackathon path is to use a Zerve development layer for the pipeline and a Zerve Streamlit deployment for the final interface.
- FastAPI deployment is real and supported, but should be secondary to the app.
- Scheduled jobs are useful, but should come after the pipeline is stable because active scheduled layers become read-only.
- Fleets are available for parallel work, but we should use them only if they materially help ingestion or evaluation.
- Secrets, functions, classes, and environment requirements are supported natively, which reduces the need for external infrastructure.

That means the architecture should be explicitly Zerve-native rather than “some code plus maybe deployment later”.

## Working assumptions

- Zerve is the primary runtime for analysis and deployment.
- Native Zerve deployment is preferred over a separate VPS.
- Git remains the system of record for plans, notes, exported code, prompt drafts, demo materials, and backups.
- We should optimize for a polished and explainable result, not maximum feature count.

## Build strategy

### In Git

Use this repo for:
- product docs
- architecture notes
- scoring notes
- experiment logs
- sample schemas
- app copy and demo script drafts
- exported snippets and backups from Zerve

### In Zerve

Use Zerve for:
- ingestion and transformation blocks
- feature engineering
- scoring computation
- explanation generation
- deployment of the Streamlit app
- optional FastAPI deployment
- optional scheduled refresh

## Recommended Zerve architecture

### Development layer

Use the development layer as the main pipeline.

Target outputs:
- `normalized_markets`
- `market_features`
- `ranked_markets`
- `market_explanations`
- `refresh_metadata`

Suggested pipeline stages:
1. source constants and source config
2. raw source fetchers
3. normalization blocks
4. feature engineering blocks
5. scoring blocks
6. explanation assembly
7. QA and ranking outputs

### Deployment layer

Primary deployment:
- Streamlit app consuming ranked and explained outputs from the development layer

Optional deployment:
- FastAPI endpoint serving ranked outputs and market detail views

### Scheduled jobs layer

Use only after the pipeline is stable.

Purpose:
- periodic re-run of ingestion and scoring
- fresh data for the demo

### Assets

Likely candidates:
- helper functions for normalization
- helper functions for scoring
- constants and secrets for external APIs

## Phases

### Phase 0. Decision lock

Outputs:
- approved PRD
- approved MVP scope
- staged source strategy

Working decision:
- start with Polymarket only for MVP
- keep additional sources explicitly open for later expansion
- do not require cross-source market matching in MVP
- prefer app first, API later

Reference:
- `docs/source-strategy.md`

### Phase 1. Source validation and schema

Outputs:
- tested source access
- draft normalized schema
- list of source limitations

Success criteria:
- we can reliably fetch active markets
- we know which fields are trustworthy
- we know what to store for scoring and debugging

### Phase 2. First scoring pipeline

Outputs:
- normalized data
- initial feature set
- first ranked results
- explanation components

Success criteria:
- rankings are plausible
- at least several results feel genuinely interesting
- explanations are understandable

### Phase 3. Judge-facing app

Outputs:
- Zerve Streamlit app
- ranked list page
- market detail view
- methodology page or section

Success criteria:
- app works with the pipeline outputs
- a judge can understand the concept quickly
- the happy-path demo is clean

### Phase 4. Polish and validation

Outputs:
- improved ranking quality
- cleaner app presentation
- stronger caveats and framing
- demo flow and summary draft

Success criteria:
- polished enough for a 3-minute demo
- no obvious nonsense in the top-ranked markets
- product feels intentional rather than stitched together

### Phase 5. Optional extensions

Possible outputs:
- FastAPI deployment
- scheduled refresh
- more sources
- stronger history and change tracking

Rule:
- only do these if the main app is already strong

## Requirements summary

### Must-have
- one strong question
- one coherent ranking system
- one deployed app
- clear explanations
- public Zerve project

### Nice-to-have
- API deployment
- scheduled refresh
- second or third source
- richer history

### Avoid
- too many sources too early
- fake sophistication
- giant infrastructure setup
- reliance on anything outside Zerve unless necessary

## Scope guidance

The MVP should probably be:
- one or two sources
- one normalized schema
- one interpretable scoring model
- one Streamlit app
- one simple story

That is enough to win if it is sharp.

## Immediate next steps

1. approve the PRD direction
2. choose the MVP sources
3. create `docs/architecture.md`
4. create `docs/schema.md`
5. create `docs/scoring-model-v1.md`
6. map these docs to the existing Forgejo issues

## Initial principle

We win this by being sharp, grounded, and visibly Zerve-native.

Not by being the biggest project in the room.
