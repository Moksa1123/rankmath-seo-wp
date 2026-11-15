# Examples

| File | What it shows | Check |
|---|---|---|
| `examples/sample-article.html` | Full 12-H2 article (Claude Skills, simplified from moksaweb.com post 8730): opening, Moksa quote, HowTo block under H2 #4, 3 YouTube embeds, 5 links, FAQ block under H2 #12 | `python tools/verify-article.py examples/sample-article.html "Claude Skills"` → `8 passed, 0 failed` |

The sample is short for a real post: content length scores 2/8 in Rank Math
(714 `wp.wordcount` words; full points need 2500), and its density (1.96%) is
inside the plugin's full-score band but above the KB's 1–1.5% advice. Use it
for structure and block markup, not as a length target.

Lookups that show how to use the data:

```bash
python scripts/search.py "密度"                       # density scoring + KB advice
python scripts/search.py "howto" --domain blocks      # exact save() markup
python scripts/search.py "影片 圖片"                  # media test points
python scripts/search.py all --domain site            # every site-style rule
```
