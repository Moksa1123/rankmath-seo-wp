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
  digit. Directory edition: reference data and checklists only; the verifier
  and tools ship in the full npm package rankmath-seo-wp.
  中文觸發：寫 WordPress 文章、部落格文章、教學文、Rank Math 分數、SEO 綠燈、
  焦點關鍵字密度、FAQ 區塊、HowTo 區塊、區塊無效內容。
author: Moksa
license: MIT
version: 1.2.2
user-invocable: true
---

# Rank Math SEO WP Writing Skill (directory edition)

This is the reference-only edition built for the Claude plugin directory: the
rules, block markup and checklists, with no scripts. The full edition adds the
verifier, the clipboard exporter, the FAQ / HowTo fixers and WP-CLI helpers:
`npx -p rankmath-seo-wp@1.2.2 rankmath-install claude-code --global`
or <https://github.com/Moksa1123/rankmath-seo-wp>.

## Sources

- **Rank Math rules** come from the plugin source, not memory:
  seo-by-rank-math 1.0.282, `assets/admin/js/analyzer.js` (every content
  test, its points and thresholds) and `includes/modules/schema/blocks/*`
  (HowTo/FAQ `save()` and `block.json`), cross-checked with the KB page
  <https://rankmath.com/kb/score-100-in-tests/>. Checked 2026-11-15.
- **Site conventions** (12 H2s, 8 FAQs, 3 YouTube, 5 links, opening quote,
  image spec) come from the author's published articles and are labelled
  站內風格 (site style). They are not Rank Math requirements.
- Every row in `data/*.json` has `source` and `trust`: 官方原始碼 (plugin
  source) > 官方文件 (KB) > 實測 (measured) > 站內風格 (site style) > 推論
  (inferred, never state as fact).

| Data file | Rows | What |
|---|---|---|
| `data/rankmath-tests.json` | 25 | Rank Math tests and score rules (plugin source) |
| `data/blocks.json` | 16 | HowTo / FAQ block markup from save() and block.json |
| `data/focus-keyword-density.json` | 7 | density bands and their points |
| `data/site-rules.json` | 18 | the author's conventions (site style) |
| `data/h2-templates.json` | 12 | 12-H2 article skeleton |
| `data/faq-topics.json` | 8 | FAQ question patterns |
| `data/power-words.json` | 19 | title power words, and whether Rank Math counts them |
| `data/terms-zh.json` | 55 | Chinese phrases mapped to English terms |
| `data/pending.json` | 5 | open questions not yet answered |

## Usage

Use when the user asks to write, fix or publish a WordPress article for a site
running Rank Math SEO, or asks about Rank Math scoring, HowTo / FAQ block
markup, or why a block shows "invalid content".

Do NOT use for: other block-editor pages, Elementor or Mosaic pages, or sites
using Yoast or another SEO plugin (different tests).

**Entry point:** read the matching file in `data/` (JSON) or `references/`
before answering. This edition runs nothing; it only reads files.

## Routing

**Iron rule: look it up first, never answer from memory.** Rank Math
thresholds, block markup and point values are in `data/`. If nothing is found,
say so, mark it 待補 (pending) and do not guess. Never present a 站內風格 or
推論 row as a Rank Math rule. Open questions are in `data/pending.json`.

| The user says | Read |
|---|---|
| 密度多少才及格 / keyword density | `data/rankmath-tests.json` (keywordDensity), `data/focus-keyword-density.json` |
| 要寫幾個字 / word count | `data/rankmath-tests.json` (lengthContent) |
| 怎樣才綠燈 / score, points | `data/rankmath-tests.json` (overallScore, scoreColor) |
| 標題要放數字嗎 / title rules | `data/rankmath-tests.json` (title* rows) |
| 強力字 / power words | `data/power-words.json` |
| FAQ / HowTo 區塊怎麼寫, invalid content | `data/blocks.json`, `references/faq-block.md`, `references/howto-block.md` |
| 圖片影片要幾個 / media | `data/rankmath-tests.json` (contentHasAssets) |
| 文章架構 / 12 H2 | `data/h2-templates.json`, `data/site-rules.json`, `references/article-template.md` |
| FAQ 題目怎麼出 | `data/faq-topics.json` |
| 引言怎麼寫 | `references/moksa-style.md` |
| 特色圖規格 | `references/image-specs.md` |
| WP-CLI 發文出錯 | `references/wp-cli-pitfalls.md` |
| 中文說法對不到英文術語 | `data/terms-zh.json` |

## Tasks

### Write a new article

1. **Plan.** Pick the focus keyword (FK); outline from `data/h2-templates.json`.
2. **Write.** Follow `references/article-template.md`; put the HowTo block under
   H2 #4 and the FAQ block under H2 #12 using the markup in `data/blocks.json`.
   Write mixed Chinese/English with spaces: Rank Math's word counter
   (`wp.wordcount`) counts an unbroken run of Chinese as one word.
3. **Check.** Go through the checklist in Verify, item by item, and say which
   items you could not check.
4. **Hand over.** Give the user the block HTML to paste into the block editor,
   plus the SEO title, description and slug to set in the Rank Math sidebar.

### Fix an existing article

| Symptom | Read | Fix |
|---|---|---|
| Density too high / low | `data/focus-keyword-density.json` | pronouns (它 / 這個工具) in H2/FAQ titles, or restore FK |
| HowTo or FAQ "invalid content" | `data/blocks.json` | rewrite the HTML so it equals what the block's `save()` writes from its JSON |
| "SEO title doesn't contain a number" | `data/rankmath-tests.json` (titleHasNumber) | add a digit: 4 步驟 / 6 大功能 |
| JSON-LD shows as text | `data/site-rules.json` (no_inline_ldjson) | remove the `wp:html` script; use the rank-math blocks |

## Verify

This edition has no verifier. Check by hand, and tell the user that the full
edition's `rankmath-verify` counts words and density exactly as Rank Math does.

Rank Math tests (plugin source, seo-by-rank-math 1.0.282):

| Test | Rule | Points |
|---|---|---|
| `keywordInTitle` | primary focus keyword appears in SEO title (word match) | 38 (36 when site locale is en) |
| `keywordInMetaDescription` | primary focus keyword appears anywhere in SEO description; KB says keep it in the first 120-160 characters | 2 |
| `keywordInPermalink` | slugified focus keyword is a substring of the slugified URL | 5 |
| `keywordIn10Percent` | keyword in first 10% of words; whole text when the text has 400 words or fewer (KB text says 300; the code says 400) | 3 |
| `keywordInContent` | focus keyword appears in content | 3 |
| `lengthContent` | wp.wordcount words: >=2500 -> 8; >=2000 -> 5; >=1500 -> 4; >=1000 -> 3; >=600 -> 2; else 0 (test fails below 600) | 8 |
| `keywordInSubheadings` | keyword words inside any <h2>-<h6> | 3 |
| `keywordInImageAlt` | featured image alt or any <img alt> contains the keyword; a [gallery] shortcode also passes | 2 |
| `keywordDensity` | density = matches of all focus keywords / wp.wordcount words x 100 (2 decimals); <0.5 fail 0; 0.5-<0.75 fair 2; 0.76-<1 good 3; up to 2.5 best 6; >2.5 fail 0 | 6 |
| `keywordDensity_kb` | KB recommends 1-1.5% and warns above 2.5%; the plugin still gives full points up to 2.5% | 0 |
| `lengthPermalink` | URL length <= 75 characters | 4 |
| `linksHasExternals` | at least 1 external link | 4 |
| `linksNotAllExternals` | at least 1 external link without nofollow | 2 |
| `linksHasInternal` | at least 1 internal link | 5 |
| `keywordNotUsed` | focus keyword not used by another post (ajax check; no points) | 0 |
| `hasContentAI` | Content AI used on the post (only applies when Content AI data exists) | 5 |
| `titleStartWithKeyword` | keyword starts before the middle character of the SEO title | 3 |
| `titleSentiment` | English locale only: title sentiment score is not 0 | 1 |
| `titleHasPowerWords` | a title word (title split on spaces) equals a power word or starts with one and is at most 4 characters longer; list = assets/vendor/powerwords/<site language>.php (11 files: de en es fi fr hu id it ja nl sv; no zh so the test is skipped) | 1 |
| `titleHasNumber` | SEO title matches /\d+/ (Arabic digits only) | 1 |
| `contentHasTOC` | TOC plugin detected or content contains wp-block-rank-math-toc-block | 2 |
| `contentHasShortParagraphs` | fails if any paragraph has more than 120 words | 3 |
| `contentHasAssets` | images (incl. featured image and [gallery]): 1->1 2->2 3->4 4+->6; videos: 1->1 2+->2; capped at 6; a video counts only if its iframe/video/[video] URL or a bare URL is YouTube or Vimeo (self-hosted mp4 does not count) | 6 |
| `overallScore` | round(sum of points / sum of max points of applicable tests x 100) | 100 |
| `scoreColor` | >80 green; >50 orange; else red | 0 |

Block markup (from each block's `save()` and `block.json`):

| Block | Item | Rule |
|---|---|---|
| `rank-math/howto-block` | wrapper | saved HTML wrapper div (plus className if set) |
| `rank-math/howto-block` | step | one div per step whose visible is not false; no extra wrapper around steps |
| `rank-math/howto-block` | step title | title written in the titleWrapper tag (default h3); omitted when title is empty |
| `rank-math/howto-block` | step content | content div; omitted when content is empty |
| `rank-math/howto-block` | attributes | block.json attributes: hasDuration days hours minutes description steps sizeSlug(full) imageID mainSizeSlug(full) listStyle timeLabel titleWrapper(h3) listCssClasses titleCssClasses contentCssClasses textAlign(left) |
| `rank-math/howto-block` | validity | saved HTML must equal save() output from the JSON (title/content text identical); otherwise the editor shows invalid content |
| `rank-math/howto-block` | multiple | only one HowTo block per post (supports.multiple false) |
| `rank-math/howto-block` | frontend | front end is rendered by PHP render_callback (classes rank-math-steps / rank-math-step / rank-math-step-title / rank-math-step-content); saved HTML is for the editor only |
| `rank-math/faq-block` | wrapper | saved HTML wrapper div (plus className if set) |
| `rank-math/faq-block` | item | one div per question with non-empty title and content and visible not false |
| `rank-math/faq-block` | question | question in the titleWrapper tag (default h3) |
| `rank-math/faq-block` | answer | answer div |
| `rank-math/faq-block` | attributes | block.json attributes: listStyle titleWrapper(h3) sizeSlug(thumbnail) questions listCssClasses titleCssClasses contentCssClasses textAlign(left) |
| `rank-math/faq-block` | validity | saved HTML must equal save() output from the JSON; regenerate HTML from JSON with tools/regenerate-faq.py |
| `rank-math/faq-block` | frontend | front end is rendered by PHP render_callback (div#rank-math-faq .rank-math-list-item) |
| `rank-math/toc-block` | toc test | content containing wp-block-rank-math-toc-block passes contentHasTOC (2 points) |

Site style (the author's conventions, not Rank Math rules):

| Rule | What | Trust |
|---|---|---|
| `h2_count` | article uses the 12-H2 skeleton (FAQ under H2 #12) | 站內風格 |
| `h2_with_fk` | 5 of 12 H2s carry the FK (1/2/4/6/10); pronouns elsewhere to hold density | 站內風格 |
| `word_target` | aim for 1400+ wp.wordcount words (2000+ ideal); Rank Math itself passes from 600 | 站內風格 |
| `faq_count` | FAQ block has 8 questions; 4 carry the FK | 站內風格 |
| `howto_steps` | HowTo block has 4 steps under H2 #4 | 站內風格 |
| `youtube_embeds` | 3 YouTube embeds in H2 #9; Rank Math media test counts at most 2 points for videos | 站內風格 |
| `external_links` | 5 external links in H2 #11 (first link internal category page) | 站內風格 |
| `meta_desc_starts_fk` | rank_math_description starts with the FK | 站內風格 |
| `seo_title_template` | rank_math_title = [FK] 完整教學：[digit] [量詞] [補充] | 站內風格 |
| `post_title_english` | keep post_title English; Chinese goes in rank_math_title | 推論 |
| `no_inline_ldjson` | no <script type=application/ld+json> in content; the author's site theme printed it as text | 推論 |
| `no_schema_word_in_h2` | no "HowTo Schema"/"FAQ Schema" text in H2 headings | 站內風格 |
| `howto_sizeslug` | HowTo JSON sizeSlug "large" (plugin default "full"; save() ignores it) | 站內風格 |
| `howto_drop_fields` | omit hasDuration/days/hours/minutes/titleWrapper from HowTo JSON (they are valid plugin attributes; save() ignores them) | 站內風格 |
| `moksa_quote` | opening blockquote in natural conversational Chinese | 站內風格 |
| `featured_image` | 2000x2000 webp; English text; Montserrat SemiBold | 站內風格 |
| `lf_newlines` | write article files with LF on Windows (newline='\n') | 站內風格 |
| `wpcli_file_arg` | wp post update ID file.html instead of --post_content=$(cat ...) | 站內風格 |

## Maintenance

This folder is generated in the main repository
(<https://github.com/Moksa1123/rankmath-seo-wp>) from its `SKILL.md`,
`data/*.csv`, `references/*.md` and the templates in `scripts/directory/`.
Do not edit it by hand: change the sources there and rebuild; the main
repository's self-test fails when this folder and its sources differ.
