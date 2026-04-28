# Zerve Agentic Report Upgrade

## Why this matters

Zerve's Agentic Reports feature turns notebook work into an interactive, shareable report. The docs describe two relevant capabilities:
- reports can be auto-generated from notebook blocks and outputs, then customized with prompts
- published reports can be queried with the built-in AI agent for follow-up questions grounded in the analysis

This is a good ZerveHack fit because it makes the submission feel more native to Zerve: the judge can see both the app and a report layer that explains the analysis.

## Repo artifact

Use this source in a Zerve **R Markdown** block:

- `zerve/reports/agentic-market-mispricing-report.Rmd`

It is self-contained and based on the current locked safe demo bundle. The report highlights the current default drilldown:

- `Putin out as President of Russia by December 31, 2026?`

## Zerve publish flow

1. Open the Market Mispricing Radar notebook/canvas in Zerve.
2. Add an **R Markdown** block.
3. Paste `zerve/reports/agentic-market-mispricing-report.Rmd` into the block.
4. Run the block.
5. Use **publish report** from the block dropdown.
6. Open **Reports** from the organization menu, then share/export if the report is clean.

## Customization prompt

Use this prompt when publishing/customizing the report:

> Create a concise, judge-facing report for a hackathon submission. Focus on why this project is more than a dashboard: it uses a Zerve notebook pipeline to ingest prediction-market data, compute explainable fragility signals, and ship an interactive app. Highlight the locked Putin drilldown, the honest scope limits, and three useful follow-up questions a reviewer can ask the report agent.

## Demo questions for the report agent

Ask these in the final video only if the report is published and opens cleanly:

1. Why is the Putin market ranked first right now?
2. Which top-ranked market looks most like a false positive, and why?
3. What evidence would you want before acting on one of these flags?

## Submission posture

Do **not** overclaim this as part of the final submission until it is actually published and opened in Zerve. Current wording should be:

- safe: "An Agentic Report source is prepared and can be published from an R Markdown block."
- unsafe until verified: "The final public report is live and shareable."

If the report is published before recording, use it as a short wow-factor beat after the app drilldown: app shows the operational workflow; report shows Zerve's agentic explanation layer.
