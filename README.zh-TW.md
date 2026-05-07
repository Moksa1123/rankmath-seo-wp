<h1 align="center">Rank Math SEO WP — Agent Skill</h1>

<p align="center">
  <strong>讓 AI 寫出 Rank Math 80 分以上的 WordPress 文章——一鍵複製貼上就能進區塊編輯器，不用 SSH</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
  <a href="https://moksaweb.com"><img src="https://img.shields.io/badge/author-moksa-orange?style=flat-square" alt="moksa"></a>
</p>

<p align="center">
  <strong>語言：</strong>
  <a href="README.md">English</a> ·
  <strong>繁體中文</strong> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

---

[moksaweb.com](https://moksaweb.com) 在 30+ 篇 Claude AI 教學文章中實戰打磨而成。
內建一行指令安裝器，支援 **8 個 AI 平台**——Claude Code、Claude.ai、Cursor、OpenAI Codex CLI、Gemini CLI、Windsurf、GitHub Copilot、Continue——
以及任何遵循 [Anthropic Agent Skills 標準](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) 的 AI 工具。

## 亮點

- **區塊複製貼上匯出**——整篇文章複製到剪貼簿，貼進 WP 區塊編輯器即可，HowTo / FAQ / YouTube / 表格全部正確渲染。**不需要 SSH 或 WP-CLI**。
- **Python + Node 雙語工具**——每個 CLI 都有 `.py` 和 `.mjs` 兩個版本，挑你已經有的就好。
- **結構化 CSV 參考資料**——關鍵字密度區間、H2 範本、FAQ 主題、SEO power words，工具與人類都能讀。
- **驗證器**——自動檢查 FK 密度（1.0–1.5% 甜蜜點）、12 H2 結構、HowTo / FAQ JSON↔HTML 對齊、禁用模式。
- **多平台安裝對照表**——支援 Claude / Claude.ai / Cursor / Codex / Gemini CLI / Windsurf / Copilot / Continue（見 `data/platforms.csv`）。

## 這個 Skill 做什麼

當 AI 偵測到以下指令時，就會自動觸發：

- 「幫我寫一篇 WordPress 文章關於 X」
- "Write a WP article about X with Rank Math SEO"
- 「幫 moksaweb.com 寫一篇 Y 的部落格」
- 「修一下這篇文章讓它符合 Rank Math」

接著 AI 會產出符合下列規範的文章：

- **12 個 H2 結構**（開場 + Moksa 觀點 + 12 個段落，FAQ 放在 H2 #12）
- **焦點關鍵字密度 1.0–1.5%**（自動計算、不亂塞）
- **Rank Math HowTo block** 採用標準 Gutenberg 格式
- **Rank Math FAQ block** JSON ↔ HTML 完全對齊
- **SEO Title 必含阿拉伯數字**（Rank Math 硬性要求）
- **自然中文文體**——不堆英文行話
- **2,000 字以上** 配 3 個 YouTube 影片 + 5 個外部權威連結

## 快速開始 — 一行指令安裝

clone 下來、執行你 AI 平台對應的 installer。Installer 會把 Skill 內容放到該平台規定的路徑、檔名、frontmatter 形態。

```bash
git clone https://github.com/Moksa1123/rankmath-seo-wp
cd rankmath-seo-wp

# 列出全部 8 個支援的平台
python tools/install-skill.py --list
# 或: node tools/install-skill.mjs --list
# 或: npx rankmath-install --list

# 安裝到目前專案
python tools/install-skill.py claude-code   # full install -> .claude/skills/rankmath-seo-wp/
python tools/install-skill.py cursor        # rule         -> .cursor/rules/rankmath-seo-wp.mdc
python tools/install-skill.py copilot       # 附加         -> .github/copilot-instructions.md
python tools/install-skill.py claude-ai --to ./build  # zip -> build/rankmath-seo-wp.zip

# 安裝到 user-global（平台支援時）
python tools/install-skill.py claude-code --global   # ~/.claude/skills/rankmath-seo-wp/

# 不寫檔，只看計畫
python tools/install-skill.py --info cursor
python tools/install-skill.py --dry-run claude-code
```

### 支援的平台

| 平台               | Key            | 安裝類型             | 預設路徑                                               |
|--------------------|----------------|----------------------|--------------------------------------------------------|
| Claude Code        | `claude-code`  | full                 | `.claude/skills/rankmath-seo-wp/SKILL.md`              |
| Claude.ai (web)    | `claude-ai`    | zip-upload           | `./rankmath-seo-wp.zip` → 設定 → Skills → 上傳         |
| Cursor             | `cursor`       | rule                 | `.cursor/rules/rankmath-seo-wp.mdc`                    |
| OpenAI Codex CLI   | `codex-cli`    | full                 | `.codex/skills/rankmath-seo-wp/SKILL.md`               |
| Gemini CLI         | `gemini-cli`   | full                 | `.gemini/extensions/rankmath-seo-wp/GEMINI.md`         |
| Windsurf           | `windsurf`     | rule                 | `.windsurf/rules/rankmath-seo-wp.md`                   |
| GitHub Copilot     | `copilot`      | instructions-append  | `.github/copilot-instructions.md`                      |
| Continue           | `continue`     | rule                 | `.continue/rules/rankmath-seo-wp.md`                   |

Codex CLI 與 Gemini CLI 為 best-effort，請以你目前版本的官方文件為準。

### 安裝後試試

重啟 AI 工具，輸入：

```
> 幫我寫一篇 Claude Code Hooks 的教學文章
```

### 不安裝、當參考文件用

即使不執行 installer，`references/` 與 `data/` 的內容也很完整，可直接翻閱。

## 兩種交付路徑

依照你有沒有 WordPress 主機 SSH 存取權，選一條路。

### 路徑 A · 區塊複製貼上（不需 SSH）

```bash
# 1. 驗證
python tools/verify-article.py article.html "你的焦點關鍵字"
# 或: node tools/verify-article.mjs article.html "你的焦點關鍵字"

# 2. 匯出——將「貼上即用」的 HTML 複製到剪貼簿
python tools/export-blocks.py article.html
# 或: npx rankmath-export article.html

# 3. WP 後台：文章 → 新增 → 編輯器內按 Ctrl+V / Cmd+V
```

Gutenberg 解析貼上的 `<!-- wp:... -->` 區塊註解，把每個區塊重建出來——HowTo、FAQ、YouTube、表格、程式碼區塊全部正確還原。接著在側邊欄設定 Rank Math meta（焦點關鍵字、含數字的 SEO Title、描述、slug）並上傳特色圖片即可。

只匯出單一區塊：

```bash
python tools/export-blocks.py article.html --only howto   # 只匯出 HowTo
python tools/export-blocks.py article.html --only faq     # 只匯出 FAQ
```

或寫到檔案：

```bash
python tools/export-blocks.py article.html --to-file ready.html
python tools/export-blocks.py article.html --print > ready.html
```

### 路徑 B · WP-CLI 批次（需主機存取）

```bash
export WP_SSH_KEY=~/.ssh/id_rsa
export WP_SSH_HOST=user@your-wp-host.example.com
export WP_PATH=/path/to/wordpress

# 一次修多篇舊版 HowTo block
python tools/fix-howto-block.py 8489 8478 8466

# 一次修多篇 FAQ 對齊問題
python tools/regenerate-faq.py 8489 8478 8579
```

## 驗證任一篇文章

```bash
python tools/verify-article.py article.html "你的焦點關鍵字"
# 或
node tools/verify-article.mjs article.html "你的焦點關鍵字"
```

範例輸出：

```
=== article.html ===
Word count:      1495 visible words
                 OK above 1400 minimum
FK count:        22 visible occurrences
FK density:      1.47%
                 OK in target range 1.0-1.5%
Heading balance: 12 open / 12 close
                 OK 12/12 (target structure)
HowTo block:     OK
FAQ block:       OK (8 questions aligned)
Forbidden:       OK none found

=== Result: 8 passed, 0 failed ===
```

## 資料夾結構

```
rankmath-seo-wp/
├── SKILL.md                          # 主要進入點（自動載入）
├── README.md                         # 英文 README
├── README.{zh-TW,ja,ko}.md           # 多語翻譯
├── CLAUDE.md                         # AI 編輯本 Skill 時的開發守則
├── CONTRIBUTING.md                   # 人類貢獻者指南
├── LICENSE                           # MIT
├── package.json                      # npm 中繼資料 + bin 設定
├── data/                             # 結構化 CSV 參考資料
│   ├── focus-keyword-density.csv     # 密度區間 → 結論 + 修正建議
│   ├── h2-templates.csv              # 12 H2 結構與 FK 配置
│   ├── faq-topics.csv                # 8 個 FAQ 主題範本（中英）
│   ├── power-words.csv               # SEO Title 強力詞
│   └── platforms.csv                 # 各 AI 平台安裝路徑
├── references/                       # 詳細指南（按需載入）
│   ├── article-template.md           # 12 H2 結構 + FK 分佈
│   ├── howto-block.md                # rank-math/howto-block 標準格式
│   ├── faq-block.md                  # FAQ JSON ↔ HTML 對齊規則
│   ├── seo-checklist.md              # Rank Math 100 分拆解
│   ├── moksa-style.md                # Moksa 觀點寫作風格 + 替換詞表
│   ├── image-specs.md                # 特色圖規格 + PIL 範本
│   └── wp-cli-pitfalls.md            # 9 個 WP-CLI 部署地雷
├── tools/                            # 雙語 CLI 工具（Python + Node）
│   ├── verify-article.py    / .mjs   # FK 密度與結構驗證
│   ├── export-blocks.py     / .mjs   # 區塊貼上匯出
│   ├── install-skill.py     / .mjs   # 多平台安裝器
│   ├── regenerate-faq.py    / .mjs   # FAQ JSON↔HTML 對齊（含 WP-CLI 批次）
│   └── fix-howto-block.py   / .mjs   # 舊版 HowTo 格式升級（含 WP-CLI 批次）
└── examples/
    └── sample-article.html           # 通過全部檢查的示範文章
```

## 解決哪些痛點

發 30+ 篇後，這幾個問題反覆出現：

| 痛點                                  | 本 Skill 的對策                                            |
|---------------------------------------|-----------------------------------------------------------|
| Rank Math 分數 < 60                   | 照 `seo-checklist.md` 的 100 分檢核清單                    |
| FK 密度 3% 以上（堆關鍵字）            | `article-template.md` 的分佈表（5 H2 + 4 FAQ + 段落首句）  |
| FK 密度 0.5%（太低）                   | `verify-article.{py,mjs}` 自動驗證                         |
| HowTo「區塊包含未預期的內容」錯誤      | 套用 `howto-block.md` 的 8594 標準格式                     |
| FAQ block 驗證錯誤                     | 用 `regenerate-faq.py` 對齊 JSON ↔ HTML                    |
| `<script>` JSON-LD 顯示成原始文字     | Skill 明確警告不要用 inline script                        |
| H2 出現「HowTo Schema」字樣            | Skill 與驗證器同時偵測                                     |
| Windows Python 寫出 `\r\n`             | 工具一律強制 `newline='\n'`                                |
| `--post_content="$(cat)"` 噴錯         | 教你用 `wp post update file.html` 語法                    |
| SEO Title 沒有數字的警告               | 強制套用 `[FK] 完整教學：N 大功能` 範本                   |
| 沒 SSH 也想上稿                        | `export-blocks` 把貼上即用的 HTML 丟進剪貼簿              |

## 套用到其他主題

本 Skill 為中文科技教學量身設計，但規則可通用：

- 把 `Moksa 觀點` 換成你的招牌開場
- 依領域改寫 `references/article-template.md` 的 H2 結構
- 1.0–1.5% 的 FK 密度適用大多數語言
- 在 `references/wp-cli-pitfalls.md` 改成你的 WP host / path
- 在 `references/image-specs.md` 改成你的特色圖底圖路徑

## 開放標準

遵循 [Anthropic Agent Skills 規範](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)：
`SKILL.md` + YAML frontmatter（`name`、`description`）+ 扁平 reference 檔案。跨 AI 平台格式相容。

## 作者

由 **moksa** 撰寫並維護——[moksaweb.com](https://moksaweb.com) 站長，
這份 Skill 在每一篇 Claude AI 教學文章上實戰打磨而成。

- 網站：[moksaweb.com](https://moksaweb.com)
- 作者：[moksa](https://moksaweb.com)

若這份 Skill 替你省了幾小時調 Rank Math 的時間，歡迎到 GitHub 給個 ⭐
或在你的文章加上連回 [moksaweb.com](https://moksaweb.com) 的回饋連結。

## 授權

MIT 授權——見 [LICENSE](LICENSE)。Copyright © 2026 moksa (moksaweb.com)。

## 貢獻

詳見 [CONTRIBUTING.md](CONTRIBUTING.md)。歡迎以下 PR：

- 翻譯（除了 EN / zh-TW / ja / ko 以外的語系）
- 新的修正工具（圖片損毀、外部連結失效等）
- 其他垂直領域的文章範本（電商、新聞、財經）
- 其他 SEO 外掛的驗證規則（Yoast、AIOSEO、SEOPress）

---

由 [moksa](https://moksaweb.com) 透過 [Claude Code](https://claude.com/claude-code) 打造。
