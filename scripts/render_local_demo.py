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
    parser.add_argument("--top", type=int, default=10, help="initial number of ranked rows to show in the radar section")
    parser.add_argument("--detail-count", type=int, default=3, help="number of detail cards to render from the filtered view")
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


def render_html(bundle: dict, top: int, detail_count: int) -> str:
    refresh = bundle["refresh_metadata"]
    category_breakdown = "".join(
        f"<li><strong>{esc(item['category'])}</strong>: {esc(item['market_count'])}</li>"
        for item in refresh.get("category_breakdown", [])[:8]
    )
    bundle_json = json.dumps(bundle)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Market Mispricing Radar, local demo</title>
  <style>
    body {{ font-family: Inter, Arial, sans-serif; margin: 2rem auto; max-width: 1200px; line-height: 1.45; color: #111827; background: #f8fafc; padding: 0 1rem; }}
    h1, h2, h3, h4 {{ color: #0f172a; }}
    .panel {{ background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,.04); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .controls {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: .75rem; align-items: end; }}
    .control label {{ display: block; font-size: .9rem; color: #334155; margin-bottom: .25rem; }}
    .control select, .control input {{ width: 100%; padding: .5rem; border: 1px solid #cbd5e1; border-radius: 8px; background: white; }}
    .range-readout {{ font-size: .9rem; color: #475569; margin-top: .25rem; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ text-align: left; padding: .65rem; border-bottom: 1px solid #e5e7eb; vertical-align: top; }}
    th {{ background: #f1f5f9; }}
    .meta {{ color: #475569; }}
    .detail-card {{ background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1rem; }}
    .pill-list {{ display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .5rem; }}
    .pill {{ background: #e2e8f0; color: #0f172a; border-radius: 999px; padding: .2rem .55rem; font-size: .85rem; }}
    .muted {{ color: #64748b; }}
    ul {{ margin: .5rem 0 0 1.1rem; }}
    code {{ background: #e2e8f0; padding: .1rem .3rem; border-radius: 4px; }}
    .empty {{ padding: 1rem; border: 1px dashed #cbd5e1; border-radius: 10px; color: #475569; background: #f8fafc; }}
  </style>
</head>
<body>
  <section class="panel">
    <h1>Market Mispricing Radar, local demo view</h1>
    <p>This is a lightweight local rendering of the current app bundle. It is a bridge artifact for the planned Zerve Streamlit app, not the final surface.</p>
    <div class="grid">
      <div><strong>Fetched at</strong><br>{esc(refresh['fetched_at'])}</div>
      <div><strong>Markets processed</strong><br>{esc(refresh['market_count'])}</div>
      <div><strong>Category count</strong><br>{esc(len(refresh.get('category_breakdown', [])))}</div>
      <div><strong>Pipeline version</strong><br>{esc(refresh['pipeline_version'])}</div>
      <div><strong>Score version</strong><br>{esc(refresh['score_version'])}</div>
    </div>
  </section>

  <section class="panel">
    <h2>Category snapshot</h2>
    <p class="meta">Heuristic category mix from <code>refresh_metadata.category_breakdown</code>.</p>
    <ul>{category_breakdown}</ul>
  </section>

  <section class="panel">
    <h2>Radar controls</h2>
    <p class="meta">Local bridge controls mirroring the planned Radar widgets.</p>
    <div class="controls">
      <div class="control">
        <label for="source-filter">Source</label>
        <select id="source-filter"></select>
      </div>
      <div class="control">
        <label for="category-filter">Category</label>
        <select id="category-filter"></select>
      </div>
      <div class="control">
        <label for="score-threshold">Minimum score</label>
        <input id="score-threshold" type="range" min="0" max="1" step="0.05" value="0">
        <div class="range-readout">Current threshold: <span id="score-threshold-readout">0.00</span></div>
      </div>
      <div class="control">
        <label for="result-count">Result count</label>
        <select id="result-count">
          <option value="5">Top 5</option>
          <option value="10" selected>Top 10</option>
          <option value="25">Top 25</option>
          <option value="50">Top 50</option>
        </select>
      </div>
      <div class="control">
        <label for="sort-order">Sort</label>
        <select id="sort-order">
          <option value="score_desc" selected>Highest score</option>
          <option value="stale_desc">Most stale</option>
          <option value="resolution_asc">Closest to resolution</option>
        </select>
      </div>
    </div>
  </section>

  <section class="panel">
    <h2>Radar</h2>
    <p class="meta">Interactive local view over <code>ranked_markets</code>.</p>
    <table>
      <thead>
        <tr><th>Rank</th><th>Market</th><th>Category</th><th>Source</th><th>Prob.</th><th>Score</th><th>Headline reason</th><th>Stale age</th></tr>
      </thead>
      <tbody id="radar-body"></tbody>
    </table>
    <div id="radar-empty" class="empty" style="display:none; margin-top: 1rem;">No results match the current filters. Reset the controls and try again.</div>
  </section>

  <section class="panel">
    <h2>Market detail</h2>
    <p class="meta">Sample detail cards from the currently filtered results.</p>
    <div id="detail-cards"></div>
    <div id="detail-empty" class="empty" style="display:none;">No detail cards are available because the current filters returned no rows.</div>
  </section>

  <section class="panel">
    <h2>Methodology</h2>
    <ul>
      <li>Single-source Polymarket-first MVP</li>
      <li>Ranks markets that look stale, fragile, extreme, or weakly supported</li>
      <li>Shows explanation fields derived from explicit score components</li>
      <li>Not a fair-value oracle and not financial advice</li>
    </ul>
  </section>

  <script>
    const bundle = {bundle_json};
    const explanationLookup = Object.fromEntries(bundle.market_explanations.map(item => [item.market_id, item]));
    const initialTop = {top};
    const detailCount = {detail_count};

    const sourceFilter = document.getElementById('source-filter');
    const categoryFilter = document.getElementById('category-filter');
    const scoreThreshold = document.getElementById('score-threshold');
    const scoreReadout = document.getElementById('score-threshold-readout');
    const resultCount = document.getElementById('result-count');
    const sortOrder = document.getElementById('sort-order');
    const radarBody = document.getElementById('radar-body');
    const radarEmpty = document.getElementById('radar-empty');
    const detailCards = document.getElementById('detail-cards');
    const detailEmpty = document.getElementById('detail-empty');

    function numberOrNull(value) {{
      return typeof value === 'number' ? value : null;
    }}

    function escapeHtml(value) {{
      return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }}

    function populateSelect(select, values, allLabel, selectedValue = 'all') {{
      select.innerHTML = '';
      const allOption = document.createElement('option');
      allOption.value = 'all';
      allOption.textContent = allLabel;
      select.appendChild(allOption);
      values.forEach(value => {{
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
      }});
      select.value = selectedValue;
    }}

    function sortRows(rows, order) {{
      const sorted = [...rows];
      sorted.sort((a, b) => {{
        if (order === 'stale_desc') {{
          return (numberOrNull(b.time_since_update_hours) ?? -Infinity) - (numberOrNull(a.time_since_update_hours) ?? -Infinity);
        }}
        if (order === 'resolution_asc') {{
          return (numberOrNull(a.time_to_resolution_hours) ?? Infinity) - (numberOrNull(b.time_to_resolution_hours) ?? Infinity);
        }}
        return (numberOrNull(b.final_score) ?? -Infinity) - (numberOrNull(a.final_score) ?? -Infinity);
      }});
      return sorted;
    }}

    function filteredRows() {{
      const selectedSource = sourceFilter.value;
      const selectedCategory = categoryFilter.value;
      const minScore = parseFloat(scoreThreshold.value || '0');
      const limit = parseInt(resultCount.value || String(initialTop), 10);

      let rows = bundle.ranked_markets.filter(row => {{
        if (selectedSource !== 'all' && row.source !== selectedSource) return false;
        if (selectedCategory !== 'all' && row.category !== selectedCategory) return false;
        if ((numberOrNull(row.final_score) ?? 0) < minScore) return false;
        return true;
      }});

      rows = sortRows(rows, sortOrder.value).slice(0, limit);
      return rows;
    }}

    function renderRadar(rows) {{
      if (!rows.length) {{
        radarBody.innerHTML = '';
        radarEmpty.style.display = 'block';
        return;
      }}
      radarEmpty.style.display = 'none';
      radarBody.innerHTML = rows.map(row => `
        <tr>
          <td>${{escapeHtml(row.rank)}}</td>
          <td><a href="#detail-${{escapeHtml(row.market_id)}}">${{escapeHtml(row.title)}}</a></td>
          <td>${{escapeHtml(row.category)}}</td>
          <td>${{escapeHtml(row.source)}}</td>
          <td>${{numberOrNull(row.current_probability)?.toFixed(3) ?? 'n/a'}}</td>
          <td>${{numberOrNull(row.final_score)?.toFixed(3) ?? 'n/a'}}</td>
          <td>${{escapeHtml(row.headline_reason)}}</td>
          <td>${{numberOrNull(row.time_since_update_hours)?.toFixed(1) ?? 'n/a'}}h</td>
        </tr>
      `).join('');
    }}

    function renderDetails(rows) {{
      const detailRows = rows.slice(0, detailCount);
      if (!detailRows.length) {{
        detailCards.innerHTML = '';
        detailEmpty.style.display = 'block';
        return;
      }}
      detailEmpty.style.display = 'none';
      detailCards.innerHTML = detailRows.map(row => {{
        const exp = explanationLookup[row.market_id] || {{ caveats: [], supporting_signals: [], score_components: {{}}, topic_tags: [] }};
        const topicTags = (exp.topic_tags || []).map(tag => `<span class="pill">${{escapeHtml(tag)}}</span>`).join('');
        const caveats = (exp.caveats || []).map(item => `<li>${{escapeHtml(item)}}</li>`).join('');
        const signals = (exp.supporting_signals || []).map(item => `<li>${{escapeHtml(item)}}</li>`).join('');
        const components = Object.entries(exp.score_components || {{}}).map(([key, value]) => `<li><strong>${{escapeHtml(key)}}</strong>: ${{escapeHtml(value)}}</li>`).join('');
        return `
          <section class="detail-card" id="detail-${{escapeHtml(row.market_id)}}">
            <h3>${{escapeHtml(row.title)}}</h3>
            <p class="meta">Category ${{escapeHtml(row.category)}} • Score ${{numberOrNull(row.final_score)?.toFixed(3) ?? 'n/a'}} • Probability ${{numberOrNull(row.current_probability)?.toFixed(3) ?? 'n/a'}} • <a href="${{escapeHtml(row.source_url)}}">Source</a></p>
            <p class="meta">Event context: ${{escapeHtml(row.event_title || 'n/a')}}</p>
            <p><strong>${{escapeHtml(exp.headline_reason || row.headline_reason)}}</strong></p>
            <p>${{escapeHtml(exp.short_explanation || '')}}</p>
            <p>${{escapeHtml(exp.detailed_explanation || '')}}</p>
            <div class="pill-list">${{topicTags || '<span class="muted">No topic tags</span>'}}</div>
            <div class="grid" style="margin-top: 1rem;">
              <div><h4>Caveats</h4><ul>${{caveats}}</ul></div>
              <div><h4>Supporting signals</h4><ul>${{signals}}</ul></div>
              <div><h4>Score components</h4><ul>${{components}}</ul></div>
            </div>
          </section>
        `;
      }}).join('');
    }}

    function refreshView() {{
      scoreReadout.textContent = Number(scoreThreshold.value || '0').toFixed(2);
      const rows = filteredRows();
      renderRadar(rows);
      renderDetails(rows);
    }}

    const sources = [...new Set(bundle.ranked_markets.map(row => row.source))].sort();
    const categories = [...new Set(bundle.ranked_markets.map(row => row.category))].sort();
    populateSelect(sourceFilter, sources, 'All sources');
    populateSelect(categoryFilter, categories, 'All categories');
    resultCount.value = String(initialTop);
    scoreThreshold.value = '0';

    [sourceFilter, categoryFilter, scoreThreshold, resultCount, sortOrder].forEach(control => {{
      control.addEventListener('input', refreshView);
      control.addEventListener('change', refreshView);
    }});

    refreshView();
  </script>
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
