# Rank Math HowTo Block — Canonical Format

The `wp:rank-math/howto-block` Gutenberg block is highly format-sensitive.
Wrong format triggers "區塊包含未預期或無效的內容" (Block contains unexpected
or invalid content) error in editor. Below is the canonical format proven
working on moksaweb.com (reference post 8594).

## Canonical format

```html
<!-- wp:rank-math/howto-block {"steps":[{"id":"step-1","visible":true,"title":"STEP_1_TITLE","content":"STEP_1_CONTENT"},{"id":"step-2","visible":true,"title":"STEP_2_TITLE","content":"STEP_2_CONTENT"},{"id":"step-3","visible":true,"title":"STEP_3_TITLE","content":"STEP_3_CONTENT"},{"id":"step-4","visible":true,"title":"STEP_4_TITLE","content":"STEP_4_CONTENT"}],"sizeSlug":"large"} -->
<div class="wp-block-rank-math-howto-block"><div class="rank-math-howto-step"><h3 class="rank-math-howto-title">STEP_1_TITLE</h3><div class="rank-math-howto-content">STEP_1_CONTENT</div></div><div class="rank-math-howto-step"><h3 class="rank-math-howto-title">STEP_2_TITLE</h3><div class="rank-math-howto-content">STEP_2_CONTENT</div></div><div class="rank-math-howto-step"><h3 class="rank-math-howto-title">STEP_3_TITLE</h3><div class="rank-math-howto-content">STEP_3_CONTENT</div></div><div class="rank-math-howto-step"><h3 class="rank-math-howto-title">STEP_4_TITLE</h3><div class="rank-math-howto-content">STEP_4_CONTENT</div></div></div>
<!-- /wp:rank-math/howto-block -->
```

## Required structure rules

### JSON metadata (in `<!-- wp:rank-math/howto-block ... -->` comment)

ONLY these fields:
```json
{
  "steps": [
    {"id": "step-1", "visible": true, "title": "...", "content": "..."},
    ...
  ],
  "sizeSlug": "large"
}
```

**Forbidden** (will break block validation):
- `hasDuration`, `days`, `hours`, `minutes`
- `hasTotalTime`, `timeDays`, `timeHours`, `timeMinutes`
- `titleWrapper` (FAQ has it, HowTo does not)
- Any other field beyond `steps` + `sizeSlug`

### HTML structure (between block comments)

Outermost: `<div class="wp-block-rank-math-howto-block">`
Inside: directly contain step divs (NO wrapper, NO outer h3 title)
Each step: `<div class="rank-math-howto-step">` containing:
  - `<h3 class="rank-math-howto-title">` (NOT h4, NOT step-title)
  - `<div class="rank-math-howto-content">` (NOT step-content)

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
1. JSON has `hasDuration` etc — extra fields break validation
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

- Always 4 steps (Rank Math HowTo schema preferred 4-step structure)
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

Many themes (including moksaweb.com) strip inline `<script>` tags or escape
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

## Verifier checklist

```python
content = fetch_post_content(post_id)
import re

# 1. Extract JSON
m = re.search(r'wp:rank-math/howto-block (\{.*?\}) -->', content, re.DOTALL)
if not m:
    raise ValueError("No HowTo block")

json_data = json.loads(m.group(1))

# 2. Forbidden fields check
for forbidden in ['hasDuration', 'days', 'hasTotalTime', 'titleWrapper']:
    assert forbidden not in json_data, f"Forbidden field: {forbidden}"

# 3. Required fields
assert 'steps' in json_data
assert 'sizeSlug' in json_data
assert json_data['sizeSlug'] == 'large'

# 4. HTML structure
assert '<div class="rank-math-howto-step">' in content
assert '<h3 class="rank-math-howto-title">' in content  # h3 not h4
assert '<div class="rank-math-howto-content">' in content

# 5. Forbidden HTML patterns
assert '<h4 class="rank-math-howto-step-title">' not in content
assert '<h4 class="rank-math-howto-title">' not in content
assert '<div class="rank-math-howto-steps">' not in content
assert '<div class="rank-math-howto-step-content">' not in content
```

See `tools/fix-howto-block.py` for batch fixer that converts old broken
formats to canonical format.
