#!/usr/bin/env python3
from pathlib import Path
import html
import shutil

repo = Path(__file__).resolve().parents[1]
out = repo / 'artifacts' / 'submission' / 'slides-generator-deck'
img_dir = out / 'images'
out.mkdir(parents=True, exist_ok=True)
img_dir.mkdir(parents=True, exist_ok=True)

generated = {
    'hero': img_dir / 'hero.png',
    'inspection': img_dir / 'inspection.png',
    'pipeline': img_dir / 'pipeline.png',
}
for key, src in generated.items():
    dest = img_dir / f'{key}.png'
    if src.resolve() != dest.resolve():
        shutil.copy2(src, dest)

screens = {
    'radar': repo / 'artifacts/submission/slide-ready/local-radar-view-16x9.png',
    'detail': repo / 'artifacts/submission/slide-ready/local-market-detail-view-16x9.png',
    'methodology': repo / 'artifacts/submission/slide-ready/local-methodology-view-16x9.png',
}
for key, src in screens.items():
    dest = img_dir / f'{key}.png'
    if src.resolve() != dest.resolve():
        shutil.copy2(src, dest)

base_css = """
* { box-sizing: border-box; }
html, body { margin: 0; min-height: 100%; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0f172a; color: #f8fafc; }
.deck { width: 100vw; min-height: 100vh; overflow: hidden; }
.slide { display: none; position: relative; width: 100vw; min-height: 100vh; padding: 64px 72px; background: #111827; }
.slide.active { display: grid; }
.slide.title { place-items: end start; background-size: cover; background-position: center; }
.slide.split { grid-template-columns: 1fr 1fr; gap: 48px; align-items: center; }
.slide.image-focus { grid-template-rows: auto 1fr; gap: 28px; }
.slide .content { max-width: 920px; z-index: 1; }
.slide h1 { margin: 0 0 20px; font-size: 56px; line-height: 1.04; letter-spacing: 0; }
.slide h2 { margin: 0 0 20px; font-size: 42px; line-height: 1.1; letter-spacing: 0; }
.slide p, .slide li { font-size: 24px; line-height: 1.35; }
.slide ul { padding-left: 1.2em; }
.eyebrow { font-size: 16px; text-transform: uppercase; letter-spacing: 0.08em; color: #93c5fd; font-weight: 700; }
.subtitle { max-width: 780px; color: #dbeafe; }
.byline { color: #bfdbfe; }
.slide img { max-width: 100%; max-height: 72vh; object-fit: contain; border-radius: 8px; }
.nav { position: fixed; left: 50%; bottom: 20px; transform: translateX(-50%); display: flex; gap: 8px; z-index: 10; }
.dot { width: 10px; height: 10px; border-radius: 999px; border: 0; background: #64748b; }
.dot.active { background: #f8fafc; }
"""

slides = [
    {
        'type': 'title',
        'eyebrow': 'ZerveHack submission',
        'title': 'Market Mispricing Radar',
        'subtitle': 'A live prediction-market radar that surfaces fragile, stale, extreme, or weakly supported prices',
        'byline': 'Niek / Jefke · locked safe local default ready',
        'bg': 'images/hero.png',
        'notes': 'Open with the inspection problem: prediction markets are dense, but most interfaces leave triage to the user.'
    },
    {
        'type': 'split',
        'image': 'images/inspection.png',
        'alt': 'market cards pulled into a focused inspection beam',
        'headline': 'Raw odds are not enough',
        'points': [
            'Too many markets compete for attention',
            'Fragile pricing can hide in plain sight',
            'Users need reasons, not just ranks'
        ],
        'notes': 'Frame the problem as inspection and prioritization, not guaranteed arbitrage.'
    },
    {
        'type': 'content',
        'headline': 'The product is an explainable triage surface',
        'points': [
            'Fetch live Polymarket market data',
            'Score staleness, extremeness, weak support, and instability',
            'Rank markets by inspection priority',
            'Explain why each market surfaced',
            'Expose caveats instead of hiding them'
        ],
        'notes': 'Keep this as a product story: the app helps decide what deserves a second look.'
    },
    {
        'type': 'image',
        'image': 'images/radar.png',
        'alt': 'Market Mispricing Radar ranked cards view',
        'caption': 'Radar view: ranked cards, explanation headlines, category context, and caveats',
        'notes': 'Show the top-ranked markets and point out the refreshed default Putin drilldown path.'
    },
    {
        'type': 'split',
        'image': 'images/detail.png',
        'alt': 'Market Detail view with score drivers and observed market signals',
        'headline': 'The score is inspection evidence, not a profit promise',
        'points': [
            'Score drivers show what moved the market up the radar',
            'Observed signals make the ranking auditable',
            'Caveats keep the MVP honest'
        ],
        'notes': 'Use Putin as the refreshed locked default drilldown example.'
    },
    {
        'type': 'image',
        'image': 'images/methodology.png',
        'alt': 'Methodology view explaining scope and limitations',
        'caption': 'Methodology view: Polymarket-first, explanation-first, clear about limitations',
        'notes': 'This is the honesty beat. Say what the score does and does not claim.'
    },
    {
        'type': 'split',
        'image': 'images/pipeline.png',
        'alt': 'notebook blocks connected into a deployed app surface',
        'headline': 'Why this fits ZerveHack',
        'points': [
            'Notebook blocks produce the live analysis pipeline',
            'Outputs flow into a deployed Streamlit product',
            'The workflow turns analysis into something judges can inspect'
        ],
        'notes': 'Close the loop from Zerve notebook to deployed app. Mention the safe local default only if needed for recording reliability.'
    },
    {
        'type': 'stats',
        'headline': 'Submission status is near-ready, not pretend-complete',
        'stats': [
            ('Ready', 'locked safe local demo path'),
            ('Ready', 'submission copy + notes'),
            ('Ready', 'verified public Zerve notebook link')
        ],
        'notes': 'Be explicit: the public Zerve notebook link is verified; remaining external action is the human-approved public share post.'
    },
    {
        'type': 'closer',
        'headline': 'A usable radar for markets worth a second look',
        'contact': 'Default demo: locked safe local path · Drilldown: Putin out as President of Russia by December 31, 2026?',
        'notes': 'End on the value: fast triage, explainable evidence, honest scope.'
    },
]

def esc(value):
    return html.escape(str(value), quote=True)

parts = []
for i, slide in enumerate(slides, start=1):
    notes = f'<aside class="speaker-notes">{esc(slide["notes"])}</aside>'
    if slide['type'] == 'title':
        bg = f" style=\"--slide-bg-image: url('{esc(slide['bg'])}')\""
        parts.append(f'''<section class="slide slide--title has-bg" id="s{i}"{bg}>
  <div class="scrim"></div>
  <div class="title-card reveal">
    <p class="eyebrow">{esc(slide['eyebrow'])}</p>
    <h1>{esc(slide['title'])}</h1>
    <p class="subtitle">{esc(slide['subtitle'])}</p>
    <p class="byline">{esc(slide['byline'])}</p>
  </div>
  {notes}
</section>''')
    elif slide['type'] == 'content':
        lis = '\n'.join(f'    <li>{esc(p)}</li>' for p in slide['points'])
        parts.append(f'''<section class="slide slide--content" id="s{i}">
  <p class="eyebrow reveal">Product shape</p>
  <h2 class="reveal">{esc(slide['headline'])}</h2>
  <ul class="stagger bullet-list">
{lis}
  </ul>
  {notes}
</section>''')
    elif slide['type'] == 'image':
        parts.append(f'''<section class="slide slide--image" id="s{i}">
  <figure class="reveal screenshot-frame">
    <img src="{esc(slide['image'])}" alt="{esc(slide['alt'])}" />
    <figcaption>{esc(slide['caption'])}</figcaption>
  </figure>
  {notes}
</section>''')
    elif slide['type'] == 'split':
        lis = '\n'.join(f'      <li>{esc(p)}</li>' for p in slide['points'])
        parts.append(f'''<section class="slide slide--split" id="s{i}">
  <div class="split__media reveal">
    <img src="{esc(slide['image'])}" alt="{esc(slide['alt'])}" />
  </div>
  <div class="split__body">
    <p class="eyebrow reveal">Market inspection</p>
    <h2 class="reveal">{esc(slide['headline'])}</h2>
    <ul class="stagger bullet-list">
{lis}
    </ul>
  </div>
  {notes}
</section>''')
    elif slide['type'] == 'stats':
        stat_html = '\n'.join(f'''    <div class="stat">
      <strong class="stat__value">{esc(value)}</strong>
      <span class="stat__label">{esc(label)}</span>
    </div>''' for value, label in slide['stats'])
        parts.append(f'''<section class="slide slide--stats" id="s{i}">
  <p class="eyebrow reveal">Final-mile truth</p>
  <h2 class="reveal">{esc(slide['headline'])}</h2>
  <div class="stats stagger">
{stat_html}
  </div>
  <p class="status-note reveal">Safe local demo is verified. Public Zerve notebook link is verified; public share post still needs human-approved platform/copy.</p>
  {notes}
</section>''')
    elif slide['type'] == 'closer':
        parts.append(f'''<section class="slide slide--closer" id="s{i}">
  <div class="reveal closer-card">
    <p class="eyebrow">Close</p>
    <h2>{esc(slide['headline'])}</h2>
    <p class="contact">{esc(slide['contact'])}</p>
  </div>
  {notes}
</section>''')

controller = r'''
<script>
  class SlidePresentation {
    constructor() {
      this.slides = Array.from(document.querySelectorAll('section.slide'));
      this.progressFill = document.querySelector('.deck-progress .fill');
      this.current = 0;
      this.buildNav();
      this.bindKeyboard();
      this.bindTouch();
      this.bindWheel();
      this.bindScroll();
      this.observeReveal();
    }

    buildNav() {
      const nav = document.createElement('nav');
      nav.className = 'deck-nav';
      nav.setAttribute('aria-label', 'Slide navigation');
      const frag = document.createDocumentFragment();
      this.slides.forEach((slide, i) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.setAttribute('aria-label', `Go to slide ${i + 1}`);
        btn.addEventListener('click', () => this.goTo(i));
        frag.appendChild(btn);
      });
      nav.replaceChildren(frag);
      document.body.appendChild(nav);
      this.navButtons = Array.from(nav.querySelectorAll('button'));
      this.updateNav();
    }

    updateNav() {
      this.navButtons.forEach((btn, i) => {
        if (i === this.current) btn.setAttribute('aria-current', 'true');
        else btn.removeAttribute('aria-current');
      });
    }

    goTo(index) {
      const clamped = Math.max(0, Math.min(this.slides.length - 1, index));
      this.slides[clamped].scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    bindKeyboard() {
      window.addEventListener('keydown', (e) => {
        const forward = ['ArrowRight', 'ArrowDown', 'PageDown', ' '];
        const back = ['ArrowLeft', 'ArrowUp', 'PageUp'];
        if (forward.includes(e.key)) { e.preventDefault(); this.goTo(this.current + 1); }
        else if (back.includes(e.key)) { e.preventDefault(); this.goTo(this.current - 1); }
        else if (e.key === 'Home') { e.preventDefault(); this.goTo(0); }
        else if (e.key === 'End') { e.preventDefault(); this.goTo(this.slides.length - 1); }
      });
    }

    bindTouch() {
      let startY = 0;
      window.addEventListener('touchstart', (e) => { startY = e.touches[0].clientY; }, { passive: true });
      window.addEventListener('touchend', (e) => {
        const dy = e.changedTouches[0].clientY - startY;
        if (Math.abs(dy) < 50) return;
        this.goTo(this.current + (dy < 0 ? 1 : -1));
      }, { passive: true });
    }

    bindWheel() {
      let locked = false;
      window.addEventListener('wheel', (e) => {
        if (locked) return;
        if (Math.abs(e.deltaY) < 30) return;
        locked = true;
        this.goTo(this.current + (e.deltaY > 0 ? 1 : -1));
        setTimeout(() => { locked = false; }, 700);
      }, { passive: true });
    }

    bindScroll() {
      const updateProgress = () => {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
        if (this.progressFill) this.progressFill.style.width = `${pct}%`;
        let best = 0, bestRatio = 0;
        this.slides.forEach((slide, i) => {
          const rect = slide.getBoundingClientRect();
          const ratio = Math.max(0, Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, 0)) / window.innerHeight;
          if (ratio > bestRatio) { bestRatio = ratio; best = i; }
        });
        if (best !== this.current) { this.current = best; this.updateNav(); }
      };
      window.addEventListener('scroll', updateProgress, { passive: true });
      updateProgress();
    }

    observeReveal() {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add('visible');
        });
      }, { threshold: 0.3 });
      this.slides.forEach((s) => io.observe(s));
    }
  }

  document.addEventListener('DOMContentLoaded', () => new SlidePresentation());
</script>'''

theme_css = r'''
:root {
  --color-bg: oklch(0.16 0.025 255);
  --color-text: oklch(0.95 0.015 85);
  --color-accent: oklch(0.72 0.16 190);
  --color-warn: oklch(0.78 0.16 70);
  --color-muted: oklch(0.72 0.025 240);
  --panel: color-mix(in oklch, var(--color-bg) 78%, white 8%);
  --line: color-mix(in oklch, var(--color-text) 22%, transparent);
  --font-display: 'Space Grotesk', sans-serif;
  --font-body: 'IBM Plex Mono', monospace;
}

body { background: radial-gradient(circle at 20% 10%, color-mix(in oklch, var(--color-accent) 18%, transparent), transparent 34%), var(--color-bg); }
.slide { isolation: isolate; }
.slide::after { content: ''; position: absolute; inset: 1.25rem; border: 1px solid var(--line); border-radius: 28px; pointer-events: none; opacity: .7; }
.eyebrow { color: var(--color-accent); text-transform: uppercase; letter-spacing: .16em; font-weight: 700; font-size: clamp(.78rem, .7vw + .45rem, 1rem); margin-bottom: 1rem; }
.byline, .subtitle, .contact, figcaption, .status-note, .speaker-notes { color: var(--color-muted); }
.subtitle { max-width: 760px; margin-top: 1.2rem; font-size: clamp(1.1rem, 1.3vw + .7rem, 1.6rem); }
.byline { margin-top: 2rem; font-size: .95rem; }
.has-bg { background-image: linear-gradient(90deg, color-mix(in oklch, var(--color-bg) 92%, black 8%) 0 38%, transparent 70%), var(--slide-bg-image); background-size: cover; background-position: center; }
.scrim { position: absolute; inset: 0; background: radial-gradient(circle at 70% 50%, transparent 0 28%, color-mix(in oklch, var(--color-bg) 70%, transparent) 70%); z-index: -1; }
.title-card, .closer-card { max-width: 900px; }
.slide--content h2, .slide--stats h2 { max-width: 980px; }
.bullet-list { margin-top: 2rem; display: grid; gap: 1rem; max-width: 980px; }
.bullet-list li { padding: 1rem 1.1rem; border-left: 3px solid var(--color-accent); background: color-mix(in oklch, var(--panel) 88%, transparent); border-radius: 0 18px 18px 0; }
.slide--split { flex-direction: row; gap: clamp(2rem, 5vw, 5rem); align-items: center; }
.split__media, .split__body { flex: 1; min-width: 0; }
.split__media img, .screenshot-frame img { border-radius: 28px; border: 1px solid var(--line); background: var(--panel); box-shadow: 0 24px 80px color-mix(in oklch, black 48%, transparent); }
.split__media img { max-height: 62vh; object-fit: cover; width: 100%; }
.screenshot-frame { width: min(1100px, 92vw); margin: 0 auto; }
.screenshot-frame img { width: 100%; max-height: 68vh; }
.screenshot-frame figcaption { margin-top: 1rem; text-align: left; font-size: clamp(.9rem, .8vw + .55rem, 1.1rem); }
.stats { margin-top: 2.5rem; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.stat { padding: 1.4rem; border: 1px solid var(--line); border-radius: 24px; background: var(--panel); }
.stat__value { display: block; font-family: var(--font-display); font-size: clamp(1.8rem, 3vw + .5rem, 3.4rem); color: var(--color-accent); line-height: 1; }
.stat:nth-child(3) .stat__value { color: var(--color-warn); }
.stat__label { display: block; margin-top: .85rem; color: var(--color-muted); }
.status-note { margin-top: 2rem; max-width: 850px; }
.speaker-notes { position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }
.slide--closer { background: radial-gradient(circle at 70% 30%, color-mix(in oklch, var(--color-accent) 20%, transparent), transparent 30%), var(--color-bg); }
.slide--closer h2 { max-width: 980px; }
@media screen and (max-width: 900px) {
  .slide--split { flex-direction: column; align-items: stretch; }
  .stats { grid-template-columns: 1fr; }
}
'''

html_text = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>Market Mispricing Radar — ZerveHack Submission Deck</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
  <style>
{base_css}
{theme_css}
  </style>
</head>
<body>
  <div class="deck-progress" aria-hidden="true"><div class="fill"></div></div>
  <main class="slides">
{chr(10).join(parts)}
  </main>
{controller}
</body>
</html>
'''
(out / 'slides.html').write_text(html_text)
print(out / 'slides.html')
print('slides', len(slides))
print('images', len(list(img_dir.glob('*.png'))))
