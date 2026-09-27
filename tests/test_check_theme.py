import io
import pathlib
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from tests.helpers import REPO, load_tool

check = load_tool("check-theme")

CONTRACT = """# Themes

## The HTML the builder writes

| Class | What |
|---|---|
| `.sr-only` | screen readers |
| `.wordmark`, `.tilde` | the h1 |
| `.b.grid`, `.members` | markers |
| `.callout`, `.callout--info`, `--warning`, `--error`, `.callout-label` | boxes |
| `pre.code[data-lang]`, `.hl-k` | code |
| `u.u` | underlined |

## Something else

| `.not-a-class-of-the-contract` | ignored |
"""


class ContractClasses(unittest.TestCase):
    def test_reads_the_first_column_of_the_section(self):
        self.assertEqual(check.contract_classes(CONTRACT), [
            "sr-only", "wordmark", "tilde", "b", "grid", "members", "callout",
            "callout--info", "callout--warning", "callout--error", "callout-label",
            "code", "hl-k", "u"])

    def test_the_real_contract_has_the_classes_of_tilder_1_1(self):
        classes = check.contract_classes((REPO / "tools" / "tilder-theme.md").read_text())
        for name in ("collection-nav", "collection-group-label", "prev-label", "next-label",
                     "languages", "callout--error", "hl-gh", "task--todo", "toc-label"):
            self.assertIn(name, classes)

    def test_a_contract_without_the_section_is_an_error(self):
        with self.assertRaises(ValueError):
            check.contract_classes("# Themes\n\nNothing here.\n")


class Missing(unittest.TestCase):
    def test_a_class_counts_only_as_a_whole_selector_name(self):
        css = ".nav-bar { } .callout--info, .callout--warning { } .b.grid { }"
        self.assertEqual(check.missing(css, ["nav", "callout--info", "callout", "b", "grid"]),
                         ["nav", "callout"])

    def test_a_class_named_only_in_a_comment_is_missing(self):
        self.assertEqual(check.missing("/* .tag */ .meta { }", ["tag", "meta"]), ["tag"])


class Main(unittest.TestCase):
    def run_main(self, css):
        with tempfile.TemporaryDirectory() as d:
            style, contract = pathlib.Path(d, "style.css"), pathlib.Path(d, "theme.md")
            style.write_text(css)
            contract.write_text(CONTRACT)
            err, out = io.StringIO(), io.StringIO()
            with redirect_stderr(err), redirect_stdout(out):
                code = check.main(["check-theme.py", str(style), str(contract)])
        return code, out.getvalue(), err.getvalue()

    def test_every_class_styled_exits_0(self):
        css = " ".join("." + c + " {}" for c in check.contract_classes(CONTRACT))
        code, out, _ = self.run_main(css)
        self.assertEqual(code, 0)
        self.assertIn("14 classes", out)

    def test_a_missing_class_exits_1_and_names_it(self):
        code, _, err = self.run_main(".sr-only {}")
        self.assertEqual(code, 1)
        self.assertIn(".wordmark is written by tilder and not styled", err)

    def test_an_unreadable_contract_exits_2(self):
        err = io.StringIO()
        with redirect_stderr(err):
            code = check.main(["check-theme.py", "/nonexistent.css", "/nonexistent.md"])
        self.assertEqual(code, 2)
