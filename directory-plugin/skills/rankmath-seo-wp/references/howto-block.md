# Rank Math HowTo Block — Canonical Format

> Directory edition: commands that mention `tools/` or `scripts/` need the full edition (`npm` package `rankmath-seo-wp`); this folder ships reference files only.

The `wp:rank-math/howto-block` Gutenberg block is highly format-sensitive.
Wrong format triggers "區塊包含未預期或無效的內容" (Block contains unexpected
or invalid content) error in editor. Below is the canonical format proven
working on the author's site (reference post 8594).

## Canonical format

```html
<!-- wp:rank-math/howto-block {"steps":[{"id":"step-1","visible":true,"title":"STEP_1_TITLE","content":"STEP_1_CONTENT"},{"id":"step-2","visible":true,"title":"STEP_2_TITLE","content":"STEP_2_CONTENT"},{"id":"step-3","visible":true,"title":"STEP_3_TITLE","content":"STEP_3_CONTENT"},{"id":"step-4","visible":true,"title":"STEP_4_TITLE","content":"STEP_4_CONTENT"}],"sizeSlug":"large"} -->
<div class="wp-block-rank-math-howto-block"><div class="rank-math-howto-step"><h3 class="rank-math-howto-title">STEP_1_TITLE</h3><div class="rank-math-howto-content">STEP_1_CONTENT</div></div><div class="rank-math-howto-step"><h3 class="rank-math-howto-title">STEP_2_TITLE</h3><div class="rank-math-howto-content">STEP_2_CONTENT</div></div><div class="rank-math-howto-step"><h3 class="rank-math-howto-title">STEP_3_TITLE</h3><div class="rank-math-howto-content">STEP_3_CONTENT</div></div><div class="rank-math-howto-step"><h3 class="rank-math-howto-title">STEP_4_TITLE</h3><div class="rank-math-howto-content">STEP_4_CONTENT</div></div></div>
<!-- /wp:rank-math/howto-block -->
```

## What makes the block valid (官方原始碼)

The editor re-runs the block's `save()` on the JSON and compares the result
with the saved HTML. Any difference shows "區塊包含未預期或無效的內容".
`save()` (seo-by-rank-math 1.0.282, `blocks/howto/assets/js/index.js`) writes:

- `<div class="wp-block-rank-math-howto-block">` (plus `className` if set)
- one `<div class="rank-math-howto-step">` per step whose `visible` is not false
- inside it `<{titleWrapper} class="rank-math-howto-title">` (titleWrapper
  defaults to `h3`; omitted when the title is empty) and
  `<div class="rank-math-howto-content">` (omitted when content is empty)
- nothing else: no outer title, no wrapper around the steps

So the HTML title/content must be the exact JSON strings, and the heading tag
must equal `titleWrapper`. `hasDuration`, `days`, `hours`, `minutes`,
`titleWrapper`, `description` and `sizeSlug` are all real block attributes
(`block.json`); `save()` ignores them, so they **do not** break validation.
Only one HowTo block per post (`supports.multiple: false`). The front end is
rendered separately by PHP (`render_callback`), so the saved HTML only matters
to the editor. Row by row: `python scripts/search.py "howto" --domain blocks`.

## The author's site canonical form (站內風格, post 8594)

JSON with only `steps` + `sizeSlug: "large"`, no duration fields, no
`titleWrapper`. This keeps every article identical; it is not a Rank Math
requirement (plugin default `sizeSlug` is `"full"`). `verify-article`
reports deviations as "Site style (post 8594)" issues.

## Common BROKEN formats (avoid)

### Broken Format 1: Old version with extra JSON fields + wrapper

```html
<!-- wp:rank-math/howto-block {"hasDuration":false,"days":"","hours":"","minutes":"","hasTotalTime":false,"timeDays":"","timeHours":"","timeMinutes":"","sizeSlug":"large","steps":[...]} -->
<div class="wp-block-rank-math-howto-block">
  <h3 class="rank-math-howto-title">外層大標題</h3>
  <div class="rank-math-howto-steps">
    <div class="rank-math-howto-step">
      <h4 class="rank-math-howto-step-title">步驟 1</h4>
      <div class="rank-math-howto-step-content">內容</div>
    </div>
  </div>
</div>
```

Problems:
1. JSON has `hasDuration` etc — valid attributes, but not the site form (site style)
2. Outer `<h3 class="rank-math-howto-title">` outside step div
3. `<div class="rank-math-howto-steps">` wrapper (extra layer)
4. `<h4 class="rank-math-howto-step-title">` — wrong class name AND h4 not h3
5. `<div class="rank-math-howto-step-content">` — wrong class name

### Broken Format 2: half-fixed format (h4 inside step)

```html
<!-- wp:rank-math/howto-block {"steps":[...],"sizeSlug":"large"} -->
<div class="wp-block-rank-math-howto-block">
  <div class="rank-math-howto-step">
    <h4 class="rank-math-howto-title">步驟 1</h4>
    <div class="rank-math-howto-content">內容</div>
  </div>
</div>
```

Problem: `<h4>` should be `<h3>`. JSON is OK, container is OK, but heading
level wrong. Found in many pre-canonical-fix articles.

## Step content rules

- 4 steps (站內風格; Rank Math has no step-count rule)
- Step title: 2-5 words English, action-oriented (Verb + Object)
  - ✅ "Verify Excel version"
  - ✅ "Install from Marketplace"
  - ❌ "First you need to check that..."
- Step content: 1-3 sentences mixed Chinese-English
  - Tell user exactly what to do, what to look for, what config to set
  - Avoid metaphors, be concrete
- Place HowTo block under H2 #4 (which contains FK in heading)
- H2 heading should be like "[FK] 4 步驟啟用設定" (NOT "HowTo Schema")

## H2 heading rules around HowTo block

**Forbidden**: H2 saying "HowTo Schema" (this is an SEO term, not user-facing label)
- ❌ "4. Claude for Excel 設定步驟 HowTo Schema"
- ❌ "4. Claude Skills 安裝 HowTo Schema"

**Correct**: Plain action description
- ✅ "4. Claude for Excel 4 步驟安裝設定"
- ✅ "4. Claude Skills 4 步驟使用內建 Skills"
- ✅ "4. Claude Voice Mode 4 步驟啟用設定"

## CRITICAL: Do not use inline `<script>` for HowTo schema

Many themes (including the author's site) strip inline `<script>` tags or escape
their angle brackets, causing the JSON-LD to render as visible raw text.

**Don't do this**:
```html
<!-- wp:html -->
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HowTo",...}
</script>
<!-- /wp:html -->
```

The proper `wp:rank-math/howto-block` Gutenberg block emits the schema markup
correctly through Rank Math's own renderer — no inline script needed.

## Validation

After publishing, open the post in Gutenberg editor. If you see:
- "區塊包含未預期或無效的內容" (Block contains unexpected/invalid content)
- "嘗試復原" (Try to recover) button

The HowTo block format is wrong. Fix using `tools/fix-howto-block.py` or
manually rewrite to canonical format above.

## Verifier

`python tools/verify-article.py article.html "FK"` rebuilds the `save()`
output from the JSON and compares it with the HTML (entities decoded,
whitespace between tags ignored). It also lists site-style deviations.
`tools/fix-howto-block.py` converts old formats to the site form.
