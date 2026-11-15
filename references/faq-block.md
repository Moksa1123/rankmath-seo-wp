# Rank Math FAQ Block — Alignment Rules

The `wp:rank-math/faq-block` requires JSON metadata and visible HTML to align
character-by-character (after html.unescape). Mismatch triggers Gutenberg
block validation error.

## Canonical format

```html
<!-- wp:rank-math/faq-block {"questions":[{"id":"faq-1","title":"Q1?","content":"A1","visible":true},{"id":"faq-2","title":"Q2?","content":"A2","visible":true}]} -->
<div class="wp-block-rank-math-faq-block"><div class="rank-math-faq-item"><h3 class="rank-math-question">Q1?</h3><div class="rank-math-answer">A1</div></div><div class="rank-math-faq-item"><h3 class="rank-math-question">Q2?</h3><div class="rank-math-answer">A2</div></div></div>
<!-- /wp:rank-math/faq-block -->
```

## Required structure

### JSON metadata fields

```json
{
  "questions": [
    {
      "id": "faq-N",
      "title": "Question text?",
      "content": "Answer text.",
      "visible": true
    }
  ]
}
```

Optional: `"titleWrapper": "h3"` — older articles include this, newer don't.
Both work but be consistent within an article.

### HTML structure

- Outer: `<div class="wp-block-rank-math-faq-block">` (single wrapper)
- Each item: `<div class="rank-math-faq-item">` containing `<h3 class="rank-math-question">` and `<div class="rank-math-answer">`

## CRITICAL: JSON ↔ HTML alignment

For each question, after html.unescape, JSON title MUST equal HTML question
text, and JSON content MUST equal HTML answer text.

```python
import html

# JSON value
json_q1 = data['questions'][0]['title']
# HTML rendered (h3 inner text)
html_q1_text = '...'

# Validation
assert html.unescape(html_q1_text) == json_q1
```

### Allowed differences (after unescape they match)

These render correctly:
- JSON: `Track Changes (Review > Track Changes)`
- HTML: `Track Changes (Review &gt; Track Changes)` ✅ unescape match

Both are valid because `&gt;` decodes to `>`.

### Forbidden differences (will break validation)

Why (官方原始碼): the block's `save()` (seo-by-rank-math 1.0.282,
`blocks/faq/assets/js/index.js`) writes `<div class="wp-block-rank-math-faq-block">`,
then per question with non-empty title and content and `visible` not false
`<div class="rank-math-faq-item"><{titleWrapper} class="rank-math-question">title</…><div class="rank-math-answer">content</div></div>`
(`titleWrapper` defaults to `h3`). The editor compares that with the saved HTML.


- JSON: `今天好` vs HTML: `今天 好` (extra space) ❌
- JSON: `Hello World` vs HTML: `HelloWorld` (missing space) ❌
- JSON: `Hello & welcome` vs HTML: `Hello and welcome` (paraphrased) ❌

## Number of questions

**8 questions** per article is the moksaweb.com convention (站內風格). Rank
Math's FAQ block has no question-count rule and no FAQ test in the score.

## FK distribution in FAQ

Of 8 question titles, **4 should contain the focus keyword**:
- Q1, Q2, Q4, Q8 (typical pattern)
- Other Qs use pronouns: "它能做 X 嗎?", "這個工具支援 Y 嗎?"

## Question topic suggestions

Cover these angles:
1. Comparison vs ChatGPT/Gemini/competitor
2. Free tier availability ("Free 帳號真的可以用嗎?")
3. Pricing/cost concern ("Token 消耗會不會很貴?")
4. Compliance/Privacy ("能處理機密資料嗎?")
5. Technical capability ("能做 X 任務嗎?")
6. Integration/Cross-platform ("和 Y 平台整合怎麼設?")
7. Error handling ("出錯了怎麼辦?")
8. Chinese language support ("[FK] 中文支援怎麼樣?")

## HTML escape minimal rule

When generating FAQ HTML from JSON, escape ONLY `&` and `<`. Leave `>` literal.

```python
def faq_escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;')
```

This matches what Gutenberg's renderer outputs and what user re-saves produce.

## Common BROKEN patterns

### Broken Pattern 1: JSON differs from HTML

User edits the visible HTML in editor but doesn't update JSON metadata.
Result: validation error appears next time post is opened.

Fix: Regenerate HTML from JSON via `tools/regenerate-faq.py`.
Or: User opens post in editor, clicks "嘗試復原" (Try to recover) — Gutenberg
auto-regenerates HTML from JSON.

### Broken Pattern 2: Different question count

JSON has 8 questions but HTML has 7 (one was deleted manually).
Or JSON has 8 but HTML has 9 (extra was pasted).

Fix: Regenerate HTML from JSON.

### Broken Pattern 3: HTML escape inconsistency

JSON: literal `>`
HTML: encoded `&gt;`

After html.unescape both become `>`, so this is OK in newer Gutenberg.
But mixing escape styles within one article is a code smell.

Best practice: Use literal `>` in both JSON and HTML. Only escape `&` and `<`.

## Validation snippet

```python
import json, re, html

def validate_faq_block(content):
    m = re.search(
        r'wp:rank-math/faq-block (\{.*?\}) -->\s*'
        r'(<div class="wp-block-rank-math-faq-block">.*?</div>)\s*'
        r'<!-- /wp:rank-math/faq-block -->',
        content, re.DOTALL
    )
    if not m:
        return ['No FAQ block found']
    
    data = json.loads(m.group(1))
    html_block = m.group(2)
    
    items = re.findall(
        r'<div class="rank-math-faq-item">'
        r'<h3 class="rank-math-question">([^<]+)</h3>'
        r'<div class="rank-math-answer">(.*?)</div>'
        r'</div>',
        html_block, re.DOTALL
    )
    
    errors = []
    if len(items) != len(data['questions']):
        errors.append(f"Count mismatch: JSON {len(data['questions'])}, HTML {len(items)}")
        return errors
    
    for i, (q, (h_t, h_c)) in enumerate(zip(data['questions'], items)):
        if html.unescape(h_t) != q['title']:
            errors.append(f"Q{i+1} title mismatch")
        if html.unescape(h_c) != q['content']:
            errors.append(f"Q{i+1} content mismatch")
    
    return errors if errors else ['OK']
```

## H2 heading rule

The H2 introducing FAQ block should be plain "12. 常見問題 FAQ".

❌ Don't say "FAQ Schema"
❌ Don't say "FAQ 結構標記"
✅ Just "常見問題 FAQ"

## Manual user fix workflow

If user reports "區塊包含未預期或無效的內容" warning on FAQ block:
1. Open post in Gutenberg editor
2. Click on the broken FAQ block
3. Click "嘗試復原" (Try to recover) button at top of block
4. Gutenberg regenerates HTML from JSON metadata
5. Save post

This works because JSON is treated as source of truth. The visible HTML is
regenerated from JSON.

## When to use the regenerate-faq.py tool

When you can't ask user to manually re-save (batch processing many articles),
or when you've programmatically modified JSON and need HTML to match:

```bash
python tools/regenerate-faq.py 8489 8478 8579
```

The script:
1. Fetches each post via wp post get
2. Extracts FAQ block JSON
3. Regenerates canonical HTML from JSON
4. Pushes back via wp post update file.html
