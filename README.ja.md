<h1 align="center">Rank Math SEO WP Writer</h1>

<h3 align="center">Rank Math SEO 文章撰寫工具</h3>

<p align="center">
  <strong>Rank Math のテストルール · 有効な HowTo／FAQ ブロック · 公開前の検証ツール</strong>
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

<p align="center"><a href="README.md">English</a> · <a href="README.zh-TW.md">正體中文</a> · <strong>日本語</strong> · <a href="README.ko.md">한국어</a></p>

> これは非公式のコミュニティプロジェクトです。Rank Math およびその開発元が作成・承認したものではなく、関係もありません。Rank Math SEO はサードパーティ製ソフトウェアで、このリポジトリには含まれていません。

## 機能

「WordPress の記事を書いて」という依頼を、Rank Math 自身のテストに通り 80 点以上を取る記事にします。Rank Math のルールを推測する必要はありません。

| 分野 | 内容 |
|---|---|
| Rank Math のルール | Rank Math の 25 項目のテストと採点ルール（点数、しきい値、KB へのリンク）。seo-by-rank-math 1.0.282 のソースコードから読み取り |
| ブロック | 各ブロックの `save()` と同じ HowTo／FAQ マークアップで、エディターに「無効なコンテンツ」が出ません |
| 検証ツール | 単語数と密度を Rank Math と同じ方法で数え、どれか 1 項目でも不合格なら終了コード 1 を返します |
| 検索 | 中国語でも英語でも `data/` から回答し、出典を付けます |
| 公開 | クリップボードへのブロック貼り付け（サーバー権限不要）、または自分のサーバーで WP-CLI |
| ツール | すべての CLI に Python 版と Node 版があり、標準ライブラリのみ。8 つの AI プラットフォームにインストール可能 |

### ルールはプラグインから読み取り

```bash
python scripts/search.py "密度"
# [tests] keywordDensity ... <0.5 fail 0; ... up to 2.5 best 6; >2.5 fail 0
#    trust=官方原始碼  source=analyzer.js keywordDensity calculateScore (1.0.282)
```

### 公開前の検証ツール

```bash
rankmath-verify article.html "フォーカスキーワード"    # または python tools/verify-article.py
```

### SSH なしでブロックを貼り付け

```bash
rankmath-export article.html                    # 記事全体をクリップボードへ
rankmath-export article.html --only faq         # FAQ ブロックだけ
```

### ブロック修正ツール

```bash
python tools/regenerate-faq.py article.html     # JSON から FAQ の HTML を再生成
python tools/fix-howto-block.py 101 --dry       # 投稿 101 の HowTo 修正をプレビュー
```

### 解決する問題

| 問題 | この skill での対処 |
|---|---|
| 密度が高すぎる・低すぎる | `data/focus-keyword-density.csv` はプラグインの採点帯。検証ツールはプラグインと同じ数え方 |
| HowTo や FAQ ブロックに「無効なコンテンツ」 | HTML はブロックの `save()` と一致が必要。`fix-howto-block`、`regenerate-faq` が作り直します |
| JSON-LD の `<script>` が文字として表示される | rank-math ブロックを使う。検証ツールがインライン `ld+json` を検出 |
| 「Your SEO title doesn't contain a number」 | タイトルの型 `[FK] 完整教學：N 大功能` |
| `--post_content="$(cat …)"` が失敗、Windows が `\r\n` を書く | ファイルを `wp post update` に渡す。全ツールが LF で書き込み |
| サーバーへの SSH 権限がない | `rankmath-export` が貼り付け可能なブロックをコピー |

## 使う場面

| 使う | 使わない（代わりに） |
|---|---|
| Rank Math SEO を使う WordPress サイトで記事を書く・直す・公開する | その他のブロックエディターのページ → `gutenberg-headless` |
| HowTo・FAQ ブロックを含むチュートリアル、ガイド、ブログ記事（繁体字中国語でも他の言語でも） | Elementor や Mosaic のページ → `elementor-headless`、`mosaic-headless` |
| エディターが無効と表示する HowTo／FAQ ブロックの修復 | Yoast など別の SEO プラグインを使うサイト（テスト項目が異なる） |

## インストール

| 必要なもの | 用途 |
|---|---|
| Python 3.9 以上または Node.js 18 以上 | ツールの実行（標準ライブラリのみ） |
| `ssh` とサーバー側の WP-CLI | WP-CLI で公開・一括修正する場合のみ |
| Windows、macOS、Linux | すべて |

### Step 1：インストール方法を選ぶ

Claude plugin（Claude Code。Claude 公式ディレクトリに掲載後はそこからも可）：

```
/plugin marketplace add Moksa1123/rankmath-seo-wp
/plugin install rankmath-seo-wp@rankmath-seo-wp
```

npx（Claude Code と下表の他の AI ツール）：

```bash
npx -p rankmath-seo-wp@1.2.2 rankmath-install claude-code --global
npx -p rankmath-seo-wp@1.2.2 rankmath-install --list
```

手動コピー：

```bash
git clone https://github.com/Moksa1123/rankmath-seo-wp.git
cp -r rankmath-seo-wp ~/.claude/skills/rankmath-seo-wp
```

| プラットフォーム | キー | 方式 | 既定のパス |
|---|---|---|---|
| Claude Code | `claude-code` | full | `.claude/skills/rankmath-seo-wp/SKILL.md` |
| Claude.ai（Web） | `claude-ai` | zip-upload | `./rankmath-seo-wp.zip` → Settings → Skills |
| Cursor | `cursor` | rule | `.cursor/rules/rankmath-seo-wp.mdc` |
| OpenAI Codex CLI | `codex-cli` | full | `.codex/skills/rankmath-seo-wp/SKILL.md` |
| Gemini CLI | `gemini-cli` | full | `.gemini/skills/rankmath-seo-wp/SKILL.md` |
| Devin Desktop（旧 Windsurf） | `windsurf` | rule | `.devin/rules/rankmath-seo-wp.md` |
| GitHub Copilot | `copilot` | full | `.github/skills/rankmath-seo-wp/SKILL.md` |
| Continue | `continue` | rule | `.continue/rules/rankmath-seo-wp.md` |

## クイックスタート

### Step 2：記事をチェック

```bash
npx -p rankmath-seo-wp@1.2.2 rankmath-verify examples/sample-article.html "Claude Skills"
```

```
FK density:      1.96%
                 OK full score band 1.0-2.5% (6/6; KB recommends 1.0-1.5%)
...
=== Result: 8 passed, 0 failed ===
```

### Step 3：アシスタントに頼む

| 頼み方 | 何が起きるか |
|---|---|
| 「Claude Code Hooks についての WordPress チュートリアルを書いて。フォーカスキーワードは Claude Code Hooks。」 | 記事を書き、検証ツールを実行 |
| 「この記事の FAQ ブロックが無効なコンテンツと表示される。直して。」 | ブロックの JSON から FAQ の HTML を再生成 |
| 「Rank Math でキーワード密度はどれくらいなら満点？」 | `data/` を調べ、プラグインのルールを引用 |

| CLI | 役割 |
|---|---|
| `rankmath-verify article.html "FK"` | 記事を採点。全項目合格なら exit 0 |
| `rankmath-export article.html` | 貼り付け可能なブロックをコピー（`--only faq`、`--to-file`、`--print`） |
| `rankmath-install <platform>` | AI ツールにインストール（`--list`、`--info`、`--global`） |
| `python scripts/search.py "<語句>"` | Rank Math のルール、ブロックのマークアップ、サイトのルールを検索 |
| `python tools/regenerate-faq.py <ファイルまたは投稿 ID>` | JSON から FAQ の HTML を再生成（`--dry` でプレビュー） |
| `python tools/fix-howto-block.py <ファイルまたは投稿 ID>` | 古い HowTo マークアップを変換（`--dry` でプレビュー） |

全出力、すべてのオプション、記事の構成：[docs/guide.md](docs/guide.md)。

## トリガーフレーズ

English: write a WordPress article, blog post or tutorial, Rank Math score, SEO green light, focus keyword density, FAQ block, HowTo block, block contains invalid content, publish with WP-CLI.

中文：寫 WordPress 文章、部落格文章、教學文、Rank Math 分數、SEO 綠燈、焦點關鍵字密度、FAQ 區塊、HowTo 區塊、區塊無效內容、WP-CLI 發文。

## 実行する内容と接続先

勝手には何も動きません。この plugin にはフック、MCP サーバー、バックグラウンド処理がありません。Claude が `SKILL.md` に従い、あなたがコマンドを承認したときだけツールが動きます。

| ツール | 読むもの | 書くもの | 接続先 |
|---|---|---|---|
| `scripts/search.py`、`tools/verify-article.*`、セルフテスト、数値チェック | このフォルダーのファイル、指定した記事 | なし | なし |
| `rankmath-export` | 記事 | クリップボード（`clip`、`pbcopy`、`xclip`、`xsel`、`wl-copy`）または指定したファイル | なし |
| `rankmath-install` | このフォルダー | AI ツールの skill／rule フォルダー（プロジェクト内、または `--global` でホームフォルダー）、または zip | なし |
| `regenerate-faq`、`fix-howto-block` にローカルの `.html` | そのファイル | そのファイル | なし |
| `regenerate-faq`、`fix-howto-block` に投稿 ID | 投稿（`wp post get`） | 投稿（`wp post update`、日付は維持）、サーバーの `/tmp` の一時ファイル（実行後も残る） | あなたのサーバー（`ssh`） |
| 公開（依頼されたとき Claude が WP-CLI を実行） | あなたの WordPress | 投稿、Rank Math の項目（`rank_math_focus_keyword`、`rank_math_title`、`rank_math_description`）、カテゴリー、スラッグ、アイキャッチ画像 | あなたのサーバー（`ssh`） |

| 設定 | 環境変数 | `userConfig` キー | 例 |
|---|---|---|---|
| SSH のユーザーとホスト | `WP_SSH_HOST` | `wp_ssh_host` | `user@your-wp-host.example.com` |
| SSH 秘密鍵のパス | `WP_SSH_KEY` | `wp_ssh_key` | `~/.ssh/id_rsa`（未設定時に使用） |
| サーバー上の WordPress のパス | `WP_PATH` | `wp_path` | `/path/to/wordpress` |

plugin としてインストールすると、Claude Code がこれらを `userConfig` の値として尋ねます。ツールを実行するときは上の環境変数名でエクスポートしてください。秘密鍵はあなたのマシンから出ず、`ssh` がログインに使うだけです。WordPress のパスワードや API キーは不要で、インストール時に何もダウンロードせず、作者や第三者にデータを送りません。

## 検証方法

| 項目 | 結果 | 根拠 |
|---|---|---|
| Rank Math のルール | seo-by-rank-math 1.0.282（`analyzer.js`、HowTo／FAQ の `save()` と `block.json`）から読み取り、2026-11-15 に [Rank Math KB](https://rankmath.com/kb/score-100-in-tests/) と照合 | `data/rankmath-tests.csv`、`data/blocks.csv` |
| サイト独自の慣例 | サイトのスタイルとして区別し、Rank Math のルールとは扱わない | `data/site-rules.csv` |
| 単語カウント | 比較したすべてのファイルで `@wordpress/wordcount` パッケージと一致 | `scripts/test_verify.py` |
| セルフテスト | オフラインの 35 項目：Python 版と Node 版の一致、壊れた記事は不合格、しきい値とデータの一致 | `python scripts/test_verify.py` |
| evals | 11 問。skill ありで 11/11、なしで 0/11 | [evals/RESULTS.md](evals/RESULTS.md) |
| 文書の数値 | `SKILL.md` とこれらの README の数値はすべてデータと一致 | `python scripts/check_numbers.py` |

## 制限

| 制限 | 内容 |
|---|---|
| Rank Math のバージョン | ルールは Rank Math 1.0.282（無料版）から読み取り。Pro 専用のテストや新しいバージョンは読み直しが必要 |
| 検証ツールが見る範囲 | 記事の HTML のみ。SEO タイトル、メタディスクリプション、スラッグ、リンク、画像は Rank Math のサイドバーで確認 |
| 実機との照合 | 検証ツールの数値は、実際の Rank Math サイドバーとまだ照合していません |
| プラットフォームのパス | 他の AI ツールのインストール先は最新の文書でまだ再確認していません（[data/platforms.csv](data/platforms.csv)） |
| 未解決の質問 | [data/pending.csv](data/pending.csv) |

## リポジトリ構成

```
SKILL.md          アシスタントが読み込む内容：出典、ルーティング、タスク、検証
data/             Rank Math のテスト、ブロックのマークアップ、サイトのルール（CSV）、未解決リスト
references/       ブロック形式、チェックリスト、文体、WP-CLI の落とし穴
scripts/          search.py（入口）、セルフテスト、数値チェック
tools/            検証、エクスポート、インストール、FAQ／HowTo 修正（Python＋Node）
examples/         検証ツールに通るサンプル記事
evals/            採点問題と結果
docs/             詳しいガイド
.claude-plugin/   plugin と marketplace のマニフェスト
```

## ライセンスと作者

MIT ライセンス。作者 Moksa（[moksaweb.com](https://moksaweb.com)）。問題の報告：[GitHub](https://github.com/Moksa1123/rankmath-seo-wp/issues)。
