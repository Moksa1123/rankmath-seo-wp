<h1 align="center">Rank Math SEO WP — Agent Skill</h1>

<p align="center">
  <strong>Rank Math 80점 이상의 WordPress 글을 AI 가 작성 — 클립보드에서 바로 복사 → 붙여넣기로 Gutenberg 블록 복원, SSH 불필요</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
  <a href="https://moksaweb.com"><img src="https://img.shields.io/badge/author-moksa-orange?style=flat-square" alt="moksa"></a>
</p>

<p align="center">
  <strong>언어:</strong>
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <strong>한국어</strong>
</p>

---

[moksaweb.com](https://moksaweb.com) 에서 발행된 30 편 이상의 Claude AI 튜토리얼에서 실전 검증된 Skill 입니다.
한 줄 인스톨러로 **8 개 AI 플랫폼** 지원 — Claude Code, Claude.ai, Cursor, OpenAI Codex CLI, Gemini CLI, Windsurf, GitHub Copilot, Continue —
그리고 [Anthropic Agent Skills 표준](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) 을 지원하는 모든 AI 도구와 호환됩니다.

## 핵심 특징

- **Gutenberg 블록 붙여넣기 출력** — 글 전체를 클립보드에 복사 후 WP 블록 에디터에 붙여넣기만 하면 HowTo / FAQ / YouTube 임베드 / 테이블이 모두 복원됨. **SSH 또는 WP-CLI 불필요**.
- **Python + Node 트윈 도구** — 모든 CLI 가 `.py` 와 `.mjs` 두 버전 제공. 사용 환경에 맞춰 선택 가능.
- **구조화된 CSV 레퍼런스 데이터** — 키워드 밀도 구간, H2 템플릿, FAQ 주제, SEO 파워 워드. 도구와 사람이 함께 읽음.
- **검증 도구** — FK 밀도 (1.0–1.5% 스위트 스폿), 12 H2 구조, HowTo / FAQ JSON↔HTML 정합성, 금지 패턴 자동 검사.
- **멀티 플랫폼 설치 표** — Claude / Claude.ai / Cursor / Codex / Gemini CLI / Windsurf / Copilot / Continue (`data/platforms.csv`).

## 이 Skill 이 하는 일

다음과 같은 요청을 감지하면 자동으로 작동합니다:

- 「WordPress 글을 X 주제로 써줘」
- "Write a WP article about X with Rank Math SEO"
- "moksaweb.com 에 Y 관련 블로그 글 작성"
- "이 글을 Rank Math 기준에 맞게 수정"

다음을 만족하는 글을 출력합니다:

- **12 개 H2 구조** (도입 + Moksa 관점 + 12 개 섹션, FAQ 블록은 H2 #12 아래)
- **포커스 키워드 밀도 1.0–1.5%** (계산 기반, 단순 채워넣기 금지)
- **Rank Math HowTo 블록**을 표준 Gutenberg 포맷으로 출력
- **Rank Math FAQ 블록** JSON ↔ HTML 정합성 보장
- **SEO 제목에 아라비아 숫자 포함 필수** (Rank Math 강제 요건)
- **자연스러운 중국어 문체** — 영어 전문용어 남발 금지
- **2,000 단어 이상**, YouTube 임베드 3 개 + 외부 권위 링크 5 개

## 빠른 시작 — 한 줄 설치

클론 후 사용 중인 AI 플랫폼의 인스톨러를 실행하세요. 인스톨러가 각 도구의 규약에 맞춰 경로 / 파일명 / frontmatter 를 자동으로 변환해 Skill 내용을 배치합니다.

```bash
git clone https://github.com/Moksa1123/rankmath-seo-wp
cd rankmath-seo-wp

# 지원하는 8 개 플랫폼 목록
python tools/install-skill.py --list
# 또는: node tools/install-skill.mjs --list
# 또는: npx rankmath-install --list

# 현재 프로젝트에 설치
python tools/install-skill.py claude-code   # full install -> .claude/skills/rankmath-seo-wp/
python tools/install-skill.py cursor        # rule         -> .cursor/rules/rankmath-seo-wp.mdc
python tools/install-skill.py copilot       # 추가         -> .github/copilot-instructions.md
python tools/install-skill.py claude-ai --to ./build  # zip -> build/rankmath-seo-wp.zip

# 유저 글로벌 설치 (플랫폼 지원 시)
python tools/install-skill.py claude-code --global   # ~/.claude/skills/rankmath-seo-wp/

# 쓰지 않고 계획만 확인
python tools/install-skill.py --info cursor
python tools/install-skill.py --dry-run claude-code
```

### 지원 플랫폼

| 플랫폼              | Key            | 설치 타입            | 기본 경로                                              |
|--------------------|----------------|----------------------|--------------------------------------------------------|
| Claude Code        | `claude-code`  | full                 | `.claude/skills/rankmath-seo-wp/SKILL.md`              |
| Claude.ai (web)    | `claude-ai`    | zip-upload           | `./rankmath-seo-wp.zip` → 설정 → Skills → 업로드       |
| Cursor             | `cursor`       | rule                 | `.cursor/rules/rankmath-seo-wp.mdc`                    |
| OpenAI Codex CLI   | `codex-cli`    | full                 | `.codex/skills/rankmath-seo-wp/SKILL.md`               |
| Gemini CLI         | `gemini-cli`   | full                 | `.gemini/extensions/rankmath-seo-wp/GEMINI.md`         |
| Windsurf           | `windsurf`     | rule                 | `.windsurf/rules/rankmath-seo-wp.md`                   |
| GitHub Copilot     | `copilot`      | instructions-append  | `.github/copilot-instructions.md`                      |
| Continue           | `continue`     | rule                 | `.continue/rules/rankmath-seo-wp.md`                   |

Codex CLI 와 Gemini CLI 는 best-effort 입니다. 사용 중인 버전의 공식 문서로 반드시 확인하세요.

### 설치 후 시도

AI 도구를 재시작하고:

```
> Claude Code Hooks 튜토리얼 글을 써줘
```

### 설치 없이 레퍼런스로 사용

인스톨러를 실행하지 않아도 `references/` 와 `data/` 만으로 충분히 실용적입니다.

## 두 가지 배포 경로

WordPress 서버 SSH 접근 권한 유무에 따라 두 경로 중 선택.

### Path A · 블록 붙여넣기 (SSH 불필요)

```bash
# 1. 검증
python tools/verify-article.py article.html "당신의 포커스 키워드"
# 또는: node tools/verify-article.mjs article.html "당신의 포커스 키워드"

# 2. 출력 — "붙이면 바로" HTML 을 클립보드로 복사
python tools/export-blocks.py article.html
# 또는: npx rankmath-export article.html

# 3. WP 관리자: 글 → 새로 추가 → 에디터 안에 커서 → Ctrl+V / Cmd+V
```

Gutenberg 가 붙여넣은 `<!-- wp:... -->` 블록 코멘트를 파싱해서 HowTo / FAQ / YouTube 임베드 / 테이블 / 코드 블록 모두 복원합니다. 그다음 사이드바에서 Rank Math 메타 (포커스 키워드, 숫자 포함 SEO 제목, 메타 설명, 슬러그) 를 설정하고 대표 이미지를 업로드하면 됩니다.

특정 블록만 추출:

```bash
python tools/export-blocks.py article.html --only howto   # HowTo 만
python tools/export-blocks.py article.html --only faq     # FAQ 만
```

파일로 저장:

```bash
python tools/export-blocks.py article.html --to-file ready.html
python tools/export-blocks.py article.html --print > ready.html
```

### Path B · WP-CLI 일괄 (서버 접근)

```bash
export WP_SSH_KEY=~/.ssh/id_rsa
export WP_SSH_HOST=user@your-wp-host.example.com
export WP_PATH=/path/to/wordpress

# 구식 HowTo 블록을 여러 글에서 일괄 수정
python tools/fix-howto-block.py 8489 8478 8466

# FAQ 정합성을 여러 글에서 일괄 수정
python tools/regenerate-faq.py 8489 8478 8579
```

## 임의의 글 검증

```bash
python tools/verify-article.py article.html "당신의 포커스 키워드"
# 또는
node tools/verify-article.mjs article.html "당신의 포커스 키워드"
```

샘플 출력:

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

## 폴더 구조

```
rankmath-seo-wp/
├── SKILL.md                          # 메인 진입점 (자동 로드)
├── README.md                         # 영문 README
├── README.{zh-TW,ja,ko}.md           # 다국어 번역
├── CLAUDE.md                         # AI 가 Skill 자체를 편집할 때의 규칙
├── CONTRIBUTING.md                   # 사람 기여자 가이드
├── LICENSE                           # MIT
├── package.json                      # npm 메타 + bin 엔트리
├── data/                             # 구조화된 CSV 레퍼런스
│   ├── focus-keyword-density.csv     # 밀도 구간 → 판정 + 조치
│   ├── h2-templates.csv              # 12 H2 구조와 FK 배치
│   ├── faq-topics.csv                # 8 개 FAQ 주제 패턴 (중·영)
│   ├── power-words.csv               # SEO 제목용 파워 워드
│   └── platforms.csv                 # AI 플랫폼별 설치 경로
├── references/                       # 상세 가이드 (필요 시 로드)
│   ├── article-template.md           # 12 H2 구조 + FK 분포
│   ├── howto-block.md                # rank-math/howto-block 표준 포맷
│   ├── faq-block.md                  # FAQ JSON ↔ HTML 정렬 규칙
│   ├── seo-checklist.md              # Rank Math 100점 분해표
│   ├── moksa-style.md                # Moksa 관점 문체 + 치환 단어표
│   ├── image-specs.md                # 대표 이미지 사양 + PIL 템플릿
│   └── wp-cli-pitfalls.md            # WP-CLI 배포 함정 9 가지
├── tools/                            # 트윈 도구 (Python + Node)
│   ├── verify-article.py    / .mjs   # FK 밀도 + 구조 검증
│   ├── export-blocks.py     / .mjs   # 블록 붙여넣기 출력
│   ├── install-skill.py     / .mjs   # 멀티 플랫폼 인스톨러
│   ├── regenerate-faq.py    / .mjs   # FAQ JSON↔HTML 정렬 (WP-CLI 일괄 지원)
│   └── fix-howto-block.py   / .mjs   # 구식 HowTo 포맷 변환 (WP-CLI 일괄 지원)
└── examples/
    └── sample-article.html           # 모든 검사 통과 샘플 글
```

## 어떤 문제를 해결하나

30 편 이상 발행하면서 반복적으로 부딪힌 문제들:

| 문제                                       | 이 Skill 의 해결 방식                                       |
|--------------------------------------------|-------------------------------------------------------------|
| Rank Math 점수 60 미만                      | `seo-checklist.md` 의 100점 체크리스트 준수                  |
| FK 밀도 3% 이상 (키워드 채우기)             | `article-template.md` 의 분포표 (5 H2 + 4 FAQ + 본문)       |
| FK 밀도 0.5% (너무 낮음 경고)               | `verify-article.{py,mjs}` 로 자동 측정                       |
| HowTo "예상치 못한 내용" 오류               | `howto-block.md` 의 8594 표준 포맷 적용                      |
| FAQ 블록 검증 오류                          | `regenerate-faq.py` 로 JSON ↔ HTML 정렬                      |
| `<script>` JSON-LD 가 원본 텍스트로 노출    | inline script 사용을 명시적으로 금지                         |
| H2 에 "HowTo Schema" 노출                   | Skill 과 검증기 양쪽에서 검출                                |
| Windows Python 이 `\r\n` 으로 기록          | 도구가 `newline='\n'` 을 강제                                |
| `--post_content="$(cat)"` 셸 오류           | `wp post update file.html` 구문 안내                         |
| SEO Title 에 숫자 없음 경고                 | `[FK] 完整教學：N 大功能` 템플릿 강제                        |
| 서버 SSH 권한 없음                          | `export-blocks` 가 블록 붙여넣기용 HTML 을 클립보드로 전달   |

## 다른 분야에 적용하기

이 Skill 은 중국어 기술 튜토리얼을 타깃으로 하지만 규칙은 범용입니다:

- `Moksa 觀點` 도입부를 자기 브랜드의 시그니처로 교체
- `references/article-template.md` H2 구조를 자기 분야에 맞게 변경
- 1.0–1.5% FK 밀도는 대부분 언어에서 통용
- `references/wp-cli-pitfalls.md` 의 WP 호스트 / 경로를 본인 환경으로
- `references/image-specs.md` 의 베이스 이미지 경로를 본인 환경으로

## 오픈 스탠다드

[Anthropic Agent Skills 규격](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) 을 따릅니다:
`SKILL.md` + YAML frontmatter (`name`, `description`) + 평면 reference 파일.
여러 AI 플랫폼 간 호환됩니다.

## 작성자

**moksa** 가 직접 개발 및 유지보수 — [moksaweb.com](https://moksaweb.com) 운영자로,
공개된 모든 Claude AI 튜토리얼 글에서 실전 검증된 Skill 입니다.

- 웹사이트: [moksaweb.com](https://moksaweb.com)
- 작성자: [moksa](https://moksaweb.com)

이 Skill 이 Rank Math 디버깅 시간을 줄여줬다면,
GitHub 에 ⭐ 또는 [moksaweb.com](https://moksaweb.com) 으로의 백링크 환영합니다.

## 라이선스

MIT — [LICENSE](LICENSE) 참고. Copyright © 2026 moksa (moksaweb.com).

## 기여

[CONTRIBUTING.md](CONTRIBUTING.md) 참고. 다음과 같은 PR 환영:

- 번역 (EN / zh-TW / ja / ko 외 다른 로케일)
- 추가 수정 도구 (이미지 깨짐, 외부 링크 끊김 등)
- 다른 분야용 글 템플릿 (이커머스, 뉴스, 금융 등)
- 다른 SEO 플러그인 검증 규칙 (Yoast, AIOSEO, SEOPress 등)

---

[moksa](https://moksaweb.com) 가 [Claude Code](https://claude.com/claude-code) 로 제작.
