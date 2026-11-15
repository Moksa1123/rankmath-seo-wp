#!/usr/bin/env python3
"""search.py — the skill's single entry point: look up a rule before writing.

Searches data/*.csv and references/*.md. Chinese phrasing is expanded with
data/terms-zh.csv, so "密度門檻" finds the keywordDensity row. Every CSV hit
prints its source and trust (官方原始碼 / 官方文件 / 實測 / 站內風格 / 推論).
Nothing found = say so and log it in data/pending.csv; never guess.

Usage:
    python scripts/search.py "keyword density"
    python scripts/search.py "密度" --domain tests
    python scripts/search.py "faq 區塊" -n 3
    python scripts/search.py stats            # row counts + plugin version
    python scripts/search.py domains          # list domains

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REFS = ROOT / "references"

# domain -> CSV file (stem). "refs" searches references/*.md.
DOMAINS = {
    "tests": "rankmath-tests",
    "blocks": "blocks",
    "site": "site-rules",
    "density": "focus-keyword-density",
    "h2": "h2-templates",
    "faq": "faq-topics",
    "power": "power-words",
    "platforms": "platforms",
    "pending": "pending",
}


def use_utf8_stdout() -> None:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")


def load_csv(stem: str) -> list[dict]:
    with open(DATA / f"{stem}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_terms() -> list[tuple[str, str]]:
    return [(r["zh"], r["en"]) for r in load_csv("terms-zh")]


def expand(query: str) -> list[str]:
    """Split the query into tokens and append English terms for Chinese phrases."""
    q = query.lower()
    tokens = [t for t in re.split(r"[\s,，、/]+", q) if t]
    for zh, en in sorted(load_terms(), key=lambda t: -len(t[0])):
        if zh.lower() in q:
            tokens.extend(en.lower().split())
    seen, out = set(), []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def score_text(text: str, tokens: list[str]) -> int:
    low = text.lower()
    return sum(low.count(t) * (3 if len(t) > 3 else 1) for t in tokens)


def search(query: str, domain: str | None = None, max_results: int = 5) -> list[dict]:
    tokens = expand(query)
    hits: list[dict] = []
    domains = [domain] if domain else list(DOMAINS) + ["refs"]
    for d in domains:
        if d == "refs":
            for p in sorted(REFS.glob("*.md")):
                for i, chunk in enumerate(re.split(r"\n(?=## )", p.read_text(encoding="utf-8"))):
                    s = score_text(chunk, tokens)
                    if s:
                        title = chunk.strip().splitlines()[0].lstrip("# ")
                        hits.append({"_domain": "refs", "_score": s, "file": f"references/{p.name}",
                                     "section": title, "text": chunk.strip()[:400]})
            continue
        for r in load_csv(DOMAINS[d]):
            s = score_text(" ".join(r.values()), tokens)
            if s:
                hits.append({"_domain": d, "_score": s, **r})
    hits.sort(key=lambda h: -h["_score"])
    return hits[:max_results]


def dataset_stats() -> dict[str, int]:
    return {d: len(load_csv(stem)) for d, stem in DOMAINS.items()}


def plugin_version() -> str:
    for r in load_csv("rankmath-tests"):
        m = re.search(r"seo-by-rank-math (\d+\.\d+\.\d+)", r["source"])
        if m:
            return m.group(1)
    return "?"


def print_hit(h: dict) -> None:
    d = h["_domain"]
    if d == "refs":
        print(f"[refs] {h['file']} — {h['section']}")
        print("   " + h["text"].replace("\n", "\n   "))
        return
    body = {k: v for k, v in h.items() if not k.startswith("_") and k not in ("source", "trust", "doc_url")}
    print(f"[{d}] " + " | ".join(f"{k}={v}" for k, v in body.items() if v))
    src = h.get("doc_url") or ""
    print(f"   trust={h.get('trust', '?')}  source={h.get('source', '?')}" + (f"  {src}" if src else ""))


def main() -> int:
    use_utf8_stdout()
    ap = argparse.ArgumentParser(description="Look up Rank Math rules, block markup and site style.")
    ap.add_argument("query", nargs="+", help='search words, or "stats" / "domains"')
    ap.add_argument("--domain", choices=list(DOMAINS) + ["refs"])
    ap.add_argument("-n", type=int, default=5, help="max results (default 5)")
    args = ap.parse_args()
    q = " ".join(args.query)

    if q == "stats":
        stats = dataset_stats()
        print(f"Rank Math plugin source: seo-by-rank-math {plugin_version()}")
        for d, n in stats.items():
            print(f"  {d:10s} {n:3d} rows  data/{DOMAINS[d]}.csv")
        print(f"  {'total':10s} {sum(stats.values()):3d} rows")
        return 0
    if q == "domains":
        for d, stem in DOMAINS.items():
            print(f"{d:10s} data/{stem}.csv")
        print("refs       references/*.md")
        return 0

    hits = search(q, args.domain, args.n)
    if not hits:
        print(f"No match for {q!r}. Do not guess: tell the user and add a row to data/pending.csv.")
        return 1
    for h in hits:
        print_hit(h)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
