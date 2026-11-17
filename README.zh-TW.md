<h1 align="center">Rank Math SEO WP Writer</h1>

<h3 align="center">Rank Math SEO 文章撰寫工具</h3>

<p align="center">
  <strong>Rank Math 測試規則 · 有效的 HowTo／FAQ 區塊 · 發布前驗證器</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+">
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Rank%20Math%20tests-25-success?style=flat-square" alt="25 Rank Math tests">
  <img src="https://img.shields.io/badge/AI%20platforms-8-blueviolet?style=flat-square" alt="8 AI platforms">
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><img src="https://img.shields.io/npm/v/rankmath-seo-wp?style=flat-square&color=cb3837&logo=npm&logoColor=white&label=npm" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><img src="https://img.shields.io/npm/dm/rankmath-seo-wp?style=flat-square&color=cb3837&logo=npm&logoColor=white" alt="npm downloads"></a>
  <a href="https://github.com/Moksa1123/rankmath-seo-wp"><img src="https://img.shields.io/github/stars/Moksa1123/rankmath-seo-wp?style=flat-square&logo=github&logoColor=white&color=181717" alt="GitHub stars"></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
</p>

<p align="center"><a href="README.md">English</a> · <strong>正體中文</strong> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a></p>

> 這是非官方的社群專案，不是 Rank Math 或其開發商製作或背書，也和他們沒有關係。Rank Math SEO 是第三方軟體，本專案不包含它。

## 功能

把「幫我寫一篇 WordPress 文章」變成能通過 Rank Math 自家測試、拿到 80 分以上的文章，不用猜 Rank Math 的規則。

| 項目 | 內容 |
|---|---|
| Rank Math 規則 | 25 項 Rank Math 測試與計分規則，含分數、門檻、KB 連結，從 seo-by-rank-math 1.0.282 原始碼讀出 |
| 區塊 | HowTo 與 FAQ 標記照各區塊的 `save()` 寫，編輯器不會出現「無效內容」 |
| 驗證器 | 字數和密度的算法和 Rank Math 一樣，任何一項沒過就回 exit code 1 |
| 查詢 | 中文或英文提問都從 `data/` 回答，每筆附出處 |
| 發布 | 剪貼簿貼上區塊（不需要主機權限），或在你自己的主機用 WP-CLI |
| 工具 | 每個指令都有 Python 和 Node 兩版，只用標準函式庫；可安裝到 8 個 AI 平台 |

### 規則直接讀自外掛

```bash
python scripts/search.py "密度"
# [tests] keywordDensity ... <0.5 fail 0; ... up to 2.5 best 6; >2.5 fail 0
#    trust=官方原始碼  source=analyzer.js keywordDensity calculateScore (1.0.282)
```

### 發布前驗證器

```bash
rankmath-verify article.html "焦點關鍵字"    # 或：python tools/verify-article.py
```

### 不用 SSH，貼上區塊

```bash
rankmath-export article.html                    # 整篇複製到剪貼簿
rankmath-export article.html --only faq         # 只複製 FAQ 區塊
```

### 區塊修正工具

```bash
python tools/regenerate-faq.py article.html     # 從 JSON 重建 FAQ HTML
python tools/fix-howto-block.py 101 --dry       # 預覽文章 101 的 HowTo 修正
```

### 解決的問題

| 問題 | 本 skill 的做法 |
|---|---|
| 密度太高或太低 | `data/focus-keyword-density.csv` 是外掛的計分區間；驗證器的算法和外掛相同 |
| HowTo 或 FAQ 區塊顯示「無效內容」 | HTML 必須等於區塊 `save()` 的輸出；`fix-howto-block`、`regenerate-faq` 會重建 |
| JSON-LD `<script>` 被印成文字 | 改用 rank-math 區塊；驗證器會擋 inline `ld+json` |
| 「Your SEO title doesn't contain a number」 | 標題範本 `[FK] 完整教學：N 大功能` |
| `--post_content="$(cat …)"` 失敗、Windows 寫出 `\r\n` | 把檔案直接交給 `wp post update`；所有工具都寫 LF |
| 沒有主機的 SSH 權限 | `rankmath-export` 複製可直接貼上的區塊 |

## 適用情境

| 適用 | 不適用（改用） |
|---|---|
| 在裝了 Rank Math SEO 的 WordPress 網站撰寫、修正或發布文章 | 其他區塊編輯器頁面 → `gutenberg-headless` |
| 含 HowTo 與 FAQ 區塊的教學、指南、部落格文章，正體中文或其他語言 | Elementor 或 Mosaic 頁面 → `elementor-headless`、`mosaic-headless` |
| 修好編輯器標示為無效的 HowTo／FAQ 區塊 | 使用 Yoast 或其他 SEO 外掛的網站（測試項目不同） |

## 安裝

| 需求 | 用途 |
|---|---|
| Python 3.9 以上或 Node.js 18 以上 | 執行工具（只用標準函式庫） |
| `ssh`，主機上要有 WP-CLI | 只有用 WP-CLI 發布或批次修文章時需要 |
| Windows、macOS 或 Linux | 全部功能 |

### Step 1：選一種安裝方式

Claude plugin（Claude Code；上架 Claude 官方目錄後也可以從目錄安裝）：

```
/plugin marketplace add Moksa1123/rankmath-seo-wp
/plugin install rankmath-seo-wp@rankmath-seo-wp
```

npx（Claude Code 和下表其他 AI 工具）：

```bash
npx -p rankmath-seo-wp@1.2.1 rankmath-install claude-code --global
npx -p rankmath-seo-wp@1.2.1 rankmath-install --list
```

手動複製：

```bash
git clone https://github.com/Moksa1123/rankmath-seo-wp.git
cp -r rankmath-seo-wp ~/.claude/skills/rankmath-seo-wp
```

| 平台 | 代號 | 安裝方式 | 預設路徑 |
|---|---|---|---|
| Claude Code | `claude-code` | full | `.claude/skills/rankmath-seo-wp/SKILL.md` |
| Claude.ai（網頁版） | `claude-ai` | zip-upload | `./rankmath-seo-wp.zip` → Settings → Skills |
| Cursor | `cursor` | rule | `.cursor/rules/rankmath-seo-wp.mdc` |
| OpenAI Codex CLI | `codex-cli` | full | `.codex/skills/rankmath-seo-wp/SKILL.md` |
| Gemini CLI | `gemini-cli` | full | `.gemini/skills/rankmath-seo-wp/SKILL.md` |
| Devin Desktop（原 Windsurf） | `windsurf` | rule | `.devin/rules/rankmath-seo-wp.md` |
| GitHub Copilot | `copilot` | full | `.github/skills/rankmath-seo-wp/SKILL.md` |
| Continue | `continue` | rule | `.continue/rules/rankmath-seo-wp.md` |

## 快速開始

### Step 2：檢查一篇文章

```bash
npx -p rankmath-seo-wp@1.2.1 rankmath-verify examples/sample-article.html "Claude Skills"
```

```
FK density:      1.96%
                 OK full score band 1.0-2.5% (6/6; KB recommends 1.0-1.5%)
...
=== Result: 8 passed, 0 failed ===
```

### Step 3：跟助理說

| 你說 | 會發生什麼 |
|---|---|
| 「幫我寫一篇 Claude Code Hooks 的 WordPress 教學，焦點關鍵字是 Claude Code Hooks。」 | 寫好文章，再跑驗證器 |
| 「這篇文章的 FAQ 區塊顯示無效內容，幫我修好。」 | 從區塊的 JSON 重建 FAQ HTML |
| 「Rank Math 的關鍵字密度多少才拿滿分？」 | 到 `data/` 查，引用外掛的規則 |

| 指令 | 用途 |
|---|---|
| `rankmath-verify article.html "FK"` | 為文章評分；全部通過回 exit 0 |
| `rankmath-export article.html` | 複製可直接貼上的區塊（`--only faq`、`--to-file`、`--print`） |
| `rankmath-install <platform>` | 安裝到 AI 工具（`--list`、`--info`、`--global`） |
| `python scripts/search.py "<關鍵字>"` | 查 Rank Math 規則、區塊標記或站內規則 |
| `python tools/regenerate-faq.py <檔案或文章 ID>` | 從 JSON 重建 FAQ HTML（`--dry` 預覽） |
| `python tools/fix-howto-block.py <檔案或文章 ID>` | 轉換舊版 HowTo 標記（`--dry` 預覽） |

完整輸出、所有選項和文章架構：[docs/guide.md](docs/guide.md)。

## 觸發詞

English: write a WordPress article, blog post or tutorial, Rank Math score, SEO green light, focus keyword density, FAQ block, HowTo block, block contains invalid content, publish with WP-CLI.

中文：寫 WordPress 文章、部落格文章、教學文、Rank Math 分數、SEO 綠燈、焦點關鍵字密度、FAQ 區塊、HowTo 區塊、區塊無效內容、WP-CLI 發文。

## 會執行與連線的內容

不會自己執行任何東西：這個 plugin 沒有 hook、沒有 MCP 伺服器、沒有背景程式。只有 Claude 照 `SKILL.md` 操作、而且你同意指令時，工具才會執行。

| 工具 | 讀取 | 寫入 | 連線到 |
|---|---|---|---|
| `scripts/search.py`、`tools/verify-article.*`、自我測試、數字核對 | 本資料夾的檔案、你指定的文章 | 不寫入 | 不連線 |
| `rankmath-export` | 文章 | 剪貼簿（`clip`、`pbcopy`、`xclip`、`xsel` 或 `wl-copy`），或你指定的檔案 | 不連線 |
| `rankmath-install` | 本資料夾 | AI 工具的 skill 或 rule 資料夾（專案內，或加 `--global` 寫到家目錄），或 zip | 不連線 |
| `regenerate-faq`、`fix-howto-block` 給本機 `.html` | 那個檔案 | 那個檔案 | 不連線 |
| `regenerate-faq`、`fix-howto-block` 給文章 ID | 文章（`wp post get`） | 文章（`wp post update`，保留原日期）；主機 `/tmp` 的暫存檔，執行後留在那裡 | 你的主機（`ssh`） |
| 發布（你要求時 Claude 執行 WP-CLI） | 你的 WordPress | 文章、Rank Math 欄位（`rank_math_focus_keyword`、`rank_math_title`、`rank_math_description`）、分類、網址代稱、特色圖片 | 你的主機（`ssh`） |

| 設定 | 環境變數 | `userConfig` 鍵 | 範例 |
|---|---|---|---|
| SSH 使用者與主機 | `WP_SSH_HOST` | `wp_ssh_host` | `user@your-wp-host.example.com` |
| SSH 私鑰路徑 | `WP_SSH_KEY` | `wp_ssh_key` | `~/.ssh/id_rsa`（沒設定時用這個） |
| 主機上的 WordPress 路徑 | `WP_PATH` | `wp_path` | `/path/to/wordpress` |

以 plugin 安裝時，Claude Code 會用 `userConfig` 詢問這幾個值；執行工具時以上表的環境變數名稱匯出。私鑰不會離開你的電腦，只由 `ssh` 用來登入。不需要 WordPress 密碼或 API 金鑰；安裝時不下載任何東西，也不會把資料傳給作者或任何人。

## 驗證方式

| 項目 | 結果 | 證據 |
|---|---|---|
| Rank Math 規則 | 從 seo-by-rank-math 1.0.282 讀出（`analyzer.js`、HowTo／FAQ 的 `save()` 與 `block.json`），2026-11-15 對照 [Rank Math KB](https://rankmath.com/kb/score-100-in-tests/) | `data/rankmath-tests.csv`、`data/blocks.csv` |
| 站內慣例 | 標為站內風格，不當成 Rank Math 規則 | `data/site-rules.csv` |
| 字數計算 | 和 `@wordpress/wordcount` 套件比對過的每個檔案結果相同 | `scripts/test_verify.py` |
| 自我測試 | 30 項離線測試：Python 與 Node 驗證器一致、壞掉的文章會被擋下、門檻和資料一致 | `python scripts/test_verify.py` |
| evals | 11 題；有 skill 11/11，沒有 skill 0/11 | [evals/RESULTS.md](evals/RESULTS.md) |
| 文件數字 | `SKILL.md` 和這幾份 README 的每個數字都和資料一致 | `python scripts/check_numbers.py` |

## 限制

| 限制 | 說明 |
|---|---|
| Rank Math 版本 | 規則讀自 Rank Math 1.0.282（免費版）；Pro 才有的測試和之後的版本要重新讀 |
| 驗證器看得到的範圍 | 只有文章 HTML；SEO 標題、Meta 描述、網址代稱、連結、圖片要在 Rank Math 側欄確認 |
| 實際比對 | 驗證器的數字還沒和實際的 Rank Math 側欄比對過 |
| 平台路徑 | 其他 AI 工具的安裝路徑還沒對照最新文件重新確認（[data/platforms.csv](data/platforms.csv)） |
| 待補問題 | [data/pending.csv](data/pending.csv) |

## 目錄結構

```
SKILL.md          助理載入的內容：出處、路由、任務、驗證
data/             Rank Math 測試、區塊標記、站內規則（CSV）、待補清單
references/       區塊格式、檢查清單、寫作風格、WP-CLI 踩坑
scripts/          search.py（入口）、自我測試、數字核對
tools/            驗證、匯出、安裝、FAQ／HowTo 修正（Python＋Node）
examples/         通過驗證器的範例文章
evals/            評分題目與結果
docs/             完整說明
.claude-plugin/   plugin 與 marketplace 設定檔
```

## 授權與作者

MIT 授權。作者 Moksa（[moksaweb.com](https://moksaweb.com)）。問題回報：[GitHub](https://github.com/Moksa1123/rankmath-seo-wp/issues)。
