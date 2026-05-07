#!/usr/bin/env python3
"""Regenerate FAQ block HTML from JSON metadata to fix alignment errors.

Use cases:
- "區塊包含未預期或無效的內容" warning on FAQ block
- JSON questions field manually edited but HTML not updated
- Batch fixing many articles' FAQ blocks

Modes:
1. Local file: python regenerate-faq.py article.html
2. WP-CLI batch: python regenerate-faq.py 8489 8478 8579
   (requires SSH config — set SSH_KEY/SSH_HOST/WP_PATH env vars)

The JSON in <!-- wp:rank-math/faq-block ... --> is treated as source of truth.
HTML between block comments is regenerated to match.
"""
import re
import json
import html
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


def faq_escape(s):
    """Minimal HTML escape — matches Gutenberg's FAQ output."""
    return s.replace('&', '&amp;').replace('<', '&lt;')


def regenerate_faq(content):
    """Find FAQ block, regenerate HTML from JSON. Returns updated content."""
    pattern = re.compile(
        r'(<!-- wp:rank-math/faq-block (\{.*?\}) -->)'
        r'\s*'
        r'(<div class="wp-block-rank-math-faq-block">.*?</div>)'
        r'\s*'
        r'(<!-- /wp:rank-math/faq-block -->)',
        re.DOTALL,
    )

    def replace(m):
        prefix = m.group(1)
        json_str = m.group(2)
        suffix = m.group(4)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f'  WARN: FAQ JSON parse error: {e}', file=sys.stderr)
            return m.group(0)  # keep original on parse failure

        questions = data.get('questions', [])
        if not questions:
            return m.group(0)

        items = []
        for q in questions:
            t = faq_escape(q.get('title', ''))
            c = faq_escape(q.get('content', ''))
            items.append(
                f'<div class="rank-math-faq-item">'
                f'<h3 class="rank-math-question">{t}</h3>'
                f'<div class="rank-math-answer">{c}</div>'
                f'</div>'
            )

        new_html = (
            '<div class="wp-block-rank-math-faq-block">'
            + ''.join(items)
            + '</div>'
        )
        return f'{prefix}\n{new_html}\n{suffix}'

    return pattern.sub(replace, content)


def fix_local_file(path, dry=False):
    """Fix a local HTML file in place (or print diff in dry mode)."""
    p = Path(path)
    content = p.read_text(encoding='utf-8')
    new_content = regenerate_faq(content)

    if content == new_content:
        print(f'{path}: no FAQ changes needed')
        return True

    if dry:
        print(f'{path}: would regenerate FAQ block ({len(content)} -> {len(new_content)} bytes)')
        return True

    p.write_text(new_content, encoding='utf-8', newline='\n')
    print(f'{path}: FAQ regenerated ({len(content)} -> {len(new_content)} bytes)')
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
    """Push fixed content to WP via file argument syntax (LF newlines)."""
    with tempfile.NamedTemporaryFile(
        mode='w', encoding='utf-8',
        delete=False, suffix='.html',
        newline='\n',
    ) as f:
        f.write(content)
        local_tmp = f.name

    remote_tmp = f'/tmp/regenfaq_{post_id}.html'
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

    new_content = regenerate_faq(content)

    if content == new_content:
        print('  no FAQ changes needed')
        return True

    print(f'  FAQ regenerated ({len(content)} -> {len(new_content)} bytes)')

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
            # Treat as WP post ID
            try:
                post_id = int(arg)
                fix_wp_post(post_id, dry=dry)
            except ValueError:
                print(f'Skip "{arg}" — not a valid path or post ID')


if __name__ == '__main__':
    main()
