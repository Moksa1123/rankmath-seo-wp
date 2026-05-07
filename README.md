<h1 align="center">Rank Math SEO WP — Agent Skill</h1>

<p align="center">
  <strong>Write Rank Math 80+ scoring WordPress articles via AI — paste-ready Gutenberg blocks, no SSH needed</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
  <a href="https://moksaweb.com"><img src="https://img.shields.io/badge/author-moksa-orange?style=flat-square" alt="moksa"></a>
</p>

<p align="center">
  <strong>Languages:</strong>
  <strong>English</strong> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

---

Battle-tested on [moksaweb.com](https://moksaweb.com) across 30+ published Claude AI tutorials.
Ships with a one-shot installer for **8 AI platforms** — Claude Code, Claude.ai,
Cursor, OpenAI Codex CLI, Gemini CLI, Windsurf, GitHub Copilot, and Continue —
plus any AI tool that follows the
[Anthropic Agent Skills standard](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

## Highlights

- **Paste-ready Gutenberg export** — clipboard the entire article, paste into the WP block editor, every block (HowTo / FAQ / embed / table) renders. No WP-CLI required.
- **Twin Python + Node tooling** — every CLI ships as both `.py` and `.mjs`. Pick whichever toolchain you already have.
- **Structured CSV reference data** — density bands, H2 templates, FAQ topics, power words. Read by both tools and humans.
- **Verifier** — checks FK density (1.0–1.5 % sweet spot), 12 H2 balance, HowTo / FAQ JSON↔HTML alignment, forbidden patterns.
- **Multi-platform installer** — supports Claude / Claude.ai / Cursor / Codex / Gemini CLI / Windsurf / Copilot / Continue (see `data/platforms.csv`).

## What this skill does

The skill triggers automatically when the assistant detects requests like:

- 「幫我寫一篇 WordPress 文章關於 X」
- "Write a WP article about X with Rank Math SEO"
- "Create blog post for moksaweb.com on Y"
- "Fix this article for Rank Math compliance"

The AI then produces an article with:

- **12 H2 structure** (opening + Moksa quote + 12 sections; FAQ block under H2 #12)
- **Focus-keyword density 1.0–1.5 %** (computed, not blindly stuffed)
- **Rank Math HowTo block** in canonical Gutenberg format
- **Rank Math FAQ block** with JSON ↔ HTML alignment
- **SEO Title containing a digit** (Rank Math hard requirement)
- **Natural Chinese writing style** — no English-jargon dump
- **2,000+ word count** with 3 YouTube embeds + 5 external authoritative links

## Quick start — one-liner install

Clone, then run the installer for your AI platform. The installer copies the
skill content to the correct path with the correct filename and frontmatter
for each tool.

```bash
git clone https://github.com/Moksa1123/rankmath-seo-wp
cd rankmath-seo-wp

# See all 8 supported platforms
python tools/install-skill.py --list
# or: node tools/install-skill.mjs --list
# or: npx rankmath-install --list

# Install into your current project
python tools/install-skill.py claude-code   # full install -> .claude/skills/rankmath-seo-wp/
python tools/install-skill.py cursor        # rule        -> .cursor/rules/rankmath-seo-wp.mdc
python tools/install-skill.py copilot       # append      -> .github/copilot-instructions.md
python tools/install-skill.py claude-ai --to ./build  # zip -> build/rankmath-seo-wp.zip

# Install globally (where supported by the platform)
python tools/install-skill.py claude-code --global   # ~/.claude/skills/rankmath-seo-wp/

# Inspect without writing
python tools/install-skill.py --info cursor
python tools/install-skill.py --dry-run claude-code
```

### Supported platforms

| Platform           | Key            | Install type         | Default path                                           |
|--------------------|----------------|----------------------|--------------------------------------------------------|
| Claude Code        | `claude-code`  | full                 | `.claude/skills/rankmath-seo-wp/SKILL.md`              |
| Claude.ai (web)    | `claude-ai`    | zip-upload           | `./rankmath-seo-wp.zip` → upload via Settings → Skills |
| Cursor             | `cursor`       | rule                 | `.cursor/rules/rankmath-seo-wp.mdc`                    |
| OpenAI Codex CLI   | `codex-cli`    | full                 | `.codex/skills/rankmath-seo-wp/SKILL.md`               |
| Gemini CLI         | `gemini-cli`   | full                 | `.gemini/extensions/rankmath-seo-wp/GEMINI.md`         |
| Windsurf           | `windsurf`     | rule                 | `.windsurf/rules/rankmath-seo-wp.md`                   |
| GitHub Copilot     | `copilot`      | instructions-append  | `.github/copilot-instructions.md`                      |
| Continue           | `continue`     | rule                 | `.continue/rules/rankmath-seo-wp.md`                   |

Codex CLI and Gemini CLI are best-effort — confirm against your tool's docs.

### Try it

After install, restart your AI tool and try:

```
> 幫我寫一篇 Claude Code Hooks 的教學文章
```

### Use as reference docs (no install)

Even without an installer, the `references/` and `data/` folders are
comprehensive documentation. Browse manually.

## Two delivery paths

This skill supports two delivery paths depending on whether you have shell
access to your WordPress server.

### Path A · Block paste (no SSH)

```bash
# 1. Verify
python tools/verify-article.py article.html "Your Focus Keyword"
# or: node tools/verify-article.mjs article.html "Your Focus Keyword"

# 2. Export — copies paste-ready HTML to clipboard
python tools/export-blocks.py article.html
# or: npx rankmath-export article.html

# 3. In WP admin: Posts → Add New → click in editor → Ctrl+V / Cmd+V
```

Gutenberg parses the `<!-- wp:... -->` block comments on paste and rebuilds
every block — HowTo, FAQ, YouTube embeds, tables, code blocks. Then set Rank
Math meta in the sidebar (focus keyword, SEO title with a digit, description,
slug) and upload your featured image.

Extract just one block:

```bash
python tools/export-blocks.py article.html --only howto   # HowTo only
python tools/export-blocks.py article.html --only faq     # FAQ only
```

Or write to file instead of clipboard:

```bash
python tools/export-blocks.py article.html --to-file ready.html
python tools/export-blocks.py article.html --print > ready.html
```

### Path B · WP-CLI batch (server access)

```bash
export WP_SSH_KEY=~/.ssh/id_rsa
export WP_SSH_HOST=user@your-wp-host.example.com
export WP_PATH=/path/to/wordpress

# Fix legacy HowTo blocks across multiple posts
python tools/fix-howto-block.py 8489 8478 8466

# Fix broken FAQ alignment across multiple posts
python tools/regenerate-faq.py 8489 8478 8579
```

## Verify any article

```bash
python tools/verify-article.py article.html "Your Focus Keyword"
# or
node tools/verify-article.mjs article.html "Your Focus Keyword"
```

Sample output:

```
=== article.html ===
Word count:      1495 visible words
                 OK above 1400 minimum
FK count:        22 visible occurrences
FK density:      1.47%
                 OK in target range 1.0-1.5%
Heading balance: 12 open / 12 close
                 OK 12/12 (target structure)
HowTo block:     OK
FAQ block:       OK (8 questions aligned)
Forbidden:       OK none found

=== Result: 8 passed, 0 failed ===
```

## Folder structure

```
rankmath-seo-wp/
├── SKILL.md                          # Skill contract (auto-loaded)
├── README.md                         # English entry (this file)
├── README.{zh-TW,ja,ko}.md           # Translations
├── CLAUDE.md                         # Conventions for AI assistants editing the skill
├── CONTRIBUTING.md                   # Human contributor guide
├── LICENSE                           # MIT
├── package.json                      # npm metadata + bin entries
├── data/                             # Structured CSV reference data
│   ├── focus-keyword-density.csv     # Density bands → verdict + remediation
│   ├── h2-templates.csv              # 12 H2 structure with FK placement
│   ├── faq-topics.csv                # 8 FAQ topic patterns (zh-TW + en)
│   ├── power-words.csv               # SEO-Title power words
│   └── platforms.csv                 # Install paths per AI platform
├── references/                       # Long-form guides (loaded on-demand)
│   ├── article-template.md           # 12 H2 structure + FK distribution
│   ├── howto-block.md                # rank-math/howto-block canonical format
│   ├── faq-block.md                  # FAQ JSON ↔ HTML alignment rules
│   ├── seo-checklist.md              # Rank Math 100-point breakdown
│   ├── moksa-style.md                # Personal-quote style + replacement table
│   ├── image-specs.md                # Featured-image specs + PIL template
│   └── wp-cli-pitfalls.md            # 9 WP-CLI deployment gotchas
├── tools/                            # Twin CLI tools (Python + Node)
│   ├── verify-article.py    / .mjs   # FK density + structure verifier
│   ├── export-blocks.py     / .mjs   # Block-paste-ready exporter
│   ├── install-skill.py     / .mjs   # Multi-platform installer
│   ├── regenerate-faq.py    / .mjs   # FAQ JSON↔HTML aligner (also batches via WP-CLI)
│   └── fix-howto-block.py   / .mjs   # Legacy HowTo format upgrader (also batches via WP-CLI)
└── examples/
    └── sample-article.html           # Reference article (passes all checks)
```

## What problems does this solve?

After publishing 30+ articles, the same paper-cuts kept showing up:

| Problem                                | This skill fixes by…                                                |
|----------------------------------------|---------------------------------------------------------------------|
| Rank Math SEO score under 60           | Following the 100-point checklist in `seo-checklist.md`             |
| FK density 3 %+ ("keyword stuffing")   | Distribution map in `article-template.md` (5 H2 + 4 FAQ + body)     |
| FK density 0.5 % ("too low")           | Verifier in `verify-article.{py,mjs}`                               |
| HowTo "區塊包含未預期的內容" error      | Canonical 8594 format in `howto-block.md`                           |
| FAQ block validation error             | JSON ↔ HTML alignment via `regenerate-faq.py`                       |
| `<script>` JSON-LD shows as raw text   | Skill explicitly warns against inline scripts                       |
| H2 contains "HowTo Schema" suffix      | Skill and verifier both flag this anti-pattern                      |
| Windows Python writes `\r\n`           | All tools force `newline='\n'`                                      |
| `--post_content="$(cat)"` shell error  | Skill teaches `wp post update file.html` syntax                     |
| SEO Title missing-number warning       | `[FK] 完整教學：N 大功能` template enforced                          |
| No SSH access to WP server             | `export-blocks` clipboards paste-ready HTML for the block editor    |

## Adapting to other niches

The skill targets Chinese tech tutorials, but the rules generalise:

- Replace `Moksa 觀點` opening with your brand's signature device
- Adjust `references/article-template.md` H2 structure for your domain
- 1.0–1.5 % FK density works for most languages
- Update WP host/path placeholders in `references/wp-cli-pitfalls.md`
- Update image base-template path in `references/image-specs.md`

## Open Standard

Follows the [Anthropic Agent Skills spec](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview):
`SKILL.md` with YAML frontmatter (`name`, `description`) + flat reference files.
Format-compatible across AI platforms.

## Author

Built and maintained by **moksa** — author of [moksaweb.com](https://moksaweb.com),
where this skill is battle-tested on every published Claude AI tutorial.

- Website: [moksaweb.com](https://moksaweb.com)
- Author: [moksa](https://moksaweb.com)

If this skill saved you a few hours of Rank Math debugging, a star ⭐ on the repo
or a link back to [moksaweb.com](https://moksaweb.com) is appreciated.

## License

MIT — see [LICENSE](LICENSE). Copyright © 2026 moksa (moksaweb.com).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome for:

- Translations (additional README locales beyond EN / zh-TW / ja / ko)
- Additional fix tools (broken image, broken external link, etc.)
- Niche-specific article templates (e-commerce, news, finance)
- Validation rules for other SEO plugins (Yoast, AIOSEO, SEOPress)

---

Crafted with [Claude Code](https://claude.com/claude-code) by [moksa](https://moksaweb.com).
