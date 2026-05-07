#!/usr/bin/env node
/**
 * Verify a Rank Math WP article meets all SEO and structure requirements.
 *
 * Mirror of tools/verify-article.py for users who prefer Node.
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

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function decodeEntities(s) {
  // Match Python's html.unescape coverage. Handles named entities for the
  // common cases plus all numeric character references.
  const named = {
    "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"',
    "&apos;": "'", "&#39;": "'", "&nbsp;": " ", "&copy;": "©",
    "&reg;": "®", "&trade;": "™", "&hellip;": "…",
    "&mdash;": "—", "&ndash;": "–", "&lsquo;": "‘",
    "&rsquo;": "’", "&ldquo;": "“", "&rdquo;": "”",
  };
  let out = s;
  for (const [k, v] of Object.entries(named)) {
    out = out.split(k).join(v);
  }
  // Numeric refs: &#NNNN; (decimal) and &#xHHHH; (hex)
  out = out.replace(/&#(\d+);/g, (_m, n) => String.fromCodePoint(parseInt(n, 10)));
  out = out.replace(/&#x([0-9a-fA-F]+);/g, (_m, n) => String.fromCodePoint(parseInt(n, 16)));
  return out;
}

function stripMetadata(content) {
  return content
    .replace(/<!-- wp:rank-math\/(?:faq|howto)-block \{[\s\S]+?\} -->/g, "")
    .replace(/<!--[\s\S]*?-->/g, "");
}

function visibleWordCount(content) {
  const visible = stripMetadata(content);
  const text = visible.replace(/<[^>]+>/g, " ");
  const m = text.match(/\S+/g);
  return m ? m.length : 0;
}

function visibleFkCount(content, fk) {
  const visible = stripMetadata(content);
  return visible.split(fk).length - 1;
}

function checkHowto(content) {
  const m = content.match(/<!-- wp:rank-math\/howto-block (\{[\s\S]*?\}) -->[\s\S]*?<!-- \/wp:rank-math\/howto-block -->/);
  if (!m) return ["No HowTo block found"];
  const issues = [];
  let data;
  try {
    data = JSON.parse(m[1]);
  } catch (e) {
    return [`HowTo JSON parse error: ${e.message}`];
  }
  for (const f of ["hasDuration", "days", "hours", "minutes", "hasTotalTime", "timeDays", "timeHours", "timeMinutes", "titleWrapper"]) {
    if (f in data) issues.push(`Forbidden JSON field: ${f}`);
  }
  if (!("steps" in data)) issues.push("Missing JSON.steps");
  if (data.sizeSlug !== "large") issues.push('JSON.sizeSlug should be "large"');
  if (m[0].includes("rank-math-howto-step-title")) issues.push("Old class: rank-math-howto-step-title");
  if (m[0].includes("rank-math-howto-step-content")) issues.push("Old class: rank-math-howto-step-content");
  if (m[0].includes('<div class="rank-math-howto-steps">')) issues.push("Wrapper div rank-math-howto-steps found");
  if (/rank-math-howto-step"><h4/.test(m[0])) issues.push("h4 inside step (should be h3)");
  if (/wp-block-rank-math-howto-block"><h3 class="rank-math-howto-title">/.test(m[0])) {
    issues.push("Outer h3 title (should not exist, only step-level h3)");
  }
  return issues.length ? issues : ["OK"];
}

function checkFaq(content) {
  const m = content.match(/<!-- wp:rank-math\/faq-block (\{[\s\S]*?\}) -->\s*(<div class="wp-block-rank-math-faq-block">[\s\S]*?<\/div>)\s*<!-- \/wp:rank-math\/faq-block -->/);
  if (!m) return ["No FAQ block found"];
  let data;
  try {
    data = JSON.parse(m[1]);
  } catch (e) {
    return [`FAQ JSON parse error: ${e.message}`];
  }
  const itemRe = /<div class="rank-math-faq-item"><h3 class="rank-math-question">([^<]+)<\/h3><div class="rank-math-answer">([\s\S]*?)<\/div><\/div>/g;
  const items = [];
  let it;
  while ((it = itemRe.exec(m[2])) !== null) items.push([it[1], it[2]]);
  if (items.length !== data.questions.length) {
    return [`Count mismatch: JSON ${data.questions.length}, HTML ${items.length}`];
  }
  const issues = [];
  data.questions.forEach((q, i) => {
    const [hT, hC] = items[i];
    if (decodeEntities(hT) !== q.title) issues.push(`Q${i + 1} title mismatch`);
    if (decodeEntities(hC) !== q.content) issues.push(`Q${i + 1} content mismatch`);
  });
  return issues.length ? issues : [`OK (${items.length} questions aligned)`];
}

function checkForbidden(content) {
  const issues = [];
  if (content.includes("HowTo Schema")) {
    if (/<h2[^>]*>[^<]*HowTo Schema[^<]*<\/h2>/.test(content)) {
      issues.push('"HowTo Schema" in H2 heading (forbidden)');
    } else {
      issues.push('"HowTo Schema" text in body (review)');
    }
  }
  if (content.includes("application/ld+json")) issues.push('Inline <script type="application/ld+json">');
  if (content.includes("FAQ Schema") && /<h2[^>]*>[^<]*FAQ Schema[^<]*<\/h2>/.test(content)) {
    issues.push('"FAQ Schema" in H2 heading (forbidden)');
  }
  return issues;
}

function checkFkInOpening(content, fk) {
  const visible = stripMetadata(content);
  const m = visible.match(/<p>([\s\S]+?)<\/p>/);
  return m ? m[1].includes(fk) : false;
}

async function main() {
  if (argv.length !== 4) {
    stderr.write('Usage: verify-article.mjs article.html "Focus Keyword"\n');
    return 1;
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
  const density = wN ? (fkN * 100) / wN : 0;

  let pass = 0;
  let fail = 0;
  const ok = (t) => { stdout.write(`                 OK ${t}\n`); pass++; };
  const bad = (t) => { stdout.write(`                 FAIL ${t}\n`); fail++; };

  stdout.write(`Word count:      ${wN} visible words\n`);
  if (wN >= 1400) ok("above 1400 minimum"); else bad("below 1400 minimum");

  stdout.write(`FK count:        ${fkN} visible occurrences\n`);
  stdout.write(`FK density:      ${density.toFixed(2)}%\n`);
  if (density >= 1.0 && density <= 1.7) ok("in target range 1.0-1.5%");
  else if (density >= 0.7 && density < 1.0) bad("slightly low (target 1.0-1.5%)");
  else if (density > 1.7 && density <= 2.5) bad("slightly high (target 1.0-1.5%)");
  else bad("outside acceptable range");

  const hOpen = (content.match(/<!-- wp:heading/g) || []).length;
  const hClose = (content.match(/<!-- \/wp:heading/g) || []).length;
  stdout.write(`Heading balance: ${hOpen} open / ${hClose} close\n`);
  if (hOpen === hClose && hOpen === 12) ok("12/12 (target structure)");
  else if (hOpen === hClose) ok(`balanced ${hOpen}/${hClose} (non-standard count)`);
  else bad("unbalanced — fix before publish");

  const fkInOpen = checkFkInOpening(content, fk);
  stdout.write(`FK in opening:   ${fkInOpen ? "OK" : "FAIL"}\n`);
  fkInOpen ? pass++ : fail++;

  const h2Re = new RegExp(`<h2[^>]*>[^<]*${escapeRegExp(fk)}[^<]*<\\/h2>`, "g");
  const h2N = (content.match(h2Re) || []).length;
  stdout.write(`FK in H2:        ${h2N} occurrences\n`);
  h2N >= 1 ? ok("at least 1 H2 contains FK") : bad("no H2 contains FK");

  const howtoIssues = checkHowto(content);
  stdout.write(`HowTo block:     ${howtoIssues[0]}\n`);
  for (const i of howtoIssues.slice(1)) stdout.write(`                 - ${i}\n`);
  howtoIssues[0] === "OK" ? pass++ : fail++;

  const faqIssues = checkFaq(content);
  stdout.write(`FAQ block:       ${faqIssues[0]}\n`);
  for (const i of faqIssues.slice(1)) stdout.write(`                 - ${i}\n`);
  faqIssues[0].startsWith("OK") ? pass++ : fail++;

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
