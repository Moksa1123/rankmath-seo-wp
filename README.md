<div align="center">

# Rank Math SEO WP

### A WordPress article writer skill that produces Rank Math 80+ scoring posts. Paste-ready Gutenberg blocks. No SSH needed.

<p>
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><img src="https://img.shields.io/npm/v/rankmath-seo-wp?style=flat-square&color=cb3837&logo=npm&logoColor=white&label=npm" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><img src="https://img.shields.io/npm/dm/rankmath-seo-wp?style=flat-square&color=cb3837&logo=npm&logoColor=white" alt="npm downloads"></a>
  <a href="https://github.com/Moksa1123/rankmath-seo-wp"><img src="https://img.shields.io/github/stars/Moksa1123/rankmath-seo-wp?style=flat-square&logo=github&logoColor=white&color=181717" alt="GitHub stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
</p>

<p>
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+">
  <img src="https://img.shields.io/badge/AI%20platforms-8-blueviolet?style=flat-square" alt="8 AI platforms">
</p>

<p>
  <a href="#quick-start"><strong>Get started</strong></a> ·
  <a href="https://github.com/Moksa1123/rankmath-seo-wp"><strong>GitHub</strong></a> ·
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><strong>npm</strong></a> ·
  <a href="https://moksaweb.com"><strong>moksaweb.com</strong></a>
</p>

<p>
  <strong>English</strong> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

</div>

---

<table>
<tr>
<td width="33%" valign="top">

#### Block paste, no SSH

`rankmath-export article.html` copies the entire article to your clipboard. Paste into the WP block editor — every HowTo / FAQ / embed block reconstructs perfectly.

</td>
<td width="33%" valign="top">

#### 8-platform installer

`rankmath-install <platform>` drops the skill into the right path with the right frontmatter for Claude Code, Claude.ai, Cursor, Codex CLI, Gemini CLI, Windsurf, GitHub Copilot, and Continue.

</td>
<td width="33%" valign="top">

#### Pre-publish verifier

`rankmath-verify article.html "FK"` validates focus-keyword density (1.0–1.5%), 12 H2 structure, HowTo / FAQ block integrity, and 30+ Rank Math anti-patterns.

</td>
</tr>
<tr>
<td valign="top">

#### Twin Python and Node CLIs

Every CLI ships as a `.py` and `.mjs` twin pair, parity-tested. Pick whichever toolchain you already have — both produce identical output.

</td>
<td valign="top">

#### Structured CSV reference data

Density bands, H2 templates, FAQ topics, SEO power words, and platform install paths in machine-readable CSV. Tools and humans both read it.

</td>
<td valign="top">

#### Multilingual documentation

Full README in English, 繁體中文, 日本語, and 한국어, with synced structure and Chinese-language SEO defaults.

</td>
</tr>
</table>

---

## Quick start

```bash
# Use right now via npx (no install needed)
npx rankmath-install claude-code              # full skill -> .claude/skills/rankmath-seo-wp/
npx rankmath-export article.html              # copy paste-ready HTML to clipboard
npx rankmath-verify article.html "Claude Skills"

# Or install globally
npm install -g rankmath-seo-wp
rankmath-install --list                       # show all 8 supported AI platforms
```

After install, restart your AI tool and try:

```
> 幫我寫一篇 Claude Code Hooks 的教學文章
```

The skill triggers on requests to write WordPress articles. Output is Gutenberg-block-paste-ready and scores 80+ on Rank Math.

> [!TIP]
> Want to inspect before installing? Run `rankmath-install --info cursor` to see exact paths, frontmatter, and loader behaviour.

---

## Supported AI platforms

| # | Platform | Key | Strategy | Default path |
|---|----------|-----|----------|--------------|
| 1 | **Claude Code** | `claude-code` | full | `.claude/skills/rankmath-seo-wp/SKILL.md` |
| 2 | **Claude.ai (web)** | `claude-ai` | zip-upload | `./rankmath-seo-wp.zip` → Settings → Skills |
| 3 | **Cursor** | `cursor` | rule | `.cursor/rules/rankmath-seo-wp.mdc` |
| 4 | **OpenAI Codex CLI** | `codex-cli` | full | `.codex/skills/rankmath-seo-wp/SKILL.md` |
| 5 | **Gemini CLI** | `gemini-cli` | full | `.gemini/extensions/rankmath-seo-wp/GEMINI.md` |
| 6 | **Windsurf** | `windsurf` | rule | `.windsurf/rules/rankmath-seo-wp.md` |
| 7 | **GitHub Copilot** | `copilot` | append | `.github/copilot-instructions.md` |
| 8 | **Continue** | `continue` | rule | `.continue/rules/rankmath-seo-wp.md` |

> [!NOTE]
> `claude-code`, `claude-ai`, `cursor`, `windsurf`, `copilot`, and `continue` are verified. `codex-cli` and `gemini-cli` are best-effort — confirm against your tool's current docs.

---

## CLI cheatsheet

<details>
<summary><strong>Block-paste export</strong> — <code>rankmath-export</code></summary>

```bash
rankmath-export article.html                  # copy whole article to clipboard
rankmath-export article.html --only howto     # copy just the HowTo block
rankmath-export article.html --only faq       # copy just the FAQ block
rankmath-export article.html --to-file out.html
rankmath-export article.html --print > out.html
rankmath-export article.html --no-validate    # skip block validation
```

In WordPress: **Posts → Add New → click in editor → Ctrl+V / Cmd+V**.
Gutenberg parses the block comments and rebuilds every block.

</details>

<details>
<summary><strong>Article verifier</strong> — <code>rankmath-verify</code></summary>

```bash
rankmath-verify article.html "Your Focus Keyword"
```

Sample output:

```
=== article.html ===
Word count:      1495 visible words           OK above 1400 minimum
FK count:        22 visible occurrences
FK density:      1.47%                        OK in target range 1.0-1.5%
Heading balance: 12 open / 12 close           OK 12/12 (target structure)
HowTo block:     OK
FAQ block:       OK (8 questions aligned)
Forbidden:       OK none found

=== Result: 8 passed, 0 failed ===
```

</details>

<details>
<summary><strong>Multi-platform installer</strong> — <code>rankmath-install</code></summary>

```bash
rankmath-install --list                       # list 8 platforms
rankmath-install --info cursor                # inspect target path & loader
rankmath-install claude-code                  # install to ./.claude/skills/...
rankmath-install claude-code --global         # install to ~/.claude/skills/...
rankmath-install claude-ai --to ./build       # build zip in ./build/
rankmath-install --dry-run claude-code        # plan without writing
rankmath-install                              # interactive picker
```

</details>

<details>
<summary><strong>WP-CLI batch fixers</strong> — Python or Node (server access required)</summary>

```bash
export WP_SSH_KEY=~/.ssh/id_rsa
export WP_SSH_HOST=user@your-wp-host.example.com
export WP_PATH=/path/to/wordpress

# Fix legacy HowTo blocks across multiple posts
python tools/fix-howto-block.py 8489 8478 8466
node   tools/fix-howto-block.mjs 8489 8478 8466

# Fix broken FAQ JSON↔HTML alignment
python tools/regenerate-faq.py 8489 8478 8579
node   tools/regenerate-faq.mjs 8489 8478 8579
```

</details>

---

## Article anatomy

The skill produces an article matching this skeleton — every published moksaweb.com article follows it:

```
[Opening paragraph]            ~150 words, FK 2-3 times
[Moksa observation quote]      natural Chinese, FK 1 time, no jargon dump
H2 #1   什麼是 [FK]?
H2 #2   [FK] 和 [Competitor] 怎麼選?       ← comparison table
H2 #3   如何啟用這個工具?                   ← code block
H2 #4   [FK] 4 步驟啟用設定                 ← HowTo block
H2 #5   它能做哪些 X 工作?
H2 #6   [Persona] 怎麼用 [FK]?
H2 #7   [Killer feature] 怎麼運作?
H2 #8   進階主題或場景
H2 #9   哪裡可以找到更多官方資源?           ← 3 YouTube embeds
H2 #10  使用 [FK] 有哪些限制?               ← 6 paragraphs
H2 #11  參考依據                             ← 5 external links
H2 #12  常見問題 FAQ                         ← FAQ block
```

Result: 1,400–2,000+ words, FK density 1.0–1.5%, Rank Math 80+ score, paste-ready Gutenberg blocks.

---

## Repo layout

<details>
<summary>Click to expand</summary>

```
rankmath-seo-wp/
├── SKILL.md                          # Skill contract (auto-loaded)
├── README.md / .zh-TW / .ja / .ko    # Multilingual docs
├── CLAUDE.md                         # Conventions for AI editing the skill
├── CONTRIBUTING.md                   # Human contributor guide
├── LICENSE                           # MIT
├── package.json                      # npm metadata + 3 bin entries
│
├── assets/templates/platforms/       # 8 platform install configs
│   ├── claude-code.json              # full
│   ├── claude-ai.json                # zip-upload
│   ├── cursor.json                   # rule (.mdc + globs)
│   ├── codex-cli.json                # full
│   ├── gemini-cli.json               # full (GEMINI.md)
│   ├── windsurf.json                 # rule (model_decision)
│   ├── copilot.json                  # instructions-append (idempotent)
│   └── continue.json                 # rule (alwaysApply)
│
├── data/                             # Structured CSV reference
│   ├── focus-keyword-density.csv
│   ├── h2-templates.csv
│   ├── faq-topics.csv
│   ├── power-words.csv
│   └── platforms.csv
│
├── references/                       # Long-form prose guides
│   ├── article-template.md
│   ├── howto-block.md
│   ├── faq-block.md
│   ├── seo-checklist.md              # Rank Math 100-point breakdown
│   ├── moksa-style.md                # Personal-quote style guide
│   ├── image-specs.md                # Featured-image PIL template
│   └── wp-cli-pitfalls.md            # 9 deployment gotchas
│
├── tools/                            # Twin Python + Node CLIs
│   ├── verify-article.py    / .mjs   # FK density + structure verifier
│   ├── export-blocks.py     / .mjs   # Block-paste-ready exporter
│   ├── install-skill.py     / .mjs   # Multi-platform installer
│   ├── regenerate-faq.py    / .mjs   # FAQ JSON↔HTML aligner (also batches)
│   └── fix-howto-block.py   / .mjs   # Legacy HowTo format upgrader
│
└── examples/
    └── sample-article.html
```

</details>

---

## What this skill solves

After publishing 30+ articles, the same paper-cuts kept showing up:

| Problem | Fix shipped in this skill |
|---------|---------------------------|
| Rank Math SEO score under 60 | 100-point checklist in `references/seo-checklist.md` |
| FK density 3%+ ("keyword stuffing") | Distribution map: 5 H2 + 4 FAQ + selective body |
| FK density 0.5% ("too low") | Verifier in `verify-article.{py,mjs}` |
| HowTo "區塊包含未預期的內容" error | Canonical 8594 format in `references/howto-block.md` |
| FAQ block validation error | JSON ↔ HTML aligner `regenerate-faq.{py,mjs}` |
| `<script>` JSON-LD shows as raw text | Skill explicitly warns against inline scripts |
| `HowTo Schema` text in H2 heading | Both skill and verifier flag this anti-pattern |
| Windows Python writes `\r\n` | All tools force `newline='\n'` |
| `--post_content="$(cat)"` shell error | Skill teaches `wp post update file.html` syntax |
| SEO Title missing-number warning | `[FK] 完整教學：N 大功能` template enforced |
| **No SSH access to WP server** | **`rankmath-export` clipboards paste-ready HTML** |

---

## Adapting to other niches

This skill targets Chinese tech tutorials, but the rules generalise:

- Replace `Moksa 觀點` with your brand's signature opening device
- Adjust `references/article-template.md` H2 structure for your domain
- 1.0–1.5% FK density works for most languages
- Update WP host placeholders in `references/wp-cli-pitfalls.md`
- Update image base-template path in `references/image-specs.md`

---

## Open standard

Built on the [Anthropic Agent Skills spec](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview):
`SKILL.md` with YAML frontmatter (`name`, `description`) plus flat reference files.
Cross-platform-compatible by design.

---

## Author

<table>
<tr>
<td>

**[moksa](https://moksaweb.com)** — author of [moksaweb.com](https://moksaweb.com), where this skill is used on every published Claude AI tutorial.

This skill distils 30+ articles' worth of Rank Math debugging into a reusable, multi-platform, multi-language toolkit.

</td>
<td align="center" width="200">

<a href="https://moksaweb.com">
  <img src="https://img.shields.io/badge/website-moksaweb.com-2563EB?style=for-the-badge" alt="Website">
</a>
<br>
<a href="https://github.com/Moksa1123">
  <img src="https://img.shields.io/badge/GitHub-Moksa1123-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>

</td>
</tr>
</table>

If this skill saved you a few hours of Rank Math debugging, a star on the repo or a link back to [moksaweb.com](https://moksaweb.com) is appreciated.

---

## License and contributing

MIT — see [LICENSE](LICENSE). Copyright © 2026 moksa (moksaweb.com).

PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Especially:

- Translations (additional README locales beyond EN, zh-TW, ja, ko)
- Additional fix tools (broken image, broken external link, etc.)
- Niche-specific article templates (e-commerce, news, finance)
- Validation rules for other SEO plugins (Yoast, AIOSEO, SEOPress)

---

<div align="center">
  <sub>Built by <a href="https://moksaweb.com">moksa</a> · <a href="https://github.com/Moksa1123/rankmath-seo-wp">GitHub</a> · <a href="https://www.npmjs.com/package/rankmath-seo-wp">npm</a></sub>
</div>
