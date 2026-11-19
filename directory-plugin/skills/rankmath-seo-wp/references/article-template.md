# Article Template (12 H2 Structure)

> Directory edition: commands that mention `tools/` or `scripts/` need the full edition (`npm` package `rankmath-seo-wp`); this folder ships reference files only.
> The `wp` commands below run on your WordPress server; how you connect to the server is up to you.

This is the author's site article skeleton (站內風格). Rank Math does not ask
for 12 H2s; it needs one subheading with the FK (see `data/rankmath-tests.csv`).

## Section breakdown

```
[Opening paragraph]              ~150 words, FK 2-3 times
[Moksa quote]                    ~150 words, FK 1 time, natural Chinese
H2 #1: 什麼是 [FK]?              FK in heading, 4 paragraphs body
H2 #2: [FK] 和 X 怎麼選?         FK in heading, comparison table + 2 paragraphs
H2 #3: 如何啟用這個工具?         No FK in heading, 2 paragraphs + code block
H2 #4: [FK] 4 步驟啟用設定        FK in heading, HowTo block (4 steps)
H2 #5: 它能做哪些 X 工作?         No FK, 3 paragraphs covering 6 capability areas
H2 #6: Persona 怎麼用 [FK]?      FK in heading, code examples for use case
H2 #7: Killer Feature 怎麼運作?  No FK in heading, 3 paragraphs technical detail
H2 #8: 進階主題或場景            No FK in heading, 3 paragraphs
H2 #9: 哪裡可以找到更多官方資源?  No FK, 1 intro paragraph + 3 YouTube embeds
H2 #10: 使用 [FK] 有哪些限制?     FK in heading, 6 paragraphs (limitations + ALWAYS Review)
H2 #11: 參考依據                 No FK, list with 5 external links
H2 #12: 常見問題 FAQ             No FK, FAQ block (8 questions)
```

## Word count budget

Total target: **1400-2000+ visible words** (站內風格). Rank Math's content
length test passes from 600 `wp.wordcount` words and gives full points at
2500. `wp.wordcount` counts whitespace-separated tokens, so an unbroken run of
Chinese is one word: write mixed Chinese/English with spaces, as the sample does.

Distribution (for ~1500 word article):
- Opening: 150 words
- Moksa quote: 150 words
- H2 sections 1-10: ~100-150 words each = 1100 words
- Section 11 (links): ~50 words
- Section 12 (FAQ): 8 × ~60 words = 480 words → **counted toward total**

If under 1400 words, expand H2 sections 5, 6, or 7 with more practical examples.

## FK distribution map (target 18-22 visible occurrences)

| Location | FK count | Notes |
|----------|----------|-------|
| Opening paragraph | 2 | First sentence + somewhere in middle |
| Moksa quote | 1 | Once is enough, naturally embedded |
| H2 #1 (什麼是) | 1 | "什麼是 [FK]?" |
| H2 #2 (比較) | 1 | "[FK] 和 X 怎麼選?" |
| H2 #4 (HowTo) | 1 | "[FK] 4 步驟啟用設定" |
| H2 #6 (Persona) | 1 | "Persona 怎麼用 [FK]?" |
| H2 #10 (Limits) | 1 | "使用 [FK] 有哪些限制?" |
| Body paragraphs | 5-7 | One per major section opening |
| FAQ titles | 4 | Q1, Q2, Q4, Q8 typically |
| Other (link anchor, etc.) | 1-2 | |

## Opening paragraph template

The opening tells what the topic is, who made it, when, key features, and what
the article will cover. Aim for 150-200 words.

```
[FK] 是 [Vendor] [year/launch context]. [Description in 1 sentence]. 
[Key feature 1, 2, 3 in single flowing sentence]. 
[Plan availability — Free/Pro/Max etc]. 
這篇 [FK] 完整教學會拆解 [topics covered].
```

Example (Claude Skills opening):
```
Claude Skills 是 Anthropic 在 2025 年底推出的開放式能力擴展架構、把專業領域知識
打包成 Claude 可動態載入的模組。Anthropic 官方 GitHub Repo 提供 17 個 Skills
——從 Office 文件 (pptx xlsx docx pdf) 到 Frontend Design、MCP Builder、 
Slack GIF Creator 等橫跨 Creative Development Enterprise 三大領域。除了官方
Skills、社群創作的 Custom Skills 也爆炸成長——UI/UX Pro Max 累積 71K Stars。
這篇 Claude Skills 完整教學會拆解三層架構、SKILL.md 格式、Progressive
Disclosure 機制、實戰場景、限制和最佳實踐。
```

## Moksa observation quote template

First-person experience, conversational Chinese, ONE FK occurrence, natural flow.
**No English jargon dump.** See `moksa-style.md` for full guide.

```
<!-- wp:quote -->
<blockquote class="wp-block-quote"><p><strong>Moksa 觀點：</strong>
[Personal pain point 1-2 sentences]. 
[FK] [solution one sentence]. 
[Specific time savings number]. 
[Recommended audience + ROI conclusion].
</p></blockquote>
<!-- /wp:quote -->
```

## H2 #2 comparison table

Compare to top competitor. 6-7 rows including:
- Underlying tech / model
- Pricing
- Free tier availability  
- Key differentiator
- Target user
- "Best For" final row

```
<!-- wp:table -->
<figure class="wp-block-table"><table>
<thead><tr><th>面向</th><th>[FK]</th><th>Competitor</th></tr></thead>
<tbody>
  <tr><td>X</td><td>...</td><td>...</td></tr>
  <tr><td>...</td><td>...</td><td>...</td></tr>
  <tr><td>Best For</td><td>X scenario</td><td>Y scenario</td></tr>
</tbody>
</table></figure>
<!-- /wp:table -->
```

## H2 #3 code block

Shell commands, prompts, or config snippets. No FK in heading. Include comments.

```
<!-- wp:code -->
<pre class="wp-block-code"><code># Step 1
command --flag value

# Step 2
another-command

# Verify
verification-command
</code></pre>
<!-- /wp:code -->
```

## H2 #4 HowTo block (CRITICAL FORMAT)

See `howto-block.md` for exact format. Always 4 steps, h3 not h4, no extra fields.

## H2 #6 use case prompt examples

Show 4-5 realistic prompt examples in code block:

```
<!-- wp:code -->
<pre class="wp-block-code"><code># Example 1: [Use case name]
"[realistic prompt]"

# Example 2: [Use case name]  
"[realistic prompt]"

# ... 3-5 more
</code></pre>
<!-- /wp:code -->
```

## H2 #9 YouTube embeds (3 videos)

Always 3 embeds. Use proven Anthropic YouTube IDs:
- `a8PmR-fNQ_0` — How Claude is transforming financial services
- `BX2PxxM15Zc` — Testing Claude
- `zfWfczd6keE` — The Future of AI at Work / Cowork

```
<!-- wp:embed {"url":"https://www.youtube.com/watch?v=ID","type":"video","providerNameSlug":"youtube","responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->
<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">
https://www.youtube.com/watch?v=ID
</div><figcaption class="wp-element-caption">Caption text</figcaption></figure>
<!-- /wp:embed -->
```

## H2 #10 limitations (6 paragraphs)

Always 6 numbered paragraphs covering:
1. Technical limitation (rate limit, file size, etc.)
2. Edge case or known issue
3. Cost or quota concern
4. "Use Cases to Avoid" — 3-4 scenarios
5. Privacy/Compliance concern
6. **Always Review/Verify** — final paragraph emphasizing human oversight

## H2 #11 references (5 external links)

```
<!-- wp:list -->
<ul class="wp-block-list">
  <li><a href="https://example.com/category/claude-code/">Moksa Claude Code 完整教學系列</a></li>
  <li><a href="OFFICIAL_DOC_URL">Anthropic 官方 X 文件</a></li>
  <li><a href="ANNOUNCEMENT_URL">X 發布公告</a></li>
  <li><a href="WEBINAR_URL">相關 Webinar</a></li>
  <li><a href="THIRD_PARTY_URL">補充參考資料</a></li>
</ul>
<!-- /wp:list -->
```

First link is ALWAYS Moksa internal category page (improves internal link SEO).

## H2 #12 FAQ block (8 questions)

See `faq-block.md` for exact format. Always 8 questions, JSON+HTML must align.

Question topics (suggest):
1. Comparison to ChatGPT/Gemini/competitor
2. Free tier availability
3. Pricing or cost concern
4. Compliance/Privacy concern (specific industry)
5. Technical capability question
6. Cross-platform/Integration question
7. "出錯了怎麼辦?" — error handling
8. Chinese language support

## Required meta fields

After publishing, set these via wp post meta update:
- `rank_math_focus_keyword`: The FK string
- `rank_math_title`: Must contain a digit, format: `[FK] 完整教學：[數字] [量詞]`
- `rank_math_description`: Starts with FK, summarizes benefits, 100-150 chars
- `post_name` (slug): kebab-case of FK, e.g. `claude-skills`

Example:
```bash
wp post meta update POST_ID rank_math_focus_keyword 'Claude Skills'
wp post meta update POST_ID rank_math_title 'Claude Skills 完整教學：3 層架構 + SKILL.md'
wp post meta update POST_ID rank_math_description 'Claude Skills 完整教學：Pre-built / Custom / Workspace 三層架構、SKILL.md 格式、Progressive Disclosure 機制與 Open Standard 跨平台。'
wp post update POST_ID --post_name='claude-skills'
```
