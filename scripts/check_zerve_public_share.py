#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

CANVAS_ID = "1b13702d-5502-47d1-b1e0-6ba476250dc4"
CANVAS_API = "https://canvas.api.zerve.ai"
NOTEBOOK_URL = f"https://app.zerve.ai/notebook/{CANVAS_ID}"
DEFAULT_TIMEOUT = 20


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def http_json(url, headers=None, timeout=DEFAULT_TIMEOUT):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", "replace")
        return {
            "status": resp.status,
            "url": resp.geturl(),
            "headers": dict(resp.headers.items()),
            "json": json.loads(body),
        }


def http_text(url, headers=None, timeout=DEFAULT_TIMEOUT):
    req = urllib.request.Request(
        url,
        headers=headers
        or {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147 Safari/537.36"
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read(4096).decode("utf-8", "replace")
        return {
            "status": resp.status,
            "url": resp.geturl(),
            "headers": dict(resp.headers.items()),
            "body_excerpt": body[:500],
        }


def interpret_public_route(body_excerpt):
    body = (body_excerpt or "").lower()
    looks_like_generic_shell = (
        "data work for the ai era" in body
        or 'og:title" content="zerve ai' in body
        or 'content="zerve, ai, platform"' in body
    )
    mentions_canvas = CANVAS_ID in body or "/notebook/" in body
    return {
        "looks_like_generic_shell": looks_like_generic_shell,
        "mentions_canvas_id": CANVAS_ID in body,
        "route_looks_verified": (not looks_like_generic_shell) and mentions_canvas,
    }


def try_public_route(url):
    try:
        res = http_text(url)
        return {"ok": True, **res, "interpretation": interpret_public_route(res.get("body_excerpt", ""))}
    except urllib.error.HTTPError as e:
        body = e.read(2048).decode("utf-8", "replace")
        return {
            "ok": False,
            "status": e.code,
            "url": e.geturl(),
            "headers": dict(e.headers.items()),
            "body_excerpt": body[:500],
            "interpretation": interpret_public_route(body[:500]),
            "error": f"HTTPError {e.code}",
        }
    except Exception as e:
        return {"ok": False, "error": repr(e)}


def try_canvas_status(bearer):
    headers = {"Authorization": f"Bearer {bearer}"}
    result = {"used_bearer": True}
    try:
        canvas = http_json(f"{CANVAS_API}/canvas/{CANVAS_ID}", headers=headers)
        result["canvas"] = {
            "status": canvas["status"],
            "url": canvas["url"],
            "is_public": canvas["json"].get("is_public"),
            "is_community": canvas["json"].get("is_community"),
            "name": canvas["json"].get("name"),
        }
    except Exception as e:
        result["canvas_error"] = repr(e)

    try:
        layout = http_json(f"{CANVAS_API}/canvas/canvas_layout/{CANVAS_ID}", headers=headers)
        result["canvas_layout"] = {
            "status": layout["status"],
            "url": layout["url"],
            "canvas_is_public": layout["json"].get("canvas", {}).get("is_public"),
            "canvas_is_community": layout["json"].get("canvas", {}).get("is_community"),
        }
    except Exception as e:
        result["canvas_layout_error"] = repr(e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Check Zerve public-share readiness for Market Mispricing Radar.")
    parser.add_argument("--output", help="Write JSON result to this path.")
    parser.add_argument("--bearer", help="Bearer token for authenticated canvas checks. Defaults to ZERVE_BEARER env var.")
    args = parser.parse_args()

    bearer = args.bearer or os.environ.get("ZERVE_BEARER")

    result = {
        "checked_at": now_iso(),
        "canvas_id": CANVAS_ID,
        "notebook_share_url": NOTEBOOK_URL,
        "public_route_check": try_public_route(NOTEBOOK_URL),
        "auth_check": {"used_bearer": False, "note": "Set ZERVE_BEARER or pass --bearer to check canvas.is_public directly."},
    }

    if bearer:
        result["auth_check"] = try_canvas_status(bearer)

    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    print(text)


if __name__ == "__main__":
    sys.exit(main())
