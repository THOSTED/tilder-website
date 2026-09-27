import io
import pathlib
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from tests.helpers import load_tool

check = load_tool("check-contrast")

NAMES = ("bg", "surface", "text", "muted", "faint", "accent", "info", "warning", "error")


def css(light, dark):
    def block(values):
        return " ".join(f"--{k}: {v};" for k, v in values.items())
    return (f":root {{ {block(light)} --mono: monospace; }}\n"
            f"/* :root {{ --text: #ffffff; }} a comment */\n"
            f"@media (prefers-color-scheme: dark) {{ :root {{ {block(dark)} }} }}\n")


GOOD_LIGHT = dict({k: "#000000" for k in NAMES}, bg="#ffffff", surface="#f0f0f0")
GOOD_DARK = dict({k: "#ffffff" for k in NAMES}, bg="#000000", surface="#111111")


class Ratio(unittest.TestCase):
    def test_black_on_white_is_21(self):
        self.assertAlmostEqual(check.ratio("#000000", "#ffffff"), 21.0, places=2)

    def test_same_colour_is_1(self):
        self.assertAlmostEqual(check.ratio("#777777", "#777777"), 1.0)

    def test_known_pair(self):
        # #767676 on white is the classic 4.54:1 grey.
        self.assertAlmostEqual(check.ratio("#767676", "#ffffff"), 4.54, places=2)


class Tokens(unittest.TestCase):
    def test_reads_both_schemes_and_ignores_comments(self):
        t = check.tokens(css(GOOD_LIGHT, GOOD_DARK))
        self.assertEqual(t["light"]["text"], "#000000")
        self.assertEqual(t["dark"]["text"], "#ffffff")

    def test_no_dark_scheme_is_an_error(self):
        with self.assertRaises(ValueError):
            check.tokens(":root { --bg: #ffffff; }")

    def test_a_missing_or_malformed_token_is_an_error(self):
        light = dict(GOOD_LIGHT, muted="grey")
        with self.assertRaisesRegex(ValueError, "--muted"):
            check.results(check.tokens(css(light, GOOD_DARK)))


class Main(unittest.TestCase):
    def run_main(self, text, *flags):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d, "style.css")
            path.write_text(text)
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = check.main(["check-contrast.py", str(path), *flags])
        return code, out.getvalue(), err.getvalue()

    def test_good_pairs_exit_0(self):
        code, out, _ = self.run_main(css(GOOD_LIGHT, GOOD_DARK))
        self.assertEqual(code, 0)
        self.assertIn("28 pairs", out)

    def test_a_low_pair_exits_1_and_names_it(self):
        dark = dict(GOOD_DARK, faint="#222222")
        code, _, err = self.run_main(css(GOOD_LIGHT, dark))
        self.assertEqual(code, 1)
        self.assertIn("dark: --faint on --bg", err)

    def test_markdown_prints_the_table(self):
        code, out, _ = self.run_main(css(GOOD_LIGHT, GOOD_DARK), "--markdown")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("| scheme | foreground | background | ratio | minimum |"))
        self.assertIn("| light | `--text` | `--bg` | 21.00 | 4.5 |", out)
