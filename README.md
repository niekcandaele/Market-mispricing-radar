# Market Mispricing Radar

Support repository for the ZerveHack project.

Primary goals:

- keep plans, notes, and backups in Git
- keep project management sane
- mirror important Zerve artifacts locally

Public link:

- verified public Zerve notebook: `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`

Demo and submission:

- `docs/demo-and-submission-guide.md`

See `PROJECT_PLAN.md` for the initial project plan.

Prototype harness:

- `python3 scripts/polymarket_ranker.py`
- `python3 scripts/render_local_demo.py`

Zerve Agentic Report:

- source: `zerve/reports/agentic-market-mispricing-report.Rmd`
- optional report: `https://app.zerve.ai/report/4b2bcec4-48d2-4960-b051-cd465aa18a56` (authenticated render verified; public API readback succeeds, but unauthenticated browser route still shows Zerve login/build)

Zerve app scaffold mirror:

- `python3 -m py_compile zerve/app/streamlit_app.py`

Local Streamlit mirror run:

- `./scripts/run_local_demo.sh`
