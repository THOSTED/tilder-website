"""build.sh and the base layout, end to end, on the fixture site."""

import re
import unittest

from tests.helpers import THEME, Build, builder_missing, fixture_build


class Pipeline(unittest.TestCase):
    def setUp(self):
        self.build = fixture_build(self)

    def test_no_warning(self):
        self.assertNotRegex(self.build.stderr, r"(?m)^(warning|seo):")

    def test_the_checks_ran(self):
        self.assertIn("classes of the contract, all styled", self.build.stdout)
        self.assertIn("pairs, all at or above their minimum", self.build.stdout)

    def test_theme_files_are_served_and_configuration_is_not(self):
        out = self.build.out
        for served in ("style.css", "fonts/inter-regular.woff2", "fonts/OFL-Inter.txt"):
            self.assertTrue((out / served).is_file(), served)
        for kept in ("theme.toml", "theme.fr.toml", "layout.html", "types/doc.py", "README.md"):
            self.assertFalse((out / kept).exists(), kept)


class NotBuilt(unittest.TestCase):
    """A broken input stops build.sh; each case builds on its own."""

    def setUp(self):
        why = builder_missing()
        if why:
            self.skipTest(why)

    def test_a_build_warning_fails_the_build(self):
        page = ("---\nman: X(7)\ntitle: Warned\ndescription: A page whose code block names "
                "a language tilder does not know.\ntagline: x\nnav: -\n---\n\n## Name\n\n"
                "```nosuchlanguage\ncode\n```\n")
        build = Build({"content/warned.md": page})
        self.assertEqual(build.returncode, 1)
        self.assertIn("unknown code language", build.stderr)
        self.assertIn("the build printed warnings", build.stderr)

    def test_an_unstyled_contract_class_fails_before_the_build(self):
        css = (THEME / "style.css").read_text().replace(".tag--full", ".tag--ful")
        build = Build({"theme/style.css": css})
        self.assertEqual(build.returncode, 1)
        self.assertIn(".tag--full is written by tilder and not styled", build.stderr)


class BaseLayout(unittest.TestCase):
    def setUp(self):
        self.build = fixture_build(self)

    def pages(self):
        return sorted(self.build.out.rglob("*.html"))

    def test_every_page_keeps_the_contract(self):
        for path in self.pages():
            html = path.read_text()
            name = str(path.relative_to(self.build.out))
            self.assertEqual(len(re.findall(r"<h1[ >]", html)), 1, name)
            self.assertRegex(html, r'<html lang="(en|fr)">', name)
            self.assertRegex(html, r'<main id="contenu"[^>]* lang="(en|fr)"', name)
            self.assertIn('<link rel="canonical" href="https://docs.example/', html, name)
            self.assertNotRegex(html, r"\{\{", name)

    def test_the_man_page_frame(self):
        html = self.build.read("404.html")
        self.assertIn('class="layout-base type-page"', html)
        self.assertIn('<div class="manline manline--head" aria-hidden="true">', html)
        self.assertIn("<span>FIXTURE(7)</span>", html)
        self.assertIn("<span>Fixture Manual</span>", html)
        self.assertIn('<footer class="manline manline--foot">', html)
        self.assertIn("<span>2026-09-01</span>", html)
        self.assertIn('<a class="skip" href="#contenu">', html)

    def test_no_request_to_another_host(self):
        for path in self.pages():
            self.assertNotRegex(path.read_text(), r'(src|srcset)="https?://', path.name)
        self.assertNotRegex(self.build.read("style.css"), r"url\([\"']?https?://")

    def test_layout_comments_hold_no_placeholder(self):
        # tilder replaces {{ name }} even inside an HTML comment.
        for path in [THEME / "layout.html", *sorted((THEME / "layouts").glob("*.html"))]:
            for comment in re.findall(r"<!--.*?-->", path.read_text(), re.S):
                self.assertNotIn("{{", comment, path.name)
