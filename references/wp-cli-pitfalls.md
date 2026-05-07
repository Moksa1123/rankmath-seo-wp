# WP-CLI Pitfalls — From Real Debugging

Two critical gotchas that broke production debugging on moksaweb.com. Document
exists because these took hours to identify the first time.

## Pitfall 1: --post_content shell expansion fails on long content

### The error

```bash
$ wp post update 8489 --post_content="$(cat /tmp/article.html)"
Error: Unable to read content from 'wp:paragraph'.
```

### Why it happens

When article content starts with `<!-- wp:paragraph -->` (Gutenberg block
comment) and is passed via `$(cat file)` shell expansion, bash interprets the
content as additional arguments. WP-CLI receives "wp:paragraph" as a literal
argument and tries to read it as a filename.

### The fix: file argument syntax

WP-CLI's `wp post update` accepts a file path as positional argument:

```bash
# ✅ WORKS — file argument syntax
wp post update 8489 /tmp/article.html

# ✅ With other flags
wp post update 8489 /tmp/article.html --post_date='2026-05-08 09:00:00'
```

WP-CLI reads the file directly, no shell expansion involved.

### Same pattern for create

```bash
# Create
wp post create /tmp/article.html \
  --post_title='Article Title' \
  --post_status=future \
  --post_date='2026-05-08 09:00:00' \
  --post_author=1 \
  --porcelain
```

The `--porcelain` flag returns just the post ID for capturing.

## Pitfall 2: Python on Windows writes \r\n by default

### The error symptom

After successfully pushing content via `wp post update`, opening the post in
Gutenberg editor shows mysterious "區塊包含未預期或無效的內容" warnings on
blocks that were perfectly fine in source HTML.

### Why it happens

Python's `tempfile.NamedTemporaryFile` and `open()` on Windows default to
"text mode with universal newlines" — writes `\n` but converts to `\r\n` on
disk. Then:
1. File is uploaded to Linux server (cat | ssh)
2. wp post update reads file with `\r\n` endings
3. WP saves content with `\r\n` characters preserved
4. Gutenberg compares stored HTML vs expected HTML
5. Stored has `\r\n`, expected has `\n` — validation fails

### The fix: force LF newlines

```python
# ❌ Default (Windows adds \r\n)
with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8') as f:
    f.write(content)

# ✅ Explicit LF
with tempfile.NamedTemporaryFile(
    mode='w',
    encoding='utf-8',
    newline='\n',  # ← This is the critical line
) as f:
    f.write(content)
```

Or with regular `open()`:

```python
# ✅ LF on all platforms
with open('article.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
```

### Detection

If posts mysteriously show block validation errors after batch processing on
Windows, check for `\r` characters in saved content:

```bash
ssh user@wp-host "wp post get POST_ID --field=content" | tr -cd '\r' | wc -c
# Output > 0 means CR characters present
```

## Pitfall 3: post_status preservation across update

### Issue

When using `wp post update POST_ID file.html --post_date='YYYY-MM-DD'`, the
`post_status` is preserved by default. BUT: if the post was `future`
(scheduled) and the new `post_date` is in the past, WordPress auto-promotes
to `publish`.

### Workaround

Always explicitly set both:

```bash
wp post update POST_ID file.html \
  --post_date='2026-05-08 09:00:00' \
  --post_status=future
```

Or verify after update:

```bash
wp post list --post__in=POST_ID --fields=ID,post_status,post_date --format=table
```

## Pitfall 4: Cloudways WP-Cron unreliable

### Issue

Posts scheduled to publish at a future time via WP-Cron sometimes don't fire
on schedule on Cloudways hosting. Found posts stuck in `future` status hours
or days past their `post_date`.

### Workaround: manual publish via SQL

```bash
# Force publish any stuck future posts
ssh user@wp-host "cd /path/to/wp && wp db query \"
  UPDATE wp_posts
  SET post_status='publish'
  WHERE ID IN (SELECT ID FROM (
    SELECT ID FROM wp_posts
    WHERE post_status='future'
    AND post_date <= NOW()
  ) AS x)
\""

# Clear cache
ssh user@wp-host "cd /path/to/wp && wp cache flush"
```

Run daily via cron or as part of deploy script.

## Pitfall 5: SCP often restricted on managed hosting

### Issue

Cloudways and many managed WordPress hosts disable SCP for security. `scp`
fails silently or with permission errors.

### Workaround: base64 pipe over SSH

```bash
# Upload binary file (image)
base64 -w 0 image.webp | ssh user@host "base64 -d > /tmp/image.webp"

# Upload text file
cat article.html | ssh user@host "cat > /tmp/article.html"
```

Both work over standard SSH connection without SCP-specific permissions.

## Pitfall 6: Cache flush after meta updates

### Issue

After `wp post meta update POST_ID rank_math_focus_keyword 'X'`, sometimes
Rank Math UI in WP admin doesn't reflect the change immediately.

### Workaround

Flush WP cache after meta updates:

```bash
wp cache flush
```

If using Object Cache (Redis, Memcached), also:

```bash
wp redis flush  # If wp-cli redis plugin installed
```

## Pitfall 7: Post body argument restrictions

`wp post update` accepts file as positional only. These don't work:

```bash
# ❌ wp post update doesn't read from stdin
echo "content" | wp post update POST_ID -

# ❌ No --content-file flag exists
wp post update POST_ID --content-file=article.html
```

Only the file as second positional argument works:

```bash
# ✅
wp post update POST_ID article.html
```

## Pitfall 8: Term ID vs Slug for categories

### Issue

`wp post term set POST_ID category 64,101` doesn't work as expected. Numeric
IDs sometimes interpreted as integers vs slugs.

### Use slug instead

```bash
wp post term set POST_ID category claude-code claude-office
```

WP-CLI accepts space-separated slugs and resolves to terms.

If you must use IDs, use the `--by=id` flag:

```bash
wp post term set POST_ID category 64 101 --by=id
```

## Pitfall 9: FileBird folder assignment

### Issue

After `wp media import`, the image lands in default media library. Custom
folders (FileBird plugin) require separate DB query.

### Direct SQL workaround

```bash
ATTACH_ID=$(wp media import /tmp/image.webp ... --porcelain)

wp db query "INSERT INTO wp_fbv_attachment_folder (folder_id, attachment_id) \
  VALUES ($FBV_FOLDER_ID, $ATTACH_ID) \
  ON DUPLICATE KEY UPDATE folder_id=$FBV_FOLDER_ID"
```

Replace `$FBV_FOLDER_ID` with your FileBird folder's numeric ID.

## Recommended Python push function

Distilled from real-world fixes:

```python
import subprocess, os, tempfile

SSH_KEY = os.path.expanduser("~/.ssh/wp_key")
SSH_HOST = "user@wp-host"
WP_PATH = "/path/to/wordpress"


def ssh(cmd):
    full = f'ssh -i {SSH_KEY} {SSH_HOST} "cd {WP_PATH} && {cmd}"'
    return subprocess.run(full, shell=True, capture_output=True, text=True, encoding='utf-8')


def push_post(post_id, content, post_date=None, post_status=None):
    """Push article content to WP via file argument syntax with LF newlines."""
    
    # Critical: newline='\n' to prevent Windows \r\n
    with tempfile.NamedTemporaryFile(
        mode='w', encoding='utf-8',
        delete=False, suffix='.html',
        newline='\n',
    ) as f:
        f.write(content)
        local_tmp = f.name
    
    remote_tmp = f"/tmp/push_{post_id}.html"
    
    # Upload via cat | ssh (works around SCP restrictions)
    upload = subprocess.run(
        f'cat "{local_tmp}" | ssh -i {SSH_KEY} {SSH_HOST} "cat > {remote_tmp}"',
        shell=True, capture_output=True, text=True
    )
    if upload.returncode != 0:
        return False, upload.stderr
    
    # Build wp post update command with file argument
    flags = []
    if post_date:
        flags.append(f"--post_date='{post_date}'")
    if post_status:
        flags.append(f"--post_status={post_status}")
    
    cmd = f"wp post update {post_id} {remote_tmp} {' '.join(flags)}"
    r = ssh(cmd)
    
    os.unlink(local_tmp)
    return r.returncode == 0, r.stdout + r.stderr
```

## Pre-flight check

Before pushing to production, run locally:

```bash
# Verify article specs
python tools/verify-article.py article.html "Focus Keyword"

# Verify HowTo block format
python tools/fix-howto-block.py article.html --dry

# Verify FAQ alignment
python tools/regenerate-faq.py article.html --dry
```

If all pass, then push.
