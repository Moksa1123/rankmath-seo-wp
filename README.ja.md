<div align="center">

# Rank Math SEO WP

### Rank Math 80 点以上の WordPress 記事を AI で生成するスキル。クリップボードにコピーして貼るだけで Gutenberg ブロック復元、SSH 不要。

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
  <img src="https://img.shields.io/badge/AI%20%E3%83%97%E3%83%A9%E3%83%83%E3%83%88%E3%83%95%E3%82%A9%E3%83%BC%E3%83%A0-8-blueviolet?style=flat-square" alt="8 AI プラットフォーム">
</p>

<p>
  <a href="#クイックスタート"><strong>すぐに使う</strong></a> ·
  <a href="https://github.com/Moksa1123/rankmath-seo-wp"><strong>GitHub</strong></a> ·
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><strong>npm</strong></a> ·
  <a href="https://moksaweb.com"><strong>moksaweb.com</strong></a>
</p>

<p>
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <strong>日本語</strong> ·
  <a href="README.ko.md">한국어</a>
</p>

</div>

---

<table>
<tr>
<td width="33%" valign="top">

#### ブロック貼り付け、SSH 不要

`rankmath-export article.html` で記事全体をクリップボードへコピー。WP ブロックエディタに貼ると HowTo / FAQ / 埋め込みすべて完璧に復元されます。

</td>
<td width="33%" valign="top">

#### 8 プラットフォーム対応インストーラー

`rankmath-install <platform>` で Claude Code、Claude.ai、Cursor、Codex CLI、Gemini CLI、Devin Desktop（旧 Windsurf）、Copilot、Continue の正規パスとフロントマターに自動で配置。

</td>
<td width="33%" valign="top">

#### 公開前バリデーター

`rankmath-verify article.html "FK"` でフォーカスキーワード密度（1.0–1.5%）、12 H2 構造、HowTo / FAQ ブロック整合性、30+ 個のアンチパターンを自動チェック。

</td>
</tr>
<tr>
<td valign="top">

#### Python と Node のツインツール

各 CLI に `.py` と `.mjs` のツイン版を用意し、パリティテスト済み。お好きなツールチェーンを選択できます。

</td>
<td valign="top">

#### 構造化 CSV データ

密度バンド、H2 テンプレート、FAQ トピック、SEO パワーワード、プラットフォームインストールパス——機械可読 CSV で記述、ツールも人も読めます。

</td>
<td valign="top">

#### 多言語ドキュメント

English、繁體中文、日本語、한국어 の完全 README、章立て同期、中国語向け SEO デフォルト値は実戦検証済み。

</td>
</tr>
</table>

---

## クイックスタート

```bash
# npx で即座に試用（インストール不要）
npx -p rankmath-seo-wp rankmath-install claude-code              # full skill -> .claude/skills/rankmath-seo-wp/
npx -p rankmath-seo-wp rankmath-export article.html              # 貼ればそのまま HTML をクリップボードへ
npx -p rankmath-seo-wp rankmath-verify article.html "Claude Skills"

# またはグローバルインストール
npm install -g rankmath-seo-wp
rankmath-install --list                       # サポートする 8 つの AI プラットフォーム
```

インストール後、AI ツールを再起動して試してみてください：

```
> Claude Code Hooks のチュートリアル記事を書いて
```

スキルは WordPress 記事の作成リクエストで自動起動。出力は Gutenberg ブロック貼り付け対応で、Rank Math 80 点以上を一発で取れます。

> [!TIP]
> インストール前に確認したい？`rankmath-install --info cursor` で各プラットフォームの正確なパス、フロントマター、ローダー動作を確認できます。

---

## サポートする AI プラットフォーム

| # | プラットフォーム | Key | 戦略 | デフォルトパス |
|---|-----------------|-----|------|---------------|
| 1 | **Claude Code** | `claude-code` | full | `.claude/skills/rankmath-seo-wp/SKILL.md` |
| 2 | **Claude.ai (web)** | `claude-ai` | zip-upload | `./rankmath-seo-wp.zip` → 設定 → Skills |
| 3 | **Cursor** | `cursor` | rule | `.cursor/rules/rankmath-seo-wp.mdc` |
| 4 | **OpenAI Codex CLI** | `codex-cli` | full | `.codex/skills/rankmath-seo-wp/SKILL.md`（`--to .agents` でクロスツール標準 `.agents/skills/` にも配置可） |
| 5 | **Gemini CLI** | `gemini-cli` | full | `.gemini/skills/rankmath-seo-wp/SKILL.md` |
| 6 | **Devin Desktop**（旧 Windsurf） | `windsurf` | rule | `.devin/rules/rankmath-seo-wp.md` |
| 7 | **GitHub Copilot** | `copilot` | full | `.github/skills/rankmath-seo-wp/SKILL.md` |
| 8 | **Continue** | `continue` | rule | `.continue/rules/rankmath-seo-wp.md` |

> [!NOTE]
> 8 プラットフォームすべて 2026 年 7 月時点で検証済み。旧バージョンのツールはレガシーパスを使用：Gemini CLI は `.gemini/extensions/<name>/GEMINI.md`、Windsurf は `.windsurf/rules/`、Copilot は `.github/copilot-instructions.md` への追記——詳細は `rankmath-install --info <platform>` で確認。

---

## CLI チートシート

<details>
<summary><strong>ブロック貼り付けエクスポート</strong> — <code>rankmath-export</code></summary>

```bash
rankmath-export article.html                  # 記事全体をクリップボードへ
rankmath-export article.html --only howto     # HowTo ブロックのみ
rankmath-export article.html --only faq       # FAQ ブロックのみ
rankmath-export article.html --to-file out.html
rankmath-export article.html --print > out.html
rankmath-export article.html --no-validate    # ブロック検証をスキップ
```

WordPress 管理画面：**投稿 → 新規追加 → エディタ内にカーソル → Ctrl+V / Cmd+V**。
Gutenberg がブロックコメントを解析し、各ブロックを再構築します。

</details>

<details>
<summary><strong>記事バリデーター</strong> — <code>rankmath-verify</code></summary>

```bash
rankmath-verify article.html "あなたのフォーカスキーワード"
```

サンプル出力：

```
=== article.html ===
Word count:      1495 visible words           OK above 1400 minimum
FK count:        22 visible occurrences
FK density:      1.47%                        OK in target range 1.0-1.5%
Heading balance: 12 open / 12 close           OK 12/12 (target structure)
HowTo block:     OK
FAQ block:       OK (8 questions aligned)
Forbidden:       OK none found

=== Result: 8 passed, 0 failed ===
```

</details>

<details>
<summary><strong>マルチプラットフォームインストーラー</strong> — <code>rankmath-install</code></summary>

```bash
rankmath-install --list                       # 8 プラットフォーム一覧
rankmath-install --info cursor                # 詳細を確認
rankmath-install claude-code                  # ./.claude/skills/... に設置
rankmath-install claude-code --global         # ~/.claude/skills/... に設置
rankmath-install claude-ai --to ./build       # ./build/ に zip 生成
rankmath-install --dry-run claude-code        # 書き込まずに計画表示
rankmath-install                              # インタラクティブ選択
```

</details>

<details>
<summary><strong>WP-CLI 一括修正</strong> — Python または Node（サーバーアクセス必要）</summary>

```bash
export WP_SSH_KEY=~/.ssh/id_rsa
export WP_SSH_HOST=user@your-wp-host.example.com
export WP_PATH=/path/to/wordpress

# 旧 HowTo ブロックを複数記事まとめて修正
python tools/fix-howto-block.py 8489 8478 8466
node   tools/fix-howto-block.mjs 8489 8478 8466

# FAQ JSON↔HTML 整合性を複数記事まとめて修正
python tools/regenerate-faq.py 8489 8478 8579
node   tools/regenerate-faq.mjs 8489 8478 8579
```

</details>

---

## 記事の骨格

スキルは以下の骨格に従う記事を出力します——moksaweb.com の公開記事はすべてこの構造です：

```
[オープニング段落]            ~150 文字、FK 2-3 回
[Moksa 観点]                   自然な中国語、FK 1 回、ジャーゴン無し
H2 #1   什麼是 [FK]?
H2 #2   [FK] 和 [Competitor] 怎麼選?       ← 比較テーブル
H2 #3   如何啟用這個工具?                   ← コードブロック
H2 #4   [FK] 4 步驟啟用設定                 ← HowTo ブロック
H2 #5   它能做哪些 X 工作?
H2 #6   [Persona] 怎麼用 [FK]?
H2 #7   [Killer feature] 怎麼運作?
H2 #8   進階主題或場景
H2 #9   哪裡可以找到更多官方資源?           ← YouTube 埋め込み 3 本
H2 #10  使用 [FK] 有哪些限制?               ← 6 段落
H2 #11  參考依據                             ← 外部リンク 5 本
H2 #12  常見問題 FAQ                         ← FAQ ブロック
```

結果：1,400–2,000+ 語、FK 密度 1.0–1.5%、Rank Math 80 点以上、ブロック貼り付け対応。

---

## レポジトリ構成

<details>
<summary>クリックで展開</summary>

```
rankmath-seo-wp/
├── SKILL.md                          # スキル本体（自動ロード）
├── README.md / .zh-TW / .ja / .ko    # 多言語ドキュメント
├── CLAUDE.md                         # AI がスキル本体を編集する際の規約
├── CONTRIBUTING.md                   # 人間向け貢献ガイド
├── LICENSE                           # MIT
├── package.json                      # npm メタ + 3 個の bin
│
├── assets/templates/platforms/       # 8 個のプラットフォーム設定
│   ├── claude-code.json              # full
│   ├── claude-ai.json                # zip-upload
│   ├── cursor.json                   # rule (.mdc + globs)
│   ├── codex-cli.json                # full (.agents/skills/ optional)
│   ├── gemini-cli.json               # full (SKILL.md standard)
│   ├── windsurf.json                 # rule (.devin/rules, model_decision)
│   ├── copilot.json                  # full (.github/skills/)
│   └── continue.json                 # rule (alwaysApply)
│
├── data/                             # 構造化 CSV リファレンス
│   ├── focus-keyword-density.csv
│   ├── h2-templates.csv
│   ├── faq-topics.csv
│   ├── power-words.csv
│   └── platforms.csv
│
├── references/                       # 詳細ガイド
│   ├── article-template.md
│   ├── howto-block.md
│   ├── faq-block.md
│   ├── seo-checklist.md              # Rank Math 100 点の内訳
│   ├── moksa-style.md                # Moksa 観点の文体ガイド
│   ├── image-specs.md                # アイキャッチ画像 PIL テンプレ
│   └── wp-cli-pitfalls.md            # WP-CLI デプロイの落とし穴 9 個
│
├── tools/                            # ツインツール（Python + Node）
│   ├── verify-article.py    / .mjs   # FK 密度・構造の検証
│   ├── export-blocks.py     / .mjs   # ブロックペースト出力
│   ├── install-skill.py     / .mjs   # マルチプラットフォーム設置
│   ├── regenerate-faq.py    / .mjs   # FAQ JSON↔HTML 整合修正（一括対応）
│   └── fix-howto-block.py   / .mjs   # 旧 HowTo フォーマット変換（一括対応）
│
└── examples/
    └── sample-article.html
```

</details>

---

## 解決できる問題

30 本以上の記事を出してきた中で、繰り返し当たった痛み：

| 問題 | このスキルの対処 |
|------|-----------------|
| Rank Math スコアが 60 未満 | `references/seo-checklist.md` の 100 点チェックリスト |
| FK 密度 3% 超（キーワード詰め込み） | 配分表：5 H2 + 4 FAQ + 本文 |
| FK 密度 0.5%（低すぎ警告） | `verify-article.{py,mjs}` で自動測定 |
| HowTo「予期しない内容」エラー | `references/howto-block.md` の 8594 正規フォーマット |
| FAQ ブロックのバリデーションエラー | `regenerate-faq.{py,mjs}` で JSON ↔ HTML を整合 |
| `<script>` JSON-LD が生テキスト表示 | スキルが inline script を明示的に禁止 |
| H2 に「HowTo Schema」が混入 | スキルと検証器の両方が検出 |
| Windows Python が `\r\n` で書き込み | ツール側で `newline='\n'` を強制 |
| `--post_content="$(cat)"` がエラー | `wp post update file.html` 構文を案内 |
| SEO タイトルに数字なし警告 | `[FK] 完整教學：N 大功能` テンプレートで強制 |
| **サーバー SSH 権限なし** | **`rankmath-export` がブロックペースト用 HTML をクリップボードへ** |

---

## 別ジャンルへの応用

中国語の技術チュートリアル向けですが、ルール自体は汎用です：

- `Moksa 觀點` の冒頭をブランド独自の決め言葉に差し替え
- `references/article-template.md` の H2 構造を業界に合わせて再構成
- FK 密度 1.0–1.5% は多くの言語で通用
- `references/wp-cli-pitfalls.md` の WP ホスト / パスを自分の環境に
- `references/image-specs.md` のベース画像パスを自分の環境に

---

## オープンスタンダード

[Anthropic Agent Skills 規格](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) に準拠：
`SKILL.md` + YAML frontmatter (`name`、`description`) + フラットな reference ファイル。
複数 AI プラットフォーム互換。

---

## 作者

<table>
<tr>
<td>

**[moksa](https://moksaweb.com)** —— [moksaweb.com](https://moksaweb.com) のオーナー。公開した Claude AI チュートリアル記事すべてで実戦使用されているスキルです。

30+ 本分の Rank Math デバッグ経験を、再利用可能なマルチプラットフォーム・多言語ツールキットに凝縮しました。

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

このスキルが Rank Math のデバッグ時間を短縮できたなら、GitHub での star や [moksaweb.com](https://moksaweb.com) への被リンクを歓迎します。

---

## ライセンスと貢献

MIT — [LICENSE](LICENSE) をご参照ください。Copyright © 2026 moksa (moksaweb.com)。

PR 歓迎—— [CONTRIBUTING.md](CONTRIBUTING.md) を参照。特に：

- 翻訳（EN、zh-TW、ja、ko 以外のロケール）
- 追加の修正ツール（画像破損、外部リンク切れなど）
- 別業界向けの記事テンプレート（EC、ニュース、ファイナンスなど）
- 他 SEO プラグイン（Yoast、AIOSEO、SEOPress 等）の検証ルール

---

<div align="center">
  <sub><a href="https://moksaweb.com">moksa</a> 制作 · <a href="https://github.com/Moksa1123/rankmath-seo-wp">GitHub</a> · <a href="https://www.npmjs.com/package/rankmath-seo-wp">npm</a></sub>
</div>
