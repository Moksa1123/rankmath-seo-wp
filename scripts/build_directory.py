#!/usr/bin/env python3
"""build_directory.py — generate directory-plugin/, the Claude plugin directory edition.

Unverified publishers may only ship Markdown, text, JSON, YAML and images in a
directory plugin, with the skill under skills/<name>/. This script builds that
folder from the main repository's sources so nothing is maintained twice:

    SKILL.md frontmatter, data/*.csv, references/*.md, LICENSE,
    .claude-plugin/plugin.json and icon.png, scripts/directory/*.tmpl

CSV files become JSON, the scripts are left out, and the site name is replaced
with neutral wording. Standard library only.

Usage:
    python scripts/build_directory.py           # write directory-plugin/
    python scripts/build_directory.py --check   # exit 1 if directory-plugin/ is stale
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "directory-plugin"
TMPL = ROOT / "scripts" / "directory"
SKILL_DIR = "skills/rankmath-seo-wp"
REPO = "https://github.com/Moksa1123/rankmath-seo-wp"

# data file -> one-line description for the generated SKILL.md
DATA_FILES = {
    "rankmath-tests": "Rank Math tests and score rules (plugin source)",
    "blocks": "HowTo / FAQ block markup from save() and block.json",
    "focus-keyword-density": "density bands and their points",
    "site-rules": "the author's conventions (site style)",
    "h2-templates": "12-H2 article skeleton",
    "faq-topics": "FAQ question patterns",
    "power-words": "title power words, and whether Rank Math counts them",
    "terms-zh": "Chinese phrases mapped to English terms",
    "pending": "open questions not yet answered",
}

REFERENCE_NOTE = (
    "> Directory edition: commands that mention `tools/` or `scripts/` need the full "
    "edition (`npm` package `rankmath-seo-wp`); this folder ships reference files only.\n"
    "> The `wp` commands below run on your WordPress server; how you connect to the "
    "server is up to you.\n"
)

# The directory edition must not tell Claude to log in to a server or read a
# credential from the user's machine. These patterns may not survive the build.
FORBIDDEN = re.compile(
    r"\bssh\b|\bscp\b|wp-config|\.env\b|id_rsa|id_ed25519|\.pem\b|password|passwd|SSH_KEY|YOUR_[A-Z_]{3,}",
    re.I)
# Reference sections about moving files to the server are dropped whole.
DROP_SECTION = re.compile(r"^## .*(?:\bSCP\b|\bSSH\b|push function)", re.I)


def serverless(text: str) -> str:
    """Rewrite server examples to the bare `wp` command; drop transfer steps."""
    # whole sections about transferring files over SSH / SCP
    parts = re.split(r"(?m)^(?=## )", text)
    text = "".join(p for p in parts if not DROP_SECTION.match(p))
    # multi-line: ssh host "cd /path && wp db query \" ... \""  ->  wp db query " ... "
    text = re.sub(r'ssh \S+ "(?:cd [^&"\n]+&& )?(wp [^"\n]*?)\\"(.*?)\\""', r'\1"\2"', text, flags=re.S)
    # one-line: ssh host "cd /path && wp ..." rest  ->  wp ... rest
    text = re.sub(r'(?m)^ssh \S+ "(?:cd [^&"\n]+&& )?([^"\n]*)"', r"\1", text)
    # upload pipes and the comment that introduces them
    text = re.sub(r"(?m)^.*\| ssh .*\n", "", text)
    text = re.sub(r"(?m)^(# \d+\. )Upload via .*$",
                  r"\1Put the file on the server (how you connect is up to you)", text)
    text = re.sub(r"(?m)^# Upload (?:binary|text) file.*\n", "", text)
    text = text.replace(" (cat | ssh)", "")
    # keep pitfall numbers continuous after dropping sections
    n = iter(range(1, 100))
    text = re.sub(r"(?m)^## Pitfall \d+:", lambda m: f"## Pitfall {next(n)}:", text)
    return text


def sanitize(text: str) -> str:
    """Remove the site name: example URLs become example.com, mentions become neutral."""
    text = re.sub(r"https?://(?:www\.)?moksaweb\.com", "https://example.com", text)
    text = re.sub(r"\b(?:[Tt]he|on) moksaweb(?:\.com)?\b", lambda m: m.group(0).split()[0] + " the author's site"
                  if m.group(0).startswith("on") else "the author's site", text)
    text = re.sub(r"moksaweb\.com|moksaweb", "the author's site", text, flags=re.I)
    # sentence or heading starts
    text = re.sub(r"(^#+ |^- |^\| |^|\. )the author's site", r"\1The author's site", text, flags=re.M)
    return text


def rows(stem: str) -> list[dict]:
    with open(ROOT / "data" / f"{stem}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def cell(s: str) -> str:
    return sanitize(s).replace("|", "\\|").replace("\n", " ")


def frontmatter() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    fm = text.split("---", 2)[1]
    fm = fm.replace(
        "digit. Includes deployment helpers for WP-CLI publishing.",
        "digit. Directory edition: reference data and checklists only; the verifier\n"
        "  and tools ship in the full npm package rankmath-seo-wp.",
    )
    fm = re.sub(r"^author: .*$", "author: Moksa", fm, flags=re.M)
    fm = fm.replace("、WP-CLI 發文。", "。")
    return "---" + sanitize(fm) + "---"


def facts() -> dict:
    tests = rows("rankmath-tests")
    pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    rm_version = next(m.group(1) for r in tests if (m := re.search(r"seo-by-rank-math (\d+\.\d+\.\d+)", r["source"])))
    return {
        "PKG_VERSION": pkg["version"],
        "RM_VERSION": rm_version,
        "RM_TESTS": str(len(tests)),
        "CHECKED": next(r["checked_on"] for r in tests if r["test_id"] == "keywordDensity"),
    }


def fill(template: str, values: dict) -> str:
    out = template
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if left:
        raise SystemExit(f"unfilled placeholders: {left}")
    return out


def skill_md() -> str:
    values = facts()
    values["FRONTMATTER"] = frontmatter()
    values["DATA_FILES"] = "\n".join(
        f"| `data/{stem}.json` | {len(rows(stem))} | {desc} |" for stem, desc in DATA_FILES.items())
    values["TESTS_TABLE"] = "\n".join(
        f"| `{r['test_id']}` | {cell(r['rule'])} | {cell(r['points'])} |" for r in rows("rankmath-tests"))
    values["BLOCKS_TABLE"] = "\n".join(
        f"| `{r['block']}` | {cell(r['item'])} | {cell(r['rule'])} |" for r in rows("blocks"))
    values["SITE_TABLE"] = "\n".join(
        f"| `{r['rule_id']}` | {cell(r['rule'])} | {r['trust']} |" for r in rows("site-rules"))
    return fill((TMPL / "SKILL.md.tmpl").read_text(encoding="utf-8"), values)


def readme() -> str:
    return fill((TMPL / "README.md.tmpl").read_text(encoding="utf-8"), facts())


def plugin_json() -> str:
    pj = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    pj.pop("userConfig", None)
    pj["description"] = pj["description"].replace(
        "a verifier that scores the article the way the plugin does, and rules read from the plugin's source",
        "a pre-publish checklist, and rules read from the plugin's source. Directory edition: reference files only, no scripts",
    )
    pj["author"] = {"name": "Moksa"}
    pj["homepage"] = f"{REPO}/tree/main/directory-plugin#readme"
    pj["documentationUrl"] = f"{REPO}/tree/main/directory-plugin#readme"
    pj["privacyPolicyUrl"] = f"{REPO}/tree/main/directory-plugin#what-it-runs-and-connects-to"
    pj["skills"] = [f"./{SKILL_DIR}"]
    return json.dumps(pj, ensure_ascii=False, indent=2) + "\n"


def reference(path: Path) -> str:
    text = serverless(sanitize(path.read_text(encoding="utf-8")))
    first, _, rest = text.partition("\n")
    return f"{first}\n\n{REFERENCE_NOTE}{rest}"


def build() -> dict[str, bytes]:
    files: dict[str, str | bytes] = {
        "README.md": readme(),
        # copyright holder kept; only the site URL after the name is dropped
        "LICENSE": re.sub(r" \(https?://(?:www\.)?moksaweb\.com/?\)", "",
                          (ROOT / "LICENSE").read_text(encoding="utf-8")),
        ".claude-plugin/plugin.json": plugin_json(),
        ".claude-plugin/icon.png": (ROOT / ".claude-plugin" / "icon.png").read_bytes(),
        f"{SKILL_DIR}/SKILL.md": skill_md(),
    }
    for p in sorted((ROOT / "references").glob("*.md")):
        files[f"{SKILL_DIR}/references/{p.name}"] = reference(p)
    for stem in DATA_FILES:
        data = {"source_file": f"data/{stem}.csv",
                "rows": [{k: sanitize(v) for k, v in r.items()} for r in rows(stem)]}
        files[f"{SKILL_DIR}/data/{stem}.json"] = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    out = {k: v if isinstance(v, bytes) else v.replace("\r\n", "\n").encode("utf-8") for k, v in files.items()}
    hits = []
    for rel, data in out.items():
        if rel.endswith(".png"):
            continue
        for i, line in enumerate(data.decode("utf-8").splitlines(), 1):
            if FORBIDDEN.search(line):
                hits.append(f"{rel}:{i}: {line.strip()[:100]}")
    if hits:
        raise SystemExit("directory edition would mention server login or credentials:\n  " + "\n  ".join(hits))
    return out


def existing() -> dict[str, bytes]:
    if not OUT.exists():
        return {}
    return {p.relative_to(OUT).as_posix(): p.read_bytes() for p in OUT.rglob("*") if p.is_file()}


def differences(want: dict[str, bytes], have: dict[str, bytes]) -> list[str]:
    out = [f"missing: {k}" for k in sorted(set(want) - set(have))]
    out += [f"stale (not built from sources): {k}" for k in sorted(set(have) - set(want))]
    out += [f"out of date: {k}" for k in sorted(set(want) & set(have)) if want[k] != have[k]]
    return out


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true", help="only compare; exit 1 if stale")
    args = ap.parse_args()
    want = build()
    diff = differences(want, existing())
    if args.check:
        if diff:
            print("directory-plugin/ is out of step with its sources (run scripts/build_directory.py):")
            for d in diff:
                print("  ✗", d)
            return 1
        print(f"directory-plugin/ matches its sources ({len(want)} files).")
        return 0
    for rel, data in want.items():
        p = OUT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    stale = [d for d in diff if d.startswith("stale")]
    print(f"wrote {len(want)} files to directory-plugin/")
    for d in stale:
        print("  !", d, "(remove it by hand)")
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
