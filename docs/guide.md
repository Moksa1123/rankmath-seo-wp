# rankmath-seo-wp guide

The long material that used to live in the README: CLI reference, the
platform installer, the article skeleton, the problems this skill fixes and
how to adapt it. The README keeps the short version.

## CLI reference

Every tool ships as a Python / Node pair with the same behaviour
(`tools/<name>.py` and `tools/<name>.mjs`). After `npm install -g
rankmath-seo-wp` three of them are also on your PATH: `rankmath-verify`,
`rankmath-export`, `rankmath-install`.

### Look a rule up — `scripts/search.py`

```bash
python scripts/search.py "keyword density"          # English
python scripts/search.py "密度"                      # Chinese works too
python scripts/search.py "faq" --domain blocks      # one data file
python scripts/search.py all --domain site          # every row of one file
python scripts/search.py stats                      # row counts + plugin version
```

Every hit prints its `trust` (plugin source, KB, measured, site style,
inferred) and `source`. No match exits 1: log the question in
`data/pending.csv` instead of guessing.

### Verify an article — `rankmath-verify`

```bash
rankmath-verify article.html "Your Focus Keyword"
python tools/verify-article.py article.html "Your Focus Keyword"
```

```
=== examples/sample-article.html ===
Focus keyword: Claude Skills

Word count:      714 visible words
                 OK at least 600 (content length 2/8)
FK count:        14 visible occurrences
FK density:      1.96%
                 OK full score band 1.0-2.5% (6/6; KB recommends 1.0-1.5%)
Heading balance: 12 open / 12 close
                 OK 12/12 (site-style structure)
FK in opening:   OK
FK in H2:        4 occurrences
                 OK at least 1 H2 contains FK
HowTo block:     OK
FAQ block:       OK (8 questions aligned)
Forbidden:       OK none found

=== Result: 8 passed, 0 failed ===
```

Exit 0 when everything passes, 1 on any failure or a usage error, 2 when the
file can't be read. What each line checks and where its threshold comes from:
`SKILL.md` → Verify, and `data/rankmath-tests.csv`.

### Export paste-ready blocks — `rankmath-export`

```bash
rankmath-export article.html                  # copy whole article to clipboard
rankmath-export article.html --only howto     # just the HowTo block
rankmath-export article.html --only faq       # just the FAQ block
rankmath-export article.html --to-file out.html
rankmath-export article.html --print > out.html
rankmath-export article.html --no-validate    # skip block validation
```

In WordPress: Posts → Add New → click in the editor → Ctrl+V / Cmd+V. The
block editor parses the block comments and rebuilds every block.

### Install into other AI tools — `rankmath-install`

```bash
rankmath-install --list                       # all platforms
rankmath-install --info cursor                # target path, frontmatter, loader
rankmath-install claude-code                  # ./.claude/skills/rankmath-seo-wp/
rankmath-install claude-code --global         # ~/.claude/skills/rankmath-seo-wp/
rankmath-install claude-ai --to ./build       # zip for Claude.ai upload
rankmath-install --dry-run claude-code        # plan without writing
```

| Platform | Key | Strategy | Default path |
|---|---|---|---|
| Claude Code | `claude-code` | full | `.claude/skills/rankmath-seo-wp/SKILL.md` |
| Claude.ai (web) | `claude-ai` | zip-upload | `./rankmath-seo-wp.zip` → Settings → Skills |
| Cursor | `cursor` | rule | `.cursor/rules/rankmath-seo-wp.mdc` |
| OpenAI Codex CLI | `codex-cli` | full | `.codex/skills/rankmath-seo-wp/SKILL.md` (or `--to .agents`) |
| Gemini CLI | `gemini-cli` | full | `.gemini/skills/rankmath-seo-wp/SKILL.md` |
| Devin Desktop (formerly Windsurf) | `windsurf` | rule | `.devin/rules/rankmath-seo-wp.md` |
| GitHub Copilot | `copilot` | full | `.github/skills/rankmath-seo-wp/SKILL.md` |
| Continue | `continue` | rule | `.continue/rules/rankmath-seo-wp.md` |

These paths were checked against each tool's documentation when the installer
was written; no source URL or date was recorded, so `data/platforms.csv` marks
them as inferred until they are re-checked. Older tool versions fall back to
legacy paths (`rankmath-install --info <platform>` lists them).

### Batch-fix posts over WP-CLI — `regenerate-faq`, `fix-howto-block`

```bash
export WP_SSH_KEY=~/.ssh/id_rsa
export WP_SSH_HOST=user@your-wp-host.example.com
export WP_PATH=/path/to/wordpress

python tools/fix-howto-block.py 101 102 --dry     # show what would change
python tools/fix-howto-block.py 101 102           # rewrite legacy HowTo blocks
python tools/regenerate-faq.py article.html       # local file: rebuild FAQ HTML from its JSON
python tools/regenerate-faq.py 101 102            # same, on posts over SSH
```

Each post is read with `wp post get`, rewritten, uploaded to
`/tmp/regenfaq_<id>.html` or `/tmp/fixhowto_<id>.html` on the server and
saved with `wp post update`, keeping its original `post_date`. The temp file
on the server is not deleted.

## Article skeleton (site style)

The moksaweb.com template. Rank Math does not require 12 H2s; it needs one
subheading with the focus keyword (FK).

```
[Opening paragraph]            FK 2-3 times
[Moksa observation quote]      natural Chinese, FK once
H2 #1   什麼是 [FK]?
H2 #2   [FK] 和 [Competitor] 怎麼選?       comparison table
H2 #3   如何啟用這個工具?                   code block
H2 #4   [FK] 4 步驟啟用設定                 HowTo block
H2 #5   它能做哪些 X 工作?
H2 #6   [Persona] 怎麼用 [FK]?
H2 #7   [Killer feature] 怎麼運作?
H2 #8   進階主題或場景
H2 #9   哪裡可以找到更多官方資源?           3 YouTube embeds
H2 #10  使用 [FK] 有哪些限制?
H2 #11  參考依據                             5 external links
H2 #12  常見問題 FAQ                         FAQ block
```

Full sample text: `references/article-template.md`. Every site-style rule
and the Rank Math test it relates to: `data/site-rules.csv`.

## Problems this skill fixes

| Problem | Fix in this skill |
|---|---|
| Density too high or too low | Plugin scoring bands in `data/focus-keyword-density.csv`; the verifier computes density the way the plugin does |
| HowTo block shows "invalid content" | `references/howto-block.md`: the HTML must equal the block's `save()` output; `fix-howto-block` rewrites old formats |
| FAQ block shows "invalid content" | `regenerate-faq` rebuilds the HTML from the block's JSON |
| JSON-LD `<script>` printed as text | Use the rank-math blocks; the verifier flags inline `ld+json` |
| "HowTo Schema" in a heading | The verifier flags it |
| Windows writes `\r\n` | All tools write LF |
| `--post_content="$(cat …)"` fails | Pass the file: `wp post update <id> file.html` |
| "Your SEO title doesn't contain a number" | Title template `[FK] 完整教學：N 大功能` |
| No SSH access | `rankmath-export` copies paste-ready blocks to the clipboard |

## Adapting to other niches

- Replace the Moksa observation quote with your own opening device
  (`references/moksa-style.md`).
- Replace the 12-H2 skeleton (`data/h2-templates.csv`).
- Keep density inside the plugin's scoring band; aim for the KB's 1–1.5%.
- Change the image template path in `references/image-specs.md` and the host
  placeholders in `references/wp-cli-pitfalls.md`.

## Open standard

`SKILL.md` follows the [Agent Skills format](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview):
YAML frontmatter (`name`, `description`) plus plain reference files, so the
same folder loads in Claude Code, Claude.ai, Cursor, Codex CLI, Gemini CLI,
GitHub Copilot and Devin Desktop.
