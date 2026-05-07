#!/usr/bin/env node
/**
 * Regenerate FAQ block HTML from JSON metadata to fix alignment errors.
 * Mirror of tools/regenerate-faq.py for Node-only environments.
 *
 * Use cases:
 *   - "區塊包含未預期或無效的內容" warning on FAQ block
 *   - JSON questions field manually edited but HTML not updated
 *   - Batch fixing many articles' FAQ blocks
 *
 * Modes:
 *   1. Local file:    node tools/regenerate-faq.mjs article.html
 *   2. WP-CLI batch:  node tools/regenerate-faq.mjs 8489 8478 8579
 *
 * Env vars for WP-CLI mode:
 *   WP_SSH_KEY  : path to SSH private key (default: ~/.ssh/id_rsa)
 *   WP_SSH_HOST : user@host of WordPress server
 *   WP_PATH     : absolute path to WordPress root
 *
 * Flags:
 *   --dry      : show plan only, do not write or push
 *
 * The JSON in <!-- wp:rank-math/faq-block ... --> is treated as source of
 * truth; HTML is regenerated to match. Escaping rule matches Gutenberg's
 * own renderer (only & and < are escaped; > stays literal).
 */
import { readFile, writeFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import { argv, exit, env, stderr, stdout } from "node:process";
import { homedir } from "node:os";
import { join, resolve } from "node:path";

const SSH_KEY = env.WP_SSH_KEY || join(homedir(), ".ssh", "id_rsa");
const SSH_HOST = env.WP_SSH_HOST || "user@your-wp-host.example.com";
const WP_PATH = env.WP_PATH || "/path/to/wordpress";

// ---------- Core regeneration --------------------------------------------

function faqEscape(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
}

function regenerateFaq(content) {
  return content.replace(
    /(<!-- wp:rank-math\/faq-block (\{[\s\S]*?\}) -->)\s*(<div class="wp-block-rank-math-faq-block">[\s\S]*?<\/div>)\s*(<!-- \/wp:rank-math\/faq-block -->)/g,
    (full, prefix, jsonStr, _htmlBlock, suffix) => {
      let data;
      try {
        data = JSON.parse(jsonStr);
      } catch (e) {
        stderr.write(`  WARN: FAQ JSON parse error: ${e.message}\n`);
        return full;
      }
      const questions = data.questions || [];
      if (!questions.length) return full;

      const items = questions
        .map((q) => {
          const t = faqEscape(q.title || "");
          const c = faqEscape(q.content || "");
          return (
            `<div class="rank-math-faq-item">` +
            `<h3 class="rank-math-question">${t}</h3>` +
            `<div class="rank-math-answer">${c}</div>` +
            `</div>`
          );
        })
        .join("");
      const newHtml = `<div class="wp-block-rank-math-faq-block">${items}</div>`;
      return `${prefix}\n${newHtml}\n${suffix}`;
    },
  );
}

async function fixLocalFile(path, dry) {
  const buf = await readFile(path, "utf8");
  const next = regenerateFaq(buf);
  if (buf === next) {
    stdout.write(`${path}: no FAQ changes needed\n`);
    return true;
  }
  if (dry) {
    stdout.write(`${path}: would regenerate FAQ block (${buf.length} -> ${next.length} bytes)\n`);
    return true;
  }
  await writeFile(path, next, { encoding: "utf8" });
  stdout.write(`${path}: FAQ regenerated (${buf.length} -> ${next.length} bytes)\n`);
  return true;
}

// ---------- WP-CLI mode --------------------------------------------------

function ssh(cmd) {
  return new Promise((resolveSpawn) => {
    const full = `cd ${WP_PATH} && ${cmd}`;
    const p = spawn("ssh", ["-i", SSH_KEY, SSH_HOST, full], { stdio: ["ignore", "pipe", "pipe"] });
    let out = "";
    let err = "";
    p.stdout.on("data", (d) => { out += d.toString("utf8"); });
    p.stderr.on("data", (d) => { err += d.toString("utf8"); });
    p.on("close", (code) => resolveSpawn({ code, stdout: out, stderr: err }));
    p.on("error", (e) => resolveSpawn({ code: -1, stdout: "", stderr: e.message }));
  });
}

async function fetchPost(postId) {
  const r = await ssh(`wp post get ${postId} --field=content`);
  if (r.code !== 0) throw new Error(`Fetch ${postId} failed: ${r.stderr}`);
  return r.stdout;
}

async function getPostDate(postId) {
  const r = await ssh(
    `wp post list --post__in=${postId} --post_status=any --fields=ID,post_date --format=csv`,
  );
  const lines = r.stdout.trim().split("\n");
  return lines.length >= 2 ? lines[1].split(",")[1] : null;
}

async function pushPost(postId, content, postDate) {
  // Stream the content directly to ssh's stdin — no shell wrapper, so this
  // works on Windows, macOS, and Linux without a POSIX `sh` dependency.
  const remoteTmp = `/tmp/regenfaq_${postId}.html`;
  const upload = await new Promise((res) => {
    const p = spawn(
      "ssh",
      ["-i", SSH_KEY, SSH_HOST, `cat > ${remoteTmp}`],
      { stdio: ["pipe", "ignore", "pipe"] },
    );
    let err = "";
    p.stderr.on("data", (d) => { err += d.toString("utf8"); });
    p.on("close", (code) => res({ code, stderr: err }));
    p.on("error", (e) => res({ code: -1, stderr: e.message }));
    p.stdin.end(Buffer.from(content, "utf8"));
  });
  if (upload.code !== 0) return { ok: false, msg: upload.stderr };

  const r = await ssh(`wp post update ${postId} ${remoteTmp} --post_date='${postDate}'`);
  return { ok: r.code === 0, msg: (r.stdout + r.stderr).trim().slice(0, 100) };
}

async function fixWpPost(postId, dry) {
  stdout.write(`\n=== POST ${postId} ===\n`);
  let content;
  try {
    content = await fetchPost(postId);
  } catch (e) {
    stdout.write(`  ERROR: ${e.message}\n`);
    return false;
  }

  const next = regenerateFaq(content);
  if (content === next) {
    stdout.write("  no FAQ changes needed\n");
    return true;
  }
  stdout.write(`  FAQ regenerated (${content.length} -> ${next.length} bytes)\n`);

  if (dry) {
    stdout.write("  DRY RUN - not pushing\n");
    return true;
  }
  const pd = await getPostDate(postId);
  if (!pd) {
    stdout.write("  ERROR: could not fetch post_date\n");
    return false;
  }
  const { ok, msg } = await pushPost(postId, next, pd);
  stdout.write(`  Push: ${ok ? "OK" : "FAIL"} ${msg}\n`);
  return ok;
}

// ---------- CLI ----------------------------------------------------------

async function main() {
  const args = argv.slice(2);
  const dry = args.includes("--dry");
  const targets = args.filter((a) => a !== "--dry");
  if (!targets.length) {
    stdout.write("Usage: regenerate-faq [--dry] <article.html | post_id> [...]\n");
    return 1;
  }
  for (const t of targets) {
    if (t.endsWith(".html") || t.endsWith(".htm") || t.includes("/") || t.includes("\\")) {
      await fixLocalFile(resolve(t), dry);
    } else if (/^\d+$/.test(t)) {
      await fixWpPost(parseInt(t, 10), dry);
    } else {
      stdout.write(`Skip "${t}" — not a valid path or post ID\n`);
    }
  }
  return 0;
}

main().then((c) => exit(c ?? 0)).catch((e) => { stderr.write(`Error: ${e.message}\n`); exit(1); });
