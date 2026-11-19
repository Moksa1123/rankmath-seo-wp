<h1 align="center">Rank Math SEO WP Writer</h1>

<h3 align="center">Rank Math SEO 文章撰寫工具（官方目錄精簡版）</h3>

<p align="center">
  <strong>Rank Math test rules · Valid HowTo / FAQ blocks · Pre-publish checklist</strong>
</p>

> This is an unofficial community project. It is not made by, endorsed by, or affiliated with Rank Math or its makers. Rank Math SEO is third-party software and is not included here.

This is the **directory edition** of [rankmath-seo-wp](https://github.com/Moksa1123/rankmath-seo-wp): the same Rank Math rules, block markup and article templates, packaged as reference files only so it fits the Claude plugin directory. It contains no scripts.

## What it does

| Area | What you get |
|---|---|
| Rank Math rules | 25 Rank Math tests and score rules with points, thresholds and KB links, read from the source of seo-by-rank-math 1.0.282 |
| Blocks | HowTo and FAQ markup that matches each block's `save()`, so the editor doesn't show "invalid content" |
| Checklist | A pre-publish checklist built from those tests and the block rules |
| Site style | The author's article skeleton, FAQ topics and title patterns, labelled as conventions, not Rank Math rules |

## When to use

| Use it for | Use something else for |
|---|---|
| Writing or fixing posts for a WordPress site that runs Rank Math SEO | Other block-editor pages, Elementor or Mosaic pages |
| Questions about Rank Math scoring and HowTo / FAQ block markup | Sites on Yoast or another SEO plugin |

## Install

```
/plugin install rankmath-seo-wp
```

For the full edition with the verifier, exporter and WP-CLI fixers:

```bash
npx -p rankmath-seo-wp@1.2.2 rankmath-install claude-code --global
```

## Quick start

| You say | What happens |
|---|---|
| "Write a WordPress tutorial about Claude Code hooks, focus keyword 'Claude Code Hooks'." | Writes the article from the template and checks it against the checklist |
| "This post's FAQ block says it contains invalid content. Fix it." | Rewrites the FAQ HTML to match the block's JSON |
| "What keyword density gets full points in Rank Math?" | Quotes the rule from `data/rankmath-tests.json` |

## Trigger phrases

English: write a WordPress article, blog post or tutorial, Rank Math score, SEO green light, focus keyword density, FAQ block, HowTo block, block contains invalid content.

中文：寫 WordPress 文章、部落格文章、教學文、Rank Math 分數、SEO 綠燈、焦點關鍵字密度、FAQ 區塊、HowTo 區塊、區塊無效內容。

## What it runs and connects to

| Item | This edition |
|---|---|
| Scripts, hooks, MCP servers | None |
| Files it writes | None; Claude writes the article only where you ask |
| Network | None |
| Credentials | None |

Everything here is Markdown and JSON that Claude reads. No data is sent to the author or anyone else.

## How it's verified

| Check | Result |
|---|---|
| Rank Math rules | Read from seo-by-rank-math 1.0.282, checked against the [Rank Math KB](https://rankmath.com/kb/score-100-in-tests/) on 2026-11-15 |
| This folder | Generated from the main repository's sources by `scripts/build_directory.py`; the main repository's self-test fails if they differ |

## Limits

| Limit | Details |
|---|---|
| No verifier | Word count and density are checked by hand; the full edition's `rankmath-verify` counts exactly like Rank Math |
| No publishing tools | No clipboard exporter, FAQ / HowTo fixers or WP-CLI helpers |
| Rank Math version | Rules come from Rank Math 1.0.282 (free plugin) |
| Open questions | `skills/rankmath-seo-wp/data/pending.json` |

## Repo layout

```
.claude-plugin/                 plugin manifest and icon
skills/rankmath-seo-wp/         SKILL.md, data/*.json, references/*.md
README.md, LICENSE
```

## License & author

MIT License. Made by Moksa. Issues: [GitHub](https://github.com/Moksa1123/rankmath-seo-wp/issues).
