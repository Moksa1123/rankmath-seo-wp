<div align="center">

# Rank Math SEO WP

### Rank Math 80 점 이상의 WordPress 글을 AI 가 작성하는 Skill. 클립보드에서 복사 후 붙여넣기로 Gutenberg 블록 복원, SSH 불필요.

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
  <img src="https://img.shields.io/badge/AI%20%ED%94%8C%EB%9E%AB%ED%8F%BC-8-blueviolet?style=flat-square" alt="8 AI 플랫폼">
</p>

<p>
  <a href="#빠른-시작"><strong>지금 시작</strong></a> ·
  <a href="https://github.com/Moksa1123/rankmath-seo-wp"><strong>GitHub</strong></a> ·
  <a href="https://www.npmjs.com/package/rankmath-seo-wp"><strong>npm</strong></a> ·
  <a href="https://moksaweb.com"><strong>moksaweb.com</strong></a>
</p>

<p>
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <strong>한국어</strong>
</p>

</div>

---

<table>
<tr>
<td width="33%" valign="top">

#### 블록 붙여넣기, SSH 불필요

`rankmath-export article.html` 로 글 전체를 클립보드에 복사. WP 블록 에디터에 붙여넣으면 HowTo / FAQ / 임베드 모두 완벽 복원.

</td>
<td width="33%" valign="top">

#### 8 플랫폼 인스톨러

`rankmath-install <platform>` 으로 Claude Code, Claude.ai, Cursor, Codex CLI, Gemini CLI, Devin Desktop (구 Windsurf), Copilot, Continue 의 정규 경로와 frontmatter 에 자동 배치.

</td>
<td width="33%" valign="top">

#### 발행 전 검증기

`rankmath-verify article.html "FK"` 로 포커스 키워드 밀도 (1.0–1.5%), 12 H2 구조, HowTo / FAQ 정합성, 30+ 안티패턴 자동 검사.

</td>
</tr>
<tr>
<td valign="top">

#### Python 과 Node 트윈 도구

각 CLI 가 `.py` 와 `.mjs` 트윈 버전, 패리티 테스트 완료. 사용 환경에 맞춰 선택 가능.

</td>
<td valign="top">

#### 구조화된 CSV 데이터

밀도 구간, H2 템플릿, FAQ 주제, SEO 파워 워드, 플랫폼 설치 경로 — 기계 읽기 가능한 CSV, 도구와 사람 모두 읽음.

</td>
<td valign="top">

#### 다국어 문서

English, 繁體中文, 日本語, 한국어 완전 README, 섹션 구조 동기화, 중국어 SEO 기본값 실전 검증 완료.

</td>
</tr>
</table>

---

## 빠른 시작

```bash
# npx 로 즉시 사용 (설치 불필요)
npx -p rankmath-seo-wp rankmath-install claude-code              # full skill -> .claude/skills/rankmath-seo-wp/
npx -p rankmath-seo-wp rankmath-export article.html              # 붙이면 바로 HTML 클립보드로
npx -p rankmath-seo-wp rankmath-verify article.html "Claude Skills"

# 또는 글로벌 설치
npm install -g rankmath-seo-wp
rankmath-install --list                       # 지원하는 8 개 AI 플랫폼
```

설치 후 AI 도구 재시작하고 시도:

```
> Claude Code Hooks 튜토리얼 글을 써줘
```

Skill 이 WordPress 글 작성 요청에서 자동 트리거. 출력은 Gutenberg 블록 붙여넣기 가능, Rank Math 80 점 이상.

> [!TIP]
> 설치 전에 확인하고 싶다면? `rankmath-install --info cursor` 로 각 플랫폼의 정확한 경로, frontmatter, 로더 동작을 볼 수 있습니다.

---

## 지원 AI 플랫폼

| # | 플랫폼 | Key | 전략 | 기본 경로 |
|---|-------|-----|------|----------|
| 1 | **Claude Code** | `claude-code` | full | `.claude/skills/rankmath-seo-wp/SKILL.md` |
| 2 | **Claude.ai (web)** | `claude-ai` | zip-upload | `./rankmath-seo-wp.zip` → 설정 → Skills |
| 3 | **Cursor** | `cursor` | rule | `.cursor/rules/rankmath-seo-wp.mdc` |
| 4 | **OpenAI Codex CLI** | `codex-cli` | full | `.codex/skills/rankmath-seo-wp/SKILL.md` (`--to .agents` 로 크로스툴 표준 `.agents/skills/` 에도 설치 가능) |
| 5 | **Gemini CLI** | `gemini-cli` | full | `.gemini/skills/rankmath-seo-wp/SKILL.md` |
| 6 | **Devin Desktop** (구 Windsurf) | `windsurf` | rule | `.devin/rules/rankmath-seo-wp.md` |
| 7 | **GitHub Copilot** | `copilot` | full | `.github/skills/rankmath-seo-wp/SKILL.md` |
| 8 | **Continue** | `continue` | rule | `.continue/rules/rankmath-seo-wp.md` |

> [!NOTE]
> 8 개 플랫폼 모두 2026 년 7 월 기준 검증 완료. 구버전 도구는 레거시 경로 사용: Gemini CLI 는 `.gemini/extensions/<name>/GEMINI.md`, Windsurf 는 `.windsurf/rules/`, Copilot 은 `.github/copilot-instructions.md` 에 추가 — 자세한 내용은 `rankmath-install --info <platform>`.

---

## CLI 치트시트

<details>
<summary><strong>블록 붙여넣기 출력</strong> — <code>rankmath-export</code></summary>

```bash
rankmath-export article.html                  # 글 전체를 클립보드로
rankmath-export article.html --only howto     # HowTo 블록만
rankmath-export article.html --only faq       # FAQ 블록만
rankmath-export article.html --to-file out.html
rankmath-export article.html --print > out.html
rankmath-export article.html --no-validate    # 블록 검증 건너뛰기
```

WordPress 관리자: **글 → 새로 추가 → 에디터 안에 커서 → Ctrl+V / Cmd+V**.
Gutenberg 가 블록 코멘트를 파싱해서 각 블록 복원.

</details>

<details>
<summary><strong>글 검증기</strong> — <code>rankmath-verify</code></summary>

```bash
rankmath-verify article.html "당신의 포커스 키워드"
```

샘플 출력:

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
<summary><strong>멀티 플랫폼 인스톨러</strong> — <code>rankmath-install</code></summary>

```bash
rankmath-install --list                       # 8 플랫폼 목록
rankmath-install --info cursor                # 상세 보기
rankmath-install claude-code                  # ./.claude/skills/... 에 설치
rankmath-install claude-code --global         # ~/.claude/skills/... 에 설치
rankmath-install claude-ai --to ./build       # ./build/ 에 zip 생성
rankmath-install --dry-run claude-code        # 쓰지 않고 계획만 표시
rankmath-install                              # 인터랙티브 선택
```

</details>

<details>
<summary><strong>WP-CLI 일괄 수정</strong> — Python 또는 Node (서버 접근 필요)</summary>

```bash
export WP_SSH_KEY=~/.ssh/id_rsa
export WP_SSH_HOST=user@your-wp-host.example.com
export WP_PATH=/path/to/wordpress

# 구식 HowTo 블록을 여러 글에서 일괄 수정
python tools/fix-howto-block.py 8489 8478 8466
node   tools/fix-howto-block.mjs 8489 8478 8466

# FAQ JSON↔HTML 정합성을 여러 글에서 일괄 수정
python tools/regenerate-faq.py 8489 8478 8579
node   tools/regenerate-faq.mjs 8489 8478 8579
```

</details>

---

## 글 골격

Skill 은 다음 골격을 따르는 글을 출력합니다 — moksaweb.com 의 모든 발행 글이 이 구조:

```
[도입 문단]                   ~150 단어, FK 2-3 회
[Moksa 관점]                  자연스러운 중국어, FK 1 회, 영어 전문 용어 없음
H2 #1   什麼是 [FK]?
H2 #2   [FK] 和 [Competitor] 怎麼選?       ← 비교 테이블
H2 #3   如何啟用這個工具?                   ← 코드 블록
H2 #4   [FK] 4 步驟啟用設定                 ← HowTo 블록
H2 #5   它能做哪些 X 工作?
H2 #6   [Persona] 怎麼用 [FK]?
H2 #7   [Killer feature] 怎麼運作?
H2 #8   進階主題或場景
H2 #9   哪裡可以找到更多官方資源?           ← YouTube 임베드 3 개
H2 #10  使用 [FK] 有哪些限制?               ← 6 단락
H2 #11  參考依據                             ← 외부 링크 5 개
H2 #12  常見問題 FAQ                         ← FAQ 블록
```

결과: 1,400–2,000+ 단어, FK 밀도 1.0–1.5%, Rank Math 80 점 이상, 블록 붙여넣기 가능.

---

## 레포지토리 구조

<details>
<summary>클릭해서 펼치기</summary>

```
rankmath-seo-wp/
├── SKILL.md                          # Skill 본체 (자동 로드)
├── README.md / .zh-TW / .ja / .ko    # 다국어 문서
├── CLAUDE.md                         # AI 가 Skill 자체를 편집할 때의 규칙
├── CONTRIBUTING.md                   # 사람 기여자 가이드
├── LICENSE                           # MIT
├── package.json                      # npm 메타 + 3 개 bin
│
├── assets/templates/platforms/       # 8 개 플랫폼 설치 설정
│   ├── claude-code.json              # full
│   ├── claude-ai.json                # zip-upload
│   ├── cursor.json                   # rule (.mdc + globs)
│   ├── codex-cli.json                # full (.agents/skills/ optional)
│   ├── gemini-cli.json               # full (SKILL.md standard)
│   ├── windsurf.json                 # rule (.devin/rules, model_decision)
│   ├── copilot.json                  # full (.github/skills/)
│   └── continue.json                 # rule (alwaysApply)
│
├── data/                             # 구조화된 CSV 레퍼런스
│   ├── focus-keyword-density.csv
│   ├── h2-templates.csv
│   ├── faq-topics.csv
│   ├── power-words.csv
│   └── platforms.csv
│
├── references/                       # 상세 가이드
│   ├── article-template.md
│   ├── howto-block.md
│   ├── faq-block.md
│   ├── seo-checklist.md              # Rank Math 100점 분해표
│   ├── moksa-style.md                # Moksa 관점 문체 가이드
│   ├── image-specs.md                # 대표 이미지 PIL 템플릿
│   └── wp-cli-pitfalls.md            # WP-CLI 배포 함정 9 가지
│
├── tools/                            # 트윈 도구 (Python + Node)
│   ├── verify-article.py    / .mjs   # FK 밀도 + 구조 검증
│   ├── export-blocks.py     / .mjs   # 블록 붙여넣기 출력
│   ├── install-skill.py     / .mjs   # 멀티 플랫폼 인스톨러
│   ├── regenerate-faq.py    / .mjs   # FAQ JSON↔HTML 정렬 (일괄 지원)
│   └── fix-howto-block.py   / .mjs   # 구식 HowTo 포맷 변환 (일괄 지원)
│
└── examples/
    └── sample-article.html
```

</details>

---

## 어떤 문제를 해결하나

30 편 이상 발행하면서 반복적으로 부딪힌 문제들:

| 문제 | 이 Skill 의 해결 방식 |
|------|----------------------|
| Rank Math 점수 60 미만 | `references/seo-checklist.md` 의 100점 체크리스트 |
| FK 밀도 3% 이상 (키워드 채우기) | 분포표: 5 H2 + 4 FAQ + 본문 |
| FK 밀도 0.5% (너무 낮음 경고) | `verify-article.{py,mjs}` 자동 측정 |
| HowTo "예상치 못한 내용" 오류 | `references/howto-block.md` 의 8594 표준 포맷 |
| FAQ 블록 검증 오류 | `regenerate-faq.{py,mjs}` 로 JSON ↔ HTML 정렬 |
| `<script>` JSON-LD 가 원본 텍스트 노출 | inline script 사용을 명시적으로 금지 |
| H2 에 "HowTo Schema" 노출 | Skill 과 검증기 양쪽에서 검출 |
| Windows Python 이 `\r\n` 으로 기록 | 도구가 `newline='\n'` 강제 |
| `--post_content="$(cat)"` 셸 오류 | `wp post update file.html` 구문 안내 |
| SEO Title 에 숫자 없음 경고 | `[FK] 完整教學：N 大功能` 템플릿 강제 |
| **서버 SSH 권한 없음** | **`rankmath-export` 가 블록 붙여넣기용 HTML 을 클립보드로** |

---

## 다른 분야에 적용

이 Skill 은 중국어 기술 튜토리얼 타깃이지만 규칙은 범용:

- `Moksa 觀點` 도입부를 자기 브랜드의 시그니처로 교체
- `references/article-template.md` H2 구조를 자기 분야에 맞게 변경
- 1.0–1.5% FK 밀도는 대부분 언어에서 통용
- `references/wp-cli-pitfalls.md` 의 WP 호스트 / 경로를 본인 환경으로
- `references/image-specs.md` 의 베이스 이미지 경로를 본인 환경으로

---

## 오픈 스탠다드

[Anthropic Agent Skills 규격](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) 을 따릅니다:
`SKILL.md` + YAML frontmatter (`name`, `description`) + 평면 reference 파일.
여러 AI 플랫폼 간 호환.

---

## 작성자

<table>
<tr>
<td>

**[moksa](https://moksaweb.com)** — [moksaweb.com](https://moksaweb.com) 운영자, 공개된 모든 Claude AI 튜토리얼 글에서 실전 사용되는 Skill 입니다.

30+ 편의 Rank Math 디버깅 경험을 재사용 가능한 멀티 플랫폼·다국어 툴킷으로 응축.

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

이 Skill 이 Rank Math 디버깅 시간을 줄여줬다면, GitHub 에 star 또는 [moksaweb.com](https://moksaweb.com) 으로의 백링크 환영합니다.

---

## 라이선스 및 기여

MIT — [LICENSE](LICENSE) 참고. Copyright © 2026 moksa (moksaweb.com).

PR 환영 — [CONTRIBUTING.md](CONTRIBUTING.md) 참고. 특히:

- 번역 (EN, zh-TW, ja, ko 외 다른 로케일)
- 추가 수정 도구 (이미지 깨짐, 외부 링크 끊김 등)
- 다른 분야용 글 템플릿 (이커머스, 뉴스, 금융 등)
- 다른 SEO 플러그인 검증 규칙 (Yoast, AIOSEO, SEOPress 등)

---

<div align="center">
  <sub><a href="https://moksaweb.com">moksa</a> 제작 · <a href="https://github.com/Moksa1123/rankmath-seo-wp">GitHub</a> · <a href="https://www.npmjs.com/package/rankmath-seo-wp">npm</a></sub>
</div>
