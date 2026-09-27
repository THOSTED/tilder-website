"""The theme's scripts: ES5, no storage, no network but the index, no
words of their own; search.js's matching and its DOM under node, when
node is installed (no package, no framework)."""

import json
import re
import shutil
import subprocess
import unittest

from tests.helpers import REPO, THEME, fixture_build

SCRIPTS = sorted(p.name for p in THEME.glob("*.js"))
TOKEN = re.compile(r'(/\*.*?\*/|//[^\n]*)|("(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\')', re.S)
NOT_ES5 = [("an arrow function", r"=>"), ("let", r"\blet\b"), ("const", r"\bconst\b"),
           ("a template literal", r"`"), ("a class", r"\bclass\s+\w"), ("a spread", r"\.\.\."),
           ("async", r"\basync\b"), ("await", r"\bawait\b"), ("for...of", r"\bfor\s*\([^)]*\bof\b")]
FORBIDDEN = [("storage", r"\b(localStorage|sessionStorage|indexedDB)\b"),
             ("a cookie", r"\bdocument\.cookie\b"), ("eval", r"\beval\s*\("),
             ("fetch", r"\bfetch\s*\("), ("a style attribute", r"\.style\b")]


def split(source):
    """(the code with comments and strings blanked, [the strings])."""
    strings = []

    def blank(m):
        if m.group(2):
            strings.append(m.group(2)[1:-1])
            return '""'
        return " "
    return TOKEN.sub(blank, source), strings


class Rules(unittest.TestCase):
    def test_there_are_scripts_to_check(self):
        self.assertIn("search.js", SCRIPTS)

    def test_pure_ascii(self):
        for name in SCRIPTS:
            data = (THEME / name).read_bytes()
            try:
                data.decode("ascii")
            except UnicodeDecodeError as e:
                self.fail(f"{name}: non-ASCII byte at position {e.start}")

    def test_es5_only(self):
        for name in SCRIPTS:
            code, _ = split((THEME / name).read_text())
            for what, pattern in NOT_ES5:
                self.assertNotRegex(code, pattern, f"{name}: {what}")

    def test_no_storage_cookie_eval_or_inline_style(self):
        for name in SCRIPTS:
            code, _ = split((THEME / name).read_text())
            for what, pattern in FORBIDDEN:
                self.assertNotRegex(code, pattern, f"{name}: {what}")

    def test_no_url_and_no_words_of_their_own(self):
        for name in SCRIPTS:
            _, strings = split((THEME / name).read_text())
            for s in strings:
                self.assertNotRegex(s, r"https?:|//", f"{name}: {s!r}")
                if s != "use strict":
                    self.assertNotRegex(s, r"^[A-Za-z]+( [A-Za-z]+)+[.!?]?$", f"{name}: {s!r}")


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class SearchUnderNode(unittest.TestCase):
    INDEX = [{"t": "Élan", "u": "docs/elan", "d": "", "h": [], "x": ""},
             {"t": "Setup", "u": "docs/setup", "d": "", "h": ["Install"], "x": "elan"},
             {"t": "Options", "u": "docs/options", "d": "the elan of things", "h": [], "x": ""},
             {"t": "Other", "u": "docs/other", "d": "", "h": [], "x": "nothing"}]

    def search(self, query):
        script = ("var s = require(process.argv[1]);"
                  "var p = s.prepare(JSON.parse(process.argv[2]));"
                  "console.log(JSON.stringify(s.search(p, process.argv[3]).map(function (r) { return r.u; })));")
        done = subprocess.run(["node", "-e", script, str(THEME / "search.js"),
                               json.dumps(self.INDEX), query],
                              capture_output=True, text=True, check=True)
        return json.loads(done.stdout)

    def test_case_and_accents_are_ignored_and_the_title_ranks_first(self):
        self.assertEqual(self.search("ELAN"), ["docs/elan", "docs/options", "docs/setup"])

    def test_every_word_must_match(self):
        self.assertEqual(self.search("setup install"), ["docs/setup"])
        self.assertEqual(self.search("setup nothing"), [])

    def test_a_blank_query_finds_nothing(self):
        self.assertEqual(self.search("   "), [])

    def dom(self, words, index="[]", query=None):
        args = ["node", str(REPO / "tests" / "js" / "search-dom.js"), str(THEME / "search.js"),
                json.dumps(words), index]
        if query is not None:
            args.append(query)
        return json.loads(subprocess.run(args, capture_output=True, text=True, check=True).stdout)

    WORDS = {"data-search-index": "docs/search-index.json", "data-home": "../",
             "data-label": "Search", "data-placeholder": "words",
             "data-none": "Nothing.", "data-count": "{n} found"}

    def test_linked_twice_the_field_is_made_once_from_the_data_words(self):
        out = self.dom(self.WORDS)
        self.assertEqual(out["ready"], "true")
        self.assertEqual([(c["tag"], c["cls"]) for c in out["children"]], [
            ("LABEL", "doc-search-label"), ("INPUT", "doc-search-input"),
            ("P", "doc-search-status"), ("UL", "doc-search-results")])
        self.assertEqual(out["children"][0]["text"], "Search")
        self.assertEqual(out["children"][1]["placeholder"], "words")

    def test_results_link_from_the_language_s_landing_page(self):
        out = self.dom(self.WORDS, json.dumps(self.INDEX), "elan")
        self.assertEqual(out["requested"], ["../docs/search-index.json"])
        self.assertEqual(out["results"], ["../docs/elan", "../docs/options", "../docs/setup"])
        self.assertEqual(out["status"], "3 found")
        self.assertEqual(self.dom(self.WORDS, json.dumps(self.INDEX), "zzz")["status"], "Nothing.")

    def test_no_index_no_field(self):
        out = self.dom({"data-search-index": ""})
        self.assertEqual(out["children"], [])
        self.assertIsNone(out["ready"])

    def give_up(self, nav, mode):
        args = ["node", str(REPO / "tests" / "js" / "search-give-up-dom.js"),
                str(THEME / "search.js"), nav, mode]
        return json.loads(subprocess.run(args, capture_output=True, text=True, check=True).stdout)

    def test_a_slow_request_times_out_and_gives_up(self):
        out = self.give_up("nav", "timeout")
        self.assertEqual(out["timeout"], 10000)
        self.assertTrue(out["has_ontimeout"])
        self.assertTrue(out["has_onabort"])
        self.assertTrue(out["hidden"])

    def test_giving_up_with_the_focus_moves_it_to_the_collection_nav(self):
        self.assertEqual(self.give_up("nav", "timeout")["focused"], "link")
        self.assertEqual(self.give_up("nav", "abort")["focused"], "link")

    def test_giving_up_without_a_collection_nav_focuses_the_doc_side(self):
        out = self.give_up("nonav", "abort")
        self.assertEqual(out["focused"], "side")
        self.assertEqual(out["side_tabindex"], "-1")


class Loaded(unittest.TestCase):
    """Where each script is linked, on the built fixture."""

    def setUp(self):
        self.build = fixture_build(self)

    def test_code_js_on_pages_with_code_with_its_words(self):
        self.assertIn('<script src="code.js" defer data-copy="copy" data-copied="copied"></script>',
                      self.build.read("kitchen-sink.html"))
        self.assertNotIn("code.js", self.build.read("404.html"))

    def test_the_three_scripts_are_served(self):
        for name in ("code.js", "nav.js", "search.js"):
            self.assertTrue((self.build.out / name).is_file(), name)

    def test_search_js_twice_on_a_doc_layout_page_that_lists_docs(self):
        # doc.html links it, and the doc type's SCRIPT adds it where {docs}
        # lists pages: search.js guards against the second run.
        self.assertEqual(self.build.read("docs/index.html").count("search.js"), 2)

