#!/usr/bin/env python3
"""Convert old/broken HowTo block formats to canonical 8594 format.

Use cases:
- Pre-2026 articles using old <h4> step-title format
- Articles with extra JSON fields (hasDuration, days, hours etc.)
- Articles with outer <h3 class="rank-math-howto-title"> wrapper
- Articles with <div class="rank-math-howto-steps"> wrapper layer

Modes:
1. Local file: python fix-howto-block.py article.html
2. WP-CLI batch: python fix-howto-block.py 8489 8478 8466

The canonical format is post 8594's structure (see references/howto-block.md):
- JSON: only "steps" + "sizeSlug": "large"
- HTML: <div class="wp-block-rank-math-howto-block"> with <div class="rank-math-howto-step">
        each containing <h3 class="rank-math-howto-title"> + <div class="rank-math-howto-content">
"""
import re
import json
import sys
import os
import subprocess
import tempfile
from pathlib import Path

# WP-CLI config — set via env vars before running:
#   WP_SSH_KEY  : path to your SSH private key (default: ~/.ssh/id_rsa)
#   WP_SSH_HOST : user@host of your WordPress server
#   WP_PATH     : absolute path to WordPress root on the remote server
SSH_KEY = os.environ.get('WP_SSH_KEY', os.path.expanduser('~/.ssh/id_rsa'))
SSH_HOST = os.environ.get('WP_SSH_HOST', 'user@your-wp-host.example.com')
WP_PATH = os.environ.get('WP_PATH', '/path/to/wordpress')


def fix_h2_howto_schema(content):
    """Strip 'HowTo Schema' suffix from H2 headings."""
    def replace_h2(m):
        h2_text = m.group(0)
        h2_text = re.sub(r'\s*HowTo\s+Schema\s*', '', h2_text)
        return h2_text
    return re.sub(r'<h2 class="wp-block-heading">[^<]+</h2>', replace_h2, content)


def fix_howto_block(content):
    """Rewrite HowTo block to canonical format."""
    pattern = re.compile(
        r'<!-- wp:rank-math/howto-block (\{.*?\}) -->\s*'
        r'(.*?)'
        r'<!-- /wp:rank-math/howto-block -->',
        re.DOTALL,
    )

    def replace_block(m):
        json_str = m.group(1)
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return m.group(0)

        steps = data.get('steps', [])
        if not steps:
            return m.group(0)

        # Clean JSON: only steps + sizeSlug
        clean_data = {'steps': steps, 'sizeSlug': 'large'}
        clean_json = json.dumps(clean_data, ensure_ascii=False, separators=(',', ':'))

        # Build canonical HTML
        step_html = []
        for s in steps:
            title = s.get('title', '')
            sc = s.get('content', '')
            step_html.append(
                f'<div class="rank-math-howto-step">'
                f'<h3 class="rank-math-howto-title">{title}</h3>'
                f'<div class="rank-math-howto-content">{sc}</div>'
                f'</div>'
            )

        new_html = (
            '<div class="wp-block-rank-math-howto-block">'
            + ''.join(step_html)
            + '</div>'
        )
        return f'<!-- wp:rank-math/howto-block {clean_json} -->\n{new_html}\n<!-- /wp:rank-math/howto-block -->'

    return pattern.sub(replace_block, content)


def diagnose(content):
    issues = []
    if 'HowTo Schema' in content:
        if re.search(r'<h2 class="wp-block-heading">[^<]*HowTo Schema[^<]*</h2>', content):
            issues.append('"HowTo Schema" in H2 heading')
        else:
            issues.append('"HowTo Schema" text in body')
    if 'rank-math-howto-step-title' in content:
        issues.append('Old class: rank-math-howto-step-title')
    if 'rank-math-howto-step-content' in content:
        issues.append('Old class: rank-math-howto-step-content')
    if '<div class="rank-math-howto-steps">' in content:
        issues.append('Old wrapper: rank-math-howto-steps')
    if re.search(r'wp-block-rank-math-howto-block"><h3 class="rank-math-howto-title">', content):
        issues.append('Outer h3 title (should be removed)')
    if re.search(r'rank-math-howto-step"><h4', content):
        issues.append('h4 inside step (should be h3)')
    if 'hasDuration' in content or 'hasTotalTime' in content:
        issues.append('Extra JSON fields (hasDuration etc.)')
    return issues


def fix_local_file(path, dry=False):
    p = Path(path)
    content = p.read_text(encoding='utf-8')

    issues = diagnose(content)
    if not issues:
        print(f'{path}: clean — no fixes needed')
        return True

    print(f'{path}: issues detected')
    for i in issues:
        print(f'  - {i}')

    new_content = fix_h2_howto_schema(content)
    new_content = fix_howto_block(new_content)
    new_issues = diagnose(new_content)

    if new_issues:
        print(f'  remaining after fix:')
        for i in new_issues:
            print(f'  - {i}')
    else:
        print(f'  ✓ all fixed')

    if dry:
        print(f'  DRY RUN - not writing')
        return True

    p.write_text(new_content, encoding='utf-8', newline='\n')
    print(f'  written ({len(content)} -> {len(new_content)} bytes)')
    return True


def ssh(cmd):
    full = f'ssh -i {SSH_KEY} {SSH_HOST} "cd {WP_PATH} && {cmd}"'
    return subprocess.run(full, shell=True, capture_output=True, text=True, encoding='utf-8')


def fetch_post(post_id):
    r = ssh(f'wp post get {post_id} --field=content')
    if r.returncode != 0:
        raise RuntimeError(f'Fetch {post_id} failed: {r.stderr}')
    return r.stdout


def push_post(post_id, content, post_date):
    with tempfile.NamedTemporaryFile(
        mode='w', encoding='utf-8',
        delete=False, suffix='.html',
        newline='\n',
    ) as f:
        f.write(content)
        local_tmp = f.name

    remote_tmp = f'/tmp/fixhowto_{post_id}.html'
    upload = subprocess.run(
        f'cat "{local_tmp}" | ssh -i {SSH_KEY} {SSH_HOST} "cat > {remote_tmp}"',
        shell=True, capture_output=True, text=True,
    )
    if upload.returncode != 0:
        os.unlink(local_tmp)
        return False, upload.stderr

    cmd = f"wp post update {post_id} {remote_tmp} --post_date='{post_date}'"
    r = ssh(cmd)
    os.unlink(local_tmp)
    return r.returncode == 0, r.stdout + r.stderr


def get_post_date(post_id):
    r = ssh(
        f"wp post list --post__in={post_id} --post_status=any "
        f'--fields=ID,post_date --format=csv'
    )
    lines = r.stdout.strip().split('\n')
    return lines[1].split(',')[1] if len(lines) >= 2 else None


def fix_wp_post(post_id, dry=False):
    print(f'\n=== POST {post_id} ===')
    try:
        content = fetch_post(post_id)
    except Exception as e:
        print(f'  ERROR: {e}')
        return False

    issues = diagnose(content)
    if not issues:
        print('  CLEAN — no fixes needed')
        return True

    print(f'  Issues: {issues}')

    new_content = fix_h2_howto_schema(content)
    new_content = fix_howto_block(new_content)
    new_issues = diagnose(new_content)

    if new_issues:
        print(f'  After fix: {new_issues}')
    else:
        print('  After fix: CLEAN')

    if dry:
        print('  DRY RUN - not pushing')
        return True

    pd = get_post_date(post_id)
    if not pd:
        print('  ERROR: could not fetch post_date')
        return False

    ok, msg = push_post(post_id, new_content, pd)
    print(f'  Push: {"OK" if ok else "FAIL"} {msg.strip()[:100]}')
    return ok


def main():
    args = sys.argv[1:]
    dry = '--dry' in args
    args = [a for a in args if a != '--dry']

    if not args:
        print(__doc__)
        sys.exit(1)

    for arg in args:
        if arg.endswith('.html') or arg.endswith('.htm') or '/' in arg or '\\' in arg:
            fix_local_file(arg, dry=dry)
        else:
            try:
                post_id = int(arg)
                fix_wp_post(post_id, dry=dry)
            except ValueError:
                print(f'Skip "{arg}" — not a valid path or post ID')


if __name__ == '__main__':
    main()
