"""The theme's configuration: its words in both languages, and colours
that are the stylesheet's own."""

import re
import tomllib
import unittest

from tests.helpers import THEME


def light_tokens():
    """The custom properties of style.css's first :root rule: the light
    scheme."""
    css = re.sub(r"/\*.*?\*/", "", (THEME / "style.css").read_text(), flags=re.S)
    root = re.search(r"^:root\s*\{([^}]*)\}", css, re.M).group(1)
    return {k: v.strip() for k, v in re.findall(r"--([\w-]+)\s*:\s*([^;]+);", root)}


class ThemeToml(unittest.TestCase):
    def test_the_check_pairs_every_text_colour_with_both_backgrounds(self):
        check = tomllib.loads((THEME / "theme.toml").read_text())["check"]
        self.assertEqual(check["contrast"],
                         [[f"--{fg}", f"--{bg}"]
                          for fg in ("text", "muted", "faint", "accent", "info", "warning", "error")
                          for bg in ("bg", "surface")])
        self.assertNotIn("unstyled", check)

    def test_the_share_colours_are_the_light_tokens(self):
        share = tomllib.loads((THEME / "theme.toml").read_text())["share"]
        light = light_tokens()
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
