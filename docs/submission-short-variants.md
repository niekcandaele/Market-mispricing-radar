# Submission Short Variants

## Purpose

This document is the paste-ready short-form companion to `docs/submission-copy-draft.md`.

Use it for hackathon fields that need concise wording under length pressure.

## Project name

Market Mispricing Radar

## Tagline variants

### Default tagline
A live prediction-market radar that surfaces markets whose prices look fragile, stale, extreme, or weakly supported.

### Short tagline
An explainable radar for prediction markets that deserve a second look.

### Zerve-focused tagline
A Zerve-native market inspection radar that turns live notebook analysis into a deployed product.

## One-sentence summary variants

### Default
Market Mispricing Radar ranks prediction markets that look fragile, stale, extreme, or weakly supported, then explains why they surfaced.

### Slightly more product-focused
Market Mispricing Radar helps people spot prediction markets that deserve scrutiny instead of forcing them to scan raw odds one market at a time.

### Slightly more technical
Market Mispricing Radar ingests live market data, scores fragility signals, and deploys an explanation-rich inspection app through a real Zerve notebook pipeline.

## Short description variants

### ~160 characters
Explainable radar for prediction markets that look fragile, stale, or weakly supported, built as a live Zerve notebook-to-app workflow.

### ~250 characters
Market Mispricing Radar ranks prediction markets that deserve a second look. It surfaces fragile, stale, extreme, or weakly supported pricing and explains why each market is being flagged.

### ~400 characters
Market Mispricing Radar is a live inspection tool for prediction markets. Instead of forcing someone to scan raw odds market by market, it ranks the markets whose pricing looks fragile, stale, extreme, or weakly supported and explains why they surfaced.

## Elevator pitch variants

### 2 sentences
Prediction markets are useful, but most interfaces still force you to do the triage manually. Market Mispricing Radar turns that into an explainable workflow by ranking the markets that deserve scrutiny and showing the evidence behind the ranking.

### 3 sentences
Prediction markets are information-dense, but raw market lists do not tell you what to inspect first. Market Mispricing Radar ingests live market data, scores fragility signals like staleness and weak support, and surfaces the markets that deserve a second look. The result is an explanation-rich deployed product, not just a notebook output.

## Honest positioning variants

### Scope-safe line
This MVP does not claim perfect fair value or guaranteed arbitrage. It prioritizes which markets look most worth inspecting right now.

### Product-trust line
The score is a triage signal, not a promise of profit.

### Single-source caveat line
The current MVP is Polymarket-first and intentionally honest about that scope.

## Why this fits ZerveHack

### Short version
This project turns live notebook analysis into a deployed product inside Zerve, instead of stopping at a notebook or a static mockup.

### Slightly longer version
Market Mispricing Radar is a strong ZerveHack fit because the same environment handles live ingestion, scoring, explanation generation, and the deployed Streamlit app can actually be inspected and used.

## Built-with variants

### Minimal
Zerve, Python, Streamlit, Polymarket

### Slightly fuller
Zerve notebooks, Streamlit deployment, Python, and live Polymarket market data

## Challenge snippet

Turning the project into a credible product required solving both technical and presentation problems: stabilizing live ingestion, strengthening the notebook-to-app execution path, and iterating through multiple rounds of explainability polish.

## Accomplishment snippet

We proved a real end-to-end Zerve workflow from notebook ingestion and scoring to a deployed app that ranks markets and explains why they surfaced.

## What to paste when the form is cramped

If the submission form is annoyingly short, use this combo:

- tagline: `An explainable radar for prediction markets that deserve a second look.`
- summary: `Market Mispricing Radar ranks prediction markets that look fragile, stale, extreme, or weakly supported, then explains why they surfaced.`
- scope caveat: `The score is a triage signal, not a promise of profit.`
