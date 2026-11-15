#!/usr/bin/env python3
"""Self-test for rankmath-seo-wp (offline, standard library only).

    python scripts/test_verify.py          # exit 1 on any failure

Covers: the verifier (Python and Node twins agree, gates really fail),
Rank Math scoring ports against data/rankmath-tests.csv, data hygiene
(source + trust on every row), search routing, and check_numbers.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
DATA = ROOT / "data"
SAMPLE = ROOT / "examples" / "sample-article.html"
NODE = shutil.which("node")
sys.path.insert(0, str(ROOT / "scripts"))

import check_numbers  # noqa: E402
import search  # noqa: E402

spec = importlib.util.spec_from_file_location("verify_article", TOOLS / "verify-article.py")
va = importlib.util.module_from_spec(spec)
spec.loader.exec_module(va)

TRUST = {"官方原始碼", "官方文件", "實測", "站內風格", "推論"}


def rows(stem):
    with open(DATA / f"{stem}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_row(test_id):
    return next(r for r in rows("rankmath-tests") if r["test_id"] == test_id)


def run_py(path, fk):
    p = subprocess.run([sys.executable, str(TOOLS / "verify-article.py"), str(path), fk],
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout.replace("\r\n", "\n")


def run_js(path, fk):
    p = subprocess.run([NODE, str(TOOLS / "verify-article.mjs"), str(path), fk],
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout.replace("\r\n", "\n")


def mutate(fn):
    """Write a mutated copy of the sample to a temp file and return its path."""
    text = fn(SAMPLE.read_text(encoding="utf-8"))
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8", newline="\n")
    tmp.write(text)
    tmp.close()
    return Path(tmp.name)


def swap_block_json(text, block, change):
    m = re.search(r"(<!-- wp:rank-math/" + block + r" )(\{.*?\})( -->)", text, re.S)
    data = json.loads(m.group(2))
    change(data)
    return text[:m.start(2)] + json.dumps(data, ensure_ascii=False) + text[m.end(2):]


class Verifier(unittest.TestCase):
    def test_sample_passes_python(self):
        code, out = run_py(SAMPLE, "Claude Skills")
        self.assertEqual(code, 0, out)
        self.assertIn("=== Result: 8 passed, 0 failed ===", out)

    @unittest.skipUnless(NODE, "node not installed")
    def test_sample_passes_node_and_twins_agree(self):
        code_js, out_js = run_js(SAMPLE, "Claude Skills")
        code_py, out_py = run_py(SAMPLE, "Claude Skills")
        self.assertEqual(code_js, 0, out_js)
        self.assertEqual(out_py, out_js)

    def test_word_count_matches_wordpress_package(self):
        # @wordpress/wordcount 5.1.0 count(text.toLowerCase(), "words") on 2026-11-15:
        # sample-article.html 714, references/faq-block.md 663 (before this edit cycle)
        self.assertEqual(va.visible_word_count(SAMPLE.read_text(encoding="utf-8")), 714)

    def test_wordcount_cjk_run_is_one_word(self):
        self.assertEqual(va.wp_word_count("<p>這是一段沒有空白的中文句子</p>"), 1)
        self.assertEqual(va.wp_word_count("<p>Claude Skills 是 Open Standard</p>"), 5)
        self.assertEqual(va.wp_word_count("a -- b <!-- wp:x {\"y\":1} --> c"), 3)

    def test_fk_count_ignores_block_json_and_case(self):
        html = '<!-- wp:rank-math/faq-block {"questions":[{"title":"Claude Skills"}]} --><p>claude skills and CLAUDE SKILLS</p>'
        self.assertEqual(va.visible_fk_count(html, "Claude Skills"), 2)

    def test_density_score_matches_csv_bands(self):
        cases = {0.49: ("low", 0), 0.5: ("fair", 2), 0.74: ("fair", 2), 0.75: ("best", 6),
                 0.76: ("good", 3), 0.99: ("good", 3), 1.0: ("best", 6), 2.5: ("best", 6), 2.51: ("high", 0)}
        for d, want in cases.items():
            self.assertEqual(va.density_score(d), want, d)
        bands = rows("focus-keyword-density")
        for b in bands:
            lo = float(b["density_low"])
            self.assertEqual(f"{va.density_score(lo)[1]}/6", b["rank_math_points"], b)

    def test_constants_match_csv(self):
        self.assertEqual(str(va.WORDS_PASS), test_row("lengthContent")["threshold"])
        self.assertEqual(f"{va.DENSITY_GOOD[1]}-{va.DENSITY_FAIL_HIGH}", test_row("keywordDensity")["threshold"])
        kb = va.DENSITY_KB_RECOMMENDED
        self.assertEqual(f"{kb[0]}-{kb[1]}", test_row("keywordDensity_kb")["threshold"])
        self.assertEqual(str(va.IN10_MIN_WORDS), test_row("keywordIn10Percent")["threshold"])
        tiers = [(int(a), int(b)) for a, b in re.findall(r">=(\d+) -> (\d+)", test_row("lengthContent")["rule"])]
        self.assertEqual(tiers, va.LENGTH_TIERS)
        site = {r["rule_id"]: r for r in rows("site-rules")}
        self.assertEqual(str(va.SITE_H2_COUNT), site["h2_count"]["value"])
        self.assertEqual(va.SITE_HOWTO_SIZESLUG, site["howto_sizeslug"]["value"])

    def test_node_constants_match_python(self):
        js = (TOOLS / "verify-article.mjs").read_text(encoding="utf-8")
        for name in ["WORDS_PASS", "DENSITY_FAIL_LOW", "DENSITY_FAIL_HIGH", "IN10_MIN_WORDS", "SITE_H2_COUNT"]:
            m = re.search(rf"const {name} = ([\d.]+);", js)
            self.assertIsNotNone(m, name)
            self.assertEqual(float(m.group(1)), float(getattr(va, name)), name)
        for name in ["DENSITY_FAIR", "DENSITY_GOOD", "DENSITY_KB_RECOMMENDED"]:
            m = re.search(rf"const {name} = \[([\d.]+), ([\d.]+)\];", js)
            self.assertEqual((float(m.group(1)), float(m.group(2))), tuple(getattr(va, name)), name)
        m = re.search(r"const LENGTH_TIERS = (\[\[.*?\]\]);", js)
        self.assertEqual([tuple(x) for x in json.loads(m.group(1))], va.LENGTH_TIERS)

    # --- the gate must really fail (SOP 6-6) ---------------------------------
    def assert_fails(self, path, fk="Claude Skills", needle=None):
        code, out = run_py(path, fk)
        self.assertEqual(code, 1, out)
        if needle:
            self.assertIn(needle, out)
        if NODE:
            code_js, out_js = run_js(path, fk)
            self.assertEqual(code_js, 1, out_js)
            self.assertEqual(out, out_js)

    def test_fails_when_density_high(self):
        p = mutate(lambda t: t.replace("</p>", " Claude Skills Claude Skills Claude Skills</p>", 6))
        self.assert_fails(p, needle="FAIL high")

    def test_fails_when_too_short(self):
        p = mutate(lambda t: re.sub(r"<p>.*?</p>", "<p>Claude Skills 短</p>", t, flags=re.S))
        self.assert_fails(p, needle="below 600")

    def test_fails_on_howto_h4(self):
        p = mutate(lambda t: t.replace('<h3 class="rank-math-howto-title">', '<h4 class="rank-math-howto-title">', 1))
        self.assert_fails(p, needle="HTML differs from save() output")

    def test_howto_h4_valid_when_titlewrapper_h4(self):
        def change(t):
            t = swap_block_json(t, "howto-block", lambda d: d.update(titleWrapper="h4"))
            return re.sub(r'<h3 class="rank-math-howto-title">(.*?)</h3>', r'<h4 class="rank-math-howto-title">\1</h4>', t)
        code, out = run_py(mutate(change), "Claude Skills")
        self.assertNotIn("HTML differs", out)
        self.assertIn("Site style (post 8594): drop JSON field titleWrapper", out)

    def test_fails_on_faq_json_html_mismatch(self):
        p = mutate(lambda t: swap_block_json(t, "faq-block", lambda d: d["questions"][1].update(title="改過的問題")))
        self.assert_fails(p, needle="Q2 title mismatch")

    def test_faq_hidden_question_is_skipped(self):
        p = mutate(lambda t: swap_block_json(t, "faq-block", lambda d: d["questions"].append(
            {"id": "faq-x", "title": "hidden", "content": "hidden", "visible": False})))
        code, out = run_py(p, "Claude Skills")
        self.assertIn("FAQ block:       OK (8 questions aligned)", out)

    def test_fails_on_inline_ldjson(self):
        p = mutate(lambda t: t + '\n<!-- wp:html --><script type="application/ld+json">{}</script><!-- /wp:html -->\n')
        self.assert_fails(p, needle="application/ld+json")

    def test_fails_when_fk_not_in_first_10_percent(self):
        code, out = run_py(SAMPLE, "GPT Store")
        self.assertEqual(code, 1)
        self.assertIn("FK in opening:   FAIL", out)

    def test_usage_and_file_errors(self):
        p = subprocess.run([sys.executable, str(TOOLS / "verify-article.py")], capture_output=True)
        self.assertEqual(p.returncode, 1)
        p = subprocess.run([sys.executable, str(TOOLS / "verify-article.py"), "no-such.html", "x"], capture_output=True)
        self.assertEqual(p.returncode, 2)


class Data(unittest.TestCase):
    def test_every_row_has_source_and_trust(self):
        for stem in ["rankmath-tests", "blocks", "site-rules", "focus-keyword-density",
                     "h2-templates", "faq-topics", "power-words", "platforms"]:
            for r in rows(stem):
                self.assertTrue(r.get("source", "").strip(), (stem, r))
                self.assertIn(r.get("trust"), TRUST, (stem, r))

    def test_rank_math_rows_cite_version_and_url(self):
        for r in rows("rankmath-tests"):
            if r["trust"] == "官方原始碼":
                self.assertRegex(r["source"], r"\(.*1\.0\.\d+\)|1\.0\.\d+", r)
            self.assertTrue(r["doc_url"].startswith("https://rankmath.com/kb/"), r)

    def test_site_rules_never_claim_official(self):
        for r in rows("site-rules"):
            self.assertIn(r["trust"], {"站內風格", "推論"}, r)

    def test_pending_columns(self):
        with open(DATA / "pending.csv", encoding="utf-8", newline="") as f:
            self.assertEqual(next(csv.reader(f)), ["date", "question", "why_not_found", "asked_by", "status"])

    def test_power_words_flag_matches_plugin_rule(self):
        for r in rows("power-words"):
            if r["language"] != "en":
                self.assertTrue(r["rank_math_power_word"].startswith("n/a"), r)


class Search(unittest.TestCase):
    ROUTES = {
        "密度": ("tests", "keywordDensity"),
        "字數": ("tests", "lengthContent"),
        "總分 綠燈": ("tests", "scoreColor"),
        "標題 數字": ("tests", "titleHasNumber"),
        "影片 圖片": ("tests", "contentHasAssets"),
        "內部連結": ("tests", "linksHasInternal"),
        "區塊壞掉": ("blocks", "validity"),
        "特色圖": ("site", "featured_image"),
        "ld+json": ("site", "no_inline_ldjson"),
    }

    def test_zh_routes(self):
        for q, (domain, key) in self.ROUTES.items():
            top = search.search(q, max_results=1)[0]
            self.assertEqual(top["_domain"], domain, q)
            self.assertIn(key, (top.get("test_id"), top.get("item"), top.get("rule_id")), q)

    def test_no_match_exits_1(self):
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "search.py"), "zzqqxxyy"], capture_output=True)
        self.assertEqual(p.returncode, 1)

    def test_skill_routing_commands_return_hits(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cmds = re.findall(r'`search\.py "([^"]+)"(?: --domain (\w+))?`', text)
        self.assertGreater(len(cmds), 10)
        for q, domain in cmds:
            self.assertTrue(search.search(q, domain or None), (q, domain))


class Evals(unittest.TestCase):
    def test_cases_are_well_formed(self):
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))["cases"]
        active = [c for c in cases if not c.get("retired")]
        self.assertGreaterEqual(len(active), 10)  # SOP 6-4
        for c in cases:
            for group in c["must"]:
                for p in group:
                    self.assertFalse(any(ord(ch) < 32 for ch in p), (c["id"], repr(p)))  # heredoc \b -> 0x08
                    re.compile(p)
            self.assertIn(c["trust"], TRUST, c["id"])


class Numbers(unittest.TestCase):
    def test_skill_md_numbers(self):
        problems, _ = check_numbers.check()
        self.assertEqual(problems, [])

    def test_wrong_number_is_caught(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8").replace("word count ≥ 600", "word count ≥ 1400")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "SKILL.md"
            p.write_text(text, encoding="utf-8")
            problems, _ = check_numbers.check(p)
        self.assertTrue(any("1400" in x for x in problems), problems)


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    result = unittest.main(exit=False, verbosity=1).result
    n = result.testsRun
    bad = len(result.failures) + len(result.errors)
    print(f"\n{n - bad - len(result.skipped)}/{n} passed, {len(result.skipped)} skipped")
    sys.exit(1 if bad else 0)
