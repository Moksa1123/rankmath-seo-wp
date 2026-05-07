#!/usr/bin/env node
/**
 * Install the rankmath-seo-wp skill into any of 8 supported AI platforms.
 * Mirror of tools/install-skill.py for Node-only environments.
 *
 * Usage:
 *   node tools/install-skill.mjs --list
 *   node tools/install-skill.mjs --info claude-code
 *   node tools/install-skill.mjs claude-code              # project scope
 *   node tools/install-skill.mjs claude-code --global     # global scope
 *   node tools/install-skill.mjs cursor --to /path/to/proj
 *   node tools/install-skill.mjs --dry-run claude-code
 *   npx rankmath-install claude-code
 *
 * Zero runtime dependencies — uses only Node 18+ stdlib.
 */
import {
  readFile, writeFile, mkdir, readdir, stat, copyFile, access,
} from "node:fs/promises";
import { existsSync, createWriteStream } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { argv, exit, stderr, stdout, cwd } from "node:process";
import { homedir } from "node:os";
import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");
const PLATFORMS_DIR = join(REPO_ROOT, "assets", "templates", "platforms");

// ---------- Helpers ------------------------------------------------------

function expandPath(p) {
  if (!p) return null;
  if (p.startsWith("~")) return p.replace(/^~/, homedir());
  return p;
}

async function listPlatforms() {
  const entries = await readdir(PLATFORMS_DIR);
  return entries.filter((n) => n.endsWith(".json")).sort();
}

async function loadPlatform(name) {
  const p = join(PLATFORMS_DIR, `${name}.json`);
  if (!existsSync(p)) {
    throw new Error(`Unknown platform: ${name}\nRun --list to see options.`);
  }
  return JSON.parse(await readFile(p, "utf8"));
}

function jsonEscape(s) {
  return JSON.stringify(s);
}

function buildFrontmatter(fm) {
  if (!fm) return "";
  const lines = ["---"];
  for (const [k, v] of Object.entries(fm)) {
    if (v === null || v === undefined) continue;
    if (Array.isArray(v)) {
      lines.push(`${k}: [${v.map(jsonEscape).join(", ")}]`);
    } else if (typeof v === "boolean") {
      lines.push(`${k}: ${v ? "true" : "false"}`);
    } else if (typeof v === "string" && (v.includes("\n") || v.length > 100)) {
      lines.push(`${k}: |`);
      for (const sub of v.split("\n")) lines.push(`  ${sub}`);
    } else {
      lines.push(`${k}: ${jsonEscape(v)}`);
    }
  }
  lines.push("---");
  return lines.join("\n") + "\n\n";
}

async function readSkillBody() {
  const raw = await readFile(join(REPO_ROOT, "SKILL.md"), "utf8");
  if (raw.startsWith("---")) {
    const end = raw.indexOf("\n---", 3);
    if (end !== -1) return raw.slice(end + 4).replace(/^\n+/, "");
  }
  return raw;
}

async function embedReferences(names) {
  const parts = [];
  for (const n of names) {
    const p = join(REPO_ROOT, "references", n);
    if (!existsSync(p)) continue;
    const c = await readFile(p, "utf8");
    parts.push(`\n\n---\n\n## Reference: ${n}\n\n${c}\n`);
  }
  return parts.join("");
}

async function copyDir(src, dst, force) {
  let count = 0;
  if (!existsSync(src)) return 0;
  const stack = [src];
  while (stack.length) {
    const cur = stack.pop();
    const entries = await readdir(cur, { withFileTypes: true });
    for (const e of entries) {
      const full = join(cur, e.name);
      if (e.isDirectory()) {
        stack.push(full);
        continue;
      }
      const rel = relative(src, full);
      const target = join(dst, rel);
      await mkdir(dirname(target), { recursive: true });
      if (existsSync(target) && !force) continue;
      await copyFile(full, target);
      count++;
    }
  }
  return count;
}

// ---------- Install strategies -------------------------------------------

async function installFull(cfg, targetRoot, { force, dryRun }) {
  const fs_ = cfg.folderStructure;
  const skillDir = join(targetRoot, fs_.skillPath);
  const skillFile = join(skillDir, fs_.filename);

  const body = await readSkillBody();
  const content = buildFrontmatter(cfg.frontmatter) + body;
  const plan = { file: skillFile, size: content.length, sections: [] };

  if (dryRun) {
    for (const sec of ["references", "tools", "data", "examples"]) {
      if (cfg.sections?.[sec]) plan.sections.push(sec);
    }
    return plan;
  }

  await mkdir(skillDir, { recursive: true });
  if (existsSync(skillFile) && !force) {
    throw new Error(`Refusing to overwrite ${skillFile} — pass --force to override.`);
  }
  await writeFile(skillFile, content, "utf8");

  for (const sec of ["references", "tools", "data", "examples"]) {
    if (!cfg.sections?.[sec]) continue;
    const n = await copyDir(join(REPO_ROOT, sec), join(skillDir, sec), force);
    plan.sections.push(`${sec} (${n} files)`);
  }
  return plan;
}

async function installRule(cfg, targetRoot, { force, dryRun }) {
  const fs_ = cfg.folderStructure;
  const ruleDir = join(targetRoot, fs_.skillPath);
  const ruleFile = join(ruleDir, fs_.filename);

  let body = await readSkillBody();
  if (cfg.embedReferences?.length) body += await embedReferences(cfg.embedReferences);
  const content = buildFrontmatter(cfg.frontmatter) + body;
  const plan = { file: ruleFile, size: content.length, embedded: cfg.embedReferences || [] };

  if (dryRun) return plan;

  await mkdir(ruleDir, { recursive: true });
  if (existsSync(ruleFile) && !force) {
    throw new Error(`Refusing to overwrite ${ruleFile} — pass --force to override.`);
  }
  await writeFile(ruleFile, content, "utf8");
  return plan;
}

async function installInstructionsAppend(cfg, targetRoot, { force, dryRun }) {
  const fs_ = cfg.folderStructure;
  const target = join(targetRoot, fs_.projectRoot, fs_.filename);
  const begin = cfg.appendMarker;
  const end = cfg.appendMarkerEnd;

  let body = await readSkillBody();
  if (cfg.embedReferences?.length) body += await embedReferences(cfg.embedReferences);
  const section = `\n\n${begin}\n## Rank Math SEO WP Skill\n\n${body}\n${end}\n`;

  let existing = "";
  if (existsSync(target)) existing = await readFile(target, "utf8");
  let newContent;
  if (existing.includes(begin) && existing.includes(end)) {
    const before = existing.split(begin)[0].trimEnd();
    const after = existing.split(end)[1].trimStart();
    newContent = `${before}\n${after}`.trim() + section;
  } else {
    newContent = (existing.trimEnd() + section).replace(/^\n+/, "");
  }

  const plan = { file: target, size: newContent.length, appended: true };
  if (dryRun) return plan;

  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, newContent, "utf8");
  return plan;
}

async function zipDir(zipPath, entries) {
  // Minimal zip writer using stored (no compression) format. Adequate for
  // small text bundles and avoids any external dependency.
  const buffers = [];
  let offset = 0;
  const central = [];

  function crc32(buf) {
    let c;
    const table = crc32._table || (crc32._table = (() => {
      const t = new Uint32Array(256);
      for (let n = 0; n < 256; n++) {
        c = n;
        for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
        t[n] = c;
      }
      return t;
    })());
    let crc = 0xffffffff;
    for (let i = 0; i < buf.length; i++) crc = table[(crc ^ buf[i]) & 0xff] ^ (crc >>> 8);
    return (crc ^ 0xffffffff) >>> 0;
  }

  for (const { name, data } of entries) {
    const nameBuf = Buffer.from(name, "utf8");
    const crc = crc32(data);
    const local = Buffer.alloc(30 + nameBuf.length);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4); // version
    local.writeUInt16LE(0x0800, 6); // flags (utf8)
    local.writeUInt16LE(0, 8); // method = stored
    local.writeUInt16LE(0, 10); // time
    local.writeUInt16LE(0, 12); // date
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(data.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBuf.length, 26);
    local.writeUInt16LE(0, 28);
    nameBuf.copy(local, 30);
    buffers.push(local, data);

    const cd = Buffer.alloc(46 + nameBuf.length);
    cd.writeUInt32LE(0x02014b50, 0);
    cd.writeUInt16LE(20, 4);
    cd.writeUInt16LE(20, 6);
    cd.writeUInt16LE(0x0800, 8);
    cd.writeUInt16LE(0, 10);
    cd.writeUInt16LE(0, 12);
    cd.writeUInt16LE(0, 14);
    cd.writeUInt32LE(crc, 16);
    cd.writeUInt32LE(data.length, 20);
    cd.writeUInt32LE(data.length, 24);
    cd.writeUInt16LE(nameBuf.length, 28);
    cd.writeUInt16LE(0, 30);
    cd.writeUInt16LE(0, 32);
    cd.writeUInt16LE(0, 34);
    cd.writeUInt16LE(0, 36);
    cd.writeUInt32LE(0, 38);
    cd.writeUInt32LE(offset, 42);
    nameBuf.copy(cd, 46);
    central.push(cd);

    offset += local.length + data.length;
  }

  const cdStart = offset;
  let cdSize = 0;
  for (const cd of central) cdSize += cd.length;

  const eocd = Buffer.alloc(22);
  eocd.writeUInt32LE(0x06054b50, 0);
  eocd.writeUInt16LE(0, 4);
  eocd.writeUInt16LE(0, 6);
  eocd.writeUInt16LE(entries.length, 8);
  eocd.writeUInt16LE(entries.length, 10);
  eocd.writeUInt32LE(cdSize, 12);
  eocd.writeUInt32LE(cdStart, 16);
  eocd.writeUInt16LE(0, 20);

  const all = Buffer.concat([...buffers, ...central, eocd]);
  await writeFile(zipPath, all);
  return all.length;
}

async function installZipUpload(cfg, targetRoot, { force, dryRun }) {
  const fs_ = cfg.folderStructure;
  const outZip = join(targetRoot, fs_.skillPath);

  const body = await readSkillBody();
  const skillContent = buildFrontmatter(cfg.frontmatter) + body;

  const plan = { file: outZip, size: 0, entries: [] };
  if (dryRun) {
    plan.entries.push("rankmath-seo-wp/SKILL.md (rewritten)");
    for (const sec of ["references", "data", "examples"]) {
      if (cfg.sections?.[sec]) plan.entries.push(`rankmath-seo-wp/${sec}/`);
    }
    return plan;
  }

  await mkdir(dirname(outZip), { recursive: true });
  if (existsSync(outZip) && !force) {
    throw new Error(`Refusing to overwrite ${outZip} — pass --force to override.`);
  }

  const entries = [{ name: "rankmath-seo-wp/SKILL.md", data: Buffer.from(skillContent, "utf8") }];
  for (const sec of ["references", "data", "examples"]) {
    if (!cfg.sections?.[sec]) continue;
    const root = join(REPO_ROOT, sec);
    if (!existsSync(root)) continue;
    const stack = [root];
    while (stack.length) {
      const cur = stack.pop();
      for (const e of await readdir(cur, { withFileTypes: true })) {
        const full = join(cur, e.name);
        if (e.isDirectory()) { stack.push(full); continue; }
        const rel = relative(REPO_ROOT, full).replaceAll("\\", "/");
        entries.push({ name: `rankmath-seo-wp/${rel}`, data: await readFile(full) });
      }
    }
  }
  plan.size = await zipDir(outZip, entries);
  plan.entries = entries.map((e) => e.name);
  return plan;
}

const STRATEGIES = {
  full: installFull,
  rule: installRule,
  "instructions-append": installInstructionsAppend,
  "zip-upload": installZipUpload,
};

// ---------- CLI ----------------------------------------------------------

async function cmdList() {
  const plats = await listPlatforms();
  if (!plats.length) {
    stderr.write("No platforms configured.\n");
    return 1;
  }
  stdout.write(`${"platform".padEnd(14)} ${"install type".padEnd(22)} verified  display name\n`);
  stdout.write("-".repeat(70) + "\n");
  for (const p of plats) {
    const cfg = JSON.parse(await readFile(join(PLATFORMS_DIR, p), "utf8"));
    const verified = cfg.verified ? "yes" : "no ";
    stdout.write(`${cfg.platform.padEnd(14)} ${cfg.installType.padEnd(22)} ${verified.padEnd(8)}  ${cfg.displayName}\n`);
  }
  return 0;
}

async function cmdInfo(name) {
  const cfg = await loadPlatform(name);
  stdout.write(`Platform: ${cfg.platform}  (${cfg.displayName})\n`);
  stdout.write(`Install type: ${cfg.installType}\n`);
  const fs_ = cfg.folderStructure;
  stdout.write(`Project path: ${fs_.projectRoot}/${fs_.skillPath}/${fs_.filename}\n`.replace(/\/+/g, "/"));
  if (fs_.globalRoot) stdout.write(`Global path:  ${fs_.globalRoot}/${fs_.skillPath}/${fs_.filename}\n`.replace(/\/+/g, "/"));
  const sections = Object.entries(cfg.sections || {}).filter(([, v]) => v).map(([k]) => k).join(", ");
  stdout.write(`Sections: ${sections}\n`);
  stdout.write(`Verified: ${cfg.verified ?? false}\n`);
  if (cfg.verificationNote) stdout.write(`Note: ${cfg.verificationNote}\n`);
  stdout.write(`\n${cfg.loaderBehaviour}\n`);
  return 0;
}

async function cmdInstall(name, { to, useGlobal, force, dryRun }) {
  const target = to;
  const cfg = await loadPlatform(name);
  const fs_ = cfg.folderStructure;

  let targetRoot;
  if (target) {
    targetRoot = expandPath(target);
  } else if (useGlobal) {
    if (!fs_.globalRoot) {
      stderr.write(`${name} does not support global install; falling back to project scope.\n`);
      targetRoot = join(cwd(), fs_.projectRoot);
    } else {
      targetRoot = expandPath(fs_.globalRoot);
    }
  } else {
    if (cfg.installType === "instructions-append") targetRoot = cwd();
    else if (fs_.projectRoot) targetRoot = join(cwd(), fs_.projectRoot);
    else targetRoot = cwd();
  }

  const strategy = STRATEGIES[cfg.installType];
  if (!strategy) {
    stderr.write(`Unknown install type: ${cfg.installType}\n`);
    return 1;
  }

  stdout.write(`Installing rankmath-seo-wp -> ${cfg.displayName}${dryRun ? " (DRY RUN)" : ""}\n`);
  stdout.write(`Target root: ${targetRoot}\n`);
  const plan = await strategy(cfg, targetRoot, { force, dryRun });
  stdout.write(`  file: ${plan.file}\n`);
  stdout.write(`  size: ${(plan.size ?? 0).toLocaleString()} bytes\n`);
  if (plan.sections?.length) stdout.write(`  sections: ${plan.sections.join(", ")}\n`);
  if (plan.embedded?.length) stdout.write(`  embedded refs: ${plan.embedded.join(", ")}\n`);
  if (plan.entries?.length) stdout.write(`  zip entries: ${plan.entries.length}\n`);
  stdout.write(`\n${cfg.loaderBehaviour}\n`);
  if (!cfg.verified) stdout.write(`\nNOTE: this platform's loader behaviour is unverified — see info.\n`);
  if (dryRun) stdout.write("\n(dry run; nothing written.)\n");
  return 0;
}

async function interactivePick() {
  const plats = await listPlatforms();
  stdout.write("Select an AI platform:\n\n");
  for (let i = 0; i < plats.length; i++) {
    const cfg = JSON.parse(await readFile(join(PLATFORMS_DIR, plats[i]), "utf8"));
    stdout.write(`  ${i + 1}. ${cfg.displayName} (${cfg.platform})\n`);
  }
  stdout.write("\n");
  const rl = createInterface({ input, output });
  const choice = (await rl.question("Number (or platform key): ")).trim();
  rl.close();
  if (/^\d+$/.test(choice)) {
    const idx = parseInt(choice, 10) - 1;
    if (idx >= 0 && idx < plats.length) return plats[idx].replace(".json", "");
  }
  if (existsSync(join(PLATFORMS_DIR, `${choice}.json`))) return choice;
  throw new Error("No platform selected.");
}

function parseArgs(args) {
  const out = { platform: null, list: false, info: null, to: null, useGlobal: false, force: false, dryRun: false };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--list") out.list = true;
    else if (a === "--info") out.info = args[++i];
    else if (a === "--to") out.to = args[++i];
    else if (a === "--global") out.useGlobal = true;
    else if (a === "-f" || a === "--force") out.force = true;
    else if (a === "--dry-run") out.dryRun = true;
    else if (a === "-h" || a === "--help") {
      stdout.write("Usage: install-skill [PLATFORM] [--list] [--info P] [--to DIR] [--global] [-f] [--dry-run]\n");
      exit(0);
    } else if (!out.platform && !a.startsWith("--")) out.platform = a;
  }
  return out;
}

async function main() {
  const opts = parseArgs(argv.slice(2));
  if (opts.list) return cmdList();
  if (opts.info) return cmdInfo(opts.info);
  const name = opts.platform || (await interactivePick());
  return cmdInstall(name, opts);
}

main()
  .then((code) => exit(code ?? 0))
  .catch((e) => { stderr.write(`Error: ${e.message}\n`); exit(1); });
