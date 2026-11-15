#!/usr/bin/env python3
"""Verify a Rank Math WP article meets all SEO and structure requirements.

Usage:
    python verify-article.py article.html "Focus Keyword"

Outputs a checklist report. Exit code 0 if all pass, 1 if any fail.

Every threshold below is a row in data/rankmath-tests.csv (test_id in the
comment). Rank Math rules come from the plugin source (seo-by-rank-math
1.0.282, assets/admin/js/analyzer.js); site-style rules are labelled as such.

Checks:
- Word count: Rank Math lengthContent passes from 600 words (wp.wordcount "words")
- FK density: Rank Math keywordDensity full score band 1.0-2.5%
- Heading balance (12 H2 is site style; any balanced count passes)
- FK in first 10% of content (keywordIn10Percent) and in 1+ H2
- HowTo / FAQ block HTML equals what the block's save() would write
- Forbidden patterns ("HowTo Schema" text, inline ld+json script)
"""
import re
import json
import html
import sys
from pathlib import Path

# --- thresholds (single source: data/rankmath-tests.csv) ---------------------
WORDS_PASS = 600              # lengthContent: lowest boundary with score > 0
LENGTH_TIERS = [(2500, 8), (2000, 5), (1500, 4), (1000, 3), (600, 2)]  # lengthContent
DENSITY_FAIL_LOW = 0.5        # keywordDensity: below = fail (0/6)
DENSITY_FAIR = (0.5, 0.75)    # keywordDensity: fair 2/6 (lodash inRange, end exclusive)
DENSITY_GOOD = (0.76, 1.0)    # keywordDensity: good 3/6
DENSITY_FAIL_HIGH = 2.5       # keywordDensity: above = fail (0/6); otherwise best 6/6
DENSITY_KB_RECOMMENDED = (1.0, 1.5)  # rankmath.com/kb/score-100-in-tests/#keyword-density
IN10_MIN_WORDS = 400          # keywordIn10Percent: only slices to 10% above 400 words
SITE_H2_COUNT = 12            # site style (moksaweb.com template)
SITE_HOWTO_SIZESLUG = 'large'  # site style (post 8594); plugin default is "full"
SITE_HOWTO_DROP_FIELDS = ['hasDuration', 'days', 'hours', 'minutes',
                          'hasTotalTime', 'timeDays', 'timeHours', 'timeMinutes',
                          'titleWrapper']  # site style (post 8594); valid plugin attributes

# --- ports of the text helpers Rank Math and WordPress use -----------------------
_TAG = re.compile(r'</?[a-z][^>]*?>', re.I)
_COMMENT = re.compile(r'<!--[\s\S]*?-->')
_SC_NAME = r'[^<>&/\[\]\x00- =]+?'
_SHORTCODE_OPEN = re.compile(r'\[' + _SC_NAME + r'( [^\]]+?)?\]')
_SHORTCODE_CLOSE = re.compile(r'\[/' + _SC_NAME + r'\]')
_ENTITY = re.compile(r'&\S+?;')
_RM_SYMBOLS = re.compile('[\x80-\xbf\xd7\xf7 -⯿⸀-⹿]')
_WP_REMOVE = re.compile('[!-/:-@\\[-`{-~\x80-\xbf\xd7\xf7 -⯿⸀-⹿]')
_EDGE = "[\\u2013\\-\\(\\)_\\[\\]’“”\"'.?!:;,\xbf\xa1\xab\xbb‹›—\xd7+&<>]+"
_EDGE_START = re.compile('^' + _EDGE)
_EDGE_END = re.compile(_EDGE + '$')


def load(path):
    return Path(path).read_text(encoding='utf-8')


def _normalize_whitespace(text):
    """Rank Math helper p(): nbsp to space, collapse runs, trim."""
    text = re.sub(r'&nbsp;|&#160;', ' ', text, flags=re.I)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\s\.', '.', text)
    return text.strip()


def _normalize_quotes(text):
    """Rank Math helper $e(): curly quotes to straight quotes."""
    text = re.sub('[‘’‛`]', "'", text)
    return re.sub('[“”〝〞〟‟„]', '"', text)


def rm_words(text):
    """Port of Rank Math getWords (analyzer.js research `getWords`)."""
    text = _TAG.sub('', text)
    text = _COMMENT.sub('', text)
    text = _SHORTCODE_CLOSE.sub('', _SHORTCODE_OPEN.sub('', text))
    text = _normalize_whitespace(text)
    text = _ENTITY.sub('', text)
    text = re.sub('--|—', ' ', text)
    text = _RM_SYMBOLS.sub('', text)
    if text == '':
        return []
    words = [_EDGE_END.sub('', _EDGE_START.sub('', w)) for w in re.split(r'\s', text)]
    return [w for w in words if w.strip() != '']


def wp_word_count(text):
    """Port of @wordpress/wordcount count(text, 'words') with default settings."""
    text = _TAG.sub('\n', text)
    text = _COMMENT.sub('', text)
    text = re.sub(r'&nbsp;|&#160;', ' ', text, flags=re.I)
    text = _ENTITY.sub('', text)
    text = re.sub('--|—', ' ', text)
    text = _WP_REMOVE.sub('', text)
    return len(re.findall(r'\S\s+', text + '\n'))


def strip_metadata(content):
    """Remove block JSON metadata + all comments — leaves only visible HTML."""
    return _COMMENT.sub('', content)


def visible_word_count(content):
    """Word count exactly as Rank Math's lengthContent/keywordDensity compute it."""
    return wp_word_count(content.lower())


def visible_fk_count(content, fk):
    """FK matches as Rank Math's keywordDensity counts them (case-insensitive,
    tags and comments removed, words re-joined with single spaces)."""
    text = ' '.join(rm_words(_normalize_whitespace(_TAG.sub('', content))))
    kw = ' '.join(rm_words(_normalize_quotes(fk)))
    if not kw:
        return 0
    return len(re.findall(re.escape(kw), text, flags=re.I))


def fk_density(content, fk):
    """Density = FK count × 100 / word count, rounded like Rank Math (toFixed(2))."""
    fk_n = visible_fk_count(content, fk)
    w_n = visible_word_count(content)
    return fk_n, w_n, float(f'{fk_n * 100 / w_n:.2f}') if w_n else 0


def density_score(density):
    """keywordDensity calculateScore(): returns (verdict, points out of 6)."""
    if density < DENSITY_FAIL_LOW:
        return 'low', 0
    if density > DENSITY_FAIL_HIGH:
        return 'high', 0
    if DENSITY_FAIR[0] <= density < DENSITY_FAIR[1]:
        return 'fair', 2
    if DENSITY_GOOD[0] <= density < DENSITY_GOOD[1]:
        return 'good', 3
    return 'best', 6


def length_score(words):
    """lengthContent calculateScore(): points out of 8."""
    for boundary, score in LENGTH_TIERS:
        if words >= boundary:
            return score
    return 0


def check_headings(content):
    """Verify H2 open/close balance."""
    opens = content.count('<!-- wp:heading')
    closes = content.count('<!-- /wp:heading')
    return opens, closes


def _block(content, name):
    m = re.search(
        r'<!-- wp:rank-math/' + name + r' (\{.*?\}) -->\s*(.*?)\s*<!-- /wp:rank-math/' + name + ' -->',
        content, re.DOTALL,
    )
    return (m.group(1), m.group(2)) if m else None


def _same_html(a, b):
    """Loose equivalent of Gutenberg's block validation: entities decoded,
    whitespace between tags ignored, runs of whitespace collapsed."""
    def norm(s):
        s = html.unescape(s)
        s = re.sub(r'>\s+<', '><', s.strip())
        return re.sub(r'\s+', ' ', s)
    return norm(a) == norm(b)


def _wrapper_class(data, block):
    cls = 'wp-block-rank-math-' + block
    return cls + (' ' + data['className'] if data.get('className') else '')


def howto_save_html(data):
    """What rank-math/howto-block save() writes (blocks/howto/assets/js/index.js)."""
    steps = data.get('steps') or []
    if not steps:
        return ''
    tw = data.get('titleWrapper', 'h3')
    out = [f'<div class="{_wrapper_class(data, "howto-block")}">']
    for s in steps:
        if s.get('visible') is False:
            continue
        out.append('<div class="rank-math-howto-step">')
        if s.get('title'):
            out.append(f'<{tw} class="rank-math-howto-title">{s["title"]}</{tw}>')
        if s.get('content'):
            out.append(f'<div class="rank-math-howto-content">{s["content"]}</div>')
        out.append('</div>')
    out.append('</div>')
    return ''.join(out)


def faq_save_html(data):
    """What rank-math/faq-block save() writes (blocks/faq/assets/js/index.js)."""
    qs = data.get('questions') or []
    if not qs:
        return ''
    tw = data.get('titleWrapper', 'h3')
    out = [f'<div class="{_wrapper_class(data, "faq-block")}">']
    for q in qs:
        if not q.get('title') or not q.get('content') or q.get('visible') is False:
            continue
        out.append(f'<div class="rank-math-faq-item"><{tw} class="rank-math-question">{q["title"]}</{tw}>'
                   f'<div class="rank-math-answer">{q["content"]}</div></div>')
    out.append('</div>')
    return ''.join(out)


def check_howto_block(content):
    """HowTo HTML must equal save() output; site-style JSON rules flagged separately."""
    found = _block(content, 'howto-block')
    if not found:
        return ['No HowTo block found']
    json_str, html_part = found
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return [f'JSON parse error: {e}']

    issues = []
    if 'steps' not in data:
        issues.append('Missing JSON.steps')
    elif not _same_html(html_part, howto_save_html(data)):
        issues.append('HTML differs from save() output (editor will show "invalid content")')
        for i, s in enumerate([s for s in data['steps'] if s.get('visible') is not False], 1):
            if s.get('title') and s['title'] not in html.unescape(html_part) and s['title'] not in html_part:
                issues.append(f'Step {i} title not found in HTML')
            if s.get('content') and s['content'] not in html.unescape(html_part) and s['content'] not in html_part:
                issues.append(f'Step {i} content not found in HTML')
    for f in SITE_HOWTO_DROP_FIELDS:
        if f in data:
            issues.append(f'Site style (post 8594): drop JSON field {f}')
    if data.get('sizeSlug') != SITE_HOWTO_SIZESLUG:
        issues.append(f'Site style (post 8594): JSON.sizeSlug should be "{SITE_HOWTO_SIZESLUG}"')
    return issues if issues else ['OK']


def check_faq_alignment(content):
    """FAQ HTML must equal save() output (JSON ↔ HTML aligned)."""
    found = _block(content, 'faq-block')
    if not found:
        return ['No FAQ block found']
    try:
        data = json.loads(found[0])
    except json.JSONDecodeError as e:
        return [f'FAQ JSON parse error: {e}']
    html_part = found[1]
    shown = [q for q in data.get('questions', [])
             if q.get('title') and q.get('content') and q.get('visible') is not False]
    if _same_html(html_part, faq_save_html(data)):
        return [f'OK ({len(shown)} questions aligned)']

    tw = data.get('titleWrapper', 'h3')
    items = re.findall(
        r'<div class="rank-math-faq-item"><' + tw + r' class="rank-math-question">(.*?)</' + tw + '>'
        r'<div class="rank-math-answer">(.*?)</div></div>',
        html_part, re.DOTALL,
    )
    if len(items) != len(shown):
        return [f'Count mismatch: JSON {len(shown)}, HTML {len(items)}']
    issues = []
    for i, (q, (h_t, h_c)) in enumerate(zip(shown, items), 1):
        if not _same_html(h_t, q['title']):
            issues.append(f'Q{i} title mismatch')
        if not _same_html(h_c, q['content']):
            issues.append(f'Q{i} content mismatch')
    return issues or ['HTML differs from save() output (wrapper or markup)']


def check_fk_subheading(content, fk):
    """Verify FK appears in at least one H2/H3."""
    h2_with_fk = re.findall(rf'<h2[^>]*>[^<]*{re.escape(fk)}[^<]*</h2>', content)
    h3_with_fk = re.findall(rf'<h3[^>]*>[^<]*{re.escape(fk)}[^<]*</h3>', content)
    return len(h2_with_fk), len(h3_with_fk)


def check_fk_in_opening(content, fk):
    """keywordIn10Percent: FK in the first 10% of words (whole text if ≤ 400 words)."""
    words = rm_words(content.lower())
    if len(words) > IN10_MIN_WORDS:
        words = words[:int(0.1 * len(words))]
    kw = ' '.join(rm_words(_normalize_quotes(fk.lower())))
    return bool(kw) and kw in ' '.join(words)


def check_forbidden_patterns(content):
    """Check for known broken patterns."""
    issues = []
    if 'HowTo Schema' in content:
        if re.search(r'<h2[^>]*>[^<]*HowTo Schema[^<]*</h2>', content):
            issues.append('"HowTo Schema" in H2 heading (forbidden)')
        else:
            issues.append('"HowTo Schema" text in body (review)')
    if 'application/ld+json' in content:
        issues.append('Inline <script type="application/ld+json"> (some themes strip)')
    if 'FAQ Schema' in content and re.search(r'<h2[^>]*>[^<]*FAQ Schema[^<]*</h2>', content):
        issues.append('"FAQ Schema" in H2 heading (forbidden)')
    return issues


def main():
    if len(sys.argv) != 3:
        print("Usage: python verify-article.py article.html 'Focus Keyword'")
        sys.exit(1)

    path = sys.argv[1]
    fk = sys.argv[2]
    try:
        content = load(path)
    except OSError as e:
        print(f"File error: {e}", file=sys.stderr)
        sys.exit(2)

    print(f"=== {path} ===")
    print(f"Focus keyword: {fk}")
    print()

    pass_count = 0
    fail_count = 0

    # 1. Word count
    fk_n, w_n, density = fk_density(content, fk)
    print(f"Word count:      {w_n} visible words")
    if w_n >= WORDS_PASS:
        print(f"                 OK at least {WORDS_PASS} (content length {length_score(w_n)}/8)")
        pass_count += 1
    else:
        print(f"                 FAIL below {WORDS_PASS} (content length 0/8)")
        fail_count += 1

    # 2. FK density
    verdict, points = density_score(density)
    kb_lo, kb_hi = DENSITY_KB_RECOMMENDED
    print(f"FK count:        {fk_n} visible occurrences")
    print(f"FK density:      {density:.2f}%")
    if verdict == 'best':
        note = '' if kb_lo <= density <= kb_hi else f'; KB recommends {kb_lo}-{kb_hi}%'
        print(f"                 OK full score band {DENSITY_GOOD[1]}-{DENSITY_FAIL_HIGH}% (6/6{note})")
        pass_count += 1
    else:
        print(f"                 FAIL {verdict} ({points}/6; full score {DENSITY_GOOD[1]}-{DENSITY_FAIL_HIGH}%)")
        fail_count += 1

    # 3. Heading balance
    h_open, h_close = check_headings(content)
    print(f"Heading balance: {h_open} open / {h_close} close")
    if h_open == h_close == SITE_H2_COUNT:
        print(f"                 OK {SITE_H2_COUNT}/{SITE_H2_COUNT} (site-style structure)")
        pass_count += 1
    elif h_open == h_close:
        print(f"                 OK balanced {h_open}/{h_close} (non-standard count)")
        pass_count += 1
    else:
        print(f"                 FAIL unbalanced - fix before publish")
        fail_count += 1

    # 4. FK in opening
    in_opening = check_fk_in_opening(content, fk)
    print(f"FK in opening:   {'OK' if in_opening else 'FAIL'}")
    if in_opening:
        pass_count += 1
    else:
        fail_count += 1

    # 5. FK in subheading
    h2_n, h3_n = check_fk_subheading(content, fk)
    print(f"FK in H2:        {h2_n} occurrences")
    if h2_n >= 1:
        print(f"                 OK at least 1 H2 contains FK")
        pass_count += 1
    else:
        print(f"                 FAIL no H2 contains FK (Rank Math wants >=1)")
        fail_count += 1

    # 6. HowTo block
    howto_issues = check_howto_block(content)
    print(f"HowTo block:     {howto_issues[0] if howto_issues == ['OK'] or len(howto_issues) == 1 and howto_issues[0].startswith('No ') else 'has issues'}")
    if howto_issues != ['OK']:
        for i in howto_issues:
            print(f"                 - {i}")
        fail_count += 1
    else:
        pass_count += 1

    # 7. FAQ alignment
    faq_issues = check_faq_alignment(content)
    print(f"FAQ block:       {faq_issues[0] if faq_issues[0].startswith(('OK', 'No ')) else 'has issues'}")
    if not faq_issues[0].startswith('OK'):
        for i in faq_issues:
            if not i.startswith('No '):
                print(f"                 - {i}")
        fail_count += 1
    else:
        pass_count += 1

    # 8. Forbidden patterns
    forbidden = check_forbidden_patterns(content)
    if forbidden:
        print(f"Forbidden:       FAIL")
        for f in forbidden:
            print(f"                 - {f}")
        fail_count += 1
    else:
        print(f"Forbidden:       OK none found")
        pass_count += 1

    print()
    print(f"=== Result: {pass_count} passed, {fail_count} failed ===")

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == '__main__':
    main()
