# Contributing to rankmath-seo-wp

Thanks for considering a contribution! This skill is maintained by
[moksa](https://moksaweb.com) and battle-tested on every published article at
[moksaweb.com](https://moksaweb.com). Patches that improve coverage, accuracy,
or platform support are welcome.

## What we accept

| Contribution                                | Welcome? | Notes                                                         |
|---------------------------------------------|---------:|---------------------------------------------------------------|
| README translation (new language)           | Yes      | Mirror section order; keep code samples identical             |
| New SEO-plugin validators (Yoast / AIOSEO)  | Yes      | Add as `tools/verify-<plugin>.{py,mjs}` pair                  |
| New fix tools (broken images, links, etc.)  | Yes      | Provide both Python and Node implementations                  |
| Niche article templates (e-commerce, news)  | Yes      | Add as `references/article-template-<niche>.md`               |
| Additional CSV reference data               | Yes      | Document the schema in `SKILL.md`                             |
| Bug fixes in existing tools                 | Yes      | Include before/after sample input                             |
| Wholesale rewrite of `SKILL.md` structure   | Discuss first — open an issue                                |
| Tracking, analytics, telemetry, network IO  | No       | The skill must remain offline-safe                            |

## Development setup

Requirements:

- Python 3.9+
- Node.js 18+
- (Optional) WP-CLI access to a Rank Math test site for end-to-end testing

```bash
git clone https://github.com/Moksa1123/rankmath-seo-wp
cd rankmath-seo-wp

# Sanity check — should print Result: 8 passed, 0 failed
python tools/verify-article.py examples/sample-article.html "Claude Skills"
node tools/verify-article.mjs examples/sample-article.html "Claude Skills"
```

## Coding conventions

- See [CLAUDE.md](CLAUDE.md) for the full set. The highlights:
- Every user-facing tool in `tools/` exists as **both** `.py` and `.mjs`
  twins. Behaviour parity is enforced.
- Use `data/*.csv` for structured rules; reserve `references/*.md` for prose.
- LF newlines everywhere. Windows contributors must configure
  `core.autocrlf=input` or use `git config --global core.autocrlf input`.
- Never commit real SSH hosts, paths, account IDs, or personal directories.
  Use the placeholders documented in [CLAUDE.md](CLAUDE.md#sanitisation-rules-open-source-release).

## Multilingual READMEs

The repo ships English (`README.md`) plus Traditional Chinese, Japanese,
Korean (`README.zh-TW.md`, `README.ja.md`, `README.ko.md`). When you change
the English README structurally, propagate the change to the other three.
Pure wording / nuance changes per language are fine.

To add a new language: copy the English file, translate, register it in the
language switcher at the top of every README. Use the IETF tag (e.g.,
`README.de.md`).

## Submitting a PR

1. Fork the repo.
2. Create a topic branch (`feat/yoast-validator`, `fix/howto-h4`, etc.).
3. Run the verifiers locally — both `.py` and `.mjs` must pass.
4. Sanitise: `grep -RIn "159\.65\|cloudwaysapps\|yun19\|OneDrive" .` should
   come up empty.
5. Open a PR with: what changed, why, and a sample input/output if relevant.

## Issues

Bug? Inconsistency between Python and Node tools? Translation request?
Open an issue. Include:

- Tool / file affected
- Sample input (an `article.html` snippet is most useful)
- Expected vs actual output
- Your platform (`uname -a` or Windows version)

## License

By contributing you agree your work ships under MIT — see [LICENSE](LICENSE).

## Author

[moksa](https://moksaweb.com) · [moksaweb.com](https://moksaweb.com)
