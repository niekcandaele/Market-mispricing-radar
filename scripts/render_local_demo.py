#!/usr/bin/env python3
"""Render a lightweight local HTML demo from the prototype app bundle."""

from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RANKER = REPO_ROOT / "scripts" / "polymarket_ranker.py"
DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "local-demo.html"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=500, help="number of markets to fetch")
    parser.add_argument("--top", type=int, default=10, help="number of ranked rows to show in the radar section")
    parser.add_argument("--detail-count", type=int, default=3, help="number of detail cards to render")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="output HTML path")
    return parser.parse_args()


def load_bundle(limit: int) -> dict:
    result = subprocess.run(
        [sys.executable, str(RANKER), "--limit", str(limit), "--app-json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value))


def radar_rows(rows: list[dict]) -> str:
    rendered = []
    for row in rows:
        rendered.append(
            "<tr>"
            f"<td>{row['rank']}</td>"
            f"<td><a href=\"#detail-{esc(row['market_id'])}\">{esc(row['title'])}</a></td>"
            f"<td>{esc(row['category'])}</td>"
            f"<td>{esc(row['source'])}</td>"
            f"<td>{row['current_probability']:.3f}</td>"
            f"<td>{row['final_score']:.3f}</td>"
            f"<td>{esc(row['headline_reason'])}</td>"
            f"<td>{row['time_since_update_hours']:.1f}h</td>"
            "</tr>"
        )
    return "\n".join(rendered)


def explanation_lookup(explanations: list[dict]) -> dict[str, dict]:
    return {item["market_id"]: item for item in explanations}


def detail_cards(rows: list[dict], explanations: dict[str, dict]) -> str:
    rendered = []
    for row in rows:
        exp = explanations[row["market_id"]]
        components = "".join(
            f"<li><strong>{esc(key)}</strong>: {esc(value)}</li>"
            for key, value in exp["score_components"].items()
        )
        caveats = "".join(f"<li>{esc(item)}</li>" for item in exp["caveats"])
        signals = "".join(f"<li>{esc(item)}</li>" for item in exp["supporting_signals"])
        tags = "".join(f"<li>{esc(item)}</li>" for item in exp["topic_tags"])
        rendered.append(
            f"<section class=\"detail-card\" id=\"detail-{esc(row['market_id'])}\">"
            f"<h3>{esc(row['title'])}</h3>"
            f"<p class=\"meta\">Category {esc(row['category'])} • Score {row['final_score']:.3f} • Probability {row['current_probability']:.3f} • <a href=\"{esc(row['source_url'])}\">Source</a></p>"
            f"<p class=\"meta\">Event context: {esc(row.get('event_title') or 'n/a')}</p>"
            f"<p><strong>{esc(exp['headline_reason'])}</strong></p>"
            f"<p>{esc(exp['short_explanation'])}</p>"
            f"<p>{esc(exp['detailed_explanation'])}</p>"
            "<div class=\"grid\">"
            f"<div><h4>Topic tags</h4><ul>{tags}</ul></div>"
            f"<div><h4>Caveats</h4><ul>{caveats}</ul></div>"
            f"<div><h4>Supporting signals</h4><ul>{signals}</ul></div>"
            f"<div><h4>Score components</h4><ul>{components}</ul></div>"
            "</div>"
            "</section>"
        )
    return "\n".join(rendered)


def render_html(bundle: dict, top: int, detail_count: int) -> str:
    ranked = bundle["ranked_markets"][:top]
    explanations = explanation_lookup(bundle["market_explanations"])
    details = bundle["ranked_markets"][:detail_count]
    refresh = bundle["refresh_metadata"]
    category_breakdown = "".join(
        f"<li><strong>{esc(item['category'])}</strong>: {esc(item['market_count'])}</li>"
        for item in refresh.get("category_breakdown", [])[:8]
    )
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>Market Mispricing Radar, local demo</title>
  <style>
    body {{ font-family: Inter, Arial, sans-serif; margin: 2rem auto; max-width: 1200px; line-height: 1.45; color: #111827; background: #f8fafc; padding: 0 1rem; }}
    h1, h2, h3 {{ color: #0f172a; }}
    .panel {{ background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,.04); }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ text-align: left; padding: .65rem; border-bottom: 1px solid #e5e7eb; vertical-align: top; }}
    th {{ background: #f1f5f9; }}
    .meta {{ color: #475569; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .detail-card {{ background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1rem; }}
    ul {{ margin: .5rem 0 0 1.1rem; }}
    code {{ background: #e2e8f0; padding: .1rem .3rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <section class=\"panel\">
    <h1>Market Mispricing Radar, local demo view</h1>
    <p>This is a lightweight local rendering of the current app bundle. It is a bridge artifact for the planned Zerve Streamlit app, not the final surface.</p>
    <div class=\"grid\">
      <div><strong>Fetched at</strong><br>{esc(refresh['fetched_at'])}</div>
      <div><strong>Markets processed</strong><br>{esc(refresh['market_count'])}</div>
      <div><strong>Category count</strong><br>{esc(len(refresh.get('category_breakdown', [])))}</div>
      <div><strong>Pipeline version</strong><br>{esc(refresh['pipeline_version'])}</div>
      <div><strong>Score version</strong><br>{esc(refresh['score_version'])}</div>
    </div>
  </section>

  <section class=\"panel\">
    <h2>Category snapshot</h2>
    <p class=\"meta\">Heuristic category mix from <code>refresh_metadata.category_breakdown</code>.</p>
    <ul>{category_breakdown}</ul>
  </section>

  <section class=\"panel\">
    <h2>Radar</h2>
    <p class=\"meta\">Top flagged markets from <code>ranked_markets</code>.</p>
    <table>
      <thead>
        <tr><th>Rank</th><th>Market</th><th>Category</th><th>Source</th><th>Prob.</th><th>Score</th><th>Headline reason</th><th>Stale age</th></tr>
      </thead>
      <tbody>
        {radar_rows(ranked)}
      </tbody>
    </table>
  </section>

  <section class=\"panel\">
    <h2>Market detail</h2>
    <p class=\"meta\">Sample detail cards from <code>market_explanations</code>.</p>
    {detail_cards(details, explanations)}
  </section>

  <section class=\"panel\">
    <h2>Methodology</h2>
    <ul>
      <li>Single-source Polymarket-first MVP</li>
      <li>Ranks markets that look stale, fragile, extreme, or weakly supported</li>
      <li>Shows explanation fields derived from explicit score components</li>
      <li>Not a fair-value oracle and not financial advice</li>
    </ul>
  </section>
</body>
</html>
"""


def main() -> int:
    args = parse_args()
    bundle = load_bundle(args.limit)
    html_text = render_html(bundle, args.top, args.detail_count)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_text, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
