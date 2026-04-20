# Market Mispricing Radar

Support repository for the ZerveHack project.

Primary goals:
- keep plans, notes, and backups in Git
- keep project management sane
- mirror important Zerve artifacts locally

See `PROJECT_PLAN.md` for the initial project plan.

Project workflow and repo conventions live in `docs/repo-workflow.md`.
Judge-facing app flow notes live in `docs/app-flow.md`.
MVP source validation notes live in `docs/mvp-source-validation.md`.
Zerve hybrid execution/debug notes live in `docs/zerve-hybrid-execution.md`.
Local scoring prototype notes live in `docs/local-ranking-prototype.md`.
Local demo-view notes live in `docs/local-demo-view.md`.
The current local bridge artifacts also carry heuristic category/topic context for app shaping.

Prototype harness:
- `python3 scripts/polymarket_ranker.py`
- `python3 scripts/render_local_demo.py`

The local demo now includes interactive Radar-style controls for filtering, sorting, click-through detail selection, filter reset states, a small same-category peer comparison block, raw supporting-signal values in the selected detail view, and compact score-breakdown cards for the selected market.
