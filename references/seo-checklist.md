# Rank Math SEO Checklist (100-point breakdown)

Rank Math evaluates each post on multiple criteria. Hitting 80+ score is the
goal. Below is the full checklist with how to satisfy each.

## Basic SEO (40 points)

### Focus keyword in URL/slug (5 pts)
- `post_name` (slug) must contain the focus keyword
- Use kebab-case English: `claude-skills`, `claude-for-excel`
- Set via: `wp post update POST_ID --post_name='claude-skills'`

### Focus keyword at start of SEO Title (5 pts)
- `rank_math_title` must START with focus keyword
- Format: `[FK] 完整教學：[數字] [量詞] [補充]`
- ❌ "完整教學：Claude Skills 3 層架構" (FK not at start)
- ✅ "Claude Skills 完整教學：3 層架構 + SKILL.md"

### Focus keyword in Meta Description (5 pts)
- `rank_math_description` should contain FK, ideally in first sentence
- 100-160 characters total
- Example: "Claude Skills 完整教學：Pre-built / Custom / Workspace 三層架構、SKILL.md 格式、Progressive Disclosure 機制與 Open Standard 跨平台。"

### Focus keyword density (5 pts)
- Target **1.0-1.5%** visible density
- Below 0.4%: "too low" warning
- Above 2.5%: "too high" warning
- Sweet spot: 1.0-1.5% (sometimes up to 1.7% acceptable)
- Computation: visible_FK_count × 100 ÷ visible_word_count

### Focus keyword in first 10% of content (5 pts)
- FK should appear in opening paragraph (which is in first 10%)
- Best practice: FK in first sentence

### URL length under 75 characters (5 pts)
- Short slugs preferred: `claude-skills` not `claude-skills-complete-guide-tutorial`

### Use external links (5 pts)
- At least 1 external link to authoritative source
- moksaweb.com convention: 5 external links in section 11

### Use internal links (5 pts)
- At least 1 internal link to your own site
- Convention: First link in section 11 is to category page
- Example: `https://moksaweb.com/category/claude-code/`

## Additional SEO (40 points)

### Focus keyword in Subheading (5 pts)
- FK must appear in at least one H2 or H3
- Convention: 5 of 12 H2s contain FK (Sections 1, 2, 4, 6, 10)
- Validation: search content for `<h2[^>]*>[^<]*FK[^<]*</h2>`

### Focus keyword in Image Alt (5 pts)
- Featured image alt attribute must contain FK
- Set via: `wp media import file.webp --alt='[FK] sidebar generates X Y Z'`
- Example: alt='Claude Skills three layer architecture SKILL.md progressive disclosure'

### SEO Title contains a number (5 pts)
- `rank_math_title` MUST contain at least one Arabic digit (0-9)
- Without digit: "Your SEO title doesn't contain a number" warning
- Pattern: `[FK] 完整教學：[N] [量詞] X`
- Examples passing:
  - "Claude for Excel 完整教學：6 大功能搶先 Setup"
  - "Claude Pricing 完整指南：5 個方案 + API 計費"
  - "Claude in Xcode 完整教學：6 大功能 + Visual Loop"
- Examples failing:
  - "Claude Research 完整教學：Multi Agent 深度研究" (no digit)
  - "Claude Code Custom Themes 完整教學：客製化配色主題" (no digit)

### SEO Title length (5 pts)
- Optimal: 50-60 characters (English) or 25-30 chars (CJK width 2)
- Too long → truncated in SERP
- Too short → looks underdetermined

### Meta Description length (5 pts)
- Optimal: 120-160 characters
- Too long → truncated
- Too short → less informative

### Use H2 (5 pts)
- At least one H2 in content
- Convention: 12 H2 sections per article

### Use HowTo Schema (5 pts) [if HowTo article]
- Use `wp:rank-math/howto-block` Gutenberg block
- See `howto-block.md` for canonical format
- Triggers HowTo Rich Snippet in Google search

### Use FAQ Schema (5 pts)
- Use `wp:rank-math/faq-block` Gutenberg block
- See `faq-block.md` for canonical format
- Triggers FAQ Rich Snippet in Google search

## Title Readability (10 points)

### Title contains power word (3 pts)
- Use compelling adjectives: 完整, 終極, 最佳, 必看, 5 分鐘
- "Claude Skills 完整教學" passes

### Title contains a number (handled above)

### Title length within range (handled above)

## Content Length (10 points)

### Word count (5 pts)
- Minimum: 600 words
- Recommended: 1000+ words
- Excellent: 2000+ words
- Convention: target 1400-2000 visible words

### Content readability (5 pts)
- Short paragraphs (under 150 chars each)
- Use bullet lists, tables, code blocks for variety
- Mix sentence lengths

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
| FK density 3%+ | "Keyword stuffing" warning | Replace some FK with pronouns 它/這個工具 |
| FK density 0.5% | "Too low" warning | Add FK to H2 headings or section openings |
| No digit in SEO Title | "Title doesn't contain number" | Add 4 步驟 / 5 種 / 6 大功能 etc. |
| No FK in subheading | Missing 5 pts | Make 1 of 12 H2s contain FK |
| Inline `<script>` | Renders as visible text in some themes | Use rank-math blocks instead |
| post_title in CJK | Font rendering / breaks character limits | Keep post_title English, CJK in rank_math_title |

## Verification before publish

Run `tools/verify-article.py article.html "Focus Keyword"` which checks:
- Word count
- FK count (visible only)
- FK density (computed)
- Heading balance
- Forbidden patterns (HowTo Schema text, inline script)
- HowTo block format compliance
- FAQ block JSON+HTML alignment

Sample output:
```
=== article.html ===
Word count: 1495 visible
FK count: 22
Density: 1.47%  ✓ OK
Headings: 12 / 12  ✓ balanced
HowTo block: ✓ canonical format (4 steps)
FAQ block: ✓ JSON 8 ↔ HTML 8 (all match)
HowTo Schema text: 0  ✓
Inline script: 0  ✓
```

## Real-world score targets

Based on moksaweb.com experience:
- 80-90 score: practical floor; passes Rank Math green light
- 90-95 score: excellent; covers most points
- 95+ score: requires manual tweaking and may sacrifice readability

Don't chase 100. Hit 85+ consistently and focus on writing quality.
