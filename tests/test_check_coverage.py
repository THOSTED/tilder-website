"""tools/check-coverage.py: the documentation names every key, setting,
front-matter key, class, placeholder and option of the pinned tilder."""

import contextlib
import io
import pathlib
import shutil
import tempfile
import textwrap
import unittest

from tests.helpers import load_tool

cov = load_tool("check-coverage")

DEFAULTS = textwrap.dedent('''\
    [site]
    name = "my site"
    title_suffix = " - my site"

    [[nav]]
    label = "home"
    href = ""

    [languages]

    [collections.blog]
    type = "post"
    feed = "blog/feed.xml"
    ''')

THEME_MD = textwrap.dedent('''\
    # Themes

    ## `layout.html`

    | Placeholder | Value |
    |---|---|
    | `{{ title }}` | the title, `{{ site.lang }}` in passing |
    | `{{ page.<key> }}` | a front-matter value |
    | `{{ prev }}`, `{{ next }}` | neighbours |

    ## The HTML the builder writes

    | Class | What |
    |---|---|
    | `.sr-only` | hidden |
    | `.s`, `.b` | a section |
    | `.b.grid` | a marker |
    | `.inset`, `.callout`, `.callout--info`, `--warning` | boxes |
    | `pre.code[data-lang]` | code |
    ''')

MARKDOWN_MD = textwrap.dedent('''\
    ## Front matter

    | Key | Required | Meaning |
    |---|---|---|
    | `man` | yes | the name |
    | `text` | no | `text: no` skips the mirror |

    ## Sections
    ''')

BUILD_PY = '"""Build.\n\n    build.py --out DIR   build into DIR\n"""\nimport sys\nif "--root" in sys.argv:\n    pass\n'

POST_PY = 'NAME = "post"\nDEFAULTS = {"feed_title": "posts", "empty": "No post yet."}\n'


class Tree(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="cov-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        t = self.tilder = self.tmp / "tilder"
        (t / "docs").mkdir(parents=True)
        (t / "src").mkdir()
        (t / "types").mkdir()
        (t / "defaults.toml").write_text(DEFAULTS)
        (t / "docs" / "theme.md").write_text(THEME_MD)
        (t / "docs" / "markdown.md").write_text(MARKDOWN_MD)
        (t / "src" / "build.py").write_text(BUILD_PY)
        (t / "types" / "post.py").write_text(POST_PY)
        self.docs = self.tmp / "docs"
        self.docs.mkdir()

    def names(self, terms):
        return sorted(t.name for t in terms)


class Terms(Tree):
    def test_defaults_keys_tables_and_arrays_of_tables(self):
        self.assertEqual(self.names(cov.defaults_terms(DEFAULTS)), sorted([
            "[site]", "site.name", "site.title_suffix", "[[nav]]", "nav.label", "nav.href",
            "[languages]", "[collections.blog]", "collections.blog.type", "collections.blog.feed"]))

    def test_type_settings(self):
        self.assertEqual(self.names(cov.type_terms(self.tilder / "types")),
                         ["post.empty", "post.feed_title"])

    def test_front_matter_keys_first_column_only(self):
        self.assertEqual(self.names(cov.front_matter_terms(MARKDOWN_MD)), ["man", "text"])

    def test_classes_expand_the_modifier_shorthand_and_skip_attributes(self):
        names = self.names(cov.class_terms(THEME_MD, None))
        self.assertIn("callout--warning", names)
        self.assertIn("code", names)
        self.assertIn("grid", names)
        self.assertNotIn("data-lang", names)
        self.assertNotIn("--warning", names)

    def test_classes_from_the_contract_module_when_there_is_one(self):
        contract = 'CLASSES = ["sr-only", "collection-section"]\n'
        self.assertEqual(self.names(cov.class_terms(THEME_MD, contract)),
                         ["collection-section", "sr-only"])

    def test_placeholders_first_column_only_and_no_generic_ones(self):
        self.assertEqual(self.names(cov.placeholder_terms(THEME_MD)), ["next", "prev", "title"])

    def test_options_from_every_string_of_build_py(self):
        self.assertEqual(self.names(cov.option_terms(BUILD_PY)), ["--out", "--root"])


class Covered(Tree):
    def term(self, terms, name):
        return next(t for t in terms if t.name == name)

    def test_a_key_is_covered_by_its_dotted_name(self):
        t = self.term(cov.defaults_terms(DEFAULTS), "site.title_suffix")
        self.assertTrue(cov.covered(t, ["Set `site.title_suffix` to ..."]))

    def test_a_key_is_covered_by_its_table_and_its_name_in_one_file(self):
        t = self.term(cov.defaults_terms(DEFAULTS), "collections.blog.feed")
        self.assertTrue(cov.covered(t, ["```toml\n[collections.blog]\nfeed = \"x\"\n```"]))
        self.assertTrue(cov.covered(t, ["## `[collections.blog]`\n\n| `feed` | the RSS path |"]))
        self.assertFalse(cov.covered(t, ["[collections.blog]", "| `feed` | elsewhere |"]))

    def test_a_bare_leaf_name_is_not_enough(self):
        t = self.term(cov.defaults_terms(DEFAULTS), "site.name")
        self.assertFalse(cov.covered(t, ["the `name` of something"]))

    def test_a_dotted_name_does_not_match_a_longer_one(self):
        t = self.term(cov.defaults_terms(DEFAULTS), "site.name")
        self.assertFalse(cov.covered(t, ["`site.names`"]))

    def test_a_class_needs_its_dot_and_a_boundary(self):
        s = self.term(cov.class_terms(THEME_MD, None), "s")
        self.assertFalse(cov.covered(s, ["`.sr-only` and `.small`"]))
        self.assertTrue(cov.covered(s, ["a section, `.s`, holds"]))
        grid = self.term(cov.class_terms(THEME_MD, None), "grid")
        self.assertTrue(cov.covered(grid, ["`.b.grid`"]))

    def test_a_placeholder_allows_spacing(self):
        t = self.term(cov.placeholder_terms(THEME_MD), "title")
        self.assertTrue(cov.covered(t, ["`{{title}}`"]))
        self.assertTrue(cov.covered(t, ["`{{ title }}`"]))

    def test_an_option_is_not_a_prefix_of_another(self):
        t = self.term(cov.option_terms(BUILD_PY), "--out")
        self.assertFalse(cov.covered(t, ["`--output`"]))
        self.assertTrue(cov.covered(t, ["`--out DIR`"]))


class Main(Tree):
    FULL = textwrap.dedent('''\
        `site.name` `site.title_suffix` `[[nav]]` `nav.label` `nav.href` `[languages]`
        `[collections.blog]` `collections.blog.type` `collections.blog.feed` `[site]`
        `feed_title` `empty` `man` `text` `.sr-only` `.s` `.b` `.b.grid` `.inset` `.callout`
        `.callout--info` `.callout--warning` `pre.code` `{{ title }}` `{{ prev }}` `{{ next }}`
        `--out` `--root`
        ''')

    def run_main(self):
        return cov.main(["--tilder", str(self.tilder), "--docs", str(self.docs)])

    def test_everything_documented_in_both_languages_passes(self):
        (self.docs / "a.md").write_text(self.FULL)
        (self.docs / "sub").mkdir()
        (self.docs / "sub" / "a.fr.md").write_text(self.FULL)
        self.assertEqual(self.run_main(), 0)

    def test_a_term_missing_in_french_only_fails_and_is_named(self):
        (self.docs / "a.md").write_text(self.FULL)
        (self.docs / "a.fr.md").write_text(self.FULL.replace("`--root`", ""))
        with contextlib.redirect_stderr(io.StringIO()) as err:
            code = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("error: coverage: fr: option --root is not documented", err.getvalue())
        self.assertNotIn("en: option --root", err.getvalue())

    def test_a_missing_input_is_exit_2(self):
        (self.tilder / "defaults.toml").unlink()
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(self.run_main(), 2)
        self.assertIn("defaults.toml", err.getvalue())
