# PRD: Market Mispricing Radar

## 1. Product summary

Market Mispricing Radar is a prediction-market intelligence product for ZerveHack.

It ingests live market and forecasting data, computes a transparent ranking of potentially mispriced or fragile markets, and presents the results through a deployed Zerve app.

The goal is not to claim certainty or guaranteed arbitrage. The goal is to surface unusual markets, explain why they are suspicious, and give the user a usable decision-support interface.

## 2. Why this project should exist

The hackathon is clearly rewarding more than a notebook.

Judges want:
- genuine analytical depth
- clear end-to-end workflow
- productionized output, not just exploration
- understandable results and story
- some ambition without losing realism

This concept fits that shape well because it can demonstrate:
- a concrete question
- multi-source data analysis
- ranking logic with explainable components
- a deployed app in Zerve
- optionally an API or scheduled refresh

## 3. Product goal

Help a user quickly answer:

> Which active prediction markets look most mispriced, stale, fragile, or suspicious right now, and why?

## 4. Non-goals

We are not trying to:
- build a general-purpose trading platform
- guarantee profitable trades
- solve market-making or execution
- ingest every possible source on day one
- build a huge autonomous multi-agent system
- depend on a VPS unless Zerve forces us to

## 5. Success criteria

### Submission success
- public Zerve project exists and runs cleanly
- deployed app exists and is demoable
- summary and demo can explain the insight in under 3 minutes
- results feel analytically grounded, not cosmetic

### Product success
- ranked list produces interesting, plausible markets
- each flagged market has understandable reasons
- the app is simple enough for a judge to grasp quickly
- the project visibly uses Zerve-native strengths

## 6. Primary user

For the hackathon, the practical primary user is:
- a judge or technically curious viewer who wants fast insight into what the system discovered

Secondary user:
- an analyst, bettor, or market observer who wants a short list of unusual markets with explanations

## 7. Core user stories

- As a judge, I want to open the app and immediately see the top flagged markets so I understand what the product does.
- As a user, I want to click a market and understand why it is flagged.
- As a user, I want to see when the data was last refreshed so I trust the output.
- As a builder, I want the scoring pipeline to be modular so we can improve it without rewriting everything.
- As a builder, I want Zerve to handle exploration, iteration, and deployment without extra infra.

## 8. Zerve-grounded product constraints and opportunities

Based on the docs, the project should be designed around how Zerve actually works.

### 8.1 Relevant Zerve capabilities

#### AI-native canvas and notebook workflow
Zerve is designed for AI-assisted data workflows inside its own environment. The agent can help build, fix, and modify workflows directly in the workspace.

Implication:
- we should treat Zerve as the primary build environment for the actual pipeline
- the product story should explicitly show notebook/canvas to deployed artifact

#### DAG-style block execution and stored block outputs
Zerve passes values left-to-right between blocks and stores outputs separately from compute.

Implication:
- the scoring pipeline should be split into clean stages
- each stage should produce named outputs we can reuse downstream
- app and API code should reference stable upstream variables, not duplicate logic

#### Streamlit deployment
Zerve supports deploying Streamlit apps directly from notebook outputs and lets app code reference notebook variables using `from zerve import variable`.

Implication:
- Streamlit should be the primary judge-facing artifact
- the app should consume prepared ranking tables and explanation structures from the pipeline

#### FastAPI deployment
Zerve supports notebook-linked FastAPI deployments with previews, logs, instance selection, and variable references from notebook blocks.

Implication:
- API is optional but realistic as a stretch deliverable
- if added, it should expose already-computed outputs rather than force a huge real-time recompute path

#### Scheduled jobs
Zerve supports scheduled jobs for recurring execution, and scheduled layers become read-only while active.

Implication:
- refresh automation is feasible
- we should plan scheduled jobs only after the pipeline is stable enough to freeze the layer

#### Fleets parallelization
Zerve supports spread/gather style parallel execution.

Implication:
- useful if we parallelize per-source ingestion, per-market feature generation, or evaluation runs
- not mandatory for MVP, but very good for the demo story if it helps materially

#### Environment and package management
Each canvas has its own configurable requirements and environment variables.

Implication:
- external API clients and analysis packages are viable
- we should keep dependencies modest and explicit

#### Assets: functions, classes, constants, secrets
Zerve supports reusable functions/classes plus secret constants.

Implication:
- source-specific fetchers or scoring helpers can live as reusable assets if needed
- API keys should go in Zerve secrets, not in notebook code

#### UI blocks and hosted apps
Zerve supports input/output UI blocks and hosted apps, but the docs make Streamlit deployment feel more direct for this use case.

Implication:
- for MVP, Streamlit is the clearest path
- UI blocks are interesting but probably not the shortest path to a polished judge demo

### 8.2 Important constraints

- app and API deployments depend on upstream variables being computed cleanly
- scheduled jobs are easier after the core pipeline is stable
- cross-block outputs should be deliberate and named carefully
- the project should not depend on unsupported undocumented tricks

## 9. Proposed product scope

## 9.1 MVP

The MVP will:
- ingest one or two prediction/forecasting sources
- normalize market records into one internal schema
- compute a transparent ranking score
- attach explanation components for each score
- display ranked outputs in a deployed Streamlit app

## 9.2 Stretch scope

Only if the MVP works well:
- add a third data source
- add a FastAPI deployment
- add scheduled refresh
- add more historical tracking and change views
- add a topic filter or category view

## 10. Recommended sources

### MVP recommendation
- Polymarket
- Kalshi or Metaculus, depending on integration friction

### Why not many more
Because the hackathon reward is not breadth for its own sake. Too many sources increase mapping pain and lower polish.

## 11. Product requirements

### 11.1 Functional requirements

#### Data ingestion
- fetch active questions/markets from selected sources
- retain market metadata, probability, timestamps, and identifiers
- preserve enough raw information to debug scoring decisions

#### Normalization
- convert source records into one internal schema
- derive freshness and event-horizon fields
- assign topic/category labels when possible

#### Scoring
- compute a composite market mispricing or fragility score
- retain per-component sub-scores for explanation
- produce a ranked table suitable for UI consumption

#### Explanation
- every ranked market should include plain-language reasons
- reasons should map back to explicit signals, not vague AI text only

#### Presentation
- Streamlit app should show ranked results, detail views, and refresh information
- app should be usable without reading internal docs first

#### Optional API
- expose ranked outputs and market details through simple endpoints
- use notebook-derived variables and prepared artifacts where possible

### 11.2 Non-functional requirements

- must be demo-safe and understandable quickly
- must not overclaim confidence or certainty
- should emphasize transparency over black-box sophistication
- should stay achievable within hackathon time
- should visibly use Zerve in a way judges value

## 12. Proposed Zerve implementation architecture

### Development layer

This is the primary pipeline layer.

Proposed blocks or modules:
1. source config / constants
2. source fetchers
3. raw market snapshot tables
4. normalization logic
5. feature engineering
6. scoring logic
7. explanation generation
8. ranked output table
9. evaluation / QA outputs

Outputs to preserve explicitly:
- normalized_markets
- market_features
- ranked_markets
- market_explanations
- refresh_metadata

### Deployment layer

Primary deployment:
- Streamlit app reading `ranked_markets`, `market_explanations`, and `refresh_metadata`

Optional deployment:
- FastAPI controller and route blocks exposing ranked outputs

### Scheduled jobs layer

Later phase only.

Responsibility:
- re-run ingestion, normalization, scoring, and output generation on a schedule

### Assets layer

Possible reusable assets:
- source fetch helpers
- normalization helpers
- scoring helpers
- constants or secrets for external APIs

## 13. Proposed app experience

### Screen 1: ranked radar
Show:
- top flagged markets
- score
- source
- category
- last update time
- one-line reason summary

### Screen 2: market detail
Show:
- market title and source link
- current probability
- score breakdown
- component explanations
- caveats / uncertainty notes
- optional similar or related market comparisons

### Screen 3: methodology
Show:
- short explanation of how the score works
- what it does and does not mean
- why this is useful

## 14. First scoring model direction

The first score should be simple and interpretable.

Candidate components:
- divergence score
- staleness score
- movement or volatility anomaly score
- event-horizon pressure score
- optional calibration or forecast disagreement score

Important rule:
- if a component is weak or fake, cut it
- we should prefer 3 strong signals over 8 decorative ones

## 15. Main risks

### Technical risks
- source APIs may be inconsistent or annoying
- cross-source question matching may be difficult
- history or calibration data may be sparse
- real-time freshness may complicate the pipeline

### Product risks
- becoming a generic dashboard
- using fancy scoring without real insight
- overscoping before the app works
- leaning too hard on AI-generated explanations instead of traceable logic

## 16. Risk response

- start with fewer sources
- avoid mandatory cross-platform matching in MVP
- build score explanations from explicit numeric components first
- ship app-first, API-second
- add scheduler only after the pipeline is stable

## 17. Delivery plan

### Phase 1: documentation and design
- finalize source scope
- define internal schema
- define first scoring components
- finalize app screens

### Phase 2: Zerve pipeline MVP
- implement source ingestion
- normalize outputs
- compute ranked outputs
- validate that results are interesting

### Phase 3: deploy judge-facing app
- build Streamlit app in Zerve
- connect upstream variables
- test the happy path and edge cases

### Phase 4: polish
- improve explanations
- sharpen copy and framing
- improve visual clarity
- produce submission materials

### Phase 5: optional extras
- add API deployment
- add scheduled refresh
- add more sources or better evaluation

## 18. Ship recommendation

Recommended default ship target:
- Zerve development layer with modular scoring pipeline
- Zerve Streamlit deployment as the main user artifact
- Git repo as planning, backup, and portable artifact store

This is the strongest balance of:
- hackathon scoring fit
- technical realism
- demo quality
- finishability
