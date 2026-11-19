# Moksa Observation Quote — Style Guide

> Directory edition: commands that mention `tools/` or `scripts/` need the full edition (`npm` package `rankmath-seo-wp`); this folder ships reference files only.
> The `wp` commands below run on your WordPress server; how you connect to the server is up to you.

The Moksa observation quote is the article's signature opening device. It's a
first-person personal experience block that sets tone and credibility.
**Critical: use natural conversational Chinese, NOT English jargon dump.**

## Format

```html
<!-- wp:quote -->
<blockquote class="wp-block-quote"><p><strong>Moksa 觀點：</strong>[content]</p></blockquote>
<!-- /wp:quote -->
```

Length: 150-250 Chinese characters. Single paragraph, no bullets.

## Structure (4 beats in 4-5 sentences)

1. **Pain point** (1-2 sentences) — specific personal scenario with numbers
2. **Solution intro** (1 sentence) — `[FK]` solves it, single sentence
3. **Time savings** (1 sentence) — concrete before-after numbers
4. **Audience + ROI** (1 sentence) — who benefits, why worth it

## ❌ Bad example: English jargon dump

> 我做 SaaS 財務模型每月都要花 8 到 12 小時更新、過去用純手動 Excel 加上偶爾切到
> Claude.ai 抓建議來回切窗很痛苦。Claude for Excel 第一次真正解決這個 **Workflow
> Friction**——所有 AI 互動都在 Excel Sidebar 完成、它直接讀我的整個 Workbook 給
> **Cell Level Citation** 答案、改 **Assumption** 後 **Formula Relationship**
> 自動維持。我現在月度 SaaS Model Update 從 8 小時壓縮到 2 小時、**Quality** 反而
> 提升因為 Claude 會主動指出 **Formula Inconsistency**。對 CFO Finance Manager
> Analyst 而言月費 20 美金 Pro 訂閱換來的 **Time Save** 是 **Salary 級別的 ROI**。

Problems:
- Workflow Friction, Cell Level Citation, Formula Relationship, Quality, Formula
  Inconsistency, Time Save, Salary 級別的 ROI = forced English jargon
- Reads like marketing copy, not personal experience
- "饒口" (mouthful) — user complained directly

## ✅ Good example: natural conversational Chinese

> 我每個月光更新 SaaS 財務模型就要花 8 到 12 小時，以前手動操作 Excel、不懂的地方
> 還要切到 Claude.ai 抓建議，視窗來回切超煩。Claude for Excel 把這道牆打掉了——AI
> 對話直接在 Excel 側邊欄完成，它讀完整張表給的答案還會精準標出引用了哪幾個 Cell，
> 改一個假設值後相關公式自動連動不會壞掉。我現在月底結帳建模從 8 小時壓到 2 小時，
> 品質反而更好，因為它會主動點出我自己沒發現的公式不一致。對 CFO 或財務主管來說，
> 每月 20 美金的訂閱換到的時間省下來，等於賺到一份兼職薪水的回報。

Differences:
- Conversational Chinese verbs: 切窗、超煩、把這道牆打掉了、壓到、不會壞掉
- Concrete numbers: 8 小時 → 2 小時, 月費 20 美金, 兼職薪水
- Single FK occurrence: "Claude for Excel" once
- No forced English vocabulary

## Replacement word table

When tempted to use English jargon, use these natural Chinese alternatives:

| English jargon | 自然中文 |
|----------------|---------|
| Workflow Friction | 來回切換的痛點 / 這道牆 / 摩擦 |
| Cell Level Citation | 精準標出引用了哪幾個 Cell |
| Assumption | 假設值 |
| Formula Relationship | 公式連動 / 公式關聯 |
| Quality | 品質 |
| Formula Inconsistency | 公式不一致 |
| Time Save | 時間省下來 |
| Salary 級別的 ROI | 賺到一份薪水的回報 / 等於拿到加班費 |
| Productivity Boost | 生產力提升 / 效率變高 |
| Game Changer | 改變遊戲規則 / 翻轉了 X |
| Killer Feature | 殺手級功能 / 必殺技 |
| Native Integration | 原生整合 |
| Seamless | 順暢 / 無縫 |
| State of the Art | 業界領先 |
| Enterprise Grade | 企業級 |
| Workflow Automation | 自動化流程 / 工作流自動化 |
| Pain Point | 痛點 |
| Onboarding | 入門 / 新手導引 |

## Words OK to keep English

These technical terms can stay English (don't force translate):

- Product names: Claude, Excel, PowerPoint, Word, ChatGPT, Gemini
- UI elements: Sidebar, Cell, Workbook, Token, API, Slide Master
- Acronyms: CFO, SaaS, ROI, IRR, KPI, AI, LLM, OAuth, MCP
- Specific Anthropic features: Cell Level Citation (proper noun, can stay if
  needed once, but introduce in Chinese first)

## Tone target

Like talking to a colleague at lunch, not a press release. Specifics > generalities.
Numbers > adjectives.

❌ "節省大量時間" → ✅ "從 8 小時壓到 2 小時"
❌ "效率大幅提升" → ✅ "生產力 5 到 10 倍"
❌ "具備強大功能" → ✅ "能一鍵產出 50 頁簡報"

## Audience pronouns

Address audience as a peer, not authority figure:

✅ 對 CFO 或財務主管來說
✅ 對知識工作者而言
✅ 對工程師
❌ 想要提升的您 (too formal)
❌ 各位讀者 (too distant)

## FK placement in Moksa quote

ONE FK occurrence is enough. Place it at the natural transition between
pain point and solution. Don't force multiple appearances.

```
[Pain point]. [FK] [solution].
            ↑ FK here (exactly once)
```

Multiple FK in Moksa quote signals forced SEO writing and reads worse.

## Final word count

150-250 Chinese characters (~280-450 if counting English mixed in).
Anything over 300 chars feels too long for a "personal observation."

## Pre-publish checklist

```
[ ] Single paragraph, starts with "Moksa 觀點："
[ ] First sentence has specific number/time/scenario
[ ] FK appears exactly once
[ ] No English-jargon dump (max 2-3 unavoidable English terms)
[ ] Concrete before-after numbers somewhere
[ ] Closes with "對 X 而言" + ROI statement
[ ] Reads aloud naturally without tongue twisting
```

## Why this matters

The Moksa quote is in the first 200 words of every article — it's where reader
decides whether to keep reading. Stilted English-jargon dump reads as fake
authority and pushes readers away. Natural Chinese reads as authentic
experience and builds trust for the rest of the article.

User feedback on early drafts: "很饒口、超級硬要的感覺" — this guide exists
because that feedback came in. Follow it.
