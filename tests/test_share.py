"""share.svg: only fields tilder fills, 1200x630, nothing remote."""

import re
import tomllib
import unittest

from tests.helpers import THEME, fixture_build


class ShareSvg(unittest.TestCase):
    def test_every_field_is_one_tilder_fills(self):
        computed = {"logo", "manual_upper", "wordmark", "domain", "card_1", "card_2"}
        share = {"share." + k for k in tomllib.loads((THEME / "theme.toml").read_text())["share"]}
        fields = set(re.findall(r"\{\{\s*([\w.]+)\s*\}\}", (THEME / "share.svg").read_text()))
        self.assertEqual(fields - computed - share, set())
        self.assertIn("wordmark", fields)

    def test_1200_by_630_and_self_contained(self):
        svg = (THEME / "share.svg").read_text()
        self.assertIn('viewBox="0 0 1200 630"', svg)
        self.assertNotRegex(svg, r'href="https?:')

    def test_the_build_draws_it(self):
        build = fixture_build(self)
        self.assertEqual((build.out / "share.png").read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        self.assertNotIn("share.svg", [p.name for p in build.out.iterdir()])
