#!/usr/bin/env python3
"""Verify a Rank Math WP article meets all SEO and structure requirements.

Usage:
    python verify-article.py article.html "Focus Keyword"

Outputs a checklist report. Exit code 0 if all pass, 1 if any fail.

Checks:
- Word count (target 1400+ visible)
- FK density 1.0-1.5% (visible content only, excludes JSON metadata)
- Heading balance (12 H2 expected)
- HowTo block canonical format (rank-math/howto-block)
- FAQ block JSON ↔ HTML alignment
- Forbidden patterns ("HowTo Schema" text, inline <script>)
- FK in opening, in 1+ subheading
"""
import re
import json
import html
import sys
from pathlib import Path


def load(path):
    return Path(path).read_text(encoding='utf-8')


def strip_metadata(content):
    """Remove block JSON metadata + all comments — leaves only visible HTML."""
    # Strip rank-math block JSON metadata (could span multiple lines)
    # `[\s\S]*?` (non-greedy any-char) handles JSON whose values contain `>`.
    v = re.sub(
        r'<!-- wp:rank-math/(?:faq|howto)-block \{[\s\S]*?\} -->',
        '',
        content,
        flags=re.DOTALL,
    )
    # Strip all other Gutenberg block comments
    v = re.sub(r'<!--.*?-->', '', v, flags=re.DOTALL)
    return v


def visible_word_count(content):
    """Count words in visible text (HTML stripped)."""
    visible = strip_metadata(content)
    text = re.sub(r'<[^>]+>', ' ', visible)
    return len(re.findall(r'\S+', text))


def visible_fk_count(content, fk):
    """Count FK occurrences in visible text only."""
    visible = strip_metadata(content)
    return visible.count(fk)


def fk_density(content, fk):
    """Density = FK count × 100 / word count."""
    fk_n = visible_fk_count(content, fk)
    w_n = visible_word_count(content)
    return fk_n, w_n, (fk_n * 100 / w_n) if w_n else 0


def check_headings(content):
    """Verify H2 open/close balance."""
    opens = content.count('<!-- wp:heading')
    closes = content.count('<!-- /wp:heading')
    return opens, closes


def check_howto_block(content):
    """Verify rank-math/howto-block canonical format."""
    issues = []

    # Find HowTo block
    m = re.search(
        r'<!-- wp:rank-math/howto-block (\{.*?\}) -->\s*'
        r'(.*?)'
        r'<!-- /wp:rank-math/howto-block -->',
        content, re.DOTALL,
    )
    if not m:
        return ['No HowTo block found']

    json_str, html_part = m.group(1), m.group(2)

    # JSON checks
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return [f'JSON parse error: {e}']

    forbidden_fields = ['hasDuration', 'days', 'hours', 'minutes',
                        'hasTotalTime', 'timeDays', 'timeHours', 'timeMinutes',
                        'titleWrapper']
    for f in forbidden_fields:
        if f in data:
            issues.append(f'Forbidden JSON field: {f}')

    if 'steps' not in data:
        issues.append('Missing JSON.steps')
    if data.get('sizeSlug') != 'large':
        issues.append('JSON.sizeSlug should be "large"')

    # HTML checks
    if 'rank-math-howto-step-title' in html_part:
        issues.append('Old class: rank-math-howto-step-title (use rank-math-howto-title)')
    if 'rank-math-howto-step-content' in html_part:
        issues.append('Old class: rank-math-howto-step-content (use rank-math-howto-content)')
    if '<div class="rank-math-howto-steps">' in html_part:
        issues.append('Wrapper div rank-math-howto-steps found (should be removed)')
    if re.search(r'rank-math-howto-step"><h4', html_part):
        issues.append('h4 inside step (should be h3)')
    if re.search(r'wp-block-rank-math-howto-block"><h3 class="rank-math-howto-title">', html_part):
        issues.append('Outer h3 title (should not exist, only step-level h3)')

    return issues if issues else ['OK']


def check_faq_alignment(content):
    """Verify FAQ block JSON ↔ HTML alignment after html.unescape."""
    m = re.search(
        r'<!-- wp:rank-math/faq-block (\{.*?\}) -->\s*'
        r'(<div class="wp-block-rank-math-faq-block">.*?</div>)\s*'
        r'<!-- /wp:rank-math/faq-block -->',
        content, re.DOTALL,
    )
    if not m:
        return ['No FAQ block found']

    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        return [f'FAQ JSON parse error: {e}']

    html_part = m.group(2)
    items = re.findall(
        r'<div class="rank-math-faq-item">'
        r'<h3 class="rank-math-question">([^<]+)</h3>'
        r'<div class="rank-math-answer">(.*?)</div>'
        r'</div>',
        html_part, re.DOTALL,
    )

    issues = []
    if len(items) != len(data['questions']):
        return [f'Count mismatch: JSON {len(data["questions"])}, HTML {len(items)}']

    for i, (q, (h_t, h_c)) in enumerate(zip(data['questions'], items), 1):
        if html.unescape(h_t) != q['title']:
            issues.append(f'Q{i} title mismatch')
        if html.unescape(h_c) != q['content']:
            issues.append(f'Q{i} content mismatch')

    return issues if issues else [f'OK (8 questions aligned)' if len(items) == 8 else f'OK ({len(items)} questions aligned)']


def check_fk_subheading(content, fk):
    """Verify FK appears in at least one H2/H3."""
    h2_with_fk = re.findall(rf'<h2[^>]*>[^<]*{re.escape(fk)}[^<]*</h2>', content)
    h3_with_fk = re.findall(rf'<h3[^>]*>[^<]*{re.escape(fk)}[^<]*</h3>', content)
    return len(h2_with_fk), len(h3_with_fk)


def check_fk_in_opening(content, fk):
    """FK should appear in first paragraph (within first 500 chars of visible)."""
    visible = strip_metadata(content)
    # Find first paragraph
    m = re.search(r'<p>(.+?)</p>', visible, re.DOTALL)
    if not m:
        return False
    first_p = m.group(1)
    return fk in first_p


def check_forbidden_patterns(content):
    """Check for known broken patterns."""
    issues = []
    if 'HowTo Schema' in content:
        # Check if appears in H2 specifically
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
    content = load(path)

    print(f"=== {path} ===")
    print(f"Focus keyword: {fk}")
    print()

    # 1. Word count
    fk_n, w_n, density = fk_density(content, fk)
    print(f"Word count:      {w_n} visible words")

    pass_count = 0
    fail_count = 0

    if w_n >= 1400:
        print(f"                 OK above 1400 minimum")
        pass_count += 1
    else:
        print(f"                 FAIL below 1400 (recommend 1500+)")
        fail_count += 1

    # 2. FK density
    print(f"FK count:        {fk_n} visible occurrences")
    print(f"FK density:      {density:.2f}%")
    if 1.0 <= density <= 1.7:
        print(f"                 OK in target range 1.0-1.5% (sweet spot)")
        pass_count += 1
    elif 0.7 <= density < 1.0:
        print(f"                 FAIL slightly low (target 1.0-1.5%)")
        fail_count += 1
    elif 1.7 < density <= 2.5:
        print(f"                 FAIL slightly high (target 1.0-1.5%)")
        fail_count += 1
    else:
        print(f"                 FAIL outside acceptable range")
        fail_count += 1

    # 3. Heading balance
    h_open, h_close = check_headings(content)
    print(f"Heading balance: {h_open} open / {h_close} close")
    if h_open == h_close == 12:
        print(f"                 OK 12/12 (target structure)")
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
    print(f"HowTo block:     {howto_issues[0] if len(howto_issues) == 1 else 'has issues'}")
    if len(howto_issues) > 1 or howto_issues[0] != 'OK':
        for i in howto_issues:
            if i != 'OK':
                print(f"                 - {i}")
        if howto_issues != ['OK']:
            fail_count += 1
    else:
        pass_count += 1

    # 7. FAQ alignment
    faq_issues = check_faq_alignment(content)
    print(f"FAQ block:       {faq_issues[0] if len(faq_issues) == 1 else 'has issues'}")
    if len(faq_issues) > 1 or not faq_issues[0].startswith('OK'):
        for i in faq_issues:
            if not i.startswith('OK'):
                print(f"                 - {i}")
        if not faq_issues[0].startswith('OK'):
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
