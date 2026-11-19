# Featured Image Specs

> Directory edition: commands that mention `tools/` or `scripts/` need the full edition (`npm` package `rankmath-seo-wp`); this folder ships reference files only.

Every published article requires a featured image (post thumbnail). Below are
The author's site specs.

## Final image specs

- **Dimensions**: 2000 × 2000 pixels
- **Format**: WebP (better compression than PNG)
- **File size**: ~50-60 KB (after WebP quality 92)
- **Color space**: sRGB
- **Text**: English only (Montserrat SemiBold doesn't reliably render CJK)

## Layout

```
┌──────────────────────────────────┐
│                                  │
│   [Top half: cropped from base   │
│    template image, resized       │
│    2000×1050]                    │
│                                  │
│                                  │
├──────────────────────────────────┤  ← Y=1050 split
│                                  │
│         [Category text]          │  ← 150pt at Y=1116
│                                  │
│         [Title text]             │  ← 100pt at Y=1513
│                                  │
└──────────────────────────────────┘
```

- Top half (0-1050px): visual / branded image
- Bottom half (1050-2000px): white background with two text lines

## Typography

- **Font**: Montserrat SemiBold (or Montserrat-SemiBold.ttf)
- **Category text**: 150 points, centered, Y=1116
- **Title text**: 100 points, centered, Y=1513
- **Color**: #343434

## English-only constraint

Don't put Chinese characters in the image. Reasons:
1. Montserrat doesn't include CJK glyphs — they render as boxes (□)
2. Even with CJK font fallback, kerning breaks
3. Featured images often show as social media thumbnails — English wider audience

Examples:
- ✅ "AI Features" + "Skills"
- ✅ "Office" + "Excel"  
- ✅ "Claude Cloud" + "Pricing"
- ❌ "AI 功能" + "技能" (CJK breaks)

## Category text mapping

Used in top text line based on FileBird folder:

| FileBird Folder | Category Text |
|-----------------|---------------|
| getting-started | "Getting Started" |
| cli-commands | "CLI Commands" |
| settings | "Settings" |
| ide-integrations | "IDE Integration" |
| mcp-servers | "MCP Servers" |
| hooks | "Hooks System" |
| agents | "Custom Agents" |
| agent-sdk | "Agent SDK" |
| automation | "Automation" |
| claude-design | "Claude Design" |
| claude-office | "Office" |
| claude-ai-features | "AI Features" |
| claude-security | "Claude Security" |
| claude-cloud | "Claude Cloud" |
| claude-apps | "Claude Apps" |

## Title text rules

Title is the article-specific noun. Keep short (1-2 words ideal):

| Article | Title Text |
|---------|-----------|
| Claude for Excel | "Excel" |
| Claude Knowledge Base | "Knowledge Base" |
| Claude Voice Mode | "Voice Mode" |
| Claude in Xcode | "Xcode" |
| Claude for Chrome | "Chrome" |
| Claude Pricing | "Pricing" |

If title text is too long (3+ words), it overflows. Break into 2 lines or
shorten to essence (e.g., "Web Search" not "Web Search Tool").

## Generation script template

```python
"""Generate featured image for [article name]."""
from PIL import Image, ImageDraw, ImageFont
import os

# Source template (existing image to crop top half)
BASE = r"C:\path\to\base-template.webp"

# Output paths
OUT = r"C:\path\to\output\folder\article-slug.webp"
TMP = r"C:\path\to\temp\article-slug.webp"

os.makedirs(os.path.dirname(OUT), exist_ok=True)

# Load and crop top half
img = Image.open(BASE).convert("RGB")
top = img.crop((0, 0, img.size[0], 1050)).resize((2000, 1050), Image.LANCZOS)

# Build canvas
canvas = Image.new("RGB", (2000, 2000), "white")
canvas.paste(top, (0, 0))

# Draw text
draw = ImageDraw.Draw(canvas)
font_path = r"C:\Windows\Fonts\Montserrat-SemiBold.ttf"
f150 = ImageFont.truetype(font_path, 150)
f100 = ImageFont.truetype(font_path, 100)

cat_text = "AI Features"  # Replace per article
title_text = "Skills"     # Replace per article
color = "#343434"

# Center horizontally
cat_w = draw.textlength(cat_text, font=f150)
title_w = draw.textlength(title_text, font=f100)
draw.text(((2000 - cat_w) / 2, 1116), cat_text, font=f150, fill=color)
draw.text(((2000 - title_w) / 2, 1513), title_text, font=f100, fill=color)

# Save WebP
canvas.save(OUT, "WEBP", quality=92)
canvas.save(TMP, "WEBP", quality=92)
print(f"Saved: {os.path.getsize(TMP)} bytes")
```

## Required imports for cross-platform

```python
# pip install Pillow
from PIL import Image, ImageDraw, ImageFont
import os
```

Tested with Pillow 10+. Earlier versions may not support `textlength`.

## Font installation

Montserrat SemiBold should be in:
- Windows: `C:\Windows\Fonts\Montserrat-SemiBold.ttf`
- macOS: `/Library/Fonts/Montserrat-SemiBold.ttf`
- Linux: `/usr/share/fonts/truetype/montserrat/Montserrat-SemiBold.ttf`

If not present, download free from https://fonts.google.com/specimen/Montserrat
or via Google Fonts API.

## Upload to WordPress workflow

```bash
# 1. Generate image locally
python gen_image.py

# 2. Upload via base64 pipe (SCP often blocked on Cloudways)
base64 -w 0 image.webp | ssh user@host "base64 -d > /tmp/image.webp"

# 3. Import to WP media library
ATTACH_ID=$(wp media import /tmp/image.webp \
  --title='[FK] 完整教學' \
  --alt='[FK] keyword keyword keyword in English' \
  --porcelain)

# 4. Set as featured image
wp post meta update $POST_ID _thumbnail_id $ATTACH_ID

# 5. Assign to FileBird folder for organization
wp db query "INSERT INTO wp_fbv_attachment_folder (folder_id, attachment_id) \
  VALUES ($FBV_FOLDER_ID, $ATTACH_ID) \
  ON DUPLICATE KEY UPDATE folder_id=$FBV_FOLDER_ID"
```

## Alt text rule

Alt text MUST contain the focus keyword. This satisfies "Focus keyword in image
alt attribute" Rank Math criterion.

Format: `[FK] [English keywords describing image content]`

Examples:
- `Claude Skills three layer architecture SKILL.md progressive disclosure`
- `Claude for Excel sidebar with cell level citation`
- `Claude Voice Mode 5 voices Buttery Airy Mellow Glassy Rounded`

Keep alt under 125 characters. Use English (image is English text). Don't
keyword stuff — be descriptive.

## File naming convention

`[focus-keyword-slug].webp`

Examples:
- `claude-skills.webp`
- `claude-for-excel.webp`
- `claude-voice-mode.webp`
- `claude-pricing.webp`

Same as the post slug. Easy to trace which image goes with which article.

## Folder structure on disk

Organize per-category for backup/version control. Example layout (adapt to your
own brand and category taxonomy):

```
~/your-content-root/
├── getting-started/
├── cli-commands/
├── settings/
├── ide-integrations/      ← For Claude in Xcode etc.
├── claude-office/         ← For Excel/Word/PowerPoint
├── claude-ai-features/    ← For Skills/Memory/Research etc.
├── claude-security/
├── claude-cloud/          ← For Pricing
└── claude-apps/           ← For Mobile/Chrome
```

Save image to both:
- The category folder (for backup/version control)
- A temp path for upload (e.g., `~/temp/article-slug.webp`)

## Verify image before upload

```bash
# Check dimensions
python -c "from PIL import Image; print(Image.open('claude-skills.webp').size)"
# Expected: (2000, 2000)

# Check file size
ls -la claude-skills.webp
# Expected: 50-60 KB range
```

If file size > 100 KB, reduce quality or check for unintended PNG/JPG mode.
