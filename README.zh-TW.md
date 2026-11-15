<div align="center">

# Rank Math SEO WP

### 自動產出 Rank Math 80 分以上 WordPress 文章的 AI Skill。剪貼簿一貼就能進區塊編輯器，不用 SSH。

<p>
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><img src="https://img.shields.io/npm/v/rankmath-seo-wp?style=flat-square&color=cb3837&logo=npm&logoColor=white&label=npm" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><img src="https://img.shields.io/npm/dm/rankmath-seo-wp?style=flat-square&color=cb3837&logo=npm&logoColor=white" alt="npm downloads"></a>
  <a href="https://github.com/Moksa1123/rankmath-seo-wp"><img src="https://img.shields.io/github/stars/Moksa1123/rankmath-seo-wp?style=flat-square&logo=github&logoColor=white&color=181717" alt="GitHub stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
</p>

<p>
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+">
  <img src="https://img.shields.io/badge/AI%20%E5%B9%B3%E5%8F%B0-8-blueviolet?style=flat-square" alt="8 AI 平台">
</p>

<p>
  <a href="#快速開始"><strong>立即開始</strong></a> ·
  <a href="https://github.com/Moksa1123/rankmath-seo-wp"><strong>GitHub</strong></a> ·
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><strong>npm</strong></a> ·
  <a href="https://moksaweb.com"><strong>moksaweb.com</strong></a>
</p>

<p>
  <a href="README.md">English</a> ·
  <strong>繁體中文</strong> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

</div>

---

<table>
<tr>
<td width="33%" valign="top">

#### 區塊複製貼上、不用 SSH

`rankmath-export article.html` 把整篇文章塞進剪貼簿。貼進 WP 區塊編輯器——HowTo / FAQ / 嵌入區塊全部完美還原。

</td>
<td width="33%" valign="top">

#### 8 平台一鍵安裝器

`rankmath-install <platform>` 自動把 Skill 放到正確路徑、正確 frontmatter——支援 Claude Code、Claude.ai、Cursor、Codex CLI、Gemini CLI、Devin Desktop（原 Windsurf）、GitHub Copilot、Continue。

</td>
<td width="33%" valign="top">

#### 上稿前驗證器

`rankmath-verify article.html "FK"` 自動檢查焦點關鍵字密度（1.0–1.5%）、12 H2 結構、HowTo / FAQ 區塊完整性、30+ 個 Rank Math 反模式。

</td>
</tr>
<tr>
<td valign="top">

#### Python + Node 雙生工具

每個 CLI 都有 `.py` 和 `.mjs` 兩個版本，行為經過 parity 測試完全一致。挑你已經有的工具鏈用就好。

</td>
<td valign="top">

#### 結構化 CSV 資料

關鍵字密度區間、H2 範本、FAQ 主題、SEO power words、平台安裝路徑——全部用機器可讀的 CSV 寫好，工具與人類都能讀。

</td>
<td valign="top">

#### 多語文件

完整 README 含 English、繁體中文、日本語、한국어，章節結構同步、中文 SEO 預設值經過實戰打磨。

</td>
</tr>
</table>

---

## 快速開始

```bash
# 用 npx 立即試用（不用裝）
npx -p rankmath-seo-wp rankmath-install claude-code              # full skill -> .claude/skills/rankmath-seo-wp/
npx -p rankmath-seo-wp rankmath-export article.html              # 貼上即用 HTML 進剪貼簿
npx -p rankmath-seo-wp rankmath-verify article.html "Claude Skills"

# 或全域安裝
npm install -g rankmath-seo-wp
rankmath-install --list                       # 列出 8 個支援的 AI 平台
```

安裝完重啟 AI 工具，試試：

```
> 幫我寫一篇 Claude Code Hooks 的教學文章
```

Skill 會自動觸發，產出 Rank Math 80 分以上、貼上即用的 Gutenberg 區塊文章。

> [!TIP]
> 想先看再裝？跑 `rankmath-install --info cursor` 可以看到該平台的精確路徑、frontmatter、loader 行為。

---

## 支援的 AI 平台

| # | 平台 | Key | 策略 | 預設路徑 |
|---|------|-----|------|----------|
| 1 | **Claude Code** | `claude-code` | full | `.claude/skills/rankmath-seo-wp/SKILL.md` |
| 2 | **Claude.ai (web)** | `claude-ai` | zip-upload | `./rankmath-seo-wp.zip` → 設定 → Skills |
| 3 | **Cursor** | `cursor` | rule | `.cursor/rules/rankmath-seo-wp.mdc` |
| 4 | **OpenAI Codex CLI** | `codex-cli` | full | `.codex/skills/rankmath-seo-wp/SKILL.md`（或 `--to .agents` 裝到跨工具標準 `.agents/skills/`） |
| 5 | **Gemini CLI** | `gemini-cli` | full | `.gemini/skills/rankmath-seo-wp/SKILL.md` |
| 6 | **Devin Desktop**（原 Windsurf） | `windsurf` | rule | `.devin/rules/rankmath-seo-wp.md` |
| 7 | **GitHub Copilot** | `copilot` | full | `.github/skills/rankmath-seo-wp/SKILL.md` |
| 8 | **Continue** | `continue` | rule | `.continue/rules/rankmath-seo-wp.md` |

> [!NOTE]
> 8 個平台於 2026 年 7 月全數驗證。舊版工具請走 legacy 路徑：Gemini CLI 用 `.gemini/extensions/<name>/GEMINI.md`、Windsurf 用 `.windsurf/rules/`、Copilot 附加到 `.github/copilot-instructions.md`——細節見 `rankmath-install --info <platform>`。

---

## CLI 速查表

<details>
<summary><strong>區塊貼上匯出</strong> — <code>rankmath-export</code></summary>

```bash
rankmath-export article.html                  # 整篇進剪貼簿
rankmath-export article.html --only howto     # 只匯出 HowTo block
rankmath-export article.html --only faq       # 只匯出 FAQ block
rankmath-export article.html --to-file out.html
rankmath-export article.html --print > out.html
rankmath-export article.html --no-validate    # 跳過區塊驗證
```

WP 後台：**文章 → 新增 → 編輯器內按 Ctrl+V / Cmd+V**。
Gutenberg 解析區塊註解、把每一個區塊還原。

</details>

<details>
<summary><strong>文章驗證器</strong> — <code>rankmath-verify</code></summary>

```bash
rankmath-verify article.html "你的焦點關鍵字"
```

範例輸出：

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

</details>

<details>
<summary><strong>多平台安裝器</strong> — <code>rankmath-install</code></summary>

```bash
rankmath-install --list                       # 列出 8 個平台
rankmath-install --info cursor                # 看細節
rankmath-install claude-code                  # 安裝到 ./.claude/skills/...
rankmath-install claude-code --global         # 安裝到 ~/.claude/skills/...
rankmath-install claude-ai --to ./build       # 在 ./build/ 產 zip
rankmath-install --dry-run claude-code        # 不寫檔，只看計畫
rankmath-install                              # 互動模式
```

</details>

<details>
<summary><strong>WP-CLI 批次修復</strong> — Python 或 Node（需主機存取）</summary>

```bash
export WP_SSH_KEY=~/.ssh/id_rsa
export WP_SSH_HOST=user@your-wp-host.example.com
export WP_PATH=/path/to/wordpress

# 一次修多篇舊版 HowTo block
python tools/fix-howto-block.py 8489 8478 8466
node   tools/fix-howto-block.mjs 8489 8478 8466

# 一次修多篇 FAQ JSON↔HTML 對齊
python tools/regenerate-faq.py 8489 8478 8579
node   tools/regenerate-faq.mjs 8489 8478 8579
```

</details>

---

## 文章骨架

Skill 會產出符合下列骨架的文章——moksaweb.com 上每一篇都遵循這個結構：

```
[開場段落]                    ~150 字、FK 出現 2–3 次
[Moksa 觀點]                   自然中文、FK 1 次、不堆英文行話
H2 #1   什麼是 [FK]?
H2 #2   [FK] 和 [Competitor] 怎麼選?       ← 比較表格
H2 #3   如何啟用這個工具?                   ← 程式碼區塊
H2 #4   [FK] 4 步驟啟用設定                 ← HowTo block
H2 #5   它能做哪些 X 工作?
H2 #6   [Persona] 怎麼用 [FK]?
H2 #7   [Killer feature] 怎麼運作?
H2 #8   進階主題或場景
H2 #9   哪裡可以找到更多官方資源?           ← 3 個 YouTube 影片
H2 #10  使用 [FK] 有哪些限制?               ← 6 段
H2 #11  參考依據                             ← 5 個外部連結
H2 #12  常見問題 FAQ                         ← FAQ block
```

結果：1,400–2,000+ 字、FK 密度 1.0–1.5%、Rank Math 80 分以上、區塊貼上即用。

---

## 資料夾結構

<details>
<summary>點開展開</summary>

```
rankmath-seo-wp/
├── SKILL.md                          # Skill 主檔（自動載入）
├── README.md / .zh-TW / .ja / .ko    # 多語文件
├── CLAUDE.md                         # AI 編輯本 Skill 時的開發守則
├── CONTRIBUTING.md                   # 人類貢獻者指南
├── LICENSE                           # MIT
├── package.json                      # npm 中繼資料 + 3 個 bin
│
├── assets/templates/platforms/       # 8 個平台安裝設定
│   ├── claude-code.json              # full
│   ├── claude-ai.json                # zip-upload
│   ├── cursor.json                   # rule (.mdc + globs)
│   ├── codex-cli.json                # full (.agents/skills/ optional)
│   ├── gemini-cli.json               # full (SKILL.md standard)
│   ├── windsurf.json                 # rule (.devin/rules, model_decision)
│   ├── copilot.json                  # full (.github/skills/)
│   └── continue.json                 # rule (alwaysApply)
│
├── data/                             # 結構化 CSV 參考資料
│   ├── focus-keyword-density.csv
│   ├── h2-templates.csv
│   ├── faq-topics.csv
│   ├── power-words.csv
│   └── platforms.csv
│
├── references/                       # 長文指南
│   ├── article-template.md
│   ├── howto-block.md
│   ├── faq-block.md
│   ├── seo-checklist.md              # Rank Math 100 分拆解
│   ├── moksa-style.md                # Moksa 觀點寫作風格
│   ├── image-specs.md                # 特色圖 PIL 範本
│   └── wp-cli-pitfalls.md            # 9 個 WP-CLI 部署地雷
│
├── tools/                            # 雙語 CLI 工具
│   ├── verify-article.py    / .mjs   # FK 密度與結構驗證
│   ├── export-blocks.py     / .mjs   # 區塊貼上匯出
│   ├── install-skill.py     / .mjs   # 多平台安裝器
│   ├── regenerate-faq.py    / .mjs   # FAQ JSON↔HTML 對齊（含批次）
│   └── fix-howto-block.py   / .mjs   # 舊版 HowTo 升級（含批次）
│
└── examples/
    └── sample-article.html
```

</details>

---

## 解決哪些痛點

發 30+ 篇後反覆出現的問題：

| 痛點 | 本 Skill 的對策 |
|------|----------------|
| Rank Math 分數 < 60 | `references/seo-checklist.md` 100 分檢核清單 |
| FK 密度 3% 以上（堆關鍵字） | 分佈表：5 H2 + 4 FAQ + 段落首句 |
| FK 密度 0.5%（太低） | `verify-article.{py,mjs}` 自動驗證 |
| HowTo「區塊包含未預期的內容」錯誤 | `references/howto-block.md` 的 8594 標準格式 |
| FAQ block 驗證錯誤 | `regenerate-faq.{py,mjs}` 對齊 JSON ↔ HTML |
| `<script>` JSON-LD 顯示成原始文字 | Skill 明確禁用 inline script |
| H2 出現「HowTo Schema」字樣 | Skill 與驗證器同時偵測 |
| Windows Python 寫出 `\r\n` | 工具一律強制 `newline='\n'` |
| `--post_content="$(cat)"` 噴錯 | 教你用 `wp post update file.html` 語法 |
| SEO Title 沒有數字的警告 | 強制 `[FK] 完整教學：N 大功能` 範本 |
| **沒 SSH 也想上稿** | **`rankmath-export` 把貼上即用 HTML 丟進剪貼簿** |

---

## 套用到其他主題

本 Skill 為中文科技教學量身設計，但規則可通用：

- 把 `Moksa 觀點` 換成你品牌的招牌開場
- 依領域改寫 `references/article-template.md` 的 H2 結構
- 1.0–1.5% 的 FK 密度適用大多數語言
- 在 `references/wp-cli-pitfalls.md` 改成你的 WP host / path
- 在 `references/image-specs.md` 改成你的特色圖底圖路徑

---

## 開放標準

遵循 [Anthropic Agent Skills 規範](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)：
`SKILL.md` + YAML frontmatter（`name`、`description`）+ 扁平 reference 檔案。
跨 AI 平台格式相容。

---

## 作者

<table>
<tr>
<td>

**[moksa](https://moksaweb.com)** —— [moksaweb.com](https://moksaweb.com) 站長，這份 Skill 在每一篇 Claude AI 教學文章上實戰使用。

把 30+ 篇 Rank Math 除錯經驗濃縮成可重用的多平台、多語言工具包。

</td>
<td align="center" width="200">

<a href="https://moksaweb.com">
  <img src="https://img.shields.io/badge/website-moksaweb.com-2563EB?style=for-the-badge" alt="Website">
</a>
<br>
<a href="https://github.com/Moksa1123">
  <img src="https://img.shields.io/badge/GitHub-Moksa1123-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>

</td>
</tr>
</table>

如果這份 Skill 替你省了幾小時調 Rank Math 的時間，歡迎到 GitHub 給個 star 或在你的文章加上連回 [moksaweb.com](https://moksaweb.com) 的回饋連結。

---

## 授權與貢獻

MIT 授權—— 見 [LICENSE](LICENSE)。Copyright © 2026 moksa (moksaweb.com)。

歡迎 PR——詳見 [CONTRIBUTING.md](CONTRIBUTING.md)。特別是：

- 翻譯（除了 EN、zh-TW、ja、ko 以外的語系）
- 新的修正工具（圖片損毀、外部連結失效等）
- 其他垂直領域的文章範本（電商、新聞、財經）
- 其他 SEO 外掛的驗證規則（Yoast、AIOSEO、SEOPress）

---

<div align="center">
  <sub>由 <a href="https://moksaweb.com">moksa</a> 打造 · <a href="https://github.com/Moksa1123/rankmath-seo-wp">GitHub</a> · <a href="https://www.npmjs.com/package/rankmath-seo-wp">npm</a></sub>
</div>
