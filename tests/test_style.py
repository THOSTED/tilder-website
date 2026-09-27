import io
import re
import unittest
from contextlib import redirect_stderr, redirect_stdout

from tests.helpers import REPO, THEME, load_tool

CSS = THEME / "style.css"


class Style(unittest.TestCase):
    def test_every_class_of_the_pinned_contract_is_styled(self):
        check = load_tool("check-theme")
        classes = check.contract_classes((REPO / "tools" / "tilder-theme.md").read_text())
        self.assertEqual(check.missing(CSS.read_text(), classes), [])

    def test_every_token_pair_reaches_aa_in_both_schemes(self):
        check = load_tool("check-contrast")
        low = [r for r in check.results(check.tokens(CSS.read_text())) if r[3] < r[4]]
        self.assertEqual(low, [])

    def test_the_theme_s_own_classes_are_styled(self):
        css = CSS.read_text()
        for name in ("page", "manline", "manline--head", "manline--foot", "bar", "tagline",
                     "skip", "to-top", "pager", "home", "home-tagline", "doc", "doc--toc",
                     "doc-side", "doc-main", "doc-toc", "doc-toc-label", "doc-search",
                     "doc-search-label", "doc-search-input", "doc-search-status",
                     "doc-search-results", "code-box", "code-copy", "entry--group", "entry--example"):
            self.assertRegex(css, r"\." + re.escape(name) + r"(?![\w-])", name)

    def test_focus_motion_and_dark_scheme(self):
        css = CSS.read_text()
        self.assertIn(":focus-visible", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("@media (prefers-color-scheme: dark)", css)

    def test_the_home_hero_title_is_visually_hidden_not_duplicated(self):
        # Controller ruling C3: `.home > .s:first-of-type > h2` must not
        # repeat .sr-only's visually-hidden declarations in a rule of its
        # own; it is folded into .sr-only's selector list instead. Check
        # the behaviour (visually hidden) rather than a literal duplicate.
        css = CSS.read_text()
        selector = re.search(
            r"([^{}]*\.sr-only[^{}]*)\{([^{}]*)\}", css)
        self.assertIsNotNone(selector, "no .sr-only rule found")
        selectors, declarations = selector.groups()
        self.assertIn(".home > .s:first-of-type > h2", selectors)
        for prop in ("position: absolute", "width: 1px", "height: 1px",
                     "overflow: hidden", "white-space: nowrap"):
            self.assertIn(prop, declarations)
        # And it must not appear a second time as its own duplicate rule.
        without_comments = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        self.assertEqual(
            len(re.findall(r"\.home\s*>\s*\.s:first-of-type\s*>\s*h2", without_comments)), 1)
