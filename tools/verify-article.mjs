#!/usr/bin/env node
/**
 * Verify a Rank Math WP article meets all SEO and structure requirements.
 *
 * Mirror of tools/verify-article.py for users who prefer Node. Every threshold
 * is a row in data/rankmath-tests.csv; Rank Math rules come from the plugin
 * source (seo-by-rank-math 1.0.282, assets/admin/js/analyzer.js).
 *
 * Usage:
 *   node tools/verify-article.mjs article.html "Focus Keyword"
 *   npx rankmath-verify article.html "Focus Keyword"
 *
 * Exit codes: 0 = all pass, 1 = at least one fail, 2 = invocation error.
 */
import { readFile } from "node:fs/promises";
import { argv, exit, stderr, stdout } from "node:process";
import { resolve } from "node:path";

// --- thresholds (single source: data/rankmath-tests.csv) ---------------------
const WORDS_PASS = 600; // lengthContent
const LENGTH_TIERS = [[2500, 8], [2000, 5], [1500, 4], [1000, 3], [600, 2]]; // lengthContent
const DENSITY_FAIL_LOW = 0.5; // keywordDensity
const DENSITY_FAIR = [0.5, 0.75]; // keywordDensity
const DENSITY_GOOD = [0.76, 1.0]; // keywordDensity
const DENSITY_FAIL_HIGH = 2.5; // keywordDensity
const DENSITY_KB_RECOMMENDED = [1.0, 1.5]; // KB #keyword-density
const IN10_MIN_WORDS = 400; // keywordIn10Percent
const SITE_H2_COUNT = 12; // site style
const SITE_HOWTO_SIZESLUG = "large"; // site style (post 8594)
const SITE_HOWTO_DROP_FIELDS = ["hasDuration", "days", "hours", "minutes", "hasTotalTime",
  "timeDays", "timeHours", "timeMinutes", "titleWrapper"]; // site style (post 8594)

// --- ports of the text helpers Rank Math and WordPress use -----------------------
const TAG = /<\/?[a-z][^>]*?>/gi;
const COMMENT = /<!--[\s\S]*?-->/g;
const SC_NAME = "[^<>&/\\[\\]\\x00- =]+?";
const SHORTCODE_OPEN = new RegExp("\\[" + SC_NAME + "( [^\\]]+?)?\\]", "g");
const SHORTCODE_CLOSE = new RegExp("\\[/" + SC_NAME + "\\]", "g");
const ENTITY = /&\S+?;/g;
const RM_SYMBOLS = /[\x80-\xbf\xd7\xf7\u2000-\u2bff\u2e00-\u2e7f]/g;
const WP_REMOVE = /[!-/:-@[-`{-~\x80-\xbf\xd7\xf7\u2000-\u2bff\u2e00-\u2e7f]/g;
const EDGE = "[\\u2013\\-\\(\\)_\\[\\]\u2019\u201c\u201d\"'.?!:;,\xbf\xa1\xab\xbb\u2039\u203a\u2014\xd7+&<>]+";
const EDGE_START = new RegExp("^" + EDGE);
const EDGE_END = new RegExp(EDGE + "$");

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function decodeEntities(s) {
  // Match Python's html.unescape coverage for the common cases plus all
  // numeric character references.
  const named = {
    "&lt;": "<", "&gt;": ">", "&quot;": '"',
    "&apos;": "'", "&#39;": "'", "&nbsp;": "\u00a0", "&copy;": "©",
    "&reg;": "®", "&trade;": "™", "&hellip;": "…",
    "&mdash;": "—", "&ndash;": "–", "&lsquo;": "‘",
    "&rsquo;": "’", "&ldquo;": "“", "&rdquo;": "”",
  };
  let out = s;
  for (const [k, v] of Object.entries(named)) out = out.split(k).join(v);
  out = out.replace(/&#(\d+);/g, (_m, n) => String.fromCodePoint(parseInt(n, 10)));
  out = out.replace(/&#x([0-9a-fA-F]+);/g, (_m, n) => String.fromCodePoint(parseInt(n, 16)));
  return out.split("&amp;").join("&");
}

function normalizeWhitespace(text) {
  return text.replace(/&nbsp;|&#160;/gi, " ").replace(/\s{2,}/g, " ").replace(/\s\./g, ".").trim();
}

function normalizeQuotes(text) {
  return text.replace(/[\u2018\u2019\u201b`]/g, "'").replace(/[\u201c\u201d\u301d\u301e\u301f\u201f\u201e]/g, '"');
}

function rmWords(text) {
  let t = text.replace(TAG, "").replace(COMMENT, "");
  t = t.replace(SHORTCODE_OPEN, "").replace(SHORTCODE_CLOSE, "");
  t = normalizeWhitespace(t).replace(ENTITY, "").replace(/--|\u2014/g, " ").replace(RM_SYMBOLS, "");
  if (t === "") return [];
  return t.split(/\s/g).map((w) => w.replace(EDGE_START, "").replace(EDGE_END, "")).filter((w) => w.trim() !== "");
}

function wpWordCount(text) {
  let t = text.replace(TAG, "\n").replace(COMMENT, "").replace(/&nbsp;|&#160;/gi, " ");
  t = t.replace(ENTITY, "").replace(/--|\u2014/g, " ").replace(WP_REMOVE, "");
  return ((t + "\n").match(/\S\s+/g) || []).length;
}

function visibleWordCount(content) {
  return wpWordCount(content.toLowerCase());
}

function visibleFkCount(content, fk) {
  const text = rmWords(normalizeWhitespace(content.replace(TAG, ""))).join(" ");
  const kw = rmWords(normalizeQuotes(fk)).join(" ");
  if (!kw) return 0;
  return (text.match(new RegExp(escapeRegExp(kw), "gi")) || []).length;
}

function densityScore(d) {
  if (d < DENSITY_FAIL_LOW) return ["low", 0];
  if (d > DENSITY_FAIL_HIGH) return ["high", 0];
  if (d >= DENSITY_FAIR[0] && d < DENSITY_FAIR[1]) return ["fair", 2];
  if (d >= DENSITY_GOOD[0] && d < DENSITY_GOOD[1]) return ["good", 3];
  return ["best", 6];
}

function lengthScore(words) {
  for (const [boundary, score] of LENGTH_TIERS) if (words >= boundary) return score;
  return 0;
}

function block(content, name) {
  const re = new RegExp(`<!-- wp:rank-math/${name} (\\{[\\s\\S]*?\\}) -->\\s*([\\s\\S]*?)\\s*<!-- /wp:rank-math/${name} -->`);
  const m = content.match(re);
  return m ? [m[1], m[2]] : null;
}

function sameHtml(a, b) {
  const norm = (s) => decodeEntities(s).trim().replace(/>\s+</g, "><").replace(/\s+/g, " ");
  return norm(a) === norm(b);
}

function wrapperClass(data, name) {
  return `wp-block-rank-math-${name}` + (data.className ? ` ${data.className}` : "");
}

function howtoSaveHtml(data) {
  const steps = data.steps || [];
  if (!steps.length) return "";
  const tw = data.titleWrapper ?? "h3";
  let out = `<div class="${wrapperClass(data, "howto-block")}">`;
  for (const s of steps) {
    if (s.visible === false) continue;
    out += '<div class="rank-math-howto-step">';
    if (s.title) out += `<${tw} class="rank-math-howto-title">${s.title}</${tw}>`;
    if (s.content) out += `<div class="rank-math-howto-content">${s.content}</div>`;
    out += "</div>";
  }
  return out + "</div>";
}

function faqSaveHtml(data) {
  const qs = data.questions || [];
  if (!qs.length) return "";
  const tw = data.titleWrapper ?? "h3";
  let out = `<div class="${wrapperClass(data, "faq-block")}">`;
  for (const q of qs) {
    if (!q.title || !q.content || q.visible === false) continue;
    out += `<div class="rank-math-faq-item"><${tw} class="rank-math-question">${q.title}</${tw}><div class="rank-math-answer">${q.content}</div></div>`;
  }
  return out + "</div>";
}

function checkHowto(content) {
  const found = block(content, "howto-block");
  if (!found) return ["No HowTo block found"];
  const [jsonStr, htmlPart] = found;
  let data;
  try {
    data = JSON.parse(jsonStr);
  } catch (e) {
    return [`JSON parse error: ${e.message}`];
  }
  const issues = [];
  if (!("steps" in data)) issues.push("Missing JSON.steps");
  else if (!sameHtml(htmlPart, howtoSaveHtml(data))) {
    issues.push('HTML differs from save() output (editor will show "invalid content")');
    const decoded = decodeEntities(htmlPart);
    data.steps.filter((s) => s.visible !== false).forEach((s, i) => {
      if (s.title && !decoded.includes(s.title) && !htmlPart.includes(s.title)) issues.push(`Step ${i + 1} title not found in HTML`);
      if (s.content && !decoded.includes(s.content) && !htmlPart.includes(s.content)) issues.push(`Step ${i + 1} content not found in HTML`);
    });
  }
  for (const f of SITE_HOWTO_DROP_FIELDS) if (f in data) issues.push(`Site style (post 8594): drop JSON field ${f}`);
  if (data.sizeSlug !== SITE_HOWTO_SIZESLUG) issues.push(`Site style (post 8594): JSON.sizeSlug should be "${SITE_HOWTO_SIZESLUG}"`);
  return issues.length ? issues : ["OK"];
}

function checkFaq(content) {
  const found = block(content, "faq-block");
  if (!found) return ["No FAQ block found"];
  let data;
  try {
    data = JSON.parse(found[0]);
  } catch (e) {
    return [`FAQ JSON parse error: ${e.message}`];
  }
  const htmlPart = found[1];
  const shown = (data.questions || []).filter((q) => q.title && q.content && q.visible !== false);
  if (sameHtml(htmlPart, faqSaveHtml(data))) return [`OK (${shown.length} questions aligned)`];
  const tw = data.titleWrapper ?? "h3";
  const itemRe = new RegExp(`<div class="rank-math-faq-item"><${tw} class="rank-math-question">([\\s\\S]*?)</${tw}><div class="rank-math-answer">([\\s\\S]*?)</div></div>`, "g");
  const items = [...htmlPart.matchAll(itemRe)].map((m) => [m[1], m[2]]);
  if (items.length !== shown.length) return [`Count mismatch: JSON ${shown.length}, HTML ${items.length}`];
  const issues = [];
  shown.forEach((q, i) => {
    if (!sameHtml(items[i][0], q.title)) issues.push(`Q${i + 1} title mismatch`);
    if (!sameHtml(items[i][1], q.content)) issues.push(`Q${i + 1} content mismatch`);
  });
  return issues.length ? issues : ["HTML differs from save() output (wrapper or markup)"];
}

function checkForbidden(content) {
  const issues = [];
  if (content.includes("HowTo Schema")) {
    if (/<h2[^>]*>[^<]*HowTo Schema[^<]*<\/h2>/.test(content)) issues.push('"HowTo Schema" in H2 heading (forbidden)');
    else issues.push('"HowTo Schema" text in body (review)');
  }
  if (content.includes("application/ld+json")) issues.push('Inline <script type="application/ld+json"> (some themes strip)');
  if (content.includes("FAQ Schema") && /<h2[^>]*>[^<]*FAQ Schema[^<]*<\/h2>/.test(content)) {
    issues.push('"FAQ Schema" in H2 heading (forbidden)');
  }
  return issues;
}

function checkFkInOpening(content, fk) {
  let words = rmWords(content.toLowerCase());
  if (words.length > IN10_MIN_WORDS) words = words.slice(0, Math.floor(0.1 * words.length));
  const kw = rmWords(normalizeQuotes(fk.toLowerCase())).join(" ");
  return Boolean(kw) && words.join(" ").includes(kw);
}

async function main() {
  if (argv.length !== 4) {
    stderr.write('Usage: verify-article.mjs article.html "Focus Keyword"\n');
    return 2;
  }
  const path = argv[2];
  const fk = argv[3];
  let content;
  try {
    content = await readFile(resolve(path), "utf8");
  } catch (e) {
    stderr.write(`File error: ${e.message}\n`);
    return 2;
  }

  stdout.write(`=== ${path} ===\nFocus keyword: ${fk}\n\n`);

  const fkN = visibleFkCount(content, fk);
  const wN = visibleWordCount(content);
  const density = wN ? Number(((fkN * 100) / wN).toFixed(2)) : 0;

  let pass = 0;
  let fail = 0;
  const ok = (t) => { stdout.write(`                 OK ${t}\n`); pass++; };
  const bad = (t) => { stdout.write(`                 FAIL ${t}\n`); fail++; };

  stdout.write(`Word count:      ${wN} visible words\n`);
  if (wN >= WORDS_PASS) ok(`at least ${WORDS_PASS} (content length ${lengthScore(wN)}/8)`);
  else bad(`below ${WORDS_PASS} (content length 0/8)`);

  const [verdict, points] = densityScore(density);
  const [kbLo, kbHi] = DENSITY_KB_RECOMMENDED;
  const fmt = (n) => (Number.isInteger(n) ? n.toFixed(1) : String(n));
  stdout.write(`FK count:        ${fkN} visible occurrences\n`);
  stdout.write(`FK density:      ${density.toFixed(2)}%\n`);
  if (verdict === "best") {
    const note = density >= kbLo && density <= kbHi ? "" : `; KB recommends ${fmt(kbLo)}-${fmt(kbHi)}%`;
    ok(`full score band ${fmt(DENSITY_GOOD[1])}-${fmt(DENSITY_FAIL_HIGH)}% (6/6${note})`);
  } else {
    bad(`${verdict} (${points}/6; full score ${fmt(DENSITY_GOOD[1])}-${fmt(DENSITY_FAIL_HIGH)}%)`);
  }

  const hOpen = (content.match(/<!-- wp:heading/g) || []).length;
  const hClose = (content.match(/<!-- \/wp:heading/g) || []).length;
  stdout.write(`Heading balance: ${hOpen} open / ${hClose} close\n`);
  if (hOpen === hClose && hOpen === SITE_H2_COUNT) ok(`${SITE_H2_COUNT}/${SITE_H2_COUNT} (site-style structure)`);
  else if (hOpen === hClose) ok(`balanced ${hOpen}/${hClose} (non-standard count)`);
  else bad("unbalanced - fix before publish");

  const fkInOpen = checkFkInOpening(content, fk);
  stdout.write(`FK in opening:   ${fkInOpen ? "OK" : "FAIL"}\n`);
  fkInOpen ? pass++ : fail++;

  const h2Re = new RegExp(`<h2[^>]*>[^<]*${escapeRegExp(fk)}[^<]*<\\/h2>`, "g");
  const h2N = (content.match(h2Re) || []).length;
  stdout.write(`FK in H2:        ${h2N} occurrences\n`);
  h2N >= 1 ? ok("at least 1 H2 contains FK") : bad("no H2 contains FK (Rank Math wants >=1)");

  const howtoIssues = checkHowto(content);
  const howtoHead = howtoIssues[0] === "OK" || (howtoIssues.length === 1 && howtoIssues[0].startsWith("No ")) ? howtoIssues[0] : "has issues";
  stdout.write(`HowTo block:     ${howtoHead}\n`);
  if (howtoIssues[0] !== "OK") {
    for (const i of howtoIssues) stdout.write(`                 - ${i}\n`);
    fail++;
  } else pass++;

  const faqIssues = checkFaq(content);
  const faqHead = faqIssues[0].startsWith("OK") || faqIssues[0].startsWith("No ") ? faqIssues[0] : "has issues";
  stdout.write(`FAQ block:       ${faqHead}\n`);
  if (!faqIssues[0].startsWith("OK")) {
    for (const i of faqIssues) if (!i.startsWith("No ")) stdout.write(`                 - ${i}\n`);
    fail++;
  } else pass++;

  const forb = checkForbidden(content);
  if (forb.length) {
    stdout.write("Forbidden:       FAIL\n");
    for (const i of forb) stdout.write(`                 - ${i}\n`);
    fail++;
  } else {
    stdout.write("Forbidden:       OK none found\n");
    pass++;
  }

  stdout.write(`\n=== Result: ${pass} passed, ${fail} failed ===\n`);
  return fail === 0 ? 0 : 1;
}

main().then((code) => exit(code ?? 0));
