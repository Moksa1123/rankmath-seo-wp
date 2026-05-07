---
name: rankmath-seo-wp
description: |
  Write Rank Math SEO-compliant WordPress articles in Traditional Chinese (or any
  language) that pass the Rank Math 100-point scoring system. Use this skill when
  user asks to write WP articles, blog posts, tutorials, product guides, or content
  that will publish to a WordPress site running Rank Math SEO plugin. Outputs
  Gutenberg-block formatted HTML with correct rank-math/howto-block and
  rank-math/faq-block markup, focus keyword density 1.0-1.5%, 12 H2 structure,
  Moksa-style natural quote, no inline script tags, and SEO Title containing a
  digit. Includes deployment helpers for WP-CLI publishing.
author: moksa (https://moksaweb.com)
license: MIT
version: 1.0.1
---

# Rank Math SEO WP Writing Skill

Produces WordPress articles that score 80+ on Rank Math SEO out of the box.
Distilled from 30+ articles published on [moksaweb.com](https://moksaweb.com)
covering Claude AI tutorials.

**Maintainer:** moksa · [moksaweb.com](https://moksaweb.com) · License: MIT

## When to use

Trigger this skill when the user asks to:
- Write a WordPress article, blog post, tutorial, guide
- Create content for a WP site with Rank Math SEO plugin
- Publish via WP-CLI to a Cloudways/managed WordPress host
- Fix existing articles for Rank Math compliance
- Generate Gutenberg blocks (HowTo, FAQ, Heading, List)

Do NOT use for:
- Static HTML pages (no Gutenberg blocks needed)
- Markdown-only content
- Sites without Rank Math (other SEO plugins have different requirements)

## Quick checklist (copy-paste verify)

```
[ ] post_title: English only (no CJK characters — fonts/SEO compatibility)
[ ] rank_math_title: Contains at least one Arabic digit
[ ] rank_math_description: Starts with focus keyword
[ ] post_name (slug): kebab-case, contains focus keyword
[ ] focus keyword density: 1.0-1.5% visible (count ÷ word count × 100)
[ ] focus keyword in: opening paragraph, ≥1 H2 subheading, image alt
[ ] Article structure: opening + Moksa quote + 12 H2 sections (FAQ block lives under H2 #12)
[ ] Word count: 1400+ visible (2000+ ideal)
[ ] HowTo block: 4 steps, exact 8594-style format (see references/howto-block.md)
[ ] FAQ block: 8 questions, JSON ↔ HTML aligned (see references/faq-block.md)
[ ] 3 YouTube embeds in section 9 (resources)
[ ] 5 external authoritative links in section 11 (references)
[ ] No "HowTo Schema" text in any H2 heading
[ ] No inline <script type="application/ld+json"> (theme strips them)
[ ] Featured image: 2000x2000 webp, English text only, Montserrat SemiBold
```

## Article structure (12 H2 template)

Every article follows this skeleton. See `references/article-template.md` for
full sample text.

```
[Opening paragraph]              ← 100-200 words, FK appears 2-3 times
[Moksa observation blockquote]   ← natural Chinese, no English jargon dump
H2 #1: 什麼是 [FK]?
H2 #2: [FK] 和 [Competitor] 怎麼選?
H2 #3: 如何啟用 [FK]?
H2 #4: [FK] 4 步驟啟用設定 (HowTo block goes under this H2)
H2 #5: 它能做哪些 X 工作?
H2 #6: [Persona] 怎麼用 [FK]? (use case section)
H2 #7: [Killer feature] 怎麼運作? (technical deep dive)
H2 #8: 進階主題或場景
H2 #9: 哪裡可以找到更多官方資源? (3 YouTube embeds)
H2 #10: 使用 [FK] 有哪些限制和安全注意事項? (6 paragraphs)
H2 #11: 參考依據 (5 external links)
H2 #12: 常見問題 FAQ (FAQ block goes under this H2)
```

5 of the 12 H2s should contain the focus keyword (typically 1, 2, 4, 6, 10).
Other H2s use pronouns like "它" (it) or "這個工具" (this tool) to avoid density overflow.

## Focus keyword (FK) density

Target: **1.0-1.5%** visible density.

Computation:
```python
visible_text = strip_block_metadata(content)  # remove <!-- wp:rank-math/... JSON -->
fk_count = visible_text.count(focus_keyword)
word_count = len(re.findall(r'\S+', strip_html_tags(visible_text)))
density = fk_count * 100 / word_count
```

Distribution (for ~22 visible FK in a 1500-word article):
- Opening paragraph: 2 FK
- Moksa quote: 1 FK
- H2 headings (5 of 12): 5 FK
- Body paragraphs: 5-6 FK (1 per major section, often opening sentence)
- FAQ titles (4 of 8): 4 FK
- Section 11 link anchor: 1 FK
- HowTo block JSON name field: 1 FK

**Run `tools/verify-article.py` to compute density before publishing.**

## Block formats

Two custom Gutenberg blocks must be exact:
- **HowTo block** → `references/howto-block.md` (8594 reference format, h3 not h4)
- **FAQ block** → `references/faq-block.md` (JSON + HTML must match after html.unescape)

**Critical:** Do NOT use `<script type="application/ld+json">` for HowTo schema —
moksaweb.com theme (and many WP themes) strips inline scripts and renders them as
visible raw text. Use the proper `wp:rank-math/howto-block` Gutenberg block instead.

## Style: Moksa observation quote

The article opens with a `<blockquote>` containing the author's personal
experience. **Critical:** Use natural conversational Chinese, NOT English jargon
dump.

❌ Bad: "Workflow Friction... Cell Level Citation... Time Save 是 Salary 級別的 ROI"
✅ Good: "視窗來回切超煩。Claude for Excel 把這道牆打掉了——AI 對話直接在側邊欄完成"

See `references/moksa-style.md` for full guide with replacement word table.

## SEO Title rules

`rank_math_title` MUST contain at least one Arabic digit. Without a digit,
Rank Math shows "Your SEO title doesn't contain a number" warning.

Template: `[FK] 完整教學：[數字] [量詞] [補充]`

Examples that pass:
- `Claude for Excel 完整教學：6 大功能搶先 Setup`
- `Claude Skills 完整教學：3 層架構 + SKILL.md`
- `Claude Pricing 完整指南：5 個方案 + API 計費`

Examples that fail (no digit):
- `Claude Research 完整教學：Multi Agent 深度研究`
- `Claude Code Custom Themes 完整教學：客製化配色主題`

## Image specs

Featured image must be:
- 2000×2000 webp (~50-60 KB after compression)
- English text only (Montserrat SemiBold doesn't render CJK reliably)
- Category text 150pt at Y=1116
- Title text 100pt at Y=1513
- Color #343434
- Top half: cropped from a base template image

See `references/image-specs.md` for PIL Python script template.

## Deployment via WP-CLI

Two critical gotchas — see `references/wp-cli-pitfalls.md`:

1. **Use file argument syntax**, NOT shell expansion:
   ```bash
   # ❌ Fails on long content with Gutenberg comments:
   wp post update 8613 --post_content="$(cat /tmp/article.html)"
   # Error: Unable to read content from 'wp:paragraph'

   # ✅ Works:
   wp post update 8613 /tmp/article.html
   ```

2. **Python on Windows must force LF newlines**:
   ```python
   # ❌ Default — Windows writes \r\n, breaks Gutenberg block validation:
   tempfile.NamedTemporaryFile(mode='w', encoding='utf-8')

   # ✅ Force LF:
   tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n')
   ```

## Two delivery paths

The skill supports two workflows depending on whether you have shell access
to your WordPress server.

### Path A — Block-paste (no SSH needed)

For users editing in the WP admin UI directly:

```
1. Plan: pick FK, draft 12 H2 outline, identify 3 YouTube videos + 5 external links
2. Write: full HTML following references/article-template.md
3. Verify:  python tools/verify-article.py article.html "Focus Keyword"
            (or: node tools/verify-article.mjs article.html "Focus Keyword")
4. Export:  python tools/export-blocks.py article.html
            (or: node tools/export-blocks.mjs article.html)
            → copies the entire article to clipboard, paste-ready
5. In WP:   Posts → Add New → click in editor canvas → Ctrl+V / Cmd+V
            Gutenberg parses the block comments and rebuilds every block
6. Set Rank Math meta in the post sidebar (FK, title, description, slug)
7. Upload featured image manually via Media Library
```

The exported markup includes `<!-- wp:rank-math/howto-block -->` and
`<!-- wp:rank-math/faq-block -->` comments. Gutenberg reconstructs them
exactly as if they had been authored in the editor — no WP-CLI needed.

`--only howto` / `--only faq` extracts a single block when you only need to
patch one section.

### Path B — WP-CLI batch deploy (server access required)

For users automating multi-article deploys:

```
1-3. Same plan / write / verify steps as Path A
4. Generate image: PIL script with English-only text
5. Upload: cat | ssh, then wp post create file.html ... --post_status=future
6. Configure meta: wp post term set + wp post meta update for FK/title/desc/slug
7. Upload image: base64 pipe → wp media import → set _thumbnail_id → FBV folder
8. Re-verify: python tools/verify-article.py via wp post get
```

Set `WP_SSH_KEY` / `WP_SSH_HOST` / `WP_PATH` env vars before running the
batch tools (`fix-howto-block.py`, `regenerate-faq.py`).

## Common pitfalls (from real debugging)

| Issue | Cause | Fix |
|-------|-------|-----|
| H2 says "HowTo Schema" | Mistaking SEO term as visible label | Drop the suffix, just "X 4 步驟安裝設定" |
| HowTo block validation error | Wrong format (h4, extra wrapper, extra JSON fields) | Use 8594 canonical format only |
| FAQ block validation error | JSON ≠ HTML after html.unescape | Regenerate HTML from JSON via tools/regenerate-faq.py |
| `<script>` shows as raw text | Theme strips inline scripts | Remove wp:html script blocks entirely |
| FK density 3%+ (too high) | FK in every H2 + every FAQ + every body paragraph | Pronouns in 7 H2s, 4 FAQ titles only |
| FK density 0.5% (too low) | Replaced too many FK with pronouns | Restore FK in 5 H2 + 4 FAQ titles + body openings |
| SEO title warning "no number" | Pure-text rank_math_title | Add digit: "4 步驟" / "6 大功能" / "3 種版本" |
| post_title shows broken CJK | post_title contains Chinese | Keep post_title English, put Chinese in rank_math_title |
| Internal links 404 | Linked post still in `future` status | Wait for publish OR use category page as fallback |

## Tools (in tools/)

Every user-facing tool ships as a Python/Node twin pair so you can use whichever
toolchain you already have. Both behave identically.

| Tool                  | Python                       | Node                           | Purpose                                                       |
|-----------------------|------------------------------|--------------------------------|---------------------------------------------------------------|
| Article verifier      | `verify-article.py`          | `verify-article.mjs`           | Density, headings, block format, forbidden patterns           |
| Block-paste exporter  | `export-blocks.py`           | `export-blocks.mjs`            | Copy paste-ready HTML to clipboard / file / stdout            |
| Multi-platform installer | `install-skill.py`        | `install-skill.mjs`            | Install the skill into Claude Code / Cursor / Codex / etc.    |
| FAQ JSON↔HTML aligner | `regenerate-faq.py`          | `regenerate-faq.mjs`           | Rebuild FAQ HTML from JSON metadata (also batches via WP-CLI) |
| HowTo format upgrader | `fix-howto-block.py`         | `fix-howto-block.mjs`          | Convert legacy HowTo block formats to canonical               |

npm bin entries (after `npm install -g rankmath-seo-wp` or `npx`):

- `rankmath-export article.html` → block-paste exporter
- `rankmath-verify article.html "Focus Keyword"` → article verifier
- `rankmath-install <platform>` → install skill into a specific AI platform

## Multi-platform install

The skill supports 8 AI platforms via `assets/templates/platforms/*.json`. Each
platform has an install strategy (`full` / `rule` / `instructions-append` /
`zip-upload`) so the same skill content lands at the right path with the right
filename and frontmatter.

```bash
# List available platforms
python tools/install-skill.py --list

# Inspect a platform without writing
python tools/install-skill.py --info cursor

# Install into the current project (auto-detects strategy)
python tools/install-skill.py claude-code           # full install
python tools/install-skill.py cursor                # writes .cursor/rules/rankmath-seo-wp.mdc
python tools/install-skill.py copilot               # appends to .github/copilot-instructions.md
python tools/install-skill.py claude-ai --to ./build  # builds rankmath-seo-wp.zip

# Install globally (where supported)
python tools/install-skill.py claude-code --global  # ~/.claude/skills/rankmath-seo-wp/
```

Supported platforms: `claude-code`, `claude-ai`, `cursor`, `codex-cli`,
`gemini-cli`, `windsurf`, `copilot`, `continue`. Use `--info <platform>` for
exact paths, frontmatter, and loader behaviour. Platforms marked
`verified: false` are best-effort — confirm against your tool's current docs.

## Data (in data/)

Structured CSV references that tools and humans can both read:

- `focus-keyword-density.csv` — density bands with verdict + remediation
- `h2-templates.csv` — 12 H2 structure with FK placement and word targets
- `faq-topics.csv` — 8 FAQ topic patterns with bilingual samples
- `power-words.csv` — Chinese / English SEO-Title power words
- `platforms.csv` — install paths per AI platform (Claude / Cursor / Codex / …)

## Examples (in examples/)

- `sample-article.html` — Reference article that passes all checks (Claude Skills 8730 simplified).

## Open Standard

This skill follows the [Anthropic Agent Skills spec](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).
Format-compatible with Claude Code, Claude.ai, Cursor, Codex CLI, Gemini CLI,
and Windsurf — anywhere SKILL.md with YAML frontmatter is recognised.

## Adapting to other niches

This skill targets Chinese tech tutorials but the rules generalise:
- Replace `Moksa 觀點` with your brand's signature opening device
- Replace the 12 H2 template with your domain's structure
- Adjust FK density target (1.0–1.5% works for most languages)
- Update image template path in `references/image-specs.md`
- Update WP host placeholders in `references/wp-cli-pitfalls.md` (and the
  `WP_SSH_KEY` / `WP_SSH_HOST` / `WP_PATH` env vars used by the tools)

## Author

Built and maintained by **moksa** at [moksaweb.com](https://moksaweb.com),
distilled from real publishing pain points across 30+ Claude AI tutorial articles.

Issues, ideas, or translation pull requests welcome — see the README for
contribution paths.
