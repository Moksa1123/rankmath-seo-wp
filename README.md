<h1 align="center">Rank Math SEO WP Writer</h1>

<h3 align="center">Rank Math SEO 文章撰寫工具</h3>

<p align="center">
  <strong>Rank Math test rules · Valid HowTo / FAQ blocks · Pre-publish verifier</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+">
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Rank%20Math%20tests-25-success?style=flat-square" alt="25 Rank Math tests">
  <img src="https://img.shields.io/badge/AI%20platforms-8-blueviolet?style=flat-square" alt="8 AI platforms">
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><img src="https://img.shields.io/npm/v/rankmath-seo-wp?style=flat-square&color=cb3837&logo=npm&logoColor=white&label=npm" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><img src="https://img.shields.io/npm/dm/rankmath-seo-wp?style=flat-square&color=cb3837&logo=npm&logoColor=white" alt="npm downloads"></a>
  <a href="https://github.com/Moksa1123/rankmath-seo-wp"><img src="https://img.shields.io/github/stars/Moksa1123/rankmath-seo-wp?style=flat-square&logo=github&logoColor=white&color=181717" alt="GitHub stars"></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
</p>

<p align="center"><strong>English</strong> · <a href="README.zh-TW.md">正體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a></p>

> This is an unofficial community project. It is not made by, endorsed by, or affiliated with Rank Math or its makers. Rank Math SEO is third-party software and is not included here.

## What it does

Turns "write me a WordPress article" into an article that passes Rank Math's own tests and scores 80+, without guessing at Rank Math's rules.

| Area | What you get |
|---|---|
| Rank Math rules | 25 Rank Math tests and score rules with points, thresholds and KB links, read from the source of seo-by-rank-math 1.0.282 |
| Blocks | HowTo and FAQ markup that matches each block's `save()`, so the editor never shows "invalid content" |
| Verifier | Counts words and density the way Rank Math does; any failed check exits with exit code 1 |
| Lookup | Chinese or English questions answered from `data/`, each with its source |
| Publishing | Clipboard block paste (no server access) or WP-CLI on your own server |
| Tools | Every CLI as a Python and a Node twin, standard library only, installer for 8 AI platforms |

### Rules read from the plugin

```bash
python scripts/search.py "密度"
# [tests] keywordDensity ... <0.5 fail 0; ... up to 2.5 best 6; >2.5 fail 0
#    trust=官方原始碼  source=analyzer.js keywordDensity calculateScore (1.0.282)
```

### Pre-publish verifier

```bash
rankmath-verify article.html "Focus Keyword"    # or: python tools/verify-article.py
```

### Block paste, no SSH

```bash
rankmath-export article.html                    # whole article to the clipboard
rankmath-export article.html --only faq         # just the FAQ block
```

### Block fixers

```bash
python tools/regenerate-faq.py article.html     # rebuild FAQ HTML from its JSON
python tools/fix-howto-block.py 101 --dry       # preview a HowTo fix on post 101
```

### Problems it fixes

| Problem | Fix in this skill |
|---|---|
| Density too high or too low | Plugin scoring bands in `data/focus-keyword-density.csv`; the verifier counts like the plugin |
| HowTo or FAQ block shows "invalid content" | HTML must equal the block's `save()`; `fix-howto-block` and `regenerate-faq` rebuild it |
| JSON-LD `<script>` printed as text | Use the rank-math blocks; the verifier flags inline `ld+json` |
| "Your SEO title doesn't contain a number" | Title template `[FK] 完整教學：N 大功能` |
| `--post_content="$(cat …)"` fails, Windows writes `\r\n` | Pass the file to `wp post update`; every tool writes LF |
| No SSH access to the server | `rankmath-export` copies paste-ready blocks |

## When to use

| Use it for | Use something else for |
|---|---|
| Writing, fixing or publishing posts on a WordPress site that runs Rank Math SEO | Other block-editor pages → `gutenberg-headless` |
| Tutorials, guides and blog posts with HowTo and FAQ blocks, in Traditional Chinese or any language | Elementor or Mosaic pages → `elementor-headless`, `mosaic-headless` |
| Repairing HowTo / FAQ blocks the editor marks as invalid | Sites on Yoast or another SEO plugin (different tests) |

## Install

| Need | For |
|---|---|
| Python 3.9+ or Node.js 18+ | The tools (standard library only) |
| `ssh`, and WP-CLI on your server | Publishing or batch-fixing posts over WP-CLI only |
| Windows, macOS or Linux | Everything |

### Step 1: Pick an install method

Claude plugin (Claude Code; the Claude directory once listed):

```
/plugin marketplace add Moksa1123/rankmath-seo-wp
/plugin install rankmath-seo-wp@rankmath-seo-wp
```

npx (Claude Code and the other AI tools below):

```bash
npx -p rankmath-seo-wp@1.2.0 rankmath-install claude-code --global
npx -p rankmath-seo-wp@1.2.0 rankmath-install --list
```

Manual copy:

```bash
git clone https://github.com/Moksa1123/rankmath-seo-wp.git
cp -r rankmath-seo-wp ~/.claude/skills/rankmath-seo-wp
```

| Platform | Key | Strategy | Default path |
|---|---|---|---|
| Claude Code | `claude-code` | full | `.claude/skills/rankmath-seo-wp/SKILL.md` |
| Claude.ai (web) | `claude-ai` | zip-upload | `./rankmath-seo-wp.zip` → Settings → Skills |
| Cursor | `cursor` | rule | `.cursor/rules/rankmath-seo-wp.mdc` |
| OpenAI Codex CLI | `codex-cli` | full | `.codex/skills/rankmath-seo-wp/SKILL.md` |
| Gemini CLI | `gemini-cli` | full | `.gemini/skills/rankmath-seo-wp/SKILL.md` |
| Devin Desktop (formerly Windsurf) | `windsurf` | rule | `.devin/rules/rankmath-seo-wp.md` |
| GitHub Copilot | `copilot` | full | `.github/skills/rankmath-seo-wp/SKILL.md` |
| Continue | `continue` | rule | `.continue/rules/rankmath-seo-wp.md` |

## Quick start

### Step 2: Check an article

```bash
npx -p rankmath-seo-wp@1.2.0 rankmath-verify examples/sample-article.html "Claude Skills"
```

```
FK density:      1.96%
                 OK full score band 1.0-2.5% (6/6; KB recommends 1.0-1.5%)
...
=== Result: 8 passed, 0 failed ===
```

### Step 3: Ask the assistant

| You say | What happens |
|---|---|
| "Write a WordPress tutorial about Claude Code hooks, focus keyword 'Claude Code Hooks'." | Writes the article, then runs the verifier |
| "This post's FAQ block says it contains invalid content. Fix it." | Rebuilds the FAQ HTML from the block's JSON |
| "What keyword density gets full points in Rank Math?" | Looks it up in `data/` and quotes the plugin rule |

| CLI | Does |
|---|---|
| `rankmath-verify article.html "FK"` | Score the article; exit 0 when all checks pass |
| `rankmath-export article.html` | Copy paste-ready blocks (`--only faq`, `--to-file`, `--print`) |
| `rankmath-install <platform>` | Install into an AI tool (`--list`, `--info`, `--global`) |
| `python scripts/search.py "<words>"` | Look up a Rank Math rule, block markup or site rule |
| `python tools/regenerate-faq.py <file or post IDs>` | Rebuild FAQ HTML from its JSON (`--dry` to preview) |
| `python tools/fix-howto-block.py <file or post IDs>` | Convert old HowTo markup (`--dry` to preview) |

Full output, every option and the article skeleton: [docs/guide.md](docs/guide.md).

## Trigger phrases

English: write a WordPress article, blog post or tutorial, Rank Math score, SEO green light, focus keyword density, FAQ block, HowTo block, block contains invalid content, publish with WP-CLI.

中文：寫 WordPress 文章、部落格文章、教學文、Rank Math 分數、SEO 綠燈、焦點關鍵字密度、FAQ 區塊、HowTo 區塊、區塊無效內容、WP-CLI 發文。

## What it runs and connects to

Nothing runs on its own: the plugin has no hooks, no MCP servers and no background processes. Tools run only when Claude follows `SKILL.md` and you approve the command.

| Tool | Reads | Writes | Connects to |
|---|---|---|---|
| `scripts/search.py`, `tools/verify-article.*`, self-test, number check | Files in this folder, the article you name | Nothing | Nothing |
| `rankmath-export` | The article | Your clipboard (`clip`, `pbcopy`, `xclip`, `xsel` or `wl-copy`) or the file you name | Nothing |
| `rankmath-install` | This folder | The AI tool's skill or rule folder (project, or home folder with `--global`), or a zip | Nothing |
| `regenerate-faq`, `fix-howto-block` with a local `.html` | That file | That file | Nothing |
| `regenerate-faq`, `fix-howto-block` with post IDs | The post, via `wp post get` | The post, via `wp post update` (keeps its date); a temp file in the server's `/tmp`, left there | Your server, over `ssh` |
| Publishing (Claude runs WP-CLI when you ask) | Your WordPress | The post, its Rank Math fields (`rank_math_focus_keyword`, `rank_math_title`, `rank_math_description`), categories, slug, featured image | Your server, over `ssh` |

| Setting | Environment variable | `userConfig` key | Example |
|---|---|---|---|
| SSH user and host | `WP_SSH_HOST` | `wp_ssh_host` | `user@your-wp-host.example.com` |
| SSH private key path | `WP_SSH_KEY` | `wp_ssh_key` | `~/.ssh/id_rsa` (used when unset) |
| WordPress path on the server | `WP_PATH` | `wp_path` | `/path/to/wordpress` |

Installed as a plugin, Claude Code asks for these as `userConfig` values; export them under the variable names for a tool run. The key never leaves your machine; `ssh` uses it to log in. No WordPress password or API key is needed, nothing is downloaded at install time, and no data is sent to the author or anyone else.

## How it's verified

| Check | Result | Evidence |
|---|---|---|
| Rank Math rules | Read from seo-by-rank-math 1.0.282 (`analyzer.js`, HowTo / FAQ `save()` and `block.json`), checked against the [Rank Math KB](https://rankmath.com/kb/score-100-in-tests/) on 2026-11-15 | `data/rankmath-tests.csv`, `data/blocks.csv` |
| Site conventions | Marked as site style, never as Rank Math rules | `data/site-rules.csv` |
| Word counter | Same result as the `@wordpress/wordcount` package on every file compared | `scripts/test_verify.py` |
| Self-test | 30 offline tests: Python and Node verifiers agree, the checks fail on broken articles, thresholds match the data | `python scripts/test_verify.py` |
| Evals | 11 questions; with the skill 11/11, without it 0/11 | [evals/RESULTS.md](evals/RESULTS.md) |
| Numbers in docs | Every number in `SKILL.md` and these READMEs matches the data | `python scripts/check_numbers.py` |

## Limits

| Limit | Details |
|---|---|
| Rank Math version | Rules come from Rank Math 1.0.282 (free plugin); Pro-only tests and later versions need a re-read |
| What the verifier sees | The article HTML only; check the SEO title, meta description, slug, links and images in the Rank Math sidebar |
| Live comparison | The verifier's numbers have not yet been compared with a live Rank Math sidebar |
| Platform paths | Install paths for the other AI tools are not re-checked against current docs ([data/platforms.csv](data/platforms.csv)) |
| Open questions | [data/pending.csv](data/pending.csv) |

## Repo layout

```
SKILL.md          what the assistant loads: sources, routing, tasks, verify
data/             Rank Math tests, block markup, site rules (CSV), pending list
references/       block formats, checklist, style, WP-CLI pitfalls
scripts/          search.py (entry point), self-test, number check
tools/            verify, export, install, FAQ / HowTo fixers (Python + Node)
examples/         a sample article that passes the verifier
evals/            graded questions and results
docs/             the long guide
.claude-plugin/   plugin and marketplace manifests
```

## License & author

MIT License. Made by Moksa ([moksaweb.com](https://moksaweb.com)). Issues: [GitHub](https://github.com/Moksa1123/rankmath-seo-wp/issues).
