# Zerve UI Validation Notes

## Validation date

2026-04-19

## Project created

A real Zerve notebook project was created:
- Project name: `Market Mispricing Radar`
- Notebook URL pattern observed: `/notebook/<uuid>`

## What was validated in the live UI

### 1. Notebook creation works

The project can be created directly from the home screen using `Create Project`.

Result:
- confirmed

### 2. Core notebook controls are visible immediately

Observed controls:
- Files
- Find & Replace
- Environments
- Compute Settings
- Global Imports
- Assets
- Source Control
- Run All
- Add block
- block types including Python, R, Markdown, Query, Gen AI, Input, Output, Aggregator
- Deploy button
- Schedule button (disabled initially)
- built-in AI Agent panel

Result:
- confirmed

### 3. Environment management exists on the free-plan notebook

Observed in Environments:
- Python environments listed
- environment presets visible including Flask, Dash, Gradio, Streamlit, FastAPI, Spark Connect, Geospatial, Computer Vision, NLP, Deep Learning, ML Starter, Default
- R environments also visible
- `Add Environment` button present

Important implication:
- Streamlit and FastAPI appear to be first-class environment options in the live product
- we likely do not need external hosting for the MVP app

### 4. Compute settings are exposed

Observed in Compute Settings:
- compute mode text shown as serverless / auto-stop style behavior
- default compute type shown as AWS Lambda
- save control present

Important implication:
- MVP should assume Lambda-style default compute unless a real need emerges to change it
- lightweight ingestion and scoring are a good fit

### 5. Assets surface exists, but is initially empty

Observed in Assets:
- no assets yet in the project
- add-asset flow exists
- UI text explicitly says assets can include reusable items such as data connections and secrets

Important implication:
- later API keys or reusable helper assets can live here
- we do not need to invent a workaround for secrets yet

### 6. Source control exists, but current live path appears GitHub-oriented

Observed in Source Control:
- prompt to install `Zerve Git App`
- visible git management service field showed `GitHub`
- install flow present

Important implication:
- native source control may currently prefer GitHub integration rather than arbitrary Forgejo
- for now, Git/Forgejo should remain our external control layer, not a Zerve-integrated repo assumption

### 7. Schedule exists but is not immediately active

Observed:
- `Schedule` button visible in notebook header
- initially disabled

Important implication:
- scheduling exists, but we should not rely on it until the notebook has meaningful runnable blocks

### 8. AI agent is available directly in the notebook

Observed:
- built-in agent panel is visible on first load
- accepts natural-language prompts in the notebook context

Important implication:
- we can test whether the agent is genuinely useful for notebook scaffolding and debugging
- but we should not blindly trust it with architecture or scoring logic

## MVP-relevant conclusions

### Strongly confirmed
- Zerve can host the primary notebook workflow we want
- Zerve exposes the controls we need for environments, compute, assets, deployment, and AI assistance
- Streamlit and FastAPI are visible as real environment concepts in the live UI

### Still unvalidated
- exact Streamlit deployment flow in this account
- exact FastAPI deployment flow in this account
- secret creation workflow in practice
- package installation details in practice
- whether Polymarket ingestion works cleanly from a Python block
- whether source control supports anything beyond the GitHub app flow

## Updated execution recommendation

Proceed with:
1. first Python block for Polymarket connectivity test
2. simple notebook-side data inspection
3. validate package/runtime assumptions only if needed
4. delay native source control integration work unless it clearly supports our workflow
5. treat Streamlit deployment as the primary target once the first outputs exist

## Main surprise

The live notebook surface is better than expected and fairly integrated.

The biggest mismatch versus our earlier abstract understanding is that the notebook already brings a lot of operational controls into one place, which should make the MVP path simpler.
