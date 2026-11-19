# Rank Math SEO Checklist (what the plugin actually scores)

> Directory edition: commands that mention `tools/` or `scripts/` need the full edition (`npm` package `rankmath-seo-wp`); this folder ships reference files only.
> The `wp` commands below run on your WordPress server; how you connect to the server is up to you.

Every number here is a row in `data/rankmath-tests.csv`, taken from the
plugin source (seo-by-rank-math 1.0.282, `assets/admin/js/analyzer.js`) and
the KB page <https://rankmath.com/kb/score-100-in-tests/>. Look a rule up with
`python scripts/search.py "<words>"` instead of trusting memory.

## How the score is computed

- Each applicable test has a max score; the overall score is
  `round(sum(points) / sum(max points) × 100)` (`refreshScore`).
- Colour: **> 80 green**, > 50 orange, otherwise red (`getScoreClass`).
- Tests that do not apply (e.g. sentiment on non-English sites, power words on
  locales without a list) drop out of both sums.
- There is **no** HowTo/FAQ schema test, no SEO-title-length test and no
  meta-description-length test in the content analysis. Earlier versions of
  this file listed "5 pts" for each; those rows were invented and are gone.

## Tests and points

| Test (id) | Rule | Points |
|---|---|---|
| FK in SEO title (`keywordInTitle`) | primary FK appears in SEO title | 38 (36 on en sites) |
| FK in meta description (`keywordInMetaDescription`) | FK appears in description; KB: keep it within the first 120–160 chars | 2 |
| FK in URL (`keywordInPermalink`) | slugified FK inside the slug | 5 |
| FK at beginning (`keywordIn10Percent`) | FK in first 10% of words (whole text if ≤ 400 words) | 3 |
| FK in content (`keywordInContent`) | FK appears in content | 3 |
| Content length (`lengthContent`) | wp.wordcount words: 2500+ → 8, 2000+ → 5, 1500+ → 4, 1000+ → 3, 600+ → 2, else 0 | 8 |
| FK in subheading (`keywordInSubheadings`) | FK inside any H2–H6 | 3 |
| FK in image alt (`keywordInImageAlt`) | featured image alt or any `<img alt>` | 2 |
| Keyword density (`keywordDensity`) | < 0.5 → 0; 0.5–0.75 → 2; 0.76–1 → 3; up to 2.5 → 6; > 2.5 → 0 | 6 |
| URL length (`lengthPermalink`) | ≤ 75 characters | 4 |
| External link (`linksHasExternals`) | ≥ 1 external link | 4 |
| External dofollow (`linksNotAllExternals`) | ≥ 1 external link without nofollow | 2 |
| Internal link (`linksHasInternal`) | ≥ 1 internal link | 5 |
| Content AI (`hasContentAI`) | only when Content AI data exists | 5 |
| FK near start of title (`titleStartWithKeyword`) | FK starts before the middle of the title | 3 |
| Sentiment (`titleSentiment`) | English sites only | 1 |
| Power word (`titleHasPowerWords`) | title word from the locale's list; **no zh list exists**, so skipped on zh sites | 1 |
| Number in title (`titleHasNumber`) | title matches `\d+` | 1 |
| Table of contents (`contentHasTOC`) | TOC plugin or `wp-block-rank-math-toc-block` | 2 |
| Short paragraphs (`contentHasShortParagraphs`) | no paragraph over 120 words | 3 |
| Media (`contentHasAssets`) | images (featured counts): 1→1, 2→2, 3→4, 4+→6; videos: 1→1, 2+→2; max 6 | 6 |

## Two density numbers, one source each

- **Plugin scoring** (`官方原始碼`): full 6/6 from 1.0% up to 2.5%. The
  verifier gates on this.
- **KB advice** (`官方文件`): "between 1% and 1.5%". Aim here when writing;
  the verifier prints a note when an article is in 1.5–2.5%.
- Density = matches of all focus keywords (case-insensitive) ÷
  `wp.wordcount` words × 100. HTML comments (block JSON) are removed first.
- `wp.wordcount` counts whitespace-separated tokens, so a run of Chinese
  without spaces is **one** word. Chinese articles show far lower word counts
  than their character counts.

## The author's site conventions (站內風格, not Rank Math rules)

See `data/site-rules.csv`. The main ones: 12 H2s with the FK in 5, 1400+
words, 8 FAQ questions, 4 HowTo steps, 3 YouTube embeds, 5 external links,
meta description starting with the FK, `[FK] 完整教學：[digit] …` SEO title.

## Meta fields setup (WP-CLI commands)

After creating post, run these to set Rank Math fields:

```bash
POST_ID=8730  # Replace with actual

# Required fields
wp post meta update $POST_ID rank_math_focus_keyword 'Claude Skills'
wp post meta update $POST_ID rank_math_title 'Claude Skills 完整教學：3 層架構 + SKILL.md'
wp post meta update $POST_ID rank_math_description 'Claude Skills 完整教學：Pre-built / Custom / Workspace 三層架構、SKILL.md 格式、Progressive Disclosure 機制與 Open Standard 跨平台。'

# Slug
wp post update $POST_ID --post_name='claude-skills'

# Categories (parent + subcategory)
wp post term set $POST_ID category claude-code claude-ai-features

# Featured image (after importing media)
wp post meta update $POST_ID _thumbnail_id $ATTACH_ID
```

## Common pitfalls that hurt score

| Issue | Symptom | Fix |
|-------|---------|-----|
| FK density > 2.5% | "Keyword Density is X which is high" (0/6) | Replace some FK with pronouns 它/這個工具 |
| FK density < 0.5% | "which is low" (0/6) | Add FK to H2 headings or section openings |
| No digit in SEO title | "Your SEO title doesn't contain a number" | Add 4 步驟 / 5 種 / 6 大功能 etc. |
| No FK in subheading | loses 3 points | Put the FK in one H2 |
| Fewer than 600 words | content length 0/8 | Remember Chinese runs count as one word each |
| Inline `<script>` | renders as visible text on the author's site (推論, see pending) | Use rank-math blocks instead |

## Verification before publish

Run `python tools/verify-article.py article.html "Focus Keyword"`. Pass
criterion: `=== Result: 8 passed, 0 failed ===` and exit code 0. The
verifier covers word count, density, heading balance, FK in first 10%, FK in
H2, HowTo/FAQ HTML vs the block's `save()`, and forbidden patterns. Title,
description, slug, links, images and media are set in WordPress and are not
in the HTML file: check them in the Rank Math sidebar after pasting.
