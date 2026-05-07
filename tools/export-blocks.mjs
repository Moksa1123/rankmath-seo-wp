#!/usr/bin/env node
/**
 * Export article HTML as Gutenberg block-paste-ready output (Node version).
 *
 * Mirrors tools/export-blocks.py for users who prefer npm / npx and don't
 * want a Python toolchain.
 *
 * Usage:
 *   node tools/export-blocks.mjs article.html
 *   node tools/export-blocks.mjs article.html --to-file ready.html
 *   node tools/export-blocks.mjs article.html --print
 *   node tools/export-blocks.mjs article.html --only howto
 *   node tools/export-blocks.mjs article.html --only faq
 *
 * Or via the npm bin: `npx rankmath-export article.html`.
 *
 * Zero runtime dependencies — uses only Node 18+ stdlib (fs/promises,
 * child_process, process, path).
 */
import { readFile, writeFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import { argv, exit, platform, stderr, stdout } from "node:process";
import { resolve } from "node:path";

const CLIP_INSTRUCTIONS = `
--- HOW TO PASTE INTO WORDPRESS ----------------------------------
1. WP Admin -> Posts -> Add New (or open an existing post)
2. Click inside the editor canvas (NOT a single block)
3. Press Ctrl+V (Windows/Linux) or Cmd+V (macOS)
4. Gutenberg parses the block comments and rebuilds every block
5. Save draft and review — HowTo / FAQ / embeds should all render
------------------------------------------------------------------
`;

const SHORT_TO_FULL = {
  howto: "rank-math/howto-block",
  faq: "rank-math/faq-block",
  table: "table",
  embed: "embed",
  quote: "quote",
  code: "code",
};

// ---------- Helpers ------------------------------------------------------

function normaliseNewlines(text) {
  return text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
}

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function extractBlock(content, shortName) {
  const full = SHORT_TO_FULL[shortName] ?? shortName;
  const re = new RegExp(
    `<!--\\s*wp:${escapeRegExp(full)}\\b[\\s\\S]*?<!--\\s*/wp:${escapeRegExp(full)}\\s*-->`,
  );
  const m = content.match(re);
  return m ? m[0] : null;
}

function validateBlocks(content) {
  const errors = [];

  // Block open/close balance.
  // Use non-greedy `[\s\S]*?` for the JSON metadata so it can span the
  // inner braces inside HowTo / FAQ block JSON.
  const openRe = /<!--\s*wp:([a-z0-9/_-]+)(?:\s+\{[\s\S]*?\})?\s*(\/?)-->/g;
  const closeRe = /<!--\s*\/wp:([a-z0-9/_-]+)\s*-->/g;
  const opens = new Map();
  const closes = new Map();
  let m;
  while ((m = openRe.exec(content)) !== null) {
    if (m[2] === "/") continue;
    opens.set(m[1], (opens.get(m[1]) ?? 0) + 1);
  }
  while ((m = closeRe.exec(content)) !== null) {
    closes.set(m[1], (closes.get(m[1]) ?? 0) + 1);
  }
  for (const [name, n] of opens) {
    const c = closes.get(name) ?? 0;
    if (n !== c) errors.push(`block <${name}>: ${n} open / ${c} close`);
  }
  for (const [name] of closes) {
    if (!opens.has(name)) errors.push(`block <${name}>: closing tag without opening`);
  }

  // HowTo JSON sanity.
  const howto = content.match(/<!--\s*wp:rank-math\/howto-block\s+(\{[\s\S]*?\})\s*-->/);
  if (howto) {
    try {
      const data = JSON.parse(howto[1]);
      if (!data.steps || data.steps.length === 0) {
        errors.push("HowTo block: JSON has no steps");
      }
      for (const f of ["hasDuration", "hasTotalTime", "titleWrapper"]) {
        if (f in data) errors.push(`HowTo block: forbidden JSON field '${f}'`);
      }
    } catch (e) {
      errors.push(`HowTo block: JSON parse error — ${e.message}`);
    }
  }

  // FAQ JSON sanity.
  const faq = content.match(/<!--\s*wp:rank-math\/faq-block\s+(\{[\s\S]*?\})\s*-->/);
  if (faq) {
    try {
      const data = JSON.parse(faq[1]);
      if (!data.questions || data.questions.length === 0) {
        errors.push("FAQ block: JSON has no questions");
      }
    } catch (e) {
      errors.push(`FAQ block: JSON parse error — ${e.message}`);
    }
  }

  // Forbidden patterns.
  if (/<h2[^>]*>[^<]*HowTo Schema[^<]*<\/h2>/.test(content)) {
    errors.push('"HowTo Schema" appears in an H2 heading — strip it');
  }
  if (content.includes("application/ld+json")) {
    errors.push("Inline <script type=\"application/ld+json\"> — many themes strip it");
  }

  return errors;
}

function tryCopy(cmd, args, text, encoding) {
  return new Promise((resolveCopy) => {
    const p = spawn(cmd, args, { stdio: ["pipe", "ignore", "pipe"] });
    p.on("error", () => resolveCopy(false));
    p.on("close", (code) => resolveCopy(code === 0));
    p.stdin.end(Buffer.from(text, encoding));
  });
}

async function copyToClipboard(text) {
  if (platform === "win32") {
    return tryCopy("clip", [], text, "utf16le");
  }
  if (platform === "darwin") {
    return tryCopy("pbcopy", [], text, "utf8");
  }
  // Linux / WSL — try xclip, xsel, wl-copy in order (mirrors Python).
  for (const [cmd, args] of [
    ["xclip", ["-selection", "clipboard"]],
    ["xsel", ["--clipboard", "--input"]],
    ["wl-copy", []],
  ]) {
    if (await tryCopy(cmd, args, text, "utf8")) return true;
  }
  return false;
}

// ---------- CLI ----------------------------------------------------------

function parseArgs(args) {
  const out = { to_file: null, to_stdout: false, only: null, no_validate: false, article: null };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--to-file") out.to_file = args[++i];
    else if (a === "--print") out.to_stdout = true;
    else if (a === "--only") out.only = args[++i];
    else if (a === "--no-validate") out.no_validate = true;
    else if (a === "-h" || a === "--help") {
      stdout.write(`Usage: export-blocks article.html [--to-file PATH | --print] [--only TYPE] [--no-validate]
TYPE: howto | faq | table | embed | quote | code\n`);
      exit(0);
    } else if (!out.article) out.article = a;
  }
  if (!out.article) {
    stderr.write("Missing article path. Run with --help.\n");
    exit(2);
  }
  return out;
}

async function main() {
  const opts = parseArgs(argv.slice(2));
  let content;
  try {
    content = normaliseNewlines(await readFile(resolve(opts.article), "utf8"));
  } catch (e) {
    stderr.write(`File error: ${e.message}\n`);
    return 2;
  }

  if (opts.only) {
    const block = extractBlock(content, opts.only);
    if (!block) {
      stderr.write(`No '${opts.only}' block found in ${opts.article}\n`);
      return 1;
    }
    content = block;
  }

  if (!opts.no_validate) {
    const errors = validateBlocks(content);
    if (errors.length > 0) {
      stderr.write(`Validation failed for ${opts.article}:\n`);
      for (const e of errors) stderr.write(`  - ${e}\n`);
      stderr.write("\nFix issues or rerun with --no-validate to bypass.\n");
      return 1;
    }
  }

  if (opts.to_file) {
    await writeFile(resolve(opts.to_file), content, { encoding: "utf8" });
    stdout.write(`Wrote ${content.length.toLocaleString()} chars -> ${opts.to_file}\n`);
    stdout.write(CLIP_INSTRUCTIONS);
    return 0;
  }
  if (opts.to_stdout) {
    stdout.write(content);
    return 0;
  }
  const ok = await copyToClipboard(content);
  if (ok) {
    stdout.write(`Copied ${content.length.toLocaleString()} chars to clipboard.\n`);
    stdout.write(CLIP_INSTRUCTIONS);
    return 0;
  }
  stderr.write("Clipboard copy failed; falling back to stdout:\n");
  stdout.write(content);
  return 1;
}

main().then((code) => exit(code ?? 0));
