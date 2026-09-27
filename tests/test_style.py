import re
import unittest

from tests.helpers import THEME

CSS = THEME / "style.css"


class Style(unittest.TestCase):
    # Every class of the contract styled, every token pair at AA in both
    # schemes: tilder's --check (tests/test_build.py, make check).

    def test_the_theme_s_own_classes_are_styled(self):
        css = CSS.read_text()
        for name in ("page", "manline", "manline--head", "manline--foot", "bar", "bar-nav", "tagline",
                     "skip", "to-top", "pager", "home", "home-tagline", "doc", "doc--toc",
                     "doc-side", "doc-main", "doc-toc", "doc-toc-label", "doc-search",
                     "doc-search-label", "doc-search-input", "doc-search-status",
                     "doc-search-results", "code-box", "code-copy", "entry--group", "entry--example"):
            self.assertRegex(css, r"\." + re.escape(name) + r"(?![\w-])", name)

    def test_the_sidebar_folds_every_section_but_the_open_one(self):
        # Only a section whose label links to its own page folds: one
        # without (a span) would leave its pages out of reach.
        css = CSS.read_text()
        self.assertRegex(css, r"\.collection-section:not\(\.collection-section--open\) > "
                              r"a\.collection-section-label \+ ul[ \t]*\{[ \t]*display:\s*none")
        self.assertRegex(css, r"\.collection-section > ul[ \t]*\{[^{}]*padding-left:")

    def test_the_header_is_always_two_lines_wordmark_then_nav_and_switcher(self):
        # .bar is a plain block (the wordmark, a block h1, stacks above
        # .bar-nav on its own line at any width); .bar-nav holds .nav and
        # .languages nowrap, so that pair shares its row, the switcher
        # pinned at the far right, and never lands under the nav.
        css = CSS.read_text()
        bar = re.search(r"(?<![\w-])\.bar[ \t]*\{([^{}]*)\}", css)
        self.assertIsNotNone(bar, "no .bar rule found")
        self.assertNotIn("display: flex", bar.group(1))
        bar_nav = re.search(r"\.bar-nav[ \t]*\{([^{}]*)\}", css)
        self.assertIsNotNone(bar_nav, "no .bar-nav rule found")
        self.assertIn("flex-wrap: nowrap", bar_nav.group(1))
        self.assertIn("justify-content: space-between", bar_nav.group(1))

    def test_focus_motion_and_dark_scheme(self):
        css = CSS.read_text()
        self.assertIn(":focus-visible", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("@media (prefers-color-scheme: dark)", css)

    def test_the_wordmark_wraps_instead_of_scrolling_the_page(self):
        # A long path (~/fixture docs/documentation/Getting started, longer
        # on /fr/) must not scroll the page sideways at 360px: the wordmark
        # can break at any character, and after each separator.
        css = CSS.read_text()
        wordmark = re.search(r"\.wordmark[ \t]*\{([^{}]*)\}", css)
        self.assertIsNotNone(wordmark, "no .wordmark rule found")
        self.assertIn("overflow-wrap: anywhere", wordmark.group(1))
        self.assertRegex(css, r"\.wordmark \.slash::after[ \t]*\{[^{}]*content:\s*\"\\200B\"")
        narrow = re.search(r"@media \(max-width: 40rem\)[ \t]*\{(.*?)\n\}", css, re.S)
        self.assertIsNotNone(narrow, "no @media (max-width: 40rem) block found")
        self.assertRegex(narrow.group(1), r"\.wordmark\s*\{[^{}]*font-size:")

    def test_the_doc_text_column_is_not_squeezed_between_45_and_60rem(self):
        # Below 60rem the fixed 11ch gutter of .s leaves too little room for
        # the doc text: .doc-main .s becomes single-column there.
        css = CSS.read_text()
        self.assertRegex(
            css, r"@media \(max-width: 60rem\)[ \t]*\{[^{}]*\.doc-main \.s[ \t]*\{[^{}]*"
            r"grid-template-columns:\s*minmax\(0,\s*1fr\)")

    def test_ligatures_are_disabled_in_code(self):
        css = CSS.read_text()
        self.assertIn("font-variant-ligatures: none", css)

    def test_empty_taglines_take_no_space(self):
        css = CSS.read_text()
        self.assertRegex(css, r"\.tagline:empty,\s*\.home-tagline:empty[ \t]*\{[ \t]*display:\s*none")

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
