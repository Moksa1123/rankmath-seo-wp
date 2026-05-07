# Project instructions for AI assistants

This file is read by Claude Code, Cursor, and other AI coding assistants when
they open this repository. It supplements `SKILL.md` (the user-facing skill
contract) with development conventions for editing the skill itself.

## Identity

- Project: `rankmath-seo-wp`
- Author / maintainer: **moksa** ([moksaweb.com](https://moksaweb.com))
- License: MIT
- Purpose: write Rank Math SEO compliant WordPress articles via AI agents

## Repository layout

```
rankmath-seo-wp/
├── SKILL.md                # Skill contract — auto-loaded by AI assistants
├── README.md               # English entry (multilingual switcher at top)
├── README.{zh-TW,ja,ko}.md # Translations
├── CLAUDE.md               # This file — AI dev conventions
├── CONTRIBUTING.md         # Human contributor guide
├── LICENSE                 # MIT
├── package.json            # npm metadata + bin entries (rankmath-export, -verify)
├── data/                   # CSV — density bands, H2 templates, FAQ topics, etc.
├── examples/               # Sample articles that pass all checks
├── references/             # Long-form guides (block formats, style, pitfalls)
└── tools/                  # CLIs — Python and Node twins
    ├── export-blocks.py    # Block-paste-ready exporter (Python)
    ├── export-blocks.mjs   # Block-paste-ready exporter (Node)
    ├── verify-article.py   # Article validator (Python)
    ├── verify-article.mjs  # Article validator (Node)
    ├── fix-howto-block.py  # HowTo block format upgrader (Python)
    └── regenerate-faq.py   # FAQ JSON↔HTML aligner (Python)
```

## When editing the skill

1. **`SKILL.md` is the contract.** Keep its YAML frontmatter (`name`,
   `description`) intact — both fields are required by the Anthropic Agent
   Skills spec, and other platforms (Cursor, Codex, Gemini CLI) depend on
   the same shape.
2. **Pair Python and Node tools.** Every CLI in `tools/` should exist in both
   `.py` and `.mjs` form unless the work is genuinely Python-only (e.g.,
   PIL image generation). Keep behaviour identical; tests below verify this.
3. **Use `data/*.csv` for structured rules.** When you find yourself adding a
   table-shaped fact to a markdown reference, ask whether it belongs in CSV
   instead so tooling can read it.
4. **Multilingual READMEs stay in sync.** When you change `README.md`, also
   propagate the structural change (headings, examples, file paths) to
   `README.zh-TW.md`, `README.ja.md`, `README.ko.md`. Wording can drift
   per-language, but section order and code samples must match.

## Sanitisation rules (open-source release)

This skill is published publicly. Never commit:

- Real SSH hosts, IPs, usernames, key filenames
- Real Cloudways / managed-WP paths (`/home/<account>.cloudwaysapps.com/...`)
- Personal Windows / macOS paths (`C:\Users\<name>\...`, `~/Library/...`)
- Cloud project IDs, account numbers, FileBird folder IDs

Always use placeholders: `user@your-wp-host.example.com`, `~/.ssh/id_rsa`,
`/path/to/wordpress`, `~/your-content-root/`.

If you find a leak, sanitise it before committing and grep the entire repo
for related strings.

## Local verification before commit

```bash
# Python
python tools/verify-article.py examples/sample-article.html "Claude Skills"
python tools/export-blocks.py examples/sample-article.html --print > /dev/null

# Node
node tools/verify-article.mjs examples/sample-article.html "Claude Skills"
node tools/export-blocks.mjs examples/sample-article.html --print > /dev/null

# npm scripts
npm run verify -- examples/sample-article.html "Claude Skills"
npm run export -- examples/sample-article.html --print > /dev/null
```

Both verifiers must agree on word count, FK density, heading balance, and
block validation. If they diverge, fix the regression rather than the test.

## Adding a new tool

1. Implement `tools/your-tool.py` first (Python is the reference language).
2. Mirror it as `tools/your-tool.mjs` using only Node 18+ stdlib.
3. Document it in `SKILL.md` under "Tools".
4. Add a script + bin entry to `package.json` if it's user-facing.
5. Update each README's tool table.

## Adding a new CSV

1. Place under `data/<name>.csv` with a header row.
2. Document the schema and intended consumers in `SKILL.md` under "Data".
3. Keep cells short — long prose belongs in `references/`.

## Style

- English in code comments and identifiers.
- Chinese in user-facing docs is fine (we ship a Traditional Chinese audience).
- Markdown: ATX headings (`##`), no trailing whitespace, LF endings.
- Python: PEP 8, type hints where the signature is non-obvious.
- JS: ES modules (`.mjs`), no CommonJS, no transpilation.

---

If you're an AI assistant reading this in the middle of a task: prefer
editing existing files over creating new ones, keep the Python/Node twin
invariant, and run the verifiers before declaring done.
