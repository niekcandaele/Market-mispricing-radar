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

## Notebook execution and automation quirks

Further validation on 2026-04-19 surfaced an important implementation wrinkle.

### What worked
- the Polymarket Gamma endpoint was validated outside Zerve against `https://gamma-api.polymarket.com/markets?closed=false&limit=20`
- the notebook cell content could be updated to a standard-library Python version using `urllib.request` and `json`
- the target variable name `polymarket_raw_markets` could be staged in the notebook cell

### What did not validate yet
- a confirmed successful notebook-side run with visible printed output
- a clearly surfaced traceback or runtime error in the current UI state
- reliable browser-driven triggering of the run action for the active cell

### Observed friction
- the notebook editor behaves like a Monaco-style editor with a hidden textarea layer, which made direct automation fragile
- side panels such as Source Control and the AI Agent reduced the visible canvas area and likely obscured output regions
- repeated automation attempts could edit the cell text, but visible stdout did not appear in the page text snapshot afterward
- the run control remained hard to verify through automation, even when the cell showed a prior runtime indicator like `1.2s`
- a later direct local Playwright-over-CDP fallback reached the already-open Zerve tab without relying on the browser tool, but still failed to produce visible stdout or traceback after both a button-click path and a `Shift+Enter` path
- screenshots captured after those fallback attempts still showed `Run this block`, which suggests the run action may not actually be firing from automation or the UI is not transitioning into a visible running state

### Practical implication
For now, the repo should treat Zerve notebook execution visibility as an active blocker for the first ingestion proof, not as a solved step.

That means:
- endpoint connectivity is partially validated
- notebook code staging is partially validated
- even a direct local CDP automation fallback did not yield visible output or error text
- end-to-end notebook execution is still unconfirmed

### Recommended next step
Investigate one of these paths:
1. manually trigger the notebook block once in the live UI and inspect the resulting output region
2. identify a more reliable notebook automation hook or keyboard path for running the active cell
3. test whether a less cluttered notebook state without side panels makes output and run state visible

## Deployment tab validation (2026-04-20)

Further live validation moved beyond notebook blocks and into the built-in deployment flow.

### What was confirmed
- opening `Deploy` from the notebook exposes first-class deployment types including Streamlit, Gradio, Dash, FastAPI, Flask, and Custom
- choosing `Streamlit` opens a dedicated deployment tab inside the same notebook workspace
- the default run command is shown as `streamlit run app/main.py --server.port 8080 --server.address 0.0.0.0`
- the editable code surface is labeled `main.py` in the deployment UI
- Zerve automatically provisions a preview deployment URL for the Streamlit tab
- the preview deployment can surface runtime failures directly in the rendered preview

### Important implementation detail
There is a notable path mismatch in the visible UI:
- editor label: `main.py`
- default run command: `streamlit run app/main.py ...`

This strongly suggests the deployment editor content is materialized into an `/app/main.py` runtime path behind the scenes, even though the visible tab label is shorter.

### Live runtime signal
A deliberately rough browser-driven code edit triggered a preview error modal showing:
- `File "/app/main.py", line 11`
- `IndentationError: unexpected indent`

That result matters because it confirms the preview deployment path is real and that deployment-side Python errors are surfaced back through the Zerve UI.

### Automation progress inside the deployment editor
A later validation pass found a cleaner automation hook than raw Monaco typing.

Observed from the live React tree around the Streamlit deploy editor:
- component props included `fileName`, `code`, `scriptId`, `editorKey`, and `onChange`
- the active deployment script id matched the Streamlit tab id: `ecda0778-025a-4d74-898a-31ee7c3f709d`
- calling the component's own `onChange` handler replaced the in-memory deployment code more cleanly than browser keystroke injection

Practical significance:
- the deployment editor is not a total black box
- we have a plausible automation path for code replacement that avoids most Monaco indentation mangling
- this is materially better than the earlier notebook-cell editing situation

### Preview deployment progress
After replacing the broken code through the editor's own change handler:
- the malformed indentation error was cleared from the preview path
- the deployment UI returned to a `Start Preview Deployment` state instead of the earlier broken preview dialog
- starting preview provisioning again produced a fresh preview URL and resumed deployment progress

This does not yet prove the app rendered successfully, but it does show that the deployment code can be repaired and re-previewed without manual typing.

### Still not confirmed
- the exact `from zerve import variable` access pattern in a fully running live Streamlit deployment
- whether the editor `onChange` path also persists cleanly through the underlying deployment save API in every case
- whether deployment code lives behind a stable internal API that is easier to automate directly than the React-layer hook

### Practical implication
The Streamlit deployment path is more real than assumed earlier: it has its own code editor, preview URL, runtime, and error surface.

The remaining gap is now narrower and more specific:
- not "does Streamlit deployment exist"
- not even primarily "can we patch code there"
- but "can we cleanly prove live notebook-variable wiring in a successful deployed preview"
