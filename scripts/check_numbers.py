#!/usr/bin/env python3
"""
check_numbers.py — every number in SKILL.md must be registered and true.

skill-SOP 6-1: numbers that change (row counts, versions) are not hand-written;
the ones that must appear are checked here. Whitelist, not spot-check: every
number outside code blocks, inline `code` and URLs must be claimed by a RULES
entry or the check fails. Add a rule whenever you add a number.

Rule kinds:
    fact   computed from the data (FACTS) and compared               (--fix rewrites)
    data   a Rank Math constant: the number must appear in the given
           CSV row/column (domain|key column|key value|column)
    row    the number is a CSV key: the row whose key column equals it must
           contain a word in another column (domain|key column|column|word)
    fixed  not from the data (step numbers, pass criteria, dates); give the reason

Engine copied from line-api/scripts/check_numbers.py; only FACTS and RULES differ.

Usage:
    python scripts/check_numbers.py            # exit 1 on any problem
    python scripts/check_numbers.py --fix      # rewrite fact values in SKILL.md
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_MD = HERE.parent / "SKILL.md"
sys.path.insert(0, str(HERE))

import search  # noqa: E402


# ---------------------------------------------------------------------------
# This skill's facts and rules
# ---------------------------------------------------------------------------
FACTS = {
    "csv_count": lambda: len(search.DOMAINS),
    "pkg_version": lambda: __import__("json").loads((HERE.parent / "package.json").read_text(encoding="utf-8"))["version"],
}

# (regex, kind, arg). Group 1 is the claimed number; without a group the whole
# match is claimed. Every number inside a matched span counts as claimed.
RULES: list[tuple[str, str, str]] = [
    # ---- Rank Math constants: must be in data/rankmath-tests.csv ----
    (r"word count ≥ (600)", "data", "tests|test_id|lengthContent|threshold"),
    (r"full-score band (1\.0–2\.5)%", "data", "tests|test_id|keywordDensity|threshold"),
    (r"recommended (1–1\.5)%", "data", "tests|test_id|keywordDensity_kb|rule"),
    (r"first (10)% of words", "data", "tests|test_id|keywordIn10Percent|rule"),
    (r"slug \(≤ (75) chars", "data", "tests|test_id|lengthPermalink|threshold"),
    (r"green above (80)", "data", "tests|test_id|scoreColor|threshold"),
    (r"score above (80)", "data", "tests|test_id|scoreColor|threshold"),
    (r"density (1\.0-1\.5)%", "data", "tests|test_id|keywordDensity_kb|threshold"),
    # ---- site style: must be in data/site-rules.csv or h2-templates.csv ----
    (r"(12) H2", "data", "site|rule_id|h2_count|value"),
    (r"FK in\s+(1/2/4/6/10)", "data", "site|rule_id|h2_with_fk|rule"),
    (r"(8) FAQs", "data", "site|rule_id|faq_count|value"),
    (r"(3) YouTube", "data", "site|rule_id|youtube_embeds|value"),
    (r"(5) links", "data", "site|rule_id|external_links|value"),
    (r"HowTo under H2 #(4)", "row", "h2|order|body_type|howto"),
    (r"FAQ under H2 #(12)", "row", "h2|order|body_type|faq"),
    (r"(12) is the site target", "data", "site|rule_id|h2_count|value"),
    (r"post (8594)", "data", "site|rule_id|howto_sizeslug|source"),
    (r"(4) 步驟 / (6) 大功能", "fixed", "example digits in an SEO-title fix"),
    (r"X (4) 步驟安裝設定", "fixed", "example wording"),
    # ---- not from the data ----
    (r"Checked (2026-11-15)", "fixed", "date the plugin source and KB were read (data checked_on column)"),
    (r"(30)\+ published articles", "fixed", "history: moksaweb.com article count when the template was distilled"),
    (r"^version: (\d+\.\d+\.\d+)", "fact", "pkg_version"),
    (r"(?<![\d.v])\d\. \*\*", "fixed", "numbered task steps"),
    (r"(8) passed, (0) failed", "fixed", "verifier pass criterion"),
    (r"exit (0)", "fixed", "verifier pass criterion"),
    (r"exits non-zero \((1)\); usage errors exit (1), unreadable files (2)", "fixed", "verifier exit codes"),
    (r"Node (18)", "fixed", "minimum Node version (package.json engines)"),
    (r"at least (1) H2", "fixed", "keywordInSubheadings needs one subheading"),
    (r"\b[Hh][1-6]\b", "fixed", "heading tag names (H2, h3)"),
    (r"Steps (1)-(3) as above", "fixed", "step numbers"),
    (r"\(exit (1) on any", "fixed", "checker exit code"),
]


# ---------------------------------------------------------------------------
# Engine (copied)
# ---------------------------------------------------------------------------
NUM = re.compile(r"\d+(?:[.,]\d+)*")
_MASKS = [
    re.compile(r"^```.*?^```", re.S | re.M),   # code blocks
    re.compile(r"`[^`\n]+`"),                  # inline code
    re.compile(r"\]\([^)\n]*\)"),              # markdown link targets
    re.compile(r"<https?://[^>\s]+>"),         # autolinks
    re.compile(r"https?://[^\s)）（，、|>]+"),   # bare URLs
]


def _masked(text: str, keep_inline: bool = False) -> str:
    for i, rx in enumerate(_MASKS):
        if keep_inline and i == 1:
            continue
        text = rx.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
    return text


def _data_value(spec: str) -> str:
    domain, key_col, key_val, col = spec.split("|")
    for r in search.load_csv(search.DOMAINS[domain]):
        if r.get(key_col) == key_val:
            return r.get(col, "")
    return ""


def _norm(s: str) -> str:
    return s.replace("–", "-").replace(" ", "")


def check(path: Path = SKILL_MD, fix: bool = False) -> tuple[list[str], int]:
    text = path.read_text(encoding="utf-8")
    scan = _masked(text)
    match_view = _masked(text, keep_inline=True)
    problems: list[str] = []
    covered: set[int] = set()
    edits: list[tuple[int, int, str]] = []

    for pattern, kind, arg in RULES:
        found = list(re.finditer(pattern, match_view, re.M))
        if not found:
            problems.append(f"rule unused (SKILL.md wording changed?): {pattern}")
            continue
        for m in found:
            covered.update(range(*m.span()))
            spans = [m.span(g) for g in range(1, (m.re.groups or 0) + 1)] or [m.span()]
            for span in spans:
                got = text[span[0]:span[1]]
                if kind == "fact":
                    want = str(FACTS[arg]())
                    if got != want:
                        problems.append(f"fact {arg}: SKILL.md says {got}, data says {want}")
                        edits.append((span[0], span[1], want))
                elif kind == "row":
                    domain, key_col, col, word = arg.split("|")
                    rows = [r for r in search.load_csv(search.DOMAINS[domain]) if r.get(key_col) == got]
                    if not rows or word.lower() not in rows[0].get(col, "").lower():
                        problems.append(f"row: {domain} {key_col}={got} has no {word!r} in {col}")
                elif kind == "data":
                    val = _data_value(arg)
                    if not val:
                        problems.append(f"data: no CSV row for {arg}")
                    elif _norm(got) not in _norm(val):
                        problems.append(f"data: SKILL.md says {got}, {arg} is {val!r}")

    line_of = lambda pos: text.count("\n", 0, pos) + 1  # noqa: E731
    for m in NUM.finditer(scan):
        if not any(i in covered for i in range(*m.span())):
            problems.append(f"line {line_of(m.start())}: {m.group(0)} is not registered in RULES")

    if fix and edits:
        for start, end, want in sorted(edits, reverse=True):
            text = text[:start] + want + text[end:]
        path.write_text(text, encoding="utf-8")
    n = sum(1 for _ in NUM.finditer(scan))
    return problems, n


def main() -> int:
    search.use_utf8_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--fix", action="store_true", help="rewrite fact values in SKILL.md")
    args = ap.parse_args()
    problems, n = check(fix=args.fix)
    if not problems:
        print(f"All {n} numbers in SKILL.md are registered and match the data.")
        return 0
    print(f"SKILL.md has {len(problems)} number problem(s):")
    for p in problems:
        print("  ✗", p)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
