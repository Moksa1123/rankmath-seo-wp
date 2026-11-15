---
name: rankmath-seo-wp
description: |
  Write Rank Math SEO-compliant WordPress articles in Traditional Chinese (or any
  language) that pass the Rank Math scoring tests. Use this skill when user asks
  to write WP articles, blog posts, tutorials, product guides, or content that
  will publish to a WordPress site running Rank Math SEO plugin. Outputs
  Gutenberg-block formatted HTML with correct rank-math/howto-block and
  rank-math/faq-block markup, focus keyword density 1.0-1.5%, 12 H2 structure,
  Moksa-style natural quote, no inline script tags, and SEO Title containing a
  digit. Includes deployment helpers for WP-CLI publishing.
  中文觸發：寫 WordPress 文章、部落格文章、教學文、Rank Math 分數、SEO 綠燈、
  焦點關鍵字密度、FAQ 區塊、HowTo 區塊、區塊無效內容、WP-CLI 發文。
author: moksa (https://moksaweb.com)
license: MIT
version: 1.1.1
user-invocable: true
---

# Rank Math SEO WP Writing Skill

## Sources

- **Rank Math rules** come from the plugin source, not memory:
  seo-by-rank-math (version in `python scripts/search.py stats`),
  `assets/admin/js/analyzer.js` (every content test, its points and
  thresholds) and `includes/modules/schema/blocks/*` (HowTo/FAQ `save()` and
  `block.json`), cross-checked with the KB page
  <https://rankmath.com/kb/score-100-in-tests/>. Checked 2026-11-15.
- **Word counting** is a port of `@wordpress/wordcount` (the counter Rank Math
  calls); the port matched the npm package on every file tried.
- **moksaweb.com conventions** (12 H2s, 8 FAQs, 3 YouTube, 5 links, Moksa
  quote, image spec) come from 30+ published articles and are labelled
  站內風格 (site style). They are not Rank Math requirements.
- Row counts per data file: `python scripts/search.py stats`. Every CSV row has
  `source` and `trust`: 官方原始碼 (plugin source) > 官方文件 (KB) > 實測
  (measured) > 站內風格 (site style) > 推論 (inferred, never state as fact).

**Maintainer:** moksa · [moksaweb.com](https://moksaweb.com) · License: MIT

## Usage

Use when the user asks to:
- write a WordPress article / blog post / tutorial for a site running Rank Math
- fix an article's Rank Math score, density, or broken HowTo/FAQ blocks
- publish via WP-CLI or block-paste into Gutenberg

Do NOT use for (hand off instead):
- general Gutenberg page building, other blocks → `gutenberg-headless`
- Elementor / Mosaic pages → `elementor-headless` / `mosaic-headless`
- moksaweb.com host details, category IDs, private deploy → `moksa-wp-publish`
- sites with Yoast or another SEO plugin (different tests)

**Single entry point:** `python scripts/search.py "<question>"` — look the rule
up first; then write; then `tools/verify-article.py`.

| Tool | Who runs it | Purpose |
|---|---|---|
| `scripts/search.py` | user / agent | look up tests, block markup, site rules (zh or en) |
| `tools/verify-article.py` / `.mjs` | user / agent | gate an article before publishing |
| `tools/export-blocks.py` / `.mjs` | user / agent | copy paste-ready blocks to clipboard / file |
| `tools/regenerate-faq.py` / `.mjs` | user / agent | rebuild FAQ HTML from its JSON (also batch via WP-CLI) |
| `tools/fix-howto-block.py` / `.mjs` | user / agent | convert old HowTo markup to the site form |
| `tools/install-skill.py` / `.mjs` | user | install the skill into Claude Code / Cursor / Codex / … |
| `scripts/test_verify.py` | maintainer | self-test (verifier, search, data, twins) |
| `scripts/check_numbers.py` | maintainer | every number in this file is registered and true |
| `evals/grade.py` | maintainer | with/without-skill accuracy |

All of these use only the Python standard library / Node 18 built-ins.

## Routing

**Iron rule: look it up first, never answer from memory.** Rank Math
thresholds, block markup and point values are in `data/`; run
`scripts/search.py` before stating one. If nothing is found, say so, mark it
待補 (pending), add a row to `data/pending.csv`, and do not guess. Never
present a 站內風格 or 推論 row as a Rank Math rule.

| The user says | Data | Command |
|---|---|---|
| 密度多少才及格 / keyword density | `rankmath-tests.csv`, `focus-keyword-density.csv` | `search.py "密度"` |
| 要寫幾個字 / word count | `rankmath-tests.csv` (lengthContent) | `search.py "字數"` |
| 怎樣才綠燈 / score, points | `rankmath-tests.csv` (overallScore, scoreColor) | `search.py "總分 綠燈"` |
| 標題要放數字嗎 / title rules | `rankmath-tests.csv` (title* rows) | `search.py "標題 數字"` |
| 強力字 / power words | `power-words.csv` | `search.py "強力字" --domain power` |
| FAQ 區塊怎麼寫 / faq markup | `blocks.csv`, `references/faq-block.md` | `search.py "常見問題" --domain blocks` |
| HowTo 區塊壞掉 / invalid content | `blocks.csv`, `references/howto-block.md` | `search.py "區塊壞掉"` |
| 圖片影片要幾個 / media | `rankmath-tests.csv` (contentHasAssets) | `search.py "影片 圖片"` |
| 文章架構 / 12 H2 | `h2-templates.csv`, `site-rules.csv` | `search.py "小標" --domain h2` |
| FAQ 題目怎麼出 | `faq-topics.csv` | `search.py "faq" --domain faq` |
| Moksa 引言怎麼寫 | `references/moksa-style.md` | `search.py "引言" --domain refs` |
| 特色圖規格 | `references/image-specs.md` | `search.py "特色圖"` |
| WP-CLI 發文出錯 | `references/wp-cli-pitfalls.md` | `search.py "發布" --domain refs` |
| 裝到 Cursor / Codex | `platforms.csv` | `search.py "cursor" --domain platforms` |
| 還沒查清楚的 | `pending.csv` | `search.py all --domain pending` |

Chinese phrases are expanded through `data/terms-zh.csv`; add a row there
when a common phrase finds nothing.

## Tasks

### Write a new article (block-paste, no SSH)

1. **Plan.** Pick the FK; outline from `data/h2-templates.csv` (12 H2, FK in
   1/2/4/6/10, site style). Evidence: outline lists 12 H2s.
2. **Write.** Follow `references/article-template.md`; Moksa quote per
   `references/moksa-style.md`; HowTo under H2 #4 and FAQ under H2 #12 using
   the markup in `data/blocks.csv`. Write mixed Chinese/English with spaces:
   `wp.wordcount` counts an unbroken Chinese run as one word.
3. **Verify.** `python tools/verify-article.py article.html "FK"`.
   Evidence: `8 passed, 0 failed`, exit 0.
4. **Export.** `python tools/export-blocks.py article.html` → clipboard.
5. **Paste** into Posts → Add New; set FK, SEO title (with a digit, FK in the
   first half), description (with FK), slug (≤ 75 chars, with FK) in the Rank
   Math sidebar; upload the featured image with the FK in its alt.
   Evidence: no "invalid content" warning on the HowTo/FAQ blocks; Rank Math
   score shown in the sidebar (green above 80).

### Publish with WP-CLI (server access)

Steps 1-3 as above, then `wp post create file.html` (file argument, not
`--post_content="$(cat …)"`; write the file with LF), `wp post meta update` for
`rank_math_focus_keyword` / `rank_math_title` / `rank_math_description`, import
the image, then re-run the verifier on `wp post get <id> --field=post_content`.
Evidence: verifier passes on the live content. Details:
`references/wp-cli-pitfalls.md`; env vars `WP_SSH_KEY` / `WP_SSH_HOST` /
`WP_PATH` for the batch tools.

### Fix an existing article

| Symptom | Look up | Fix |
|---|---|---|
| Density too high / low | `search.py "密度"` | pronouns (它 / 這個工具) in H2/FAQ titles, or restore FK |
| HowTo "invalid content" | `search.py "howto" --domain blocks` | `tools/fix-howto-block.py`, then verify |
| FAQ "invalid content" | `search.py "faq" --domain blocks` | `tools/regenerate-faq.py`, then verify |
| "SEO title doesn't contain a number" | `search.py "標題 數字"` | add a digit: 4 步驟 / 6 大功能 |
| JSON-LD shows as text | `search.py "ld+json"` | delete the `wp:html` script; use the rank-math blocks |
| "HowTo Schema" in an H2 | `search.py "schema"` | plain wording: "X 4 步驟安裝設定" |

## Verify

| Output | Validator | Pass criterion |
|---|---|---|
| Article HTML | `python tools/verify-article.py article.html "FK"` (or `node tools/verify-article.mjs`) | `=== Result: 8 passed, 0 failed ===`, exit 0 |
| Published post | same verifier on `wp post get <id> --field=post_content` | same |
| Sidebar fields (title, description, slug, links, images) | Rank Math sidebar after paste | each test green; score above 80 |

What the verifier gates (thresholds are rows in `data/rankmath-tests.csv`):
- word count ≥ 600 (`lengthContent` lowest scoring tier) — prints the tier points
- density in the plugin's full-score band 1.0–2.5% (`keywordDensity`); prints a
  note when above the KB's recommended 1–1.5%
- FK in the first 10% of words (`keywordIn10Percent`) and in at least 1 H2
- HowTo / FAQ HTML equals the block's `save()` output from its JSON; site-style
  deviations (post 8594 form) are listed as "Site style" issues and also fail
- no "HowTo Schema" in H2, no inline `application/ld+json`
- headings balanced (12 is the site target; any balanced count passes)

Any failure exits non-zero (1); usage errors exit 1, unreadable files 2.
`examples/sample-article.html` passes:
`python tools/verify-article.py examples/sample-article.html "Claude Skills"`.

## Maintenance

- Self-test (offline, no network): `python scripts/test_verify.py`; the latest
  pass count is written by the test run, not here.
- Numbers in this file: `python scripts/check_numbers.py` (exit 1 on any
  unregistered or wrong number).
- Evals: `python evals/grade.py --questions`, answer with and without the
  skill, then `python evals/grade.py --with … --without … --write`; results in
  `evals/RESULTS.md`.
- After a Rank Math release: download the plugin from wordpress.org, re-read
  each test class in `analyzer.js` and both blocks' `save()` / `block.json`,
  update `data/rankmath-tests.csv` / `data/blocks.csv` (version in the
  `source` column), the constants at the top of both verifiers, then re-run
  the self-test.
- Open questions live in `data/pending.csv`.
- Install copy: copy the repo files over `~/.claude/skills/rankmath-seo-wp`
  (do not delete files that exist only there).

## Open Standard

This skill follows the [Anthropic Agent Skills spec](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).
Format-compatible with Claude Code, Claude.ai, Cursor, Codex CLI, Gemini CLI,
GitHub Copilot, and Devin Desktop (formerly Windsurf). Install with
`python tools/install-skill.py <platform>` (`--list`, `--info <platform>`,
`--global`); paths per platform in `data/platforms.csv` (marked 推論 until
re-checked).

## Adapting to other niches

- Replace `Moksa 觀點` with your brand's opening device
- Replace the 12 H2 template (`data/h2-templates.csv`) with your structure
- Keep density inside the plugin's scoring band; aim for the KB advice
- Update the image template path in `references/image-specs.md`
- Update WP host placeholders in `references/wp-cli-pitfalls.md`
