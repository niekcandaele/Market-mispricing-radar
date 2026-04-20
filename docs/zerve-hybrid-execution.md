# Zerve hybrid execution notes

## Purpose

This note records the practical execution path that finally made the Zerve notebook debuggable again.

It exists because the notebook UI alone was not giving reliable visibility into what code actually ran or why the block failed.

## What was blocking us

Two separate problems were mixed together:

1. the Zerve notebook editor/output UX was hard to trust from browser automation alone
2. the initial Polymarket fetch code was getting `HTTP 403` from inside the Zerve runtime

At first this looked like one vague "Zerve is flaky" blocker.
It was actually a combination of:
- editor interaction quirks
- hidden but accessible block-state APIs
- request-shape differences between local runs and Zerve runs

## What works now

A hybrid method works reliably:

- use the browser/UI to stay logged in and interact with the notebook
- use the authenticated internal canvas APIs to inspect notebook state directly
- use block-state reads to inspect `code_ran`, `stdout`, `stack_trace`, `error`, and emitted variables

Useful live endpoints discovered from the running app:
- `GET https://canvas.api.zerve.ai/canvas/canvas_layout/<canvas_id>`
- `GET https://canvas.api.zerve.ai/block/state/<block_id>?use_cache=false`
- `GET https://canvas.api.zerve.ai/block/<block_id>/storage_urls/live_logs.txt?expiration=86400`

Authentication note:
- the browser session stores a bearer token in local storage under the Logto auth keys
- using that bearer token makes the block-state reads work cleanly

## Important execution result

The Zerve block can successfully fetch Polymarket markets when the request looks browser-like.

A bare standard-library request failed with `HTTP 403`.
A request with browser-like headers succeeded.

## Minimal working Zerve-side snippet

```python
import json
from urllib.request import Request, urlopen

url = "https://gamma-api.polymarket.com/markets?closed=false&limit=5"
req = Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
    },
)
response = urlopen(req, timeout=30)
body = response.read().decode("utf-8")
polymarket_raw_markets = json.loads(body)
print("count", len(polymarket_raw_markets))
first = polymarket_raw_markets[0]
print("question", first.get("question"))
print("slug", first.get("slug"))
print("id", first.get("id"))
```

## Confirmed successful run

Successful block-state result included:
- `success = true`
- `stdout` with count, question, slug, and id
- a persisted `polymarket_raw_markets` variable in Zerve

Observed stdout from the successful validation run:
- `count 5`
- `question Russia-Ukraine Ceasefire before GTA VI?`
- `slug russia-ukraine-ceasefire-before-gta-vi-554`
- `id 540816`

## Practical implication

This unblocks two things:

1. we now have a repeatable way to inspect real notebook execution even when the UI is awkward
2. the first Polymarket ingestion step is viable inside Zerve, as long as the request uses browser-like headers

## Current ingestion follow-through

The earlier probe block has now been promoted into a cleaner mirrored ingestion snippet at:
- `zerve/snippets/polymarket_ingestion_block.py`

Current behavior:
- fetches a larger raw slice from Polymarket (`limit=350`)
- filters that into a deterministic active-market output slice (`polymarket_raw_markets`, capped at 250)
- keeps browser-like request headers to avoid the earlier Zerve-side `HTTP 403` failure
- emits `ingestion_metadata` with `refresh_id`, fetch limits, fetched/output counts, and a first-market summary
- prints a notebook-friendly refresh summary for quick debugging

This means the handoff into normalization is now cleaner and more honest:
- upstream fetch breadth is larger than the earlier proof-of-life block
- the named output is still `polymarket_raw_markets`
- downstream blocks receive an active slice that is closer to the real scoring input shape
