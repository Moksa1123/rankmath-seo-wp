# evals 結果

最新的在最上面。題目與評分標準見 `cases.json`，評分程式 `grade.py`。

## 2026-11-15 第 2 輪（15 題）

- 新題考外掛原始碼裡的冷門細節（0.75% 的 inRange 空隙、強力字前綴 4 字元、11 個語系檔、自架 mp4 不算影片）與 skill 自己的實測值。
- 沒 skill 又答對 7 題，已標 `retired`。其中 `skill-plugin-version` 是洩題：同一輪另一題的題目寫了「Rank Math 1.0.282」。
- `post-title-english-trust` 的評分規則本輪後修正：原規則只認「never measured」，漏判有 skill 的正確答案「has never been measured」；沒 skill 的答案（答「站內風格」）修正前後都錯。上表用修正後的規則評分。

| 項目 | 有 skill | 沒有 skill |
|---|---|---|
| 計分題答對率（8 題） | **8/8（100.0%）** | 0/8（0.0%） |
| 全部題目（15 題） | 15/15 | 7/15 |
| 模型 | claude-opus-5-5 | claude-opus-5-5 |
| 作答方式 | subagent reads SKILL.md, uses scripts/search.py and data/ | subagent, no tools, closed book |
| 答案檔 | `evals/runs/2026-11-15-r2-with-skill.json` | `evals/runs/2026-11-15-r2-without-skill.json` |

| 題目 | 可信度 | 有 skill | 沒有 skill | 備註 |
|---|---|---|---|---|
| `media-three-images` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `power-words-zh-skipped` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `howto-save-classes` | 官方原始碼 | ✅ | ❌ |  |
| `verifier-word-gate` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `site-howto-sizeslug` | 站內風格 | ✅ | ❌ |  |
| `density-075-gap` | 官方原始碼 | ✅ | ❌ |  |
| `powerword-prefix` | 官方原始碼 | ✅ | ❌ |  |
| `powerword-locale-count` | 官方原始碼 | ✅ | ❌ |  |
| `howto-empty-title` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `faq-skip-rules` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `video-self-hosted` | 官方原始碼 | ✅ | ❌ |  |
| `in10-kb-vs-code` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `skill-plugin-version` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `sample-density` | 實測 | ✅ | ❌ |  |
| `post-title-english-trust` | 站內風格 | ✅ | ❌ |  |

## 2026-11-15 第 1 輪（16 題候選）

- 沒有 skill 的模型憑記憶答對 11/16（Rank Math analyzer 的門檻、block.json 預設值它都記得），這 11 題沒有鑑別度，已在 `cases.json` 標 `retired`。
- `power-words-zh-skipped` 的評分規則本輪後修正：原規則讓「只有英文才跑」這個錯誤理由也過關（正規式裡的 `en` 對到 English）。改成要答出「外掛沒有中文清單」。上表用修正後的規則評分。

| 項目 | 有 skill | 沒有 skill |
|---|---|---|
| 計分題答對率（5 題） | **5/5（100.0%）** | 0/5（0.0%） |
| 全部題目（16 題） | 16/16 | 11/16 |
| 模型 | claude-opus-5-5 | claude-opus-5-5 |
| 作答方式 | subagent reads SKILL.md, uses scripts/search.py and data/ | subagent, no tools, closed book |
| 答案檔 | `evals/runs/2026-11-15-with-skill.json` | `evals/runs/2026-11-15-without-skill.json` |

| 題目 | 可信度 | 有 skill | 沒有 skill | 備註 |
|---|---|---|---|---|
| `density-full-band-top` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `density-good-points` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `length-1500-points` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `title-points-zh` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `media-featured-plus-3-youtube` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `media-three-images` | 官方原始碼 | ✅ | ❌ |  |
| `power-words-zh-skipped` | 官方原始碼 | ✅ | ❌ |  |
| `wordcount-cjk` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `howto-duration-valid` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `howto-save-classes` | 官方原始碼 | ✅ | ❌ |  |
| `howto-multiple` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `in10-threshold` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `faq-default-sizeslug` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `verifier-word-gate` | 官方原始碼 | ✅ | ❌ |  |
| `site-howto-sizeslug` | 站內風格 | ✅ | ❌ |  |
| `internal-vs-external-points` | 官方原始碼 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |

