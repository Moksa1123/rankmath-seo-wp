#!/usr/bin/env python3
"""Export article HTML as Gutenberg block-paste-ready output.

The WordPress block editor accepts block markup (HTML with
`<!-- wp:... -->` / `<!-- /wp:... -->` comments) when pasted as plain
text. This tool prepares an article so that paste lands cleanly:

- Normalises CRLF -> LF (Gutenberg validation breaks otherwise)
- Verifies every opening block comment has a matching closing one
- Verifies HowTo / FAQ block JSON parses
- Writes the result to clipboard, file, or stdout

Usage:
    python tools/export-blocks.py article.html               # copy to clipboard
    python tools/export-blocks.py article.html --to-file ready.html
    python tools/export-blocks.py article.html --print
    python tools/export-blocks.py article.html --only howto  # extract one block
    python tools/export-blocks.py article.html --only faq

After copying, in WordPress: Posts -> Add New -> click in the editor ->
paste (Ctrl+V or Cmd+V). Gutenberg parses the block comments and
reconstructs every block including HowTo, FAQ, embeds, tables.

Exit codes:
    0  ready, written / copied successfully
    1  validation failed (mismatched comments, broken JSON, etc.)
    2  invocation error
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


CLIP_INSTRUCTIONS = (
    "\n--- HOW TO PASTE INTO WORDPRESS ----------------------------------\n"
    "1. WP Admin -> Posts -> Add New (or open an existing post)\n"
    "2. Click inside the editor canvas (NOT a single block)\n"
    "3. Press Ctrl+V (Windows/Linux) or Cmd+V (macOS)\n"
    "4. Gutenberg will parse the block comments and rebuild every block\n"
    "5. Save draft and review — HowTo / FAQ / embeds should all render\n"
    "------------------------------------------------------------------\n"
)


# ---------- I/O helpers ----------------------------------------------------

def normalise_newlines(text: str) -> str:
    """Force LF newlines. Gutenberg validation fails on stray CR."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def copy_to_clipboard(text: str) -> bool:
    """Cross-platform clipboard copy. Returns True on success."""
    if sys.platform.startswith("win"):
        try:
            p = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=False)
            p.communicate(input=text.encode("utf-16le"))
            return p.returncode == 0
        except Exception as e:
            print(f"clip.exe failed: {e}", file=sys.stderr)
            return False

    if sys.platform == "darwin":
        try:
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(input=text.encode("utf-8"))
            return p.returncode == 0
        except Exception as e:
            print(f"pbcopy failed: {e}", file=sys.stderr)
            return False

    # Linux / WSL — try xclip, then xsel, then wl-copy.
    for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"], ["wl-copy"]):
        try:
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            p.communicate(input=text.encode("utf-8"))
            if p.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except Exception:
            continue
    print("No clipboard tool found. Install xclip / xsel / wl-clipboard, or use --to-file.", file=sys.stderr)
    return False


# ---------- Validation -----------------------------------------------------

BLOCK_OPEN = re.compile(
    r"<!--\s*wp:([a-z0-9/_-]+)(?:\s+\{[\s\S]*?\})?\s*(/?)-->",
    re.DOTALL,
)
BLOCK_CLOSE = re.compile(r"<!--\s*/wp:([a-z0-9/_-]+)\s*-->")


def validate_blocks(content: str) -> list[str]:
    """Return a list of validation error strings (empty list = OK)."""
    errors: list[str] = []

    # 1. Open / close balance per block name (skip self-closing).
    opens: dict[str, int] = {}
    for m in BLOCK_OPEN.finditer(content):
        name, slash = m.group(1), m.group(2)
        if slash:
            continue  # self-closing block, e.g. <!-- wp:separator /-->
        opens[name] = opens.get(name, 0) + 1

    closes: dict[str, int] = {}
    for m in BLOCK_CLOSE.finditer(content):
        name = m.group(1)
        closes[name] = closes.get(name, 0) + 1

    for name, n_open in opens.items():
        n_close = closes.get(name, 0)
        if n_open != n_close:
            errors.append(f"block <{name}>: {n_open} open / {n_close} close")
    for name, n_close in closes.items():
        if name not in opens:
            errors.append(f"block <{name}>: closing tag without opening")

    # 2. HowTo block JSON parses + has steps.
    m = re.search(r"<!--\s*wp:rank-math/howto-block\s+(\{.*?\})\s*-->", content, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(1))
            if "steps" not in data or not data["steps"]:
                errors.append("HowTo block: JSON has no steps")
            for forbidden in ("hasDuration", "hasTotalTime", "titleWrapper"):
                if forbidden in data:
                    errors.append(f"HowTo block: forbidden JSON field '{forbidden}'")
        except json.JSONDecodeError as e:
            errors.append(f"HowTo block: JSON parse error — {e}")

    # 3. FAQ block JSON parses + has questions.
    m = re.search(r"<!--\s*wp:rank-math/faq-block\s+(\{.*?\})\s*-->", content, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(1))
            if "questions" not in data or not data["questions"]:
                errors.append("FAQ block: JSON has no questions")
        except json.JSONDecodeError as e:
            errors.append(f"FAQ block: JSON parse error — {e}")

    # 4. Forbidden patterns that break paste.
    if re.search(r"<h2[^>]*>[^<]*HowTo Schema[^<]*</h2>", content):
        errors.append('"HowTo Schema" appears in an H2 heading — strip it')
    if "application/ld+json" in content:
        errors.append("Inline <script type=\"application/ld+json\"> — many themes strip it; use rank-math/howto-block instead")

    return errors


# ---------- Block extraction ----------------------------------------------

def extract_block(content: str, name: str) -> str | None:
    """Return the first block of the given short name (e.g. 'howto', 'faq')."""
    short_to_full = {
        "howto": "rank-math/howto-block",
        "faq": "rank-math/faq-block",
        "table": "table",
        "embed": "embed",
        "quote": "quote",
        "code": "code",
    }
    full = short_to_full.get(name, name)
    pattern = re.compile(
        rf"<!--\s*wp:{re.escape(full)}\b.*?<!--\s*/wp:{re.escape(full)}\s*-->",
        re.DOTALL,
    )
    m = pattern.search(content)
    return m.group(0) if m else None


# ---------- CLI -----------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Export an article as Gutenberg block-paste-ready output.",
    )
    ap.add_argument("article", help="Path to article.html")
    out = ap.add_mutually_exclusive_group()
    out.add_argument("--to-file", metavar="PATH", help="Write paste-ready content to file (LF newlines)")
    out.add_argument("--print", dest="to_stdout", action="store_true", help="Print to stdout instead of clipboard")
    ap.add_argument("--only", choices=["howto", "faq", "table", "embed", "quote", "code"],
                    help="Extract only one block type instead of the whole article")
    ap.add_argument("--no-validate", action="store_true", help="Skip block validation")
    args = ap.parse_args()

    path = Path(args.article)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    content = normalise_newlines(path.read_text(encoding="utf-8"))

    if args.only:
        block = extract_block(content, args.only)
        if not block:
            print(f"No '{args.only}' block found in {path}", file=sys.stderr)
            return 1
        content = block

    if not args.no_validate:
        errors = validate_blocks(content)
        if errors:
            print(f"Validation failed for {path}:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            print("\nFix issues or rerun with --no-validate to bypass.", file=sys.stderr)
            return 1

    # Output dispatch.
    if args.to_file:
        out_path = Path(args.to_file)
        out_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"Wrote {len(content):,} chars -> {out_path}")
        print(CLIP_INSTRUCTIONS)
        return 0

    if args.to_stdout:
        sys.stdout.write(content)
        return 0

    if copy_to_clipboard(content):
        print(f"Copied {len(content):,} chars to clipboard.")
        print(CLIP_INSTRUCTIONS)
        return 0

    print("Clipboard copy failed; falling back to stdout:", file=sys.stderr)
    sys.stdout.write(content)
    return 1


if __name__ == "__main__":
    sys.exit(main())
