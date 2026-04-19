# Source Strategy

## Decision

We are not locking the final multi-source stack yet.

Working decision:
- start with **Polymarket** for the MVP
- only add more sources after the first end-to-end pipeline works

This is a staged decision, not indecision.

## Why

A larger source set can make the product stronger, but only if the base system already works.

Adding sources too early increases:
- ingestion complexity
- normalization complexity
- matching complexity
- debugging burden
- risk of a half-finished product

For this hackathon, a sharp single-source product is better than a messy multi-source product.

## Source roadmap

### Stage 1: MVP
- Polymarket only

Goal:
- prove ingestion
- prove normalization
- prove ranking logic
- prove explanation quality
- prove Zerve app deployment

### Stage 2: expansion if time allows
- add Kalshi or Metaculus

Goal:
- introduce cross-source disagreement or forecast comparison
- improve the strength of the mispricing narrative

### Stage 3: ideal-world expansion
- Polymarket
- Kalshi
- Metaculus
- optional social/news context source

Goal:
- build a richer multi-signal market intelligence layer

## Practical rule

No new source gets added until the following are already true:
- the first pipeline runs end to end
- the first ranking output is interesting
- the first app is working
- the added source clearly improves the story instead of just adding work

## Notes

The ideal final product may use all three market/forecast sources plus one external context source.

But the MVP should earn the right to expand.
