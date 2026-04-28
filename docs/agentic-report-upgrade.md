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

## Current publish status

A Zerve-native Agentic Report has now been generated and verified from the authenticated report route.

- report URL: `https://app.zerve.ai/report/4b2bcec4-48d2-4960-b051-cd465aa18a56`
- report status from API: `completed`
- answerable status from API: `confirmed`
- component count: `14`
- public toggle: enabled; unauthenticated API readback returns `is_public: true`
- authenticated browser verification: route loads, report title/content render, and report AI affordance is visible
- unauthenticated browser caveat: the Zerve web route currently shows Zerve's login/build landing rather than the rendered report, even though the unauthenticated API readback succeeds

Evidence:
- public toggle/readback: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-agentic-report-public-toggle-20260428T1631Z.json`
- unauthenticated API/browser check: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-agentic-report-public-20260428T1632Z.json`
- authenticated render check: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-agentic-report-auth-20260428T1633Z.json`

Important implementation note: the prepared R Markdown block was inserted into the notebook, but Zerve's R Markdown runner failed to produce usable block output in this environment. The verified live report was created through Zerve's native **Generate automatic report** flow from notebook outputs.

## Submission posture

Safe wording now:

- "A Zerve-native Agentic Report was generated from the notebook outputs and opens cleanly in the authenticated Zerve report view."
- "The report API is public, but the unauthenticated browser route still lands on Zerve's login/build screen, so do not rely on the report URL as the main judge-facing public link unless a final unauthenticated browser check improves."

Do **not** replace the verified public notebook link with the report link for the required share post. Keep the public notebook URL as the required public project link.

If used in the recording, use it as a short optional wow-factor beat after the app drilldown: app shows the operational workflow; report shows Zerve's agentic explanation layer.
