"""The theme's configuration: its words in both languages, and colours
that are the stylesheet's own."""

import tomllib
import unittest

from tests.helpers import THEME, load_tool


class ThemeToml(unittest.TestCase):
    def test_the_share_colours_are_the_light_tokens(self):
        share = tomllib.loads((THEME / "theme.toml").read_text())["share"]
        light = load_tool("check-contrast").tokens((THEME / "style.css").read_text())["light"]
        self.assertEqual(share, {"theme_color": light["accent"], "background_color": light["bg"],
                                 "text_color": light["text"], "muted_color": light["muted"],
                                 "rule_color": light["rule"]})

    def test_both_languages_have_the_same_words(self):
        en = tomllib.loads((THEME / "theme.toml").read_text())
        fr = tomllib.loads((THEME / "theme.fr.toml").read_text())
        for table in ("search", "doc"):
            self.assertEqual(sorted(en[table]), sorted(fr[table]), table)
        self.assertEqual(sorted(en["search"]), ["count", "label", "none", "placeholder"])
        self.assertEqual(sorted(en["doc"]), ["contents", "on_this_page"])
        self.assertIn("{n}", en["search"]["count"])
        self.assertIn("{n}", fr["search"]["count"])

    def test_the_french_file_sets_no_other_language(self):
        fr = tomllib.loads((THEME / "theme.fr.toml").read_text())
        self.assertNotIn("share", fr)
        self.assertEqual(fr.get("site", {}).get("lang", "fr"), "fr")
