# Market Mispricing Radar

## Status

Chosen concept for ZerveHack.

This repository is the support layer for planning, backup, project management, and portable artifacts. The core analysis and deployment are expected to happen in Zerve, with selected assets copied between this repo and Zerve as needed.

## Goal

Build a market intelligence product that detects potentially mispriced or fragile prediction markets and explains why they are being flagged.

The hackathon version should combine:
- real analytical depth
- a clear scoring methodology
- a usable deployed interface
- strong storytelling for judges

## Product concept

Market Mispricing Radar ingests prediction market data and ranks markets that appear:
- miscalibrated
- stale
- unusually divergent across venues
- inconsistent with recent information flow
- unstable as an event approaches

The product should not claim guaranteed arbitrage or certain truth. It should surface promising anomalies, quantify uncertainty, and explain the evidence.

## Why this idea fits the hackathon

This direction matches the hackathon criteria well:
- analytical depth: build a real scoring and evaluation pipeline
- end-to-end workflow: ingest, analyze, explain, deploy
- storytelling: easy to demo with concrete flagged markets
- creativity: combines market structure, calibration, divergence, and freshness into one system

It also fits Zerve's product positioning:
- AI-native data workflows
- notebook to deployment in one platform
- context-aware analysis
- parallel processing where useful
- productionized output rather than a dead-end notebook

## Working assumptions

- Zerve is the primary runtime for analysis and deployment.
- Native Zerve deployment is preferred over a separate VPS.
- This Git repo is the system of record for plans, notes, schemas, prompts, exported code, and backup artifacts.
- We should keep scope tight enough to finish a polished demo before the deadline.

## High-level architecture

### 1. Data ingestion layer

Candidate sources:
- Polymarket
- Kalshi
- Metaculus
- optional news or trend source later if needed

Responsibilities:
- fetch active questions/markets
- normalize titles, timestamps, probabilities, categories, status
- store snapshots for repeatable analysis

### 2. Market normalization layer

Responsibilities:
- map similar questions across platforms when possible
- standardize implied probabilities and metadata
- derive event horizon and recency features
- assign market type and topic tags

### 3. Feature engineering layer

Initial feature families:
- cross-market disagreement
- probability movement and volatility
- staleness or update lag
- resolution proximity
- historical calibration signals if obtainable
- optional external information mismatch later

### 4. Scoring and explanation layer

Responsibilities:
- compute a mispricing or fragility score
- break score into explainable components
- attach confidence and caveats
- produce ranked outputs for the app and demo

### 5. Evaluation layer

Responsibilities:
- test whether the scoring surfaces interesting and credible cases
- compare top-ranked outputs against sanity checks
- avoid obviously noisy or misleading rankings
- document limitations clearly

### 6. Presentation layer

Preferred final artifact:
- Streamlit app deployed in Zerve

Optional secondary artifact:
- FastAPI endpoint in Zerve

Core UI needs:
- ranked market list
- market detail view
- explanation of why flagged
- uncertainty/confidence display
- source and timestamp visibility

### 7. Refresh layer

Responsibilities:
- scheduled refresh of ingestion and scoring
- preserve enough history for comparisons
- keep the demo data recent

Likely implementation:
- Zerve scheduled jobs

## System split: Git vs Zerve

### In Git

Use this repo for:
- project plans
- architecture notes
- requirements
- scoring design notes
- experiment logs
- exported code backups
- app copy and demo script drafts
- data schemas and mapping rules

### In Zerve

Use Zerve for:
- data ingestion workflows
- exploratory analysis
- scoring pipeline execution
- app deployment
- API deployment if included
- scheduled refresh jobs

### Sync pattern

Expected workflow:
1. design locally in Git
2. implement or iterate in Zerve
3. copy important logic, prompts, notes, and exports back into Git
4. keep the repo as the durable backup and planning layer

## Phases

### Phase 0. Planning and framing

Output:
- project plan
- architecture sketch
- scoped MVP
- source shortlist

Questions to settle:
- which market sources are in scope for MVP
- whether we do app only or app plus API
- whether cross-platform matching is reliable enough for MVP

### Phase 1. Data feasibility

Output:
- verified access to selected APIs or datasets
- sample normalized records
- list of source limitations and edge cases

Success criteria:
- can reliably fetch active markets
- can extract enough metadata for ranking
- can store snapshots for iteration

### Phase 2. MVP scoring pipeline

Output:
- first normalized dataset
- initial scoring formula
- top ranked markets with human-readable reasons

Success criteria:
- rankings are plausible
- explanations are understandable
- system produces demo-worthy examples

### Phase 3. App prototype

Output:
- deployed app with ranked list and details
- usable interface for judges

Success criteria:
- demo flow works cleanly
- outputs are readable and convincing
- no obvious broken states in the happy path

### Phase 4. Validation and polish

Output:
- improved score quality
- better explanations
- polished visuals and copy
- concise demo narrative

Success criteria:
- project tells a strong story in under 3 minutes
- top examples feel genuinely interesting
- app and project run without embarrassing failures

### Phase 5. Submission packaging

Output:
- public Zerve project
- summary copy
- demo video plan or script
- social post draft if needed

Success criteria:
- all required deliverables exist
- links are shareable
- story aligns with judging criteria

## MVP definition

The MVP should probably do only this:
- ingest one or two prediction market sources
- normalize a manageable subset of active markets
- compute a simple but defensible ranking score
- show the ranked results in a deployed app
- explain each ranking with a few clear signals

That is enough to be real.

## Stretch goals

Possible stretch goals, only after MVP works:
- add Metaculus or another forecasting source
- add external trend or news signal
- expose an API
- add historical tracking views
- add topic-specific views such as politics, economics, or AI
- add scheduled refresh with status reporting

## Requirements

### Functional requirements

- fetch market data from selected source APIs
- normalize records into a common internal schema
- compute per-market ranking features
- generate a composite score and explanation
- present ranked results in a usable app
- show source attribution and freshness

### Non-functional requirements

- must be understandable quickly by judges
- must run reliably enough for a live demo
- must avoid overclaiming confidence
- must stay within hackathon scope and time
- should visibly demonstrate Zerve-native workflow value

## Risks

- source APIs may be messy or inconsistent
- market matching across platforms may be harder than expected
- a flashy score can become fake if not grounded
- too many data sources could swamp the project
- external signal integration may add noise instead of value

## Risk controls

- start with fewer sources
- keep the first score interpretable
- prefer strong explanation over faux sophistication
- treat cross-platform matching as optional until proven
- keep one clear demo path working at all times

## Open questions

- Which exact sources should be MVP, Polymarket only or Polymarket plus Kalshi?
- Do we need cross-platform question matching for version one?
- Should the first app focus on a single topic vertical to improve clarity?
- How much historical backfill can we reasonably get during the hackathon?
- Do we want an API in the final submission, or only if it is nearly free after the app works?

## Immediate next steps

1. confirm repo structure
2. decide MVP source scope
3. verify source access and rate limits
4. define the first internal market schema
5. outline the first scoring formula
6. sketch the first app screen set

## Proposed repo structure

```text
market-mispricing-radar/
  PROJECT_PLAN.md
  README.md
  docs/
    architecture.md
    scoring-notes.md
    demo-outline.md
  zerve/
    exports/
    prompts/
    snippets/
  data/
    samples/
    schemas/
```

## Initial principle

We win this by being sharp, not huge.

The project should feel like a focused, opinionated market intelligence tool with real analytical teeth, not a generic dashboard and not an overbuilt science fair monster.
