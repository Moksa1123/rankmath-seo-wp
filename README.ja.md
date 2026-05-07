<h1 align="center">Rank Math SEO WP — Agent Skill</h1>

<p align="center">
  <strong>Rank Math 80 点以上の WordPress 記事を AI が生成 — クリップボードにコピーして貼るだけで Gutenberg ブロックが復元、SSH 不要</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
  <a href="https://moksaweb.com"><img src="https://img.shields.io/badge/author-moksa-orange?style=flat-square" alt="moksa"></a>
</p>

<p align="center">
  <strong>言語：</strong>
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <strong>日本語</strong> ·
  <a href="README.ko.md">한국어</a>
</p>

---

[moksaweb.com](https://moksaweb.com) で公開された 30 本以上の Claude AI チュートリアル記事で実戦検証されたスキルです。
ワンライナーインストーラーで **8 つの AI プラットフォーム** に対応——Claude Code、Claude.ai、Cursor、OpenAI Codex CLI、Gemini CLI、Windsurf、GitHub Copilot、Continue——
さらに [Anthropic Agent Skills 規格](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) に準拠したあらゆる AI ツールで動作します。

## ハイライト

- **Gutenberg ブロックのコピー＆ペースト出力** — 記事全体をクリップボードにコピーして WP ブロックエディタへ貼るだけで、HowTo / FAQ / YouTube 埋め込み / テーブル すべてが復元されます。**SSH や WP-CLI は不要**。
- **Python + Node のツインツール** — 各 CLI を `.py` と `.mjs` の両方で提供。手元の環境に合わせて選択。
- **構造化 CSV リファレンスデータ** — 密度バンド、H2 テンプレート、FAQ トピック、SEO パワーワード。ツールも人間も読めます。
- **検証ツール** — FK 密度（1.0–1.5% スイートスポット）、12 H2 構造、HowTo / FAQ JSON↔HTML 整合性、禁止パターン を自動チェック。
- **マルチプラットフォーム対応表** — Claude / Claude.ai / Cursor / Codex / Gemini CLI / Windsurf / Copilot / Continue の設置先を `data/platforms.csv` に整理。

## このスキルでできること

AI が次のような依頼を検出すると自動で発動します：

- 「WordPress の記事を X について書いて」
- "Write a WP article about X with Rank Math SEO"
- 「moksaweb.com 用に Y のブログを書いて」
- 「この記事を Rank Math 準拠に修正して」

出力される記事の特徴：

- **12 個の H2 構造**（オープニング + Moksa 観点 + 12 セクション、FAQ ブロックは H2 #12 配下）
- **フォーカスキーワード密度 1.0–1.5%**（自動計算、無闇に詰め込まない）
- **Rank Math HowTo ブロック**を Gutenberg 標準フォーマットで出力
- **Rank Math FAQ ブロック**の JSON ↔ HTML を完全整合
- **SEO タイトルにアラビア数字を必ず含む**（Rank Math 必須要件）
- **自然な中国語の文体**——英語ジャーゴンを並べない
- **2,000 語以上**、YouTube 埋め込み 3 本 + 外部信頼リンク 5 本

## クイックスタート — ワンライナー設置

クローン後、お使いの AI プラットフォームのインストーラーを実行します。インストーラーが各ツールの規約どおりのパス・ファイル名・frontmatter 形式に変換してスキル内容を配置します。

```bash
git clone https://github.com/Moksa1123/rankmath-seo-wp
cd rankmath-seo-wp

# サポートする 8 プラットフォームを一覧
python tools/install-skill.py --list
# または: node tools/install-skill.mjs --list
# または: npx rankmath-install --list

# 現在のプロジェクトに設置
python tools/install-skill.py claude-code   # full install -> .claude/skills/rankmath-seo-wp/
python tools/install-skill.py cursor        # rule         -> .cursor/rules/rankmath-seo-wp.mdc
python tools/install-skill.py copilot       # 追記         -> .github/copilot-instructions.md
python tools/install-skill.py claude-ai --to ./build  # zip -> build/rankmath-seo-wp.zip

# ユーザーグローバル設置（プラットフォームが対応している場合）
python tools/install-skill.py claude-code --global   # ~/.claude/skills/rankmath-seo-wp/

# 書き込まずに計画だけ表示
python tools/install-skill.py --info cursor
python tools/install-skill.py --dry-run claude-code
```

### サポートプラットフォーム

| プラットフォーム    | Key            | 設置タイプ           | デフォルトパス                                          |
|--------------------|----------------|----------------------|--------------------------------------------------------|
| Claude Code        | `claude-code`  | full                 | `.claude/skills/rankmath-seo-wp/SKILL.md`              |
| Claude.ai (web)    | `claude-ai`    | zip-upload           | `./rankmath-seo-wp.zip` → 設定 → Skills → アップロード |
| Cursor             | `cursor`       | rule                 | `.cursor/rules/rankmath-seo-wp.mdc`                    |
| OpenAI Codex CLI   | `codex-cli`    | full                 | `.codex/skills/rankmath-seo-wp/SKILL.md`               |
| Gemini CLI         | `gemini-cli`   | full                 | `.gemini/extensions/rankmath-seo-wp/GEMINI.md`         |
| Windsurf           | `windsurf`     | rule                 | `.windsurf/rules/rankmath-seo-wp.md`                   |
| GitHub Copilot     | `copilot`      | instructions-append  | `.github/copilot-instructions.md`                      |
| Continue           | `continue`     | rule                 | `.continue/rules/rankmath-seo-wp.md`                   |

Codex CLI と Gemini CLI は best-effort 対応です。ご自身のバージョンの公式ドキュメントを必ず確認してください。

### 設置後に試す

AI ツールを再起動して：

```
> Claude Code Hooks のチュートリアル記事を書いて
```

### 設置せずリファレンスとして使う

インストーラーを実行しなくても `references/` と `data/` だけで十分実用的です。

## 2 つのデリバリーパス

WordPress サーバーへの SSH アクセスの有無で 2 ルートを使い分けられます。

### Path A · ブロックペースト（SSH 不要）

```bash
# 1. 検証
python tools/verify-article.py article.html "あなたのフォーカスキーワード"
# または: node tools/verify-article.mjs article.html "あなたのフォーカスキーワード"

# 2. 出力 — 「貼ればそのまま」HTML をクリップボードにコピー
python tools/export-blocks.py article.html
# または: npx rankmath-export article.html

# 3. WP 管理画面: 投稿 → 新規追加 → エディタ内にカーソル → Ctrl+V / Cmd+V
```

Gutenberg は貼り付けられた `<!-- wp:... -->` のブロックコメントを解析し、HowTo / FAQ / YouTube 埋め込み / テーブル / コードブロック まで完全復元します。あとはサイドバーで Rank Math のメタ情報（フォーカスキーワード、数字を含む SEO タイトル、メタ説明、スラッグ）を設定し、アイキャッチ画像をアップロードするだけ。

特定のブロックだけ抽出：

```bash
python tools/export-blocks.py article.html --only howto   # HowTo のみ
python tools/export-blocks.py article.html --only faq     # FAQ のみ
```

ファイル出力：

```bash
python tools/export-blocks.py article.html --to-file ready.html
python tools/export-blocks.py article.html --print > ready.html
```

### Path B · WP-CLI 一括（サーバーアクセスあり）

```bash
export WP_SSH_KEY=~/.ssh/id_rsa
export WP_SSH_HOST=user@your-wp-host.example.com
export WP_PATH=/path/to/wordpress

# 旧 HowTo ブロックを複数記事まとめて修正
python tools/fix-howto-block.py 8489 8478 8466

# FAQ 整合性を複数記事まとめて修正
python tools/regenerate-faq.py 8489 8478 8579
```

## 任意の記事を検証

```bash
python tools/verify-article.py article.html "あなたのフォーカスキーワード"
# または
node tools/verify-article.mjs article.html "あなたのフォーカスキーワード"
```

サンプル出力：

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

## フォルダ構成

```
rankmath-seo-wp/
├── SKILL.md                          # メインエントリ（自動ロード）
├── README.md                         # 英語 README
├── README.{zh-TW,ja,ko}.md           # 各言語の翻訳
├── CLAUDE.md                         # AI がスキル本体を編集する際の規約
├── CONTRIBUTING.md                   # 人間向け貢献ガイド
├── LICENSE                           # MIT
├── package.json                      # npm メタ + bin エントリ
├── data/                             # 構造化 CSV リファレンス
│   ├── focus-keyword-density.csv     # 密度バンド → 判定 + 是正案
│   ├── h2-templates.csv              # 12 H2 構造と FK 配分
│   ├── faq-topics.csv                # 8 個の FAQ トピックパターン（中・英）
│   ├── power-words.csv               # SEO タイトル用パワーワード
│   └── platforms.csv                 # 各 AI プラットフォームの設置パス
├── references/                       # 詳細ガイド（オンデマンドロード）
│   ├── article-template.md           # 12 H2 構造 + FK 配分
│   ├── howto-block.md                # rank-math/howto-block 正規フォーマット
│   ├── faq-block.md                  # FAQ JSON ↔ HTML 整合ルール
│   ├── seo-checklist.md              # Rank Math 100 点の内訳
│   ├── moksa-style.md                # Moksa 観点の文体 + 置換語表
│   ├── image-specs.md                # アイキャッチ画像仕様 + PIL テンプレ
│   └── wp-cli-pitfalls.md            # WP-CLI デプロイの落とし穴 9 個
├── tools/                            # ツインツール（Python + Node）
│   ├── verify-article.py    / .mjs   # FK 密度・構造の検証
│   ├── export-blocks.py     / .mjs   # ブロックペースト出力
│   ├── install-skill.py     / .mjs   # マルチプラットフォーム設置
│   ├── regenerate-faq.py    / .mjs   # FAQ JSON↔HTML 整合修正（WP-CLI 一括対応）
│   └── fix-howto-block.py   / .mjs   # 旧 HowTo フォーマット変換（WP-CLI 一括対応）
└── examples/
    └── sample-article.html           # 全チェック合格のサンプル記事
```

## 解決できる問題

30 本以上の記事を出してきた中で、繰り返し当たった痛みがこちら：

| 問題                                  | このスキルの対処                                          |
|---------------------------------------|-----------------------------------------------------------|
| Rank Math スコアが 60 未満             | `seo-checklist.md` の 100 点チェックリストを順守          |
| FK 密度 3% 超（キーワード詰め込み）    | `article-template.md` の配分表（5 H2 + 4 FAQ + 本文）     |
| FK 密度 0.5%（低すぎ警告）            | `verify-article.{py,mjs}` で自動測定                      |
| HowTo「予期しない内容」エラー          | `howto-block.md` の 8594 正規フォーマットを採用           |
| FAQ ブロックのバリデーションエラー    | `regenerate-faq.py` で JSON ↔ HTML を整合                 |
| `<script>` JSON-LD が生テキスト表示    | スキルが inline script を明示的に禁止                     |
| H2 に「HowTo Schema」が混入            | スキルと検証器の両方が検出                                |
| Windows Python が `\r\n` で書き込み    | ツール側で `newline='\n'` を強制                          |
| `--post_content="$(cat)"` がエラー    | `wp post update file.html` 構文を案内                     |
| SEO タイトルに数字なし警告             | `[FK] 完整教學：N 大功能` テンプレートで強制              |
| サーバー SSH 権限なし                  | `export-blocks` がブロックペースト用 HTML をクリップボードへ |

## 別ジャンルへの応用

中国語の技術チュートリアル向けに作られていますが、ルール自体は汎用です：

- `Moksa 觀點` の冒頭をブランド独自の決め言葉に差し替え
- `references/article-template.md` の H2 構造を業界に合わせて再構成
- FK 密度 1.0–1.5% は多くの言語で通用
- `references/wp-cli-pitfalls.md` の WP ホスト / パスを自分の環境に
- `references/image-specs.md` のベース画像パスを自分の環境に

## オープンスタンダード

[Anthropic Agent Skills 規格](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) に準拠：
`SKILL.md` + YAML frontmatter (`name`、`description`) + フラットな reference ファイル。
複数 AI プラットフォームで互換動作します。

## 作者

開発・メンテナンスは **moksa**——[moksaweb.com](https://moksaweb.com) のオーナーが
公開した Claude AI チュートリアルで実戦的に磨き上げたスキルです。

- Web サイト：[moksaweb.com](https://moksaweb.com)
- 作者：[moksa](https://moksaweb.com)

このスキルが Rank Math のデバッグ時間を短縮できたなら、
GitHub での ⭐ や [moksaweb.com](https://moksaweb.com) への被リンクを歓迎します。

## ライセンス

MIT — [LICENSE](LICENSE) をご参照ください。Copyright © 2026 moksa (moksaweb.com)。

## コントリビューション

[CONTRIBUTING.md](CONTRIBUTING.md) を参照。以下の PR を歓迎します：

- 翻訳（EN / zh-TW / ja / ko 以外のロケール）
- 追加の修正ツール（画像破損、外部リンク切れなど）
- 別業界向けの記事テンプレート（EC、ニュース、ファイナンスなど）
- 他 SEO プラグイン（Yoast、AIOSEO、SEOPress 等）の検証ルール

---

[moksa](https://moksaweb.com) が [Claude Code](https://claude.com/claude-code) で開発。
