#!/usr/bin/env python3
"""
multi_fetch_json_demo.py

Demonstrates multiple ways to retrieve and parse JSON from freely available public APIs.

Dependencies:
    pip install requests aiohttp pandas

Run:
    python multi_fetch_json_demo.py
"""

import json
import asyncio
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error

import requests
import aiohttp
import pandas as pd


# ---------------------------
# Config / endpoints
# ---------------------------
JSONPLACEHOLDER_POSTS = "https://jsonplaceholder.typicode.com/posts"
JSONPLACEHOLDER_POST_1 = "https://jsonplaceholder.typicode.com/posts/1"
HTTPBIN_STREAM = "https://httpbin.org/stream/10"   # streams 10 JSON objects as NDJSON
GITHUB_REPO = "https://api.github.com/repos/psf/requests"  # nested JSON example


# ---------------------------
# Utilities
# ---------------------------
def safe_get(d: Dict[str, Any], *keys, default=None):
    """Safely get nested keys from a dict, return default if missing."""
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


# ---------------------------
# Method 1: requests .json()
# ---------------------------
def fetch_with_requests_json(url: str, timeout: int = 10) -> Any:
    """Simple GET -> response.json() (requests handles decoding)."""
    print(f"fetch_with_requests_json: GET {url}")
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    # requests calls json.loads internally; convenient for well-formed JSON
    data = resp.json()
    print(f" -> got type: {type(data).__name__}")
    return data


# ---------------------------
# Method 2: requests raw bytes + json.loads
# ---------------------------
def fetch_with_requests_raw_then_loads(url: str, timeout: int = 10) -> Any:
    """
    Get raw bytes/text with requests, then decode using json.loads.
    Useful when you want to inspect raw text or tweak decoding.
    """
    print(f"fetch_with_requests_raw_then_loads: GET {url}")
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    text = resp.content.decode(resp.encoding or "utf-8")
    # inspect first 200 characters if debugging
    print(f" -> first 200 chars: {text[:200]!r}")
    data = json.loads(text)
    print(f" -> parsed as: {type(data).__name__}")
    return data


# ---------------------------
# Method 3: Streaming NDJSON with requests.iter_lines
# ---------------------------
def fetch_streaming_ndjson(url: str, timeout: int = 30) -> List[Dict[str, Any]]:
    """
    Demonstrate streaming a newline-delimited JSON (NDJSON) endpoint.
    Each line is a separate JSON object; httpbin.org/stream/N behaves like this.
    """
    print(f"fetch_streaming_ndjson: GET {url} (stream=True)")
    out = []
    with requests.get(url, stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        for i, raw_line in enumerate(resp.iter_lines(decode_unicode=True)):
            if not raw_line:  # skip blank lines
                continue
            try:
                obj = json.loads(raw_line)
                out.append(obj)
                print(f"  streamed #{i+1}: keys={list(obj.keys())}")
            except json.JSONDecodeError as e:
                print(f"  failed to decode line #{i+1}: {e}")
    print(f" -> total streamed objects: {len(out)}")
    return out


# ---------------------------
# Method 4: urllib.request (stdlib)
# ---------------------------
def fetch_with_urllib(url: str, timeout: int = 10) -> Any:
    """
    Fetch JSON using only the Python standard library (urllib).
    Useful when you don't want external deps.
    """
    print(f"fetch_with_urllib: GET {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "python-urllib/3"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            # read Content-Type header to decide encoding (fallback utf-8)
            content_type = resp.headers.get("Content-Type", "")
            encoding = "utf-8"
            if "charset=" in content_type:
                encoding = content_type.split("charset=")[-1].strip()
            text = raw.decode(encoding, errors="replace")
            data = json.loads(text)
            print(f" -> urllib parsed type: {type(data).__name__}")
            return data
    except urllib.error.HTTPError as he:
        print(f" -> HTTP error: {he.code} {he.reason}")
        raise
    except urllib.error.URLError as ue:
        print(f" -> URL error: {ue.reason}")
        raise


# ---------------------------
# Method 5: async with aiohttp
# ---------------------------
async def fetch_with_aiohttp(url: str, timeout: int = 10) -> Any:
    """
    Asynchronous fetch using aiohttp.
    Good when you want to fetch many endpoints concurrently.
    """
    print(f"fetch_with_aiohttp: GET {url}")
    timeout_cfg = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout_cfg) as session:
        async with session.get(url, headers={"Accept": "application/json"}) as resp:
            resp.raise_for_status()
            # aiohttp has .json() coroutine
            data = await resp.json()
            print(f" -> aiohttp got type: {type(data).__name__}")
            return data


# ---------------------------
# Parsing / Normalizing Examples
# ---------------------------
def parse_posts_list(posts: List[Dict[str, Any]]):
    """Simple parsing of a list of posts from JSONPlaceholder."""
    print("parse_posts_list: extracting titles and userId counts")
    titles = [p.get("title", "") for p in posts]
    # quick count of posts per userId
    counts = {}
    for p in posts:
        uid = p.get("userId", "unknown")
        counts[uid] = counts.get(uid, 0) + 1
    print(f" -> example title 0: {titles[0] if titles else '<none>'}")
    print(f" -> posts per userId (sample): {dict(list(counts.items())[:5])}")


def normalize_github_repo(repo_json: Dict[str, Any]):
    """Demonstrate pandas.json_normalize on nested GitHub repo JSON"""
    print("normalize_github_repo: using pandas.json_normalize")
    # Flatten top-level fields and nested owner object
    df = pd.json_normalize(repo_json, sep="_")
    # show a few useful columns if present
    keys_of_interest = [
        "full_name",
        "description",
        "owner_login",
        "owner_id",
        "stargazers_count",
        "forks_count",
        "language",
        "license_name",
    ]
    # create mapping for some nested fields we want:
    df = df.rename(columns={
        "owner.login": "owner_login",
        "owner.id": "owner_id",
        "license.name": "license_name",
    })
    print(" -> columns available:", list(df.columns)[:15])
    # print a trimmed view
    print(df[["full_name", "description", "owner_login", "stargazers_count", "forks_count", "language"]].head(1).to_dict(orient="records"))


# ---------------------------
# Demonstration runner
# ---------------------------
def main():
    print("=== Multi-method JSON fetch demo ===\n")

    # 1) requests .json()
    try:
        posts = fetch_with_requests_json(JSONPLACEHOLDER_POSTS)
        if isinstance(posts, list):
            parse_posts_list(posts[:10])  # parse first 10 for demo
    except Exception as e:
        print("Error fetching posts with requests.json():", e)

    print("\n---\n")

    # 2) requests raw -> json.loads
    try:
        single_post = fetch_with_requests_raw_then_loads(JSONPLACEHOLDER_POST_1)
        print("single_post keys:", list(single_post.keys()))
    except Exception as e:
        print("Error fetching single post with raw loads:", e)

    print("\n---\n")

    # 3) streaming NDJSON
    try:
        streamed = fetch_streaming_ndjson(HTTPBIN_STREAM)
        # show a field that httpbin stream returns (it returns 'id' and 'args' typically)
        print(f"Streamed objects sample length: {len(streamed)}")
    except Exception as e:
        print("Error streaming NDJSON:", e)

    print("\n---\n")

    # 4) urllib
    try:
        posts_via_urllib = fetch_with_urllib(JSONPLACEHOLDER_POSTS)
        print("urllib posts length (sample):", len(posts_via_urllib) if isinstance(posts_via_urllib, list) else "unknown")
    except Exception as e:
        print("Error fetching with urllib:", e)

    print("\n---\n")

    # 5) aiohttp (async)
    try:
        loop = asyncio.get_event_loop()
        github_repo = loop.run_until_complete(fetch_with_aiohttp(GITHUB_REPO))
        # Demonstrate reading headers / rate-limit (requests example next)
        if isinstance(github_repo, dict):
            print("GitHub repo name:", github_repo.get("full_name"))
            normalize_github_repo(github_repo)
    except Exception as e:
        print("Error fetching GitHub repo with aiohttp:", e)

    print("\n---\n")

    # 6) requests + headers example (reading rate limit info)
    try:
        print("requests: GET GitHub repo and read rate-limit headers")
        resp = requests.get(GITHUB_REPO, timeout=10, headers={"Accept": "application/vnd.github.v3+json"})
        resp.raise_for_status()
        repo_json = resp.json()
        print("Repo:", repo_json.get("full_name"))
        # GitHub returns rate limit headers; show them if present
        rl_limit = resp.headers.get("X-RateLimit-Limit")
        rl_remaining = resp.headers.get("X-RateLimit-Remaining")
        rl_reset = resp.headers.get("X-RateLimit-Reset")
        print("Rate limit headers:", {"limit": rl_limit, "remaining": rl_remaining, "reset": rl_reset})
    except Exception as e:
        print("Error fetching GitHub repo with requests:", e)

    print("\n=== Demo finished ===")


if __name__ == "__main__":
    main()
