#!/usr/bin/env node
/**
 * Convert old / broken HowTo block formats to canonical 8594 format.
 * Mirror of tools/fix-howto-block.py for Node-only environments.
 *
 * Modes:
 *   1. Local file:    node tools/fix-howto-block.mjs article.html
 *   2. WP-CLI batch:  node tools/fix-howto-block.mjs 8489 8478 8466
 *
 * Env vars for WP-CLI mode:
 *   WP_SSH_KEY  : path to SSH private key (default: ~/.ssh/id_rsa)
 *   WP_SSH_HOST : user@host of WordPress server
 *   WP_PATH     : absolute path to WordPress root
 *
 * Flags:
 *   --dry      : diagnose only, do not write
 *
 * Canonical format (post 8594):
 *   - JSON: only "steps" + "sizeSlug": "large" (no hasDuration etc.)
 *   - HTML: <div class="wp-block-rank-math-howto-block"> with
 *           <div class="rank-math-howto-step"> > <h3 class="rank-math-howto-title">
 *           + <div class="rank-math-howto-content">
 */
import { readFile, writeFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import { argv, exit, env, stderr, stdout } from "node:process";
import { homedir } from "node:os";
import { join, resolve } from "node:path";

const SSH_KEY = env.WP_SSH_KEY || join(homedir(), ".ssh", "id_rsa");
const SSH_HOST = env.WP_SSH_HOST || "user@your-wp-host.example.com";
const WP_PATH = env.WP_PATH || "/path/to/wordpress";

// ---------- Diagnose / fix --------------------------------------------------

function diagnose(content) {
  const issues = [];
  if (content.includes("HowTo Schema")) {
    if (/<h2 class="wp-block-heading">[^<]*HowTo Schema[^<]*<\/h2>/.test(content)) {
      issues.push('"HowTo Schema" in H2 heading');
    } else {
      issues.push('"HowTo Schema" text in body');
    }
  }
  if (content.includes("rank-math-howto-step-title")) issues.push("Old class: rank-math-howto-step-title");
  if (content.includes("rank-math-howto-step-content")) issues.push("Old class: rank-math-howto-step-content");
  if (content.includes('<div class="rank-math-howto-steps">')) issues.push("Old wrapper: rank-math-howto-steps");
  if (/wp-block-rank-math-howto-block"><h3 class="rank-math-howto-title">/.test(content)) {
    issues.push("Outer h3 title (should be removed)");
  }
  if (/rank-math-howto-step"><h4/.test(content)) issues.push("h4 inside step (should be h3)");
  if (content.includes("hasDuration") || content.includes("hasTotalTime")) {
    issues.push("Extra JSON fields (hasDuration etc.)");
  }
  return issues;
}

function fixH2HowtoSchema(content) {
  return content.replace(
    /<h2 class="wp-block-heading">[^<]+<\/h2>/g,
    (m) => m.replace(/\s*HowTo\s+Schema\s*/g, ""),
  );
}

function fixHowtoBlock(content) {
  return content.replace(
    /<!-- wp:rank-math\/howto-block (\{[\s\S]*?\}) -->[\s\S]*?<!-- \/wp:rank-math\/howto-block -->/g,
    (full, jsonStr) => {
      let data;
      try {
        data = JSON.parse(jsonStr);
      } catch {
        return full;
      }
      const steps = data.steps || [];
      if (!steps.length) return full;

      const cleanData = { steps, sizeSlug: "large" };
      const cleanJson = JSON.stringify(cleanData);

      const stepHtml = steps
        .map((s) => {
          const title = s.title || "";
          const sc = s.content || "";
          return (
            `<div class="rank-math-howto-step">` +
            `<h3 class="rank-math-howto-title">${title}</h3>` +
            `<div class="rank-math-howto-content">${sc}</div>` +
            `</div>`
          );
        })
        .join("");
      const newHtml = `<div class="wp-block-rank-math-howto-block">${stepHtml}</div>`;

      return `<!-- wp:rank-math/howto-block ${cleanJson} -->\n${newHtml}\n<!-- /wp:rank-math/howto-block -->`;
    },
  );
}

async function fixLocalFile(path, dry) {
  const buf = await readFile(path, "utf8");
  const issues = diagnose(buf);
  if (!issues.length) {
    stdout.write(`${path}: clean — no fixes needed\n`);
    return true;
  }
  stdout.write(`${path}: issues detected\n`);
  for (const i of issues) stdout.write(`  - ${i}\n`);

  let next = fixH2HowtoSchema(buf);
  next = fixHowtoBlock(next);
  const remaining = diagnose(next);
  if (remaining.length) {
    stdout.write("  remaining after fix:\n");
    for (const r of remaining) stdout.write(`  - ${r}\n`);
  } else {
    stdout.write("  OK all fixed\n");
  }
  if (dry) {
    stdout.write("  DRY RUN - not writing\n");
    return true;
  }
  await writeFile(path, next, { encoding: "utf8" });
  stdout.write(`  written (${buf.length} -> ${next.length} bytes)\n`);
  return true;
}

// ---------- WP-CLI mode -----------------------------------------------------

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
  const remoteTmp = `/tmp/fixhowto_${postId}.html`;
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

  const issues = diagnose(content);
  if (!issues.length) {
    stdout.write("  CLEAN — no fixes needed\n");
    return true;
  }
  stdout.write(`  Issues: ${issues.join(", ")}\n`);

  let next = fixH2HowtoSchema(content);
  next = fixHowtoBlock(next);
  const remaining = diagnose(next);
  stdout.write(remaining.length ? `  After fix: ${remaining.join(", ")}\n` : "  After fix: CLEAN\n");

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

// ---------- CLI -------------------------------------------------------------

async function main() {
  const args = argv.slice(2);
  const dry = args.includes("--dry");
  const targets = args.filter((a) => a !== "--dry");
  if (!targets.length) {
    stdout.write("Usage: fix-howto-block [--dry] <article.html | post_id> [...]\n");
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
