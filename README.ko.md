<h1 align="center">Rank Math SEO WP Writer</h1>

<h3 align="center">Rank Math SEO 文章撰寫工具</h3>

<p align="center">
  <strong>Rank Math 테스트 규칙 · 유효한 HowTo/FAQ 블록 · 게시 전 검증기</strong>
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

<p align="center"><a href="README.md">English</a> · <a href="README.zh-TW.md">正體中文</a> · <a href="README.ja.md">日本語</a> · <strong>한국어</strong></p>

> 이 프로젝트는 비공식 커뮤니티 프로젝트입니다. Rank Math 또는 그 개발사가 만들거나 보증한 것이 아니며 관계도 없습니다. Rank Math SEO는 서드파티 소프트웨어이며 이 저장소에 포함되어 있지 않습니다.

## 기능

"WordPress 글을 써 줘"라는 요청을, Rank Math 자체 테스트를 통과하고 80점 이상을 받는 글로 바꿉니다. Rank Math 규칙을 추측할 필요가 없습니다.

| 영역 | 내용 |
|---|---|
| Rank Math 규칙 | 점수, 기준값, KB 링크를 포함한 25개 테스트와 채점 규칙. seo-by-rank-math 1.0.282 소스 코드에서 읽음 |
| 블록 | 각 블록의 `save()`와 같은 HowTo/FAQ 마크업이라 에디터에 "유효하지 않은 콘텐츠"가 뜨지 않음 |
| 검증기 | 단어 수와 밀도를 Rank Math와 같은 방식으로 세며, 하나라도 실패하면 종료 코드 1을 반환 |
| 검색 | 중국어나 영어 질문을 `data/`에서 답하고 출처를 붙임 |
| 게시 | 클립보드로 블록 붙여 넣기(서버 권한 불필요) 또는 자신의 서버에서 WP-CLI |
| 도구 | 모든 CLI에 Python·Node 버전이 있고 표준 라이브러리만 사용. 8개 AI 플랫폼에 설치 가능 |

### 규칙은 플러그인에서 직접

```bash
python scripts/search.py "密度"
# [tests] keywordDensity ... <0.5 fail 0; ... up to 2.5 best 6; >2.5 fail 0
#    trust=官方原始碼  source=analyzer.js keywordDensity calculateScore (1.0.282)
```

### 게시 전 검증기

```bash
rankmath-verify article.html "포커스 키워드"    # 또는 python tools/verify-article.py
```

### SSH 없이 블록 붙여 넣기

```bash
rankmath-export article.html                    # 글 전체를 클립보드로
rankmath-export article.html --only faq         # FAQ 블록만
```

### 블록 수정 도구

```bash
python tools/regenerate-faq.py article.html     # JSON에서 FAQ HTML 다시 생성
python tools/fix-howto-block.py 101 --dry       # 글 101의 HowTo 수정 미리 보기
```

### 해결하는 문제

| 문제 | 이 skill의 해결 방법 |
|---|---|
| 밀도가 너무 높거나 낮음 | `data/focus-keyword-density.csv`는 플러그인의 채점 구간. 검증기는 플러그인과 같은 방식으로 셈 |
| HowTo나 FAQ 블록에 "유효하지 않은 콘텐츠" | HTML이 블록의 `save()`와 같아야 함. `fix-howto-block`, `regenerate-faq`가 다시 만듦 |
| JSON-LD `<script>`가 글자로 보임 | rank-math 블록 사용. 검증기가 인라인 `ld+json`을 잡아냄 |
| "Your SEO title doesn't contain a number" | 제목 템플릿 `[FK] 完整教學：N 大功能` |
| `--post_content="$(cat …)"` 실패, Windows가 `\r\n`을 씀 | 파일을 `wp post update`에 넘김. 모든 도구가 LF로 씀 |
| 서버 SSH 권한이 없음 | `rankmath-export`가 붙여 넣을 수 있는 블록을 복사 |

## 사용 시점

| 사용 | 사용하지 않음(대신) |
|---|---|
| Rank Math SEO를 쓰는 WordPress 사이트에서 글을 쓰거나 고치거나 게시 | 그 밖의 블록 에디터 페이지 → `gutenberg-headless` |
| HowTo·FAQ 블록이 들어간 튜토리얼, 가이드, 블로그 글(번체 중국어 또는 다른 언어) | Elementor나 Mosaic 페이지 → `elementor-headless`, `mosaic-headless` |
| 에디터가 유효하지 않다고 표시한 HowTo/FAQ 블록 복구 | Yoast 등 다른 SEO 플러그인을 쓰는 사이트(테스트 항목이 다름) |

## 설치

| 필요한 것 | 용도 |
|---|---|
| Python 3.9 이상 또는 Node.js 18 이상 | 도구 실행(표준 라이브러리만 사용) |
| `ssh`와 서버의 WP-CLI | WP-CLI로 게시하거나 일괄 수정할 때만 |
| Windows, macOS, Linux | 전체 |

### Step 1: 설치 방법 선택

Claude plugin(Claude Code. Claude 공식 디렉터리에 등록된 뒤에는 디렉터리에서도 가능):

```
/plugin marketplace add Moksa1123/rankmath-seo-wp
/plugin install rankmath-seo-wp@rankmath-seo-wp
```

npx(Claude Code와 아래 표의 다른 AI 도구):

```bash
npx -p rankmath-seo-wp@1.2.0 rankmath-install claude-code --global
npx -p rankmath-seo-wp@1.2.0 rankmath-install --list
```

수동 복사:

```bash
git clone https://github.com/Moksa1123/rankmath-seo-wp.git
cp -r rankmath-seo-wp ~/.claude/skills/rankmath-seo-wp
```

| 플랫폼 | 키 | 방식 | 기본 경로 |
|---|---|---|---|
| Claude Code | `claude-code` | full | `.claude/skills/rankmath-seo-wp/SKILL.md` |
| Claude.ai(웹) | `claude-ai` | zip-upload | `./rankmath-seo-wp.zip` → Settings → Skills |
| Cursor | `cursor` | rule | `.cursor/rules/rankmath-seo-wp.mdc` |
| OpenAI Codex CLI | `codex-cli` | full | `.codex/skills/rankmath-seo-wp/SKILL.md` |
| Gemini CLI | `gemini-cli` | full | `.gemini/skills/rankmath-seo-wp/SKILL.md` |
| Devin Desktop(이전 Windsurf) | `windsurf` | rule | `.devin/rules/rankmath-seo-wp.md` |
| GitHub Copilot | `copilot` | full | `.github/skills/rankmath-seo-wp/SKILL.md` |
| Continue | `continue` | rule | `.continue/rules/rankmath-seo-wp.md` |

## 빠른 시작

### Step 2: 글 검사

```bash
npx -p rankmath-seo-wp@1.2.0 rankmath-verify examples/sample-article.html "Claude Skills"
```

```
FK density:      1.96%
                 OK full score band 1.0-2.5% (6/6; KB recommends 1.0-1.5%)
...
=== Result: 8 passed, 0 failed ===
```

### Step 3: 어시스턴트에게 요청

| 요청 | 결과 |
|---|---|
| "Claude Code Hooks에 관한 WordPress 튜토리얼을 써 줘. 포커스 키워드는 Claude Code Hooks야." | 글을 쓰고 검증기를 실행 |
| "이 글의 FAQ 블록에 유효하지 않은 콘텐츠라고 나와. 고쳐 줘." | 블록의 JSON에서 FAQ HTML을 다시 생성 |
| "Rank Math에서 키워드 밀도가 얼마면 만점이야?" | `data/`를 찾아 플러그인 규칙을 인용 |

| CLI | 역할 |
|---|---|
| `rankmath-verify article.html "FK"` | 글 채점. 모두 통과하면 exit 0 |
| `rankmath-export article.html` | 붙여 넣을 수 있는 블록 복사(`--only faq`, `--to-file`, `--print`) |
| `rankmath-install <platform>` | AI 도구에 설치(`--list`, `--info`, `--global`) |
| `python scripts/search.py "<검색어>"` | Rank Math 규칙, 블록 마크업, 사이트 규칙 검색 |
| `python tools/regenerate-faq.py <파일 또는 글 ID>` | JSON에서 FAQ HTML 다시 생성(`--dry`로 미리 보기) |
| `python tools/fix-howto-block.py <파일 또는 글 ID>` | 옛 HowTo 마크업 변환(`--dry`로 미리 보기) |

전체 출력, 모든 옵션, 글 구성: [docs/guide.md](docs/guide.md).

## 트리거 문구

English: write a WordPress article, blog post or tutorial, Rank Math score, SEO green light, focus keyword density, FAQ block, HowTo block, block contains invalid content, publish with WP-CLI.

中文：寫 WordPress 文章、部落格文章、教學文、Rank Math 分數、SEO 綠燈、焦點關鍵字密度、FAQ 區塊、HowTo 區塊、區塊無效內容、WP-CLI 發文。

## 실행 내용과 연결 대상

스스로 실행되는 것은 없습니다. 이 plugin에는 훅, MCP 서버, 백그라운드 프로세스가 없습니다. Claude가 `SKILL.md`를 따르고 사용자가 명령을 승인할 때만 도구가 실행됩니다.

| 도구 | 읽는 것 | 쓰는 것 | 연결 대상 |
|---|---|---|---|
| `scripts/search.py`, `tools/verify-article.*`, 자체 테스트, 숫자 검사 | 이 폴더의 파일, 지정한 글 | 없음 | 없음 |
| `rankmath-export` | 글 | 클립보드(`clip`, `pbcopy`, `xclip`, `xsel`, `wl-copy`) 또는 지정한 파일 | 없음 |
| `rankmath-install` | 이 폴더 | AI 도구의 skill/rule 폴더(프로젝트 안, 또는 `--global`이면 홈 폴더) 또는 zip | 없음 |
| `regenerate-faq`, `fix-howto-block`에 로컬 `.html` | 그 파일 | 그 파일 | 없음 |
| `regenerate-faq`, `fix-howto-block`에 글 ID | 글(`wp post get`) | 글(`wp post update`, 날짜 유지), 서버 `/tmp`의 임시 파일(실행 후에도 남음) | 사용자 서버(`ssh`) |
| 게시(요청하면 Claude가 WP-CLI 실행) | 사용자의 WordPress | 글, Rank Math 필드(`rank_math_focus_keyword`, `rank_math_title`, `rank_math_description`), 카테고리, 슬러그, 대표 이미지 | 사용자 서버(`ssh`) |

| 설정 | 환경 변수 | `userConfig` 키 | 예 |
|---|---|---|---|
| SSH 사용자와 호스트 | `WP_SSH_HOST` | `wp_ssh_host` | `user@your-wp-host.example.com` |
| SSH 개인 키 경로 | `WP_SSH_KEY` | `wp_ssh_key` | `~/.ssh/id_rsa`(없을 때 사용) |
| 서버의 WordPress 경로 | `WP_PATH` | `wp_path` | `/path/to/wordpress` |

plugin으로 설치하면 Claude Code가 이 값들을 `userConfig`로 물어봅니다. 도구를 실행할 때는 위 환경 변수 이름으로 내보내세요. 개인 키는 사용자의 컴퓨터를 떠나지 않고 `ssh`가 로그인에만 씁니다. WordPress 비밀번호나 API 키는 필요 없고, 설치할 때 아무것도 내려받지 않으며, 작성자나 다른 누구에게도 데이터를 보내지 않습니다.

## 검증 방법

| 항목 | 결과 | 근거 |
|---|---|---|
| Rank Math 규칙 | seo-by-rank-math 1.0.282(`analyzer.js`, HowTo/FAQ의 `save()`와 `block.json`)에서 읽고, 2026-11-15에 [Rank Math KB](https://rankmath.com/kb/score-100-in-tests/)와 대조 | `data/rankmath-tests.csv`, `data/blocks.csv` |
| 사이트 관례 | 사이트 스타일로 구분하고 Rank Math 규칙으로 취급하지 않음 | `data/site-rules.csv` |
| 단어 수 계산 | 비교한 모든 파일에서 `@wordpress/wordcount` 패키지와 같음 | `scripts/test_verify.py` |
| 자체 테스트 | 오프라인 테스트 30개: Python·Node 검증기 일치, 망가진 글은 실패, 기준값과 데이터 일치 | `python scripts/test_verify.py` |
| evals | 11문항. skill 사용 시 11/11, 미사용 시 0/11 | [evals/RESULTS.md](evals/RESULTS.md) |
| 문서의 숫자 | `SKILL.md`와 이 README들의 모든 숫자가 데이터와 일치 | `python scripts/check_numbers.py` |

## 제한 사항

| 제한 | 내용 |
|---|---|
| Rank Math 버전 | 규칙은 Rank Math 1.0.282(무료 버전)에서 읽음. Pro 전용 테스트와 이후 버전은 다시 읽어야 함 |
| 검증기가 보는 범위 | 글의 HTML만. SEO 제목, 메타 설명, 슬러그, 링크, 이미지는 Rank Math 사이드바에서 확인 |
| 실제 대조 | 검증기의 숫자는 아직 실제 Rank Math 사이드바와 대조하지 않음 |
| 플랫폼 경로 | 다른 AI 도구의 설치 경로는 최신 문서로 아직 재확인하지 않음([data/platforms.csv](data/platforms.csv)) |
| 미해결 질문 | [data/pending.csv](data/pending.csv) |

## 저장소 구조

```
SKILL.md          어시스턴트가 읽는 내용: 출처, 라우팅, 작업, 검증
data/             Rank Math 테스트, 블록 마크업, 사이트 규칙(CSV), 미해결 목록
references/       블록 형식, 체크리스트, 문체, WP-CLI 함정
scripts/          search.py(진입점), 자체 테스트, 숫자 검사
tools/            검증, 내보내기, 설치, FAQ/HowTo 수정(Python + Node)
examples/         검증기를 통과하는 예제 글
evals/            채점 문항과 결과
docs/             자세한 가이드
.claude-plugin/   plugin과 marketplace 매니페스트
```

## 라이선스와 작성자

MIT 라이선스. 작성자 Moksa([moksaweb.com](https://moksaweb.com)). 이슈: [GitHub](https://github.com/Moksa1123/rankmath-seo-wp/issues).
