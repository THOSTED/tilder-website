# Documentation Theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A generic, bilingual (English, French) tilder theme for documentation sites in `theme/`: a man-page base layout, an airy landing layout, a three-column doc layout, the `doc` and `showcase` types, three ES5 scripts, self-hosted fonts, with the checks and the build script that keep it true.

**Architecture:** The theme is plain files that tilder reads (`layout.html`, `layouts/*.html`, `style.css`, `types/*.py`, `theme*.toml`, `share.svg`) or serves (`style.css`, `fonts/`, `*.js`). Two stdlib tools (`tools/check-theme.py`, `tools/check-contrast.py`) check the stylesheet against tilder's class contract and WCAG AA, and run in `build.sh`, which builds with tilder's Docker image by default or a local checkout (`TILDER_BUILD`). A minimal fixture site (`tests/site/`), separate from the future `content/`, is built end to end by the `unittest` suite.

**Tech Stack:** HTML, CSS, ES5 JavaScript; Python 3.11+ standard library (types, tools, tests); tilder 1.1.0 (Docker image `ghcr.io/thosted/tilder:1.1.0`, or `/home/theau/Git/tilder/build.py`); node only as an optional test runner (no npm); fonttools once, in a throwaway venv, to subset the fonts.

**Spec:** `docs/superpowers/specs/2026-09-26-docs-theme-design.md` (sibling, context only: `docs/superpowers/specs/2026-09-26-site-content-design.md`). The tilder contracts it argues from: `/home/theau/Git/tilder/docs/theme.md`, `docs/types.md`, `docs/markdown.md`, `docs/languages.md`, `AGENTS.md`.

## Global Constraints

- The theme lives in `theme/` and is **generic**: no project name, no site text, no domain in layouts, CSS, scripts, types or `theme*.toml` ("any tilder project that documents something can copy the folder").
- Bilingual out of the box through `theme.toml` (English) and `theme.fr.toml` (French); every other file of the theme is in English.
- Look is **hybrid**: `layouts/home.html` airy and modern; every other page a man page.
- Styles **every** class of tilder's `docs/theme.md` (v1.1.0), light and dark; `tools/check-theme.py` proves it at every build.
- Scripts: ES5, same-origin files, progressive enhancement, no network but same-origin JSON, no storage, no cookie, no text of their own (`data-*`).
- No third-party request; fonts self-hosted (JetBrains Mono + Inter, OFL, woff2, latin + latin-ext); no CDN at runtime.
- WCAG AA contrast (4.5:1 for every text token on `--bg` and `--surface`, both schemes), visible focus, `prefers-reduced-motion`, `.sr-only`.
- Every layout keeps `lang="{{ site.lang }}"`, exactly one `{{ brand }}`, `<main id="contenu" lang="{{ content_lang }}">`, `<link rel="canonical" href="{{ canonical }}">`.
- A layout's HTML comments never contain `{{` — tilder fills placeholders inside comments too, and an unknown one stops the build.
- The build emits no warning: `build.sh` fails on any `warning:` or `seo:` line of tilder's stderr.
- Python: standard library only, for types, tools and tests. Tests run from the repository root with `python3 -m unittest`. No npm, no JS framework; node is used by tests when installed, else those tests skip.
- **Building.** `build.sh` runs tilder from the Docker image `ghcr.io/thosted/tilder:<TILDER_VERSION>` by default (`TILDER_VERSION` holds `1.1.0`: CI publishes image tags without the `v`; a leading `v` is stripped). With `TILDER_BUILD=/path/to/tilder/build.py` it runs that checkout instead. Until the image is published, every build and every build test in this plan is run as `TILDER_BUILD=/home/theau/Git/tilder/build.py …`. Without `TILDER_BUILD` and without the image pulled, the build tests skip and say why.
- A local build (`TILDER_BUILD`) needs `rsvg-convert` or ImageMagick on the machine, else tilder warns that it skips the icons and `build.sh` fails, by design. This machine has `magick`.
- `/home/theau/Git/tilder` is read-only for this work: read files and use `git -C /home/theau/Git/tilder show <ref>:<path>`, never a command that changes its branch, index or working tree.
- Commits: Conventional Commits; author `Théau TROVA <theau@thosted.fr>` (already the repository's configured identity: check with `git config user.name` / `user.email` before the first commit); **never** a `Co-Authored-By` or any other AI attribution trailer, in any commit.

## Review Focus

1. **Markdown noise in the search index.** A doc page with `##` lines inside code fences, `{#id}`/`{mono}` markers, link targets, HTML comments, table rules, callout markers: the index must hold the reader's words only and the real `##` titles. Pinned by `Index.test_headings_are_the_h2_titles_without_markers_or_code` and `test_plain_keeps_the_words_only` (Task 5).
2. **A language with untranslated pages.** On `/fr/`, the index must list the English fallback pages too, with links that stay under `/fr/`, and the theme's words must be French. Pinned by `SearchIndex.test_one_index_per_language` and `Doc.test_french_words_from_theme_fr_toml` (Task 8), `Index.test_the_url_is_from_the_language_s_landing_page` (Task 5).
3. **Queries people really type.** Upper case, accents ("Élan" vs "elan"), several words, only spaces: case- and accent-insensitive, every word must match, title first, nothing for a blank query. Pinned by `SearchUnderNode` (Task 10).
4. **Front matter written wrong in a theme type.** `order: first`, a showcase item without `url`, an `image:` that is not there: one readable error naming the value, not a traceback or a broken page. Pinned by `Order.test_an_order_that_is_not_a_number_says_so` (Task 5), `Showcase.test_url_is_required` and `test_a_missing_image_says_so` (Task 6).
5. **`search.js` linked twice.** A doc-layout page that also lists docs (`docs/index.md` with `layout: doc` and `{docs}`) gets `search.js` from the layout and from the type's `SCRIPT`: one search field, not two. Pinned by `SearchUnderNode.test_linked_twice_the_field_is_made_once_from_the_data_words` (Task 10) and `Loaded.test_search_js_twice_on_a_doc_layout_page_that_lists_docs` (Task 11).

## Resolutions

The spec read against tilder's code (branch `main`, which now holds the v1.1.0 features). Each resolution is applied in the tasks below. **[owner]** marks one that changes the spec's intent or needs a decision.

1. **`{{ search.* }}` and `{{ doc.* }}` resolve.** `page.fill` walks the merged configuration, `defaults.toml < theme.toml < theme.<lang>.toml < site.toml < site.<lang>.toml` (`config.load_config`), so any table of `theme.toml` is a placeholder and a site overrides it. Verified by a build.
2. **[owner] `theme.fr.toml` stops the build of any site that does not declare `fr`** (`languages.setup` refuses a `theme.<lang>.toml` of an undeclared language, monolingual sites included). Kept, as the spec asks; the README tells such a site to delete the file. Alternative for later: tilder could ignore undeclared `theme.<lang>.toml`.
3. **`data-*` on `.inset` is not possible** (`page.html_blocks` writes a bare `<div class="inset">`), and not needed: the page writes its own label. But an inset holds **paragraphs only** (`markdown.inset`), so a table, list, code block or callout cannot be shown live inside one. **[owner]** The theme adds one style: an entry marked `{example}` (`### Rendered {example}`, the construct indented under it) is drawn with the same dashed frame (`.entry--example`). Sub-project C uses it for block constructs.
4. **`outputs()` reads the source** from `item["src"]` (a `pathlib.Path`; the standard library is not restricted), and strips the front matter and Markdown syntax with local regular expressions (`headings`, `plain`), since `markdown` is not a module a type may import.
5. **The index's `"u"` is relative to the language's landing page** (`docs/start`, computed as `clean_url(path)` minus `clean_url("index.html")`), not the absolute `/fr/docs/start`; `search.js` puts the layout's `{{ home }}` (`data-home`) before it. Links then work under any prefix or sub-path.
6. **The layout cannot read a collection's settings**, so it cannot build the index URL from `dir` and `index`. `doc.defaults()` sets `meta["search_index"] = "{dir}/{index}"`, read as `{{ page.search_index }}`. The collection's own page is a plain page: with `layout: doc` it sets `search_index:` in its front matter; an empty value means no search field.
7. **`search.js` may run twice** (layout link + `SCRIPT`, see Review Focus 5): it marks its container `data-search-ready` and stops on a second run.
8. **[owner] The `[TOC]` is inside `{{ body }}`,** a folded `<details>`; no layout can put it in a third column. `nav.js` moves it into the right column at 60rem and wider and opens it, and puts it back, folded, when narrower. Without JavaScript there is no right column: the `[TOC]` stays in the text, as tilder draws it. The right column's "On this page" is visual (`aria-hidden`); the moved `<nav>` keeps its `labels.toc` name.
9. **[owner] `showcase` JSON-LD:** tilder overwrites every type node's `url` (and `inLanguage`) with the page's own (`seo.json_ld`), so a `WebSite` node with the listed site's `url` is impossible. The type returns a `WebPage` whose `about` is `{"@type": "WebSite", "name", "url"}`. `doc` does not set `inLanguage`: tilder does.
10. **[owner] `{docs}` "grouped":** a marker returns cards only, no headings. The cards come in the sidebar's order (ungrouped first, then each group in the order of its first page), each card's meta line names its group, and the first card of a group is marked `entry--group` (more space above).
11. **The Docker image ships no `docs/`,** so the contract cannot be "read from the pinned image". `tools/tilder-theme.md` is a verbatim copy of the pinned version's `docs/theme.md`; with `TILDER_BUILD` the checkout's own `docs/theme.md` is used. **[owner]** Alternative: add `COPY docs/theme.md` to tilder's Dockerfile.
12. **The image has no `ENTRYPOINT`** (only `CMD`), so the site spec's `docker run … image --root /site …` would fail. `build.sh` runs `python3 -B /tilder/build.py --root /site --out /out`; the tag is `1.1.0` (Resolution in Global Constraints).
13. **[owner] The CSP blocks the search.** tilder's `examples/Caddyfile` sends `default-src 'none'` with no `connect-src`, so the index request is refused. The site's Caddyfile (sub-project C) must add `connect-src 'self'`; the README says so; `search.js` removes its field when the index cannot be read.
14. **The kitchen sink** of spec §10 is content (`content/kitchen-sink.md`, sub-project C). The theme's own is the fixture's `tests/site/content/kitchen-sink.md`, which C copies. `.icon` never appears: the theme ships no `icons/`.
15. **Fonts:** five files, subset once to latin + latin-ext with fonttools in a throwaway venv (no Reserved Font Name in either licence, checked); the README records versions, sources and ranges.
16. **JS tests without npm:** `search.js` exports its matching functions when `module` exists (node) and returns before touching the DOM; `tests/js/search-dom.js` runs the real script twice against a 40-line stand-in DOM. `nav.js` and `code.js` are covered by the ES5/rules lint, the build tests and the README's manual check list.
17. **`code.js`** wraps each `pre.code` in a `.code-box` (a theme class) so the button stays put while the code scrolls.

---

## File structure

```
.gitignore                 + __pycache__/
build.sh                   checks, then tilder (Docker, or TILDER_BUILD), fails on warnings
TILDER_VERSION             1.1.0 - the image tag
tools/
  check-theme.py           every contract class is in style.css
  check-contrast.py        WCAG ratios of the colour tokens; --markdown for the README
  tilder-theme.md          verbatim docs/theme.md of the pinned tilder
theme/
  README.md  LICENSE       what it is, files, types, words, requirements, fonts, contrast
  layout.html              man-page base
  layouts/home.html        landing page
  layouts/doc.html         three columns
  style.css                fonts, tokens, frame, contract classes, home, doc, search, copy
  fonts/                   5 woff2 + OFL-Inter.txt + OFL-JetBrainsMono.txt
  share.svg                1200x630 preview
  code.js  search.js  nav.js
  types/doc.py  types/showcase.py
  theme.toml  theme.fr.toml
tests/
  __init__.py
  helpers.py               load_tool, load_type (stubs), Build, fixture_build
  js/search-dom.js         stand-in DOM for search.js, under node
  site/                    the fixture: content/ (en + fr), assets/logo.svg
  test_check_theme.py  test_check_contrast.py  test_fonts.py  test_style.py
  test_type_doc.py  test_type_showcase.py  test_build.py  test_theme_toml.py
  test_layouts.py  test_kitchen_sink.py  test_scripts.py  test_share.py  test_readme.py
```

Run everything, from `/home/theau/Git/tilder-website`:

```bash
TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest -v
```

---

### Task 1: The contract check (`tools/check-theme.py`) and the test scaffolding

**Files:**
- Create: `tools/check-theme.py`, `tools/tilder-theme.md`, `tests/__init__.py` (empty), `tests/helpers.py`, `tests/test_check_theme.py`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: nothing.
- Produces: `tests.helpers.REPO`, `THEME`, `FIXTURE` (`pathlib.Path`), `load_tool(name: str) -> module` (loads `tools/<name>.py`, hyphens allowed); in `check-theme.py`: `contract_classes(text: str) -> list[str]` (raises `ValueError`), `missing(css: str, classes: list[str]) -> list[str]`, `main(argv: list[str]) -> int` (0 all styled, 1 missing, 2 unreadable). CLI: `python3 tools/check-theme.py STYLE_CSS THEME_MD`.

- [ ] **Step 1: Vendor the pinned contract**

`tools/tilder-theme.md` is a verbatim copy of tilder's `docs/theme.md` at the pinned version (Resolution 11). Read-only in the tilder repository:

```bash
cd /home/theau/Git/tilder-website
mkdir -p tools tests
if git -C /home/theau/Git/tilder rev-parse -q --verify v1.1.0 >/dev/null; then ref=v1.1.0; else ref=main; fi
git -C /home/theau/Git/tilder show "$ref:docs/theme.md" > tools/tilder-theme.md
grep -c 'collection-nav' tools/tilder-theme.md   # expected: 1 or more (v1.1.0 contract)
```

If `$ref` was `main`, re-copy from `v1.1.0` once that tag exists (`diff` should be empty). Add `__pycache__/` to `.gitignore`, which then reads:

```
public/
__pycache__/
```

- [ ] **Step 2: Write the test scaffolding and the failing tests**

`tests/__init__.py`: an empty file. `tests/helpers.py`:

```python
"""What the theme's tests share: load a tool as a module. (Later tasks
add the theme types and the fixture build.)"""

import importlib.util
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
THEME = REPO / "theme"
FIXTURE = REPO / "tests" / "site"


def load_tool(name):
    """tools/<name>.py ("check-theme") as a module."""
    path = REPO / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

`tests/test_check_theme.py`:

```python
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
```

- [ ] **Step 3: Run them to see them fail**

Run: `python3 -m unittest tests.test_check_theme -v`
Expected: ERROR, `FileNotFoundError` for `tools/check-theme.py`.

- [ ] **Step 4: Write `tools/check-theme.py`**

```python
#!/usr/bin/env python3
"""Check that a theme's style.css styles every class tilder writes.

The classes are read from tilder's theme contract, docs/theme.md: the
first column of the table under "## The HTML the builder writes".

    python3 tools/check-theme.py theme/style.css path/to/docs/theme.md

Exit 0 when every class appears in a selector, 1 with one line per
missing class, 2 when the contract cannot be read.
"""

import re
import sys

SECTION = "## The HTML the builder writes"
CLASS = re.compile(r"\.([A-Za-z_][\w-]*)")
COMMENT = re.compile(r"/\*.*?\*/", re.S)


def contract_classes(text):
    """Every class of the contract's table, in order, without duplicates.
    A cell token like `--warning` completes the block of the class before
    it that has a modifier: `.callout--info`, `--warning` -> callout--warning."""
    if SECTION not in text:
        raise ValueError(f'no "{SECTION}" section')
    rows = text.split(SECTION, 1)[1].split("\n## ", 1)[0].splitlines()
    out, block = [], None
    for row in rows:
        if not row.startswith("| ") or row.startswith("|---"):
            continue
        first = row.split("|")[1]
        for token in re.findall(r"`([^`]+)`", first):
            if token.startswith("--"):
                if block is None:
                    raise ValueError(f"modifier {token} has no class before it")
                names = [block + token]
            else:
                names = CLASS.findall(token)
                for name in names:
                    if "--" in name:
                        block = name.split("--", 1)[0]
            for name in names:
                if name not in out:
                    out.append(name)
    if not out:
        raise ValueError("the table lists no class")
    return out


def missing(css, classes):
    """The classes that no selector of `css` names."""
    css = COMMENT.sub("", css)
    return [c for c in classes
            if not re.search(r"\." + re.escape(c) + r"(?![\w-])", css)]


def main(argv):
    if len(argv) != 3:
        print("usage: check-theme.py STYLE_CSS THEME_MD", file=sys.stderr)
        return 2
    try:
        with open(argv[2], encoding="utf-8") as f:
            classes = contract_classes(f.read())
        with open(argv[1], encoding="utf-8") as f:
            css = f.read()
    except (OSError, ValueError) as e:
        print(f"error: check-theme: {e}", file=sys.stderr)
        return 2
    gone = missing(css, classes)
    for name in gone:
        print(f"error: {argv[1]}: .{name} is written by tilder and not styled. "
              f"Add a rule for it (docs/theme.md)", file=sys.stderr)
    if not gone:
        print(f"theme: {len(classes)} classes of the contract, all styled")
    return 1 if gone else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

`chmod +x tools/check-theme.py`.

- [ ] **Step 5: Run the tests**

Run: `python3 -m unittest tests.test_check_theme -v`
Expected: 8 tests, OK. Also: `python3 tools/check-theme.py /home/theau/Git/tilder/starter/theme/style.css tools/tilder-theme.md; echo $?` prints the starter's unstyled classes (`.cursor`, `.members`...) and `1`: the check has teeth.

- [ ] **Step 6: Commit**

```bash
git add .gitignore tools/check-theme.py tools/tilder-theme.md tests/__init__.py tests/helpers.py tests/test_check_theme.py
git commit -m "feat: check that a theme styles every class of tilder's contract"
```

---

### Task 2: The contrast check (`tools/check-contrast.py`)

**Files:**
- Create: `tools/check-contrast.py`, `tests/test_check_contrast.py`

**Interfaces:**
- Consumes: `tests.helpers.load_tool`.
- Produces: `tokens(css: str) -> {"light": {name: value}, "dark": {...}}` (raises `ValueError`), `luminance(hex) -> float`, `ratio(a_hex, b_hex) -> float`, `results(schemes) -> list[(scheme, fg, bg, ratio, minimum)]` (raises `ValueError` on a missing or non-`#rrggbb` token), `markdown(rows) -> str`, `PAIRS` (fg in `text muted faint accent info warning error` × bg in `bg surface`, minimum 4.5), `main(argv) -> int`. CLI: `python3 tools/check-contrast.py STYLE_CSS [--markdown]`. The token names are the stylesheet's contract from Task 4: `--bg --surface --text --muted --faint --rule --accent --info --warning --error`.

- [ ] **Step 1: Write the failing tests**

`tests/test_check_contrast.py`:

```python
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
```

- [ ] **Step 2: Run them to see them fail**

Run: `python3 -m unittest tests.test_check_contrast -v`
Expected: ERROR, `FileNotFoundError` for `tools/check-contrast.py`.

- [ ] **Step 3: Write `tools/check-contrast.py`**

```python
#!/usr/bin/env python3
"""Check the WCAG contrast of a theme's colour tokens, light and dark.

The tokens are the custom properties of the first `:root { }` block of
style.css (light) and of the `:root { }` block inside
`@media (prefers-color-scheme: dark)` (dark). Colours are #rrggbb.

    python3 tools/check-contrast.py theme/style.css            # check
    python3 tools/check-contrast.py theme/style.css --markdown # the README table

Exit 0 when every pair reaches its minimum, 1 otherwise, 2 when the
tokens cannot be read.
"""

import re
import sys

# (foreground, background, minimum): text is 4.5:1 (WCAG 1.4.3); the
# accent is also the focus outline, and is text (links) too.
PAIRS = [(fg, bg, 4.5)
         for fg in ("text", "muted", "faint", "accent", "info", "warning", "error")
         for bg in ("bg", "surface")]
TOKEN = re.compile(r"--([\w-]+)\s*:\s*([^;]+);")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def _block(css, start):
    """The text between the brace that opens at `start` and its match."""
    depth, i = 0, css.index("{", start)
    for j in range(i, len(css)):
        depth += {"{": 1, "}": -1}.get(css[j], 0)
        if depth == 0:
            return css[i + 1:j]
    raise ValueError("unbalanced braces")


def tokens(css):
    """{"light": {name: "#rrggbb"}, "dark": {...}} from style.css."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    media = re.search(r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)", css)
    if not media:
        raise ValueError("no @media (prefers-color-scheme: dark) block")
    root = re.search(r":root\s*\{", css)
    if not root or root.start() > media.start():
        raise ValueError("no :root { } block before the dark scheme")
    dark_root = re.search(r":root\s*\{", _block(css, media.start()))
    if not dark_root:
        raise ValueError("no :root { } block in the dark scheme")
    light = dict(TOKEN.findall(_block(css, root.start())))
    dark = dict(TOKEN.findall(_block(_block(css, media.start()), dark_root.start())))
    return {"light": light, "dark": dark}


def luminance(hex_colour):
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def results(schemes):
    """[(scheme, fg, bg, ratio, minimum)], or ValueError on a missing or
    malformed token."""
    out = []
    for scheme in ("light", "dark"):
        t = schemes[scheme]
        for fg, bg, minimum in PAIRS:
            for name in (fg, bg):
                value = t.get(name, "").strip()
                if not HEX.match(value):
                    raise ValueError(f"{scheme}: --{name} must be #rrggbb, not {value or 'missing'}")
            out.append((scheme, fg, bg, ratio(t[fg].strip(), t[bg].strip()), minimum))
    return out


def markdown(rows):
    lines = ["| scheme | foreground | background | ratio | minimum |",
             "|---|---|---|---:|---:|"]
    lines += [f"| {s} | `--{fg}` | `--{bg}` | {r:.2f} | {m} |" for s, fg, bg, r, m in rows]
    return "\n".join(lines)


def main(argv):
    args = [a for a in argv[1:] if a != "--markdown"]
    if len(args) != 1:
        print("usage: check-contrast.py STYLE_CSS [--markdown]", file=sys.stderr)
        return 2
    try:
        with open(args[0], encoding="utf-8") as f:
            rows = results(tokens(f.read()))
    except (OSError, ValueError) as e:
        print(f"error: check-contrast: {e}", file=sys.stderr)
        return 2
    if "--markdown" in argv:
        print(markdown(rows))
    low = [r for r in rows if r[3] < r[4]]
    for s, fg, bg, r, m in low:
        print(f"error: {args[0]}: {s}: --{fg} on --{bg} is {r:.2f}:1, below {m}:1. "
              f"Darken or lighten one of them", file=sys.stderr)
    if not low and "--markdown" not in argv:
        print(f"contrast: {len(rows)} pairs, all at or above their minimum")
    return 1 if low else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

`chmod +x tools/check-contrast.py`.

- [ ] **Step 4: Run the tests**

Run: `python3 -m unittest tests.test_check_contrast -v`
Expected: 9 tests, OK.

- [ ] **Step 5: Commit**

```bash
git add tools/check-contrast.py tests/test_check_contrast.py
git commit -m "feat: check the WCAG contrast of a theme's colour tokens"
```

---

### Task 3: Self-hosted fonts

**Files:**
- Create: `theme/fonts/inter-regular.woff2`, `inter-italic.woff2`, `inter-bold.woff2`, `jetbrains-mono-regular.woff2`, `jetbrains-mono-bold.woff2`, `theme/fonts/OFL-Inter.txt`, `theme/fonts/OFL-JetBrainsMono.txt`, `theme/style.css` (its fonts section only; Task 4 writes the rest), `tests/test_fonts.py`

**Interfaces:**
- Consumes: `tests.helpers.THEME`.
- Produces: the families `"Inter"` (400, 400 italic, 700) and `"JetBrains Mono"` (400, 700), declared in `theme/style.css`; the file names above, which `layout.html` preloads (`fonts/inter-regular.woff2`) and `share.svg` uses by family name.

- [ ] **Step 1: Write the failing test**

`tests/test_fonts.py`:

```python
import re
import unittest

from tests.helpers import THEME

CSS = THEME / "style.css"
FACES = re.compile(r"@font-face\s*\{(.*?)\}", re.S)


class Fonts(unittest.TestCase):
    def faces(self):
        return FACES.findall(CSS.read_text())

    def test_five_faces_two_families(self):
        faces = self.faces()
        self.assertEqual(len(faces), 5)
        families = {re.search(r'font-family:\s*"([^"]+)"', f).group(1) for f in faces}
        self.assertEqual(families, {"Inter", "JetBrains Mono"})

    def test_every_face_is_a_self_hosted_subset_woff2(self):
        for face in self.faces():
            url = re.search(r'url\("([^"]+)"\)', face).group(1)
            self.assertTrue(url.startswith("fonts/"), url)
            data = (THEME / url).read_bytes()
            self.assertEqual(data[:4], b"wOF2", url)
            self.assertLess(len(data), 100_000, f"{url}: not a latin subset?")
            self.assertIn("font-display: swap", face)

    def test_each_family_ships_its_licence(self):
        for name in ("OFL-Inter.txt", "OFL-JetBrainsMono.txt"):
            text = (THEME / "fonts" / name).read_text()
            self.assertIn("SIL Open Font License", text)

    def test_nothing_is_loaded_from_another_host(self):
        self.assertIsNone(re.search(r"url\(\s*[\"']?(https?:)?//", CSS.read_text()))
```

- [ ] **Step 2: Run it to see it fail**

Run: `python3 -m unittest tests.test_fonts -v`
Expected: ERROR, `FileNotFoundError` for `theme/style.css`.

- [ ] **Step 3: Download the official releases and subset them**

Only upstream releases; fonttools lives in a throwaway venv, never in the site (no runtime dependency). Verified on 2026-09-27: both archives hold the paths below, and neither licence declares a Reserved Font Name (so modified subsets may keep their names; if a future release declares one, ship the unmodified upstream woff2 instead and raise the size limit of the test).

```bash
cd /home/theau/Git/tilder-website
work=$(mktemp -d)
curl -sSLo "$work/jbm.zip" https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip
curl -sSLo "$work/inter.zip" https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip
unzip -oq "$work/jbm.zip" -d "$work" OFL.txt fonts/webfonts/JetBrainsMono-Regular.woff2 fonts/webfonts/JetBrainsMono-Bold.woff2
unzip -oq "$work/inter.zip" -d "$work" LICENSE.txt web/Inter-Regular.woff2 web/Inter-Italic.woff2 web/Inter-Bold.woff2
grep -n 'with Reserved Font Name' "$work/OFL.txt" "$work/LICENSE.txt"; echo "(expected: nothing)"
python3 -m venv "$work/venv" && "$work/venv/bin/pip" install -q fonttools brotli
ranges="U+0000-024F,U+0259,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0300-036F,U+1E00-1EFF,U+2000-206F,U+20A0-20C0,U+2100-214F,U+2190-21FF,U+2212,U+2215,U+2500-257F,U+25A0-25FF,U+FEFF,U+FFFD"
mkdir -p theme/fonts
for pair in "web/Inter-Regular.woff2 inter-regular" "web/Inter-Italic.woff2 inter-italic" \
            "web/Inter-Bold.woff2 inter-bold" \
            "fonts/webfonts/JetBrainsMono-Regular.woff2 jetbrains-mono-regular" \
            "fonts/webfonts/JetBrainsMono-Bold.woff2 jetbrains-mono-bold"; do
  set -- $pair
  "$work/venv/bin/pyftsubset" "$work/$1" --unicodes="$ranges" --layout-features='*' \
    --flavor=woff2 --output-file="theme/fonts/$2.woff2"
done
cp "$work/LICENSE.txt" theme/fonts/OFL-Inter.txt
cp "$work/OFL.txt" theme/fonts/OFL-JetBrainsMono.txt
ls -l theme/fonts   # five woff2 of about 50-63 KB, two licences
rm -rf "$work"
```

- [ ] **Step 4: Declare the faces**

`theme/style.css` (Task 4 replaces the whole file with its full version, which keeps this section unchanged):

```css
/* The documentation theme. A man page for every page but the landing
   page, which is airier. It styles every class tilder writes (tilder
   docs/theme.md; tools/check-theme.py checks it at every build), and the
   theme's own: the page frame, the home and doc layouts, the search, the
   copy button.

   Contents: fonts - tokens - base - frame (header, footer) - sections and
   blocks - entries and cards - code - collection navigation - home - doc
   layout - search - copy button - motion. */

/* --- fonts: self-hosted, OFL (fonts/OFL-*.txt) ---------------------------- */

@font-face { font-family: "Inter"; font-style: normal; font-weight: 400; font-display: swap;
	src: url("fonts/inter-regular.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: italic; font-weight: 400; font-display: swap;
	src: url("fonts/inter-italic.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: normal; font-weight: 700; font-display: swap;
	src: url("fonts/inter-bold.woff2") format("woff2"); }
@font-face { font-family: "JetBrains Mono"; font-style: normal; font-weight: 400; font-display: swap;
	src: url("fonts/jetbrains-mono-regular.woff2") format("woff2"); }
@font-face { font-family: "JetBrains Mono"; font-style: normal; font-weight: 700; font-display: swap;
	src: url("fonts/jetbrains-mono-bold.woff2") format("woff2"); }
```

- [ ] **Step 5: Run the test**

Run: `python3 -m unittest tests.test_fonts -v`
Expected: 4 tests, OK.

- [ ] **Step 6: Commit**

```bash
git add theme/fonts theme/style.css tests/test_fonts.py
git commit -m "feat(theme): self-hosted Inter and JetBrains Mono, latin subsets, OFL"
```

---

### Task 4: The stylesheet

**Files:**
- Modify: `theme/style.css` (the whole file, below)
- Create: `tests/test_style.py`

**Interfaces:**
- Consumes: `load_tool("check-theme")`, `load_tool("check-contrast")`, `tools/tilder-theme.md`.
- Produces: the colour tokens `--bg --surface --text --muted --faint --rule --accent --info --warning --error` (light on `:root`, dark on `:root` inside `@media (prefers-color-scheme: dark)`), `--mono`, `--sans`, `--measure`, `--gutter`; and the theme's own classes that later tasks write in markup: `page`, `page--wide`, `page--home`, `manline`, `manline--head`, `manline--foot`, `bar`, `tagline`, `skip`, `to-top`, `pager` (layouts, Task 7); `home`, `home-tagline`, `doc`, `doc--toc`, `doc-side`, `doc-main`, `doc-toc`, `doc-toc-label` (Task 8); `doc-search`, `doc-search-label`, `doc-search-input`, `doc-search-status`, `doc-search-results` (Task 10); `code-box`, `code-copy` (Task 11); `entry--group` (Task 5's `{docs}`), `entry--example` (Resolution 3).

- [ ] **Step 1: Write the failing tests**

`tests/test_style.py`:

```python
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
```

- [ ] **Step 2: Run them to see them fail**

Run: `python3 -m unittest tests.test_style -v`
Expected: FAIL: the contract classes are missing (`['sr-only', 'wordmark', ...]`), and ERROR in the contrast test (`ValueError: no @media (prefers-color-scheme: dark) block`).

- [ ] **Step 3: Write the stylesheet**

Replace `theme/style.css` with (the fonts section is Task 3's, unchanged). Layout notes for the reviewer: sections are the man page's grid, name in an `11ch` gutter, body at most `75ch`; the doc layout is `15rem | text` from 45rem, `15rem | text | 13rem` from 60rem when `nav.js` has moved a `[TOC]` (`.doc--toc`), one column below 45rem with the sidebar a bordered `<details>`; the home layout drops the gutter and hides the hero section's `<h2>` visually (it stays for screen readers).

```css
/* The documentation theme. A man page for every page but the landing
   page, which is airier. It styles every class tilder writes (tilder
   docs/theme.md; tools/check-theme.py checks it at every build), and the
   theme's own: the page frame, the home and doc layouts, the search, the
   copy button.

   Contents: fonts - tokens - base - frame (header, footer) - sections and
   blocks - entries and cards - code - collection navigation - home - doc
   layout - search - copy button - motion. */

/* --- fonts: self-hosted, OFL (fonts/OFL-*.txt) ---------------------------- */

@font-face { font-family: "Inter"; font-style: normal; font-weight: 400; font-display: swap;
	src: url("fonts/inter-regular.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: italic; font-weight: 400; font-display: swap;
	src: url("fonts/inter-italic.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: normal; font-weight: 700; font-display: swap;
	src: url("fonts/inter-bold.woff2") format("woff2"); }
@font-face { font-family: "JetBrains Mono"; font-style: normal; font-weight: 400; font-display: swap;
	src: url("fonts/jetbrains-mono-regular.woff2") format("woff2"); }
@font-face { font-family: "JetBrains Mono"; font-style: normal; font-weight: 700; font-display: swap;
	src: url("fonts/jetbrains-mono-bold.woff2") format("woff2"); }

/* --- tokens: every colour of the theme; tools/check-contrast.py checks the
   pairs (README.md, "Contrast"). #rrggbb only. -------------------------- */

:root {
	--bg: #fcfcfa; --surface: #f0f0ec; --text: #1c1e21; --muted: #4f565d;
	--faint: #5c636a; --rule: #d4d4cd; --accent: #00707e;
	--info: #00707e; --warning: #8a5200; --error: #b3261e;
	--mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
	--sans: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
	--measure: 75ch;         /* the text column, like the text mirror */
	--gutter: 11ch;          /* a section's name, on wide screens */
	color-scheme: light dark;
}
@media (prefers-color-scheme: dark) {
	:root {
		--bg: #121417; --surface: #1c1f23; --text: #e3e5e8; --muted: #a9afb6;
		--faint: #939aa1; --rule: #343a40; --accent: #4cc9d6;
		--info: #4cc9d6; --warning: #e5ad4f; --error: #ff8f85;
	}
}

/* --- base ------------------------------------------------------------------ */

* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--text);
	font: 1rem/1.65 var(--sans); }
a { color: var(--accent); text-underline-offset: 0.15em; }
a:hover { text-decoration-thickness: 2px; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
b, strong { font-weight: 700; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 2rem 0; }
p, ul, ol { margin: 0 0 1.1rem; }
ul, ol { padding-left: 2.5ch; }
img { max-width: 100%; height: auto; }

/* Required: read by screen readers, not shown. */
.sr-only { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0;
	overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0; }
.skip { position: absolute; left: -9999px; }
.skip:focus { position: static; display: inline-block; margin: 0.5rem 0; }

/* --- the frame: the man-page rules, the wordmark, the navigation ----------- */

.page { max-width: calc(var(--measure) + var(--gutter) + 4rem); margin: 0 auto;
	padding: 1.5rem 1.25rem 3rem; }
.page--wide { max-width: 90rem; }
.manline { display: flex; justify-content: space-between; gap: 1ch;
	font: 0.75rem/1.4 var(--mono); color: var(--muted); text-transform: uppercase; }
.manline > span:nth-child(2) { text-align: center; }
.manline--head { border-bottom: 1px solid var(--rule); padding-bottom: 0.6rem; }
.manline--foot { border-top: 1px solid var(--rule); padding-top: 0.6rem; margin-top: 3rem; }
.manline a { color: inherit; }
.bar { display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.5rem 2rem; margin: 1.5rem 0 0.3rem; }
.wordmark { font: 700 1.5rem/1.2 var(--mono); text-transform: lowercase; margin: 0; }
.wordmark a { color: inherit; text-decoration: none; }
.wordmark a:hover { text-decoration: underline; }
.wordmark .tilde { color: var(--accent); }
.wordmark .slash { color: var(--muted); font-weight: 400; }
.wordmark .here { text-transform: none; }
.wordmark .cursor { display: inline-block; width: 0.55em; height: 1em; margin-left: 0.1em;
	vertical-align: -0.12em; background: var(--accent); animation: blink 1.2s steps(1) infinite; }
@keyframes blink { 50% { opacity: 0; } }
.nav { font: 0.9rem var(--mono); }
.nav a { text-decoration: none; }
.nav a:hover { text-decoration: underline; }
.nav a[aria-current="page"] { color: var(--text); font-weight: 700; }
.nav .sep { color: var(--muted); padding: 0 0.6ch; }
.languages { font: 0.85rem var(--mono); margin-left: auto; }
.languages a { margin-left: 1ch; text-decoration: none; }
.languages a[aria-current="page"] { color: var(--text); font-weight: 700; }
.tagline { font: 0.85rem var(--mono); color: var(--muted); margin: 0 0 2.5rem; }
.to-top { font: 0.8rem var(--mono); text-align: right; margin: 3rem 0 0; }

/* --- sections: the name in a gutter, like a man page ----------------------- */

.s { display: grid; grid-template-columns: var(--gutter) minmax(0, var(--measure));
	gap: 0 1.5rem; margin: 0 0 2.5rem; }
.s > h2 { font: 700 0.8rem/1.6 var(--mono); text-transform: uppercase; letter-spacing: 0.12em;
	color: var(--muted); margin: 0.15rem 0 0; overflow-wrap: anywhere; }
.b > :last-child { margin-bottom: 0; }
.b.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
	gap: 1rem; align-items: start; }
.members, .posts, .upcoming, .past, .next-event { min-width: 0; }   /* list markers */
@media (max-width: 40rem) {
	.s { grid-template-columns: minmax(0, 1fr); }
	.s > h2 { margin-bottom: 0.6rem; }
}

.mono { font-family: var(--mono); font-size: 0.92em; }
.small { font-size: 0.85rem; }
.muted { color: var(--muted); }
.faint { color: var(--faint); }
.warn { color: var(--warning); }
.empty { font: 0.9rem var(--mono); color: var(--muted); }
u.u { text-decoration: underline dotted; text-underline-offset: 0.2em; }
del { color: var(--muted); }

/* Boxes. An inset frames a live example (the page writes its label). */
.inset { border: 1px dashed var(--muted); padding: 1rem 1.2rem; margin: 0 0 1.1rem; }
.inset > :last-child { margin-bottom: 0; }
.callout { --kind: var(--info); border-left: 3px solid var(--kind); background: var(--surface);
	padding: 0.8rem 1.1rem; margin: 0 0 1.1rem; }
.callout--info { --kind: var(--info); }
.callout--warning { --kind: var(--warning); }
.callout--error { --kind: var(--error); }
.callout > :last-child { margin-bottom: 0; }
.callout-label { font: 700 0.75rem var(--mono); letter-spacing: 0.08em; color: var(--kind);
	margin: 0 0 0.3rem; }

/* Tables: the wrapper scrolls, the page does not. */
.table { overflow-x: auto; margin: 0 0 1.1rem; }
table { border-collapse: collapse; font-size: 0.95rem; }
th, td { text-align: left; vertical-align: top; padding: 0.35rem 2ch 0.35rem 0;
	border-bottom: 1px solid var(--rule); }
th { font: 700 0.8rem var(--mono); color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
th.center, td.center { text-align: center; }
th.right, td.right { text-align: right; }

.tasks { list-style: none; padding-left: 0; }
.task { display: inline-block; width: 0.85em; height: 0.85em; border: 1px solid var(--muted);
	margin-right: 0.8ch; vertical-align: -0.05em; }
.task--done { background: var(--accent); border-color: var(--accent); }
.task--todo { background: transparent; }
.figure { margin: 1.5rem 0; }
.figure img { display: block; }
.figure figcaption { font-size: 0.85rem; color: var(--muted); margin-top: 0.4rem; }
.toc { font: 0.9rem var(--mono); border-left: 1px solid var(--rule); padding-left: 1rem; margin: 0 0 1.5rem; }
.toc-label { cursor: pointer; color: var(--muted); font-weight: 700; text-transform: uppercase;
	letter-spacing: 0.08em; font-size: 0.75rem; }
.toc ol { margin: 0.5rem 0 0; padding-left: 3ch; }

/* --- entries and cards ----------------------------------------------------- */

.entry { border-top: 1px solid var(--rule); padding: 1.1rem 0; }
.entry:first-child { border-top: 0; padding-top: 0; }
.entry h3 { font: 700 1rem/1.4 var(--mono); margin: 0 0 0.35rem; }
.entry > :last-child { margin-bottom: 0; }
.entry--link { position: relative; }
.entry--link h3 a { text-decoration: none; }
.entry--link h3 a::after { content: ""; position: absolute; inset: 0; }
.entry--link:hover h3 a { text-decoration: underline; }
.entry--next h3 { color: var(--accent); }
.entry--full h3 { color: var(--muted); }
.entry--group { margin-top: 1.5rem; }
/* A live example of a block construct: `### Rendered {example}`, the
   construct indented under it (an inset holds paragraphs only). */
.b .entry--example { border: 1px dashed var(--muted); padding: 0.9rem 1.2rem; margin: 0 0 1.1rem; }
.entry--example h3 { font: 700 0.72rem var(--mono); color: var(--muted); text-transform: uppercase;
	letter-spacing: 0.1em; }
.b.grid .entry { border: 1px solid var(--rule); padding: 1rem 1.1rem; background: var(--bg); }
.b.grid .entry--link:hover { border-color: var(--accent); }
.meta { display: flex; flex-wrap: wrap; gap: 0.2rem 1ch; font: 0.8rem var(--mono);
	color: var(--muted); margin: 0 0 0.6rem; }
.meta > span + span:not(.tag)::before { content: "\00B7\00A0"; }
.tag { border: 1px solid var(--rule); padding: 0 0.6ch; }
.tag--next { color: var(--accent); border-color: var(--accent); }
.tag--full { color: var(--warning); border-color: var(--warning); }
.profiles { display: flex; flex-wrap: wrap; gap: 0.4rem 1rem; }
.profiles a { position: relative; z-index: 1; }
.icon { width: 1.1rem; height: 1.1rem; fill: currentColor; vertical-align: -0.15em; }

/* --- code ------------------------------------------------------------------ */

code, pre { font-family: var(--mono); font-size: 0.875rem; }
:not(pre) > code { background: var(--surface); padding: 0.05em 0.35ch; border-radius: 2px; }
pre { background: var(--surface); padding: 0.9rem 1rem; margin: 0 0 1.1rem; overflow-x: auto;
	line-height: 1.55; tab-size: 4; }
pre.code { position: relative; }
pre.code[data-lang]::before { content: attr(data-lang); position: absolute; top: 0.35rem; right: 0.75rem;
	font-size: 0.72rem; color: var(--muted); }
.hl-k, .hl-t { font-weight: 700; }
.hl-s, .hl-v, .hl-gi { color: var(--accent); }
.hl-c, .hl-p, .hl-gh { color: var(--muted); }
.hl-b, .hl-n { color: var(--warning); }
.hl-gd { color: var(--error); }

/* The copy button (code.js): the block is wrapped in .code-box. */
.code-box { position: relative; margin: 0 0 1.1rem; }
.code-box > pre.code { position: static; margin: 0; }
.code-copy { position: absolute; top: 0.3rem; right: 0.4rem; font: 0.75rem var(--mono);
	color: var(--text); background: var(--bg); border: 1px solid var(--rule); border-radius: 2px;
	padding: 0.1rem 0.8ch; cursor: pointer; opacity: 0; transition: opacity 0.15s; }
.code-box:hover .code-copy, .code-box:focus-within .code-copy { opacity: 1; }
@media (hover: none) {
	.code-copy { opacity: 1; }
	.code-box > pre.code[data-lang]::before { right: 6rem; }
}

/* --- a collection's order: the sidebar, previous and next ------------------ */

.collection-nav { font: 0.88rem/1.5 var(--mono); }
.collection-nav ul { list-style: none; padding-left: 0; margin: 0; }
.collection-nav li { margin: 0.2rem 0; }
.collection-nav a { text-decoration: none; color: var(--text); display: block;
	padding: 0.1rem 0 0.1rem 1ch; border-left: 2px solid transparent; }
.collection-nav a:hover { color: var(--accent); }
.collection-nav a[aria-current="page"] { color: var(--accent); font-weight: 700;
	border-left-color: var(--accent); }
.collection-group { margin-top: 1rem; }
.collection-group-label { display: block; font: 700 0.72rem var(--mono); color: var(--muted);
	text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 0.3rem; }
.pager { display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
	border-top: 1px solid var(--rule); padding-top: 1rem; margin-top: 2.5rem; font-family: var(--mono); }
.pager:empty { display: none; }
.prev, .next { text-decoration: none; }
.prev:hover, .next:hover { text-decoration: underline; }
.next { margin-left: auto; text-align: right; }
.prev-label, .next-label { display: block; font-size: 0.75rem; color: var(--muted);
	text-transform: uppercase; letter-spacing: 0.08em; }

/* --- home: the landing page, airier ---------------------------------------- */

.page--home { max-width: 72rem; }
.home { font-size: 1.05rem; }
.home .s { grid-template-columns: minmax(0, 1fr); margin: 0 0 4rem; }
.home .s > h2 { margin-bottom: 1rem; }
.home-tagline { font: 700 clamp(2rem, 5vw, 3.4rem)/1.1 var(--sans); letter-spacing: -0.02em;
	max-width: 20ch; margin: 1rem 0 1.5rem; }
.home > .s:first-of-type { margin-bottom: 5rem; }
.home > .s:first-of-type > h2 { position: absolute; width: 1px; height: 1px; overflow: hidden;
	clip-path: inset(50%); white-space: nowrap; }
.home > .s:first-of-type .b { font-size: clamp(1.1rem, 2.2vw, 1.35rem); color: var(--muted); max-width: 60ch; }
.home .b.grid { grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)); gap: 1.25rem; }
.home .b.grid > pre, .home .b.grid > .code-box { margin: 0; height: 100%; }
.home .b.grid .entry { padding: 1.4rem; }

/* --- doc: sidebar, text, contents ------------------------------------------ */

.doc { display: grid; grid-template-columns: 15rem minmax(0, 1fr); gap: 0 3rem; align-items: start; }
.doc-side { position: sticky; top: 1rem; max-height: calc(100vh - 2rem); overflow-y: auto;
	padding-right: 0.5rem; }
.doc-side > summary { display: none; }
.doc-main { min-width: 0; }
.doc-toc { position: sticky; top: 1rem; max-height: calc(100vh - 2rem); overflow-y: auto; }
.doc-toc-label { font: 700 0.72rem var(--mono); color: var(--muted); text-transform: uppercase;
	letter-spacing: 0.1em; margin: 0 0 0.5rem; }
.doc-toc .toc { border: 0; padding: 0; margin: 0; }
.doc-toc .toc-label { display: none; }
.doc-toc .toc ol { margin: 0; padding-left: 0; list-style: none; }
.doc-toc .toc li { margin: 0.25rem 0; }
.doc-toc .toc a { text-decoration: none; color: var(--muted); }
.doc-toc .toc a:hover { color: var(--accent); }
@media (min-width: 60rem) {
	.doc--toc { grid-template-columns: 15rem minmax(0, 1fr) 13rem; }
}
@media (max-width: 45rem) {
	.doc { display: block; }
	.doc-side { position: static; max-height: none; overflow: visible; padding: 0;
		border: 1px solid var(--rule); margin: 0 0 2rem; }
	.doc-side > summary { display: list-item; cursor: pointer; padding: 0.6rem 1rem;
		font: 700 0.8rem var(--mono); text-transform: uppercase; letter-spacing: 0.08em; }
	.doc-side[open] > summary { border-bottom: 1px solid var(--rule); }
	.doc-side > :not(summary) { margin: 1rem; }
}

/* --- search (search.js) ---------------------------------------------------- */

.doc-search { margin: 0 0 1.5rem; }
.doc-search-label { display: block; font: 700 0.72rem var(--mono); color: var(--muted);
	text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 0.3rem; }
.doc-search-input { width: 100%; font: 0.9rem var(--mono); color: var(--text); background: var(--bg);
	border: 1px solid var(--muted); border-radius: 2px; padding: 0.4rem 0.6rem; }
.doc-search-status { font: 0.75rem var(--mono); color: var(--muted); margin: 0.4rem 0 0; }
.doc-search-status:empty { display: none; }
.doc-search-results { list-style: none; padding: 0; margin: 0.4rem 0 0; font-size: 0.88rem; }
.doc-search-results li { margin: 0; }
.doc-search-results a { display: block; padding: 0.35rem 0.5rem; text-decoration: none;
	border-left: 2px solid transparent; }
.doc-search-results a span { display: block; color: var(--muted); font-size: 0.8rem; }
.doc-search-results [aria-selected="true"] a { border-left-color: var(--accent); background: var(--surface); }

/* --- motion ---------------------------------------------------------------- */

@media (prefers-reduced-motion: reduce) {
	*, *::before, *::after { animation: none !important; transition: none !important;
		scroll-behavior: auto !important; }
}
```

- [ ] **Step 4: Run the tests, and both tools by hand**

Run: `python3 -m unittest tests.test_style tests.test_fonts -v`
Expected: 8 tests, OK.
Run: `python3 tools/check-theme.py theme/style.css tools/tilder-theme.md && python3 tools/check-contrast.py theme/style.css`
Expected: `theme: 69 classes of the contract, all styled` and `contrast: 28 pairs, all at or above their minimum`.

- [ ] **Step 5: Commit**

```bash
git add theme/style.css tests/test_style.py
git commit -m "feat(theme): man-page stylesheet, every contract class, light and dark"
```

---

### Task 5: The `doc` type

**Files:**
- Modify: `tests/helpers.py` (whole file below: adds `STUB`, `STUBS`, `load_type`)
- Create: `theme/types/doc.py`, `tests/test_type_doc.py`

**Interfaces:**
- Consumes: from tilder, only what `docs/types.md` lets a type import: `paths.clean_url(html_path, lang=None) -> str`, `seo.org_ref() -> dict`, `seo.page_heading(meta) -> str`. In unit tests these are stand-ins (`tests.helpers.STUBS`); `STUB["prefix"]` sets the language prefix the stand-in `clean_url` uses (`""` or `"fr/"`).
- Produces: `theme/types/doc.py` with `NAME = "doc"`, `ARTICLE = SEQUENTIAL = LOCALIZED_OUTPUTS = True`, `LAYOUT = "doc"`, `SCRIPT = "search.js"`, `DEFAULTS = {"man": "SITE-DOCS(7)", "nav": "docs/", "empty": "No page yet.", "index": "search-index.json"}`, `TEXT_MAX = 2000`; `defaults(item, conf)` (sets `meta["search_index"] = f"{conf['dir']}/{conf['index']}"`, read by `layouts/doc.html` as `{{ page.search_index }}`), `order(item) -> int`, `sort_key(item, conf) -> (int, str)`, `entry(item, link, conf) -> dict | None`, `grouped(items) -> list`, `docs(items, conf) -> dict` (`MARKERS = {"docs": docs}`), `json_ld(item, conf) -> dict`, `headings(src: str) -> list[str]`, `plain(src: str) -> str`, `url(item) -> str`, `record(item) -> dict`, `outputs(items, conf) -> {f"{dir}/{index}": json_text}`. Index records: `{"t": title, "u": url from the language's landing page, "d": description, "h": [h2 titles], "x": plain text[:2000]}` — `search.js` (Task 10) reads exactly these keys. `tests.helpers.load_type(name) -> module`.

- [ ] **Step 1: Extend the helpers**

`tests/helpers.py`, whole file:

```python
"""What the theme's tests share: load a tool or a theme type as a module.
(Task 7 adds the fixture build.)"""

import importlib.util
import pathlib
import sys
import types

REPO = pathlib.Path(__file__).resolve().parent.parent
THEME = REPO / "theme"
FIXTURE = REPO / "tests" / "site"


def load_tool(name):
    """tools/<name>.py ("check-theme") as a module."""
    path = REPO / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# What the stand-ins below answer, changed by a test: the language prefix
# of the pass ("" or "fr/").
STUB = {"prefix": ""}


def _clean_url(html_path, lang=None):
    """tilder's paths.clean_url, for the stand-in: "/", "/fr/docs/start"."""
    n, p = html_path[:-5], STUB["prefix"]
    if n == "index":
        return "/" + p
    if n.endswith("/index"):
        return "/" + p + n[:-len("/index")] + "/"
    return "/" + p + n


STUBS = {
    "paths": types.SimpleNamespace(clean_url=_clean_url),
    "seo": types.SimpleNamespace(
        org_ref=lambda: {"@id": "https://docs.example/#organization"},
        site_ref=lambda: {"@id": "https://docs.example/#website"},
        page_heading=lambda meta: meta.get("name") or meta["title"],
        page_title=lambda meta: meta["title"] + " - fixture docs"),
}


def load_type(name):
    """theme/types/<name>.py as a module, with stand-ins for the tilder
    modules a type may import (paths, seo): the unit tests need no tilder."""
    saved = {k: sys.modules.get(k) for k in STUBS}
    sys.modules.update(STUBS)
    try:
        path = THEME / "types" / f"{name}.py"
        spec = importlib.util.spec_from_file_location(f"theme_type_{name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    return module
```

- [ ] **Step 2: Write the failing tests**

`tests/test_type_doc.py`:

````python
import json
import pathlib
import tempfile
import unittest

from tests.helpers import STUB, load_type

doc = load_type("doc")

SOURCE = """---
title: Getting started
description: The first page.
order: 10
---

<!-- TO FILL: a note for editors, not for readers. -->

## Name {#name}

getting started - the **first** page, with _emphasis_ and `code` {mono}

[TOC]

## Install {html}

Read the [cli](docs/cli) page, then:

```sh
## not a heading
echo "not in the text"
```

- [x] a task
> [!WARNING]
> Mind the Élan.

### An entry, not a section

| a | b |
|---|---|
| cell | other |
"""


def item(slug, src=None, **meta):
    meta.setdefault("title", slug.title())
    return {"slug": slug, "meta": meta, "path": f"docs/{slug}.html", "src": src}


class Attributes(unittest.TestCase):
    def test_the_type_s_contract(self):
        self.assertEqual(doc.NAME, "doc")
        self.assertTrue(doc.ARTICLE)
        self.assertTrue(doc.SEQUENTIAL)
        self.assertTrue(doc.LOCALIZED_OUTPUTS)
        self.assertEqual(doc.LAYOUT, "doc")
        self.assertEqual(doc.SCRIPT, "search.js")
        self.assertEqual(doc.DEFAULTS, {"man": "SITE-DOCS(7)", "nav": "docs/",
                                        "empty": "No page yet.", "index": "search-index.json"})


class Defaults(unittest.TestCase):
    def test_fills_man_nav_and_the_search_index_path(self):
        it = item("start")
        doc.defaults(it, dict(doc.DEFAULTS, dir="manual"))
        self.assertEqual(it["meta"]["man"], "SITE-DOCS(7)")
        self.assertEqual(it["meta"]["nav"], "docs/")
        self.assertEqual(it["meta"]["search_index"], "manual/search-index.json")

    def test_keeps_what_the_front_matter_says(self):
        it = item("start", man="MINE(1)")
        doc.defaults(it, dict(doc.DEFAULTS, dir="docs"))
        self.assertEqual(it["meta"]["man"], "MINE(1)")


class Order(unittest.TestCase):
    def test_order_then_slug_default_1000(self):
        its = [item("b"), item("a", order="20"), item("c", order="5"), item("a2")]
        its.sort(key=lambda it: doc.sort_key(it, {}))
        self.assertEqual([it["slug"] for it in its], ["c", "a", "a2", "b"])

    def test_an_order_that_is_not_a_number_says_so(self):
        with self.assertRaisesRegex(ValueError, 'order must be a whole number, not "first"'):
            doc.sort_key(item("a", order="first"), {})


class Entry(unittest.TestCase):
    def test_a_card_in_a_list(self):
        node = doc.entry(item("cli", description="Options.", group="Reference"), True, {})
        self.assertEqual(node["title"], "[Cli](docs/cli)")
        self.assertEqual(node["meta"], ["Reference"])
        self.assertEqual(node["cls"], ["link"])
        self.assertEqual(node["blocks"], [{"k": "para", "text": "Options.", "cls": []}])

    def test_no_card_on_its_own_page(self):
        self.assertIsNone(doc.entry(item("cli"), False, {}))


class Marker(unittest.TestCase):
    def test_docs_lists_grouped_and_marks_each_group_s_first_card(self):
        its = [item("a"), item("b", group="Ref"), item("c", group="Guide"),
               item("d"), item("e", group="Ref")]
        out = doc.MARKERS["docs"](its, {"empty": "No page yet."})
        self.assertEqual([(it["slug"], cls) for it, cls in out["items"]],
                         [("a", []), ("d", []), ("b", ["group"]), ("e", []), ("c", ["group"])])
        self.assertEqual(out["empty"], "No page yet.")


class JsonLd(unittest.TestCase):
    def test_tech_article(self):
        node = doc.json_ld(item("cli", description="Options."), {})
        self.assertEqual(node["@type"], "TechArticle")
        self.assertEqual(node["headline"], "Cli")
        self.assertEqual(node["description"], "Options.")
        self.assertEqual(node["publisher"], {"@id": "https://docs.example/#organization"})


class Index(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.src = pathlib.Path(self.tmp.name, "start.md")
        self.src.write_text(SOURCE, encoding="utf-8")
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(STUB.update, prefix="")

    def test_headings_are_the_h2_titles_without_markers_or_code(self):
        self.assertEqual(doc.headings(SOURCE), ["Name", "Install"])

    def test_plain_keeps_the_words_only(self):
        text = doc.plain(SOURCE)
        for word in ("getting started", "first", "emphasis", "code", "Read the cli page",
                     "a task", "Mind the Élan", "An entry, not a section", "cell"):
            self.assertIn(word, text)
        for noise in ("title:", "TO FILL", "{mono}", "{#name}", "docs/cli", "[TOC]",
                      "not a heading", "echo", "**", "_emphasis_", "[x]", "[!WARNING]",
                      "|", "---", "###"):
            self.assertNotIn(noise, text)

    def test_outputs_one_index_under_the_collection_s_folder(self):
        its = [item("start", self.src, title="Getting started", description="The first page.")]
        files = doc.outputs(its, dict(doc.DEFAULTS, dir="docs"))
        self.assertEqual(list(files), ["docs/search-index.json"])
        data = json.loads(files["docs/search-index.json"])
        self.assertEqual(data, [{"t": "Getting started", "u": "docs/start",
                                 "d": "The first page.", "h": ["Name", "Install"],
                                 "x": doc.plain(SOURCE)}])

    def test_the_url_is_from_the_language_s_landing_page(self):
        STUB["prefix"] = "fr/"
        self.assertEqual(doc.url(item("start")), "docs/start")

    def test_the_text_is_cut_at_2000_characters(self):
        self.src.write_text("---\ntitle: Long\n---\n\n## Name\n\n" + "word " * 1000)
        data = json.loads(doc.outputs([item("start", self.src)], dict(doc.DEFAULTS, dir="docs"))
                          ["docs/search-index.json"])
        self.assertEqual(len(data[0]["x"]), 2000)
````

- [ ] **Step 3: Run them to see them fail**

Run: `python3 -m unittest tests.test_type_doc -v`
Expected: ERROR, `FileNotFoundError` for `theme/types/doc.py`.

- [ ] **Step 4: Write the type**

`theme/types/doc.py` (no `__init__.py` in `theme/types/`, ever — tilder imports each file on its own):

```python
"""Documentation pages: one page of a manual, in order, grouped, with prev/
next links, a sidebar, and a search index per language. A theme type
(tilder docs/types.md)."""

import json
import re

from paths import clean_url
from seo import org_ref, page_heading

NAME = "doc"
ARTICLE = True
SEQUENTIAL = True           # previous/next line in the text mirror
LOCALIZED_OUTPUTS = True    # one search index per language, fr/docs/...
LAYOUT = "doc"
SCRIPT = "search.js"        # pages that list docs; doc.html links it itself
DEFAULTS = {
    "man": "SITE-DOCS(7)",          # items' man-page name, unless one sets its own
    "nav": "docs/",                 # items' nav entry
    "empty": "No page yet.",        # a {docs} list with nothing in it
    "index": "search-index.json",   # the search index, in the collection's folder
}
TEXT_MAX = 2000                     # characters of body text per page in the index


def defaults(item, conf):
    meta = item["meta"]
    meta.setdefault("man", conf["man"])
    meta.setdefault("nav", conf["nav"])
    meta.setdefault("tagline", "")
    meta.setdefault("description", "")
    # The layout's search field reads it: {{ page.search_index }}.
    meta.setdefault("search_index", f"{conf['dir']}/{conf['index']}")


def order(item):
    value = item["meta"].get("order", "1000")
    try:
        return int(value)
    except ValueError:
        raise ValueError(f'order must be a whole number, not "{value}"') from None


def sort_key(item, conf):
    return (order(item), item["slug"])


def entry(item, link, conf):
    """The card: the title, the group, the description. None on the page
    itself: a documentation page shows no card of its own."""
    if not link:
        return None
    meta = item["meta"]
    blocks = [{"k": "para", "text": meta["description"], "cls": []}] if meta.get("description") else []
    return {"k": "entry", "id": None, "cls": ["link"],
            "title": f"[{meta['title']}]({item['path'][:-5]})",
            "meta": [meta["group"]] if meta.get("group") else [],
            "blocks": blocks, "own": False}


def grouped(items):
    """The items, the ungrouped first, then each group in the order of its
    first item: the sidebar's order ({{ collection_nav }})."""
    loose, named = [], {}
    for it in items:
        g = it["meta"].get("group") or ""
        (named.setdefault(g, []) if g else loose).append(it)
    return loose + [it for its in named.values() for it in its]


def docs(items, conf):
    """{docs}: every page, grouped; the first card of a group is marked
    (entry--group) so the theme can space the groups apart."""
    out, seen = [], set()
    for it in grouped(items):
        g = it["meta"].get("group") or ""
        out.append((it, ["group"] if g and g not in seen else []))
        seen.add(g)
    return {"items": out, "empty": conf.get("empty", "")}


MARKERS = {"docs": docs}


def json_ld(item, conf):
    meta = item["meta"]
    return {"@type": "TechArticle", "headline": page_heading(meta),
            "description": meta["description"], "publisher": org_ref()}


# --- the search index ---------------------------------------------------------

FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
FENCE = re.compile(r"^(`{3,})[^\n]*\n.*?^\1`*[ \t]*$", re.S | re.M)
COMMENT = re.compile(r"<!--.*?-->", re.S)
MARKERS_RE = re.compile(r"\s*\{[^}\n]*\}[ \t]*$", re.M)
LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
H2 = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)


def headings(src):
    """The ## titles, markers removed, outside code blocks."""
    body = FENCE.sub("", FRONT.sub("", src, count=1))
    return [MARKERS_RE.sub("", h).strip() for h in H2.findall(body)]


def plain(src):
    """The words of a Markdown source: no front matter, code blocks,
    comments, markers, link targets or punctuation of the syntax. The
    builder's parser is not a type's to import (docs/types.md)."""
    text = FENCE.sub(" ", FRONT.sub("", src, count=1))
    text = COMMENT.sub(" ", text)
    text = MARKERS_RE.sub("", text)
    text = LINK.sub(r"\1", text)
    text = re.sub(r"^\s*\[TOC\]\s*$", " ", text, flags=re.M | re.I)
    text = re.sub(r"^[ \t]*(#{2,3}|>|[-*]|\d+[.)])[ \t]+(\[[ xX]\][ \t]+)?", "", text, flags=re.M)
    text = re.sub(r"^[ \t]*\[!\w+\][ \t]*", "", text, flags=re.M)
    text = re.sub(r"^\s*\|?[-:| ]+\|?\s*$", " ", text, flags=re.M)   # table rules
    text = re.sub(r"(\*\*|\+\+|~~|`|\*|\|)", " ", text)
    text = re.sub(r"(?<!\w)_|_(?!\w)", " ", text)
    return " ".join(text.split())


def url(item):
    """The page's clean URL from the language's landing page ("docs/start",
    not "/fr/docs/start"): search.js puts the layout's {{ home }} before it,
    so the links work under any prefix and from any page."""
    return clean_url(item["path"])[len(clean_url("index.html")):]


def record(item):
    src = item["src"].read_text(encoding="utf-8")
    meta = item["meta"]
    return {"t": meta["title"], "u": url(item), "d": meta.get("description", ""),
            "h": headings(src), "x": plain(src)[:TEXT_MAX]}


def outputs(items, conf):
    """The search index of the collection, in the language of the pass:
    {dir}/{index}, under the language's prefix (LOCALIZED_OUTPUTS)."""
    data = [record(it) for it in items]
    return {f"{conf['dir']}/{conf['index']}":
            json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"}
```

- [ ] **Step 5: Run the tests**

Run: `python3 -m unittest tests.test_type_doc -v`
Expected: 14 tests, OK.

- [ ] **Step 6: Commit**

```bash
git add tests/helpers.py theme/types/doc.py tests/test_type_doc.py
git commit -m "feat(theme): doc type, ordered and grouped, with a search index per language"
```

---

### Task 6: The `showcase` type

**Files:**
- Create: `theme/types/showcase.py`, `tests/test_type_showcase.py`

**Interfaces:**
- Consumes: `tests.helpers.load_type`; from tilder `seo.page_title(meta)`, `seo.site_ref()`.
- Produces: `NAME = "showcase"`, `DEFAULTS = {"man": "SITE-SHOWCASE(7)", "nav": "showcase", "empty": "No site listed yet.", "visit": "visit ↗"}`, `defaults(item, conf)` (raises `ValueError` without an `http(s)://` `url`, or when `image` names no file next to the item), `sort_key`, `image_src(item) -> str` (the screenshot's path from `content/`), `entry(item, link, conf)`, `showcase(items, conf)` (`MARKERS = {"showcase": showcase}`, `cls: ["grid"]`), `json_ld(item, conf)` (a `WebPage` `about` the listed `WebSite`, Resolution 9).

- [ ] **Step 1: Write the failing tests**

`tests/test_type_showcase.py`:

```python
import pathlib
import tempfile
import unittest

from tests.helpers import load_type

showcase = load_type("showcase")


class Showcase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.folder = pathlib.Path(tmp.name, "showcase", "example")
        self.folder.mkdir(parents=True)
        (self.folder / "shot.png").write_bytes(b"\x89PNG")
        self.src = self.folder / "index.md"
        self.conf = dict(showcase.DEFAULTS, dir="showcase")

    def item(self, **meta):
        meta.setdefault("title", "Example site")
        meta.setdefault("url", "https://example.org/")
        return {"slug": "example", "meta": meta, "src": self.src, "path": "showcase/example.html"}

    def test_the_type_s_contract(self):
        self.assertEqual(showcase.NAME, "showcase")
        self.assertEqual(showcase.DEFAULTS, {"man": "SITE-SHOWCASE(7)", "nav": "showcase",
                                             "empty": "No site listed yet.", "visit": "visit ↗"})

    def test_defaults_tagline_is_the_host(self):
        it = self.item()
        showcase.defaults(it, self.conf)
        self.assertEqual(it["meta"]["tagline"], "example.org")
        self.assertEqual(it["meta"]["man"], "SITE-SHOWCASE(7)")

    def test_url_is_required(self):
        it = self.item()
        del it["meta"]["url"]
        with self.assertRaisesRegex(ValueError, "url must be the site's address"):
            showcase.defaults(it, self.conf)

    def test_a_missing_image_says_so(self):
        with self.assertRaisesRegex(ValueError, 'image "gone.png" is not next to index.md'):
            showcase.defaults(self.item(image="gone.png"), self.conf)

    def test_card_in_a_list(self):
        node = showcase.entry(self.item(description="A site.", image="shot.png"), True, self.conf)
        self.assertEqual(node["title"], "[Example site](showcase/example)")
        self.assertEqual(node["meta"], ["https://example.org/"])
        self.assertEqual(node["cls"], ["link"])
        self.assertEqual(node["blocks"], [
            {"k": "para", "text": "A site.", "cls": []},
            {"k": "image", "src": "showcase/example/shot.png", "alt": "Example site", "caption": ""}])

    def test_its_own_page_links_to_the_site(self):
        node = showcase.entry(self.item(), False, self.conf)
        self.assertTrue(node["own"])
        self.assertEqual(node["blocks"][-1]["text"], "[visit ↗](https://example.org/)")

    def test_a_flat_item_s_image_is_beside_it(self):
        it = self.item(image="shot.png")
        it["src"] = self.folder.parent / "example.md"
        self.assertEqual(showcase.image_src(it), "showcase/shot.png")

    def test_marker_is_a_grid_in_order(self):
        its = [self.item(order="2"), self.item(order="1")]
        its.sort(key=lambda it: showcase.sort_key(it, self.conf))
        out = showcase.MARKERS["showcase"](its, self.conf)
        self.assertEqual(out["cls"], ["grid"])
        self.assertEqual(out["empty"], "No site listed yet.")

    def test_json_ld_is_a_page_about_the_site(self):
        node = showcase.json_ld(self.item(description="A site."), self.conf)
        self.assertEqual(node["@type"], "WebPage")
        self.assertEqual(node["about"], {"@type": "WebSite", "name": "Example site",
                                         "url": "https://example.org/"})
```

- [ ] **Step 2: Run them to see them fail**

Run: `python3 -m unittest tests.test_type_showcase -v`
Expected: ERROR, `FileNotFoundError` for `theme/types/showcase.py`.

- [ ] **Step 3: Write the type**

`theme/types/showcase.py`:

```python
"""Showcase: sites built with the documented project, one item each, with
an optional screenshot next to it. A theme type (tilder docs/types.md)."""

from seo import page_title, site_ref

NAME = "showcase"
DEFAULTS = {
    "man": "SITE-SHOWCASE(7)",      # items' man-page name, unless one sets its own
    "nav": "showcase",              # items' nav entry
    "empty": "No site listed yet.", # a {showcase} list with nothing in it
    "visit": "visit ↗",             # the link to the site, on its page
}


def defaults(item, conf):
    meta = item["meta"]
    url = meta.get("url", "")
    if not url.startswith(("https://", "http://")):
        raise ValueError(f'url must be the site\'s address, https://..., not "{url}"')
    if meta.get("image") and not (item["src"].parent / meta["image"]).is_file():
        raise ValueError(f'image "{meta["image"]}" is not next to {item["src"].name}')
    meta.setdefault("man", conf["man"])
    meta.setdefault("nav", conf["nav"])
    meta.setdefault("tagline", url.split("://", 1)[1].rstrip("/"))
    meta.setdefault("description", "")


def sort_key(item, conf):
    value = item["meta"].get("order", "1000")
    try:
        return (int(value), item["slug"])
    except ValueError:
        raise ValueError(f'order must be a whole number, not "{value}"') from None


def image_src(item):
    """The screenshot's path from content/, like the builder's own images:
    next to the item's file (showcase/<slug>/shot.png, or showcase/shot.png
    for a flat showcase/<slug>.md)."""
    folder = item["path"][:-5] if item["src"].stem.split(".")[0] == "index" \
        else item["path"].rsplit("/", 1)[0]
    return f"{folder}/{item['meta']['image']}"


def entry(item, link, conf):
    """The card: the title, the address, the description, the screenshot.
    On its own page, a link to the site too."""
    meta = item["meta"]
    blocks = []
    if meta.get("description"):
        blocks.append({"k": "para", "text": meta["description"], "cls": []})
    if meta.get("image"):
        blocks.append({"k": "image", "src": image_src(item), "alt": meta["title"], "caption": ""})
    if not link:
        blocks.append({"k": "para", "text": f"[{conf['visit']}]({meta['url']})", "cls": []})
    return {"k": "entry", "id": None, "cls": ["link"] if link else [],
            "title": f"[{meta['title']}]({item['path'][:-5]})" if link else meta["title"],
            "meta": [meta["url"]], "blocks": blocks, "own": not link}


def showcase(items, conf):
    """{showcase}: every site, in order, as a grid."""
    return {"items": [(it, []) for it in items], "empty": conf.get("empty", ""), "cls": ["grid"]}


MARKERS = {"showcase": showcase}


def json_ld(item, conf):
    """The page is about another site: a WebPage whose subject is that
    WebSite. The builder sets the node's own url and inLanguage."""
    meta = item["meta"]
    return {"@type": "WebPage", "name": page_title(meta), "description": meta["description"],
            "isPartOf": site_ref(),
            "about": {"@type": "WebSite", "name": meta["title"], "url": meta["url"]}}
```

- [ ] **Step 4: Run the tests**

Run: `python3 -m unittest tests.test_type_showcase tests.test_type_doc -v`
Expected: 23 tests, OK.

- [ ] **Step 5: Commit**

```bash
git add theme/types/showcase.py tests/test_type_showcase.py
git commit -m "feat(theme): showcase type, sites built with the project, as a grid"
```

---

### Task 7: The base layout, the theme's words, the build script and the fixture site

**Files:**
- Create: `build.sh`, `TILDER_VERSION`, `theme/layout.html`, `theme/theme.toml`, `theme/theme.fr.toml`, `tests/site/content/site.toml`, `tests/site/content/site.fr.toml`, `tests/site/content/index.md`, `tests/site/content/404.md`, `tests/site/assets/logo.svg`, `tests/test_build.py`, `tests/test_theme_toml.py`
- Modify: `tests/helpers.py` (whole file below: adds `builder_missing`, `Build`, `fixture_build`)

**Interfaces:**
- Consumes: `tools/check-theme.py`, `tools/check-contrast.py`, `theme/style.css`, `theme/types/*.py` (the fixture declares both collections; their folders come in Tasks 8-9, and a declared collection without a folder is simply empty).
- Produces: `build.sh [--root DIR] [--out DIR] [--watch]` (env `TILDER_BUILD`, `DOCKER`); in `tests.helpers`: `builder_missing() -> str | None`, `Build(extra: dict[str, str] | None)` with `.returncode`, `.stdout`, `.stderr`, `.out: Path`, `.read(path) -> str` (copies `tests/site` and `theme/` to a temporary root, applies `extra` as `{relative path: text}`, runs `build.sh`), `fixture_build(test) -> Build` (one shared build per run; skips when no tilder; asserts it succeeded). Config keys the layouts use: `search.label`, `search.placeholder`, `search.none`, `search.count` (with `{n}`), `doc.contents`, `doc.on_this_page`, `share.*_color`. The fixture's site: `https://docs.example`, `en` + `fr`, collections `docs` (type `doc`) and `showcase` (type `showcase`).

- [ ] **Step 1: Write the failing tests**

`tests/helpers.py`, whole file:

```python
"""What the theme's tests share: load a tool or a theme type as a module,
and build the fixture site (tests/site) with the theme through build.sh.

Standard library only. The build needs tilder: TILDER_BUILD pointing to a
checkout's build.py, or the pinned Docker image already pulled. Without
either, the build tests are skipped, and say why."""

import atexit
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import types
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
THEME = REPO / "theme"
FIXTURE = REPO / "tests" / "site"


def load_tool(name):
    """tools/<name>.py ("check-theme") as a module."""
    path = REPO / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# What the stand-ins below answer, changed by a test: the language prefix
# of the pass ("" or "fr/").
STUB = {"prefix": ""}


def _clean_url(html_path, lang=None):
    """tilder's paths.clean_url, for the stand-in: "/", "/fr/docs/start"."""
    n, p = html_path[:-5], STUB["prefix"]
    if n == "index":
        return "/" + p
    if n.endswith("/index"):
        return "/" + p + n[:-len("/index")] + "/"
    return "/" + p + n


STUBS = {
    "paths": types.SimpleNamespace(clean_url=_clean_url),
    "seo": types.SimpleNamespace(
        org_ref=lambda: {"@id": "https://docs.example/#organization"},
        site_ref=lambda: {"@id": "https://docs.example/#website"},
        page_heading=lambda meta: meta.get("name") or meta["title"],
        page_title=lambda meta: meta["title"] + " - fixture docs"),
}


def load_type(name):
    """theme/types/<name>.py as a module, with stand-ins for the tilder
    modules a type may import (paths, seo): the unit tests need no tilder."""
    saved = {k: sys.modules.get(k) for k in STUBS}
    sys.modules.update(STUBS)
    try:
        path = THEME / "types" / f"{name}.py"
        spec = importlib.util.spec_from_file_location(f"theme_type_{name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    return module


def builder_missing():
    """Why the fixture cannot be built here, or None when it can."""
    local = os.environ.get("TILDER_BUILD")
    if local:
        return None if pathlib.Path(local).is_file() else f"TILDER_BUILD={local} is not a file"
    engine = os.environ.get("DOCKER", "docker")
    version = (REPO / "TILDER_VERSION").read_text().strip().removeprefix("v")
    image = f"ghcr.io/thosted/tilder:{version}"
    if not shutil.which(engine):
        return f"no TILDER_BUILD and no {engine}"
    found = subprocess.run([engine, "image", "inspect", image], capture_output=True)
    return None if found.returncode == 0 else f"no TILDER_BUILD and no local image {image} ({engine} pull {image})"


class Build:
    """One build of the fixture: returncode, stdout, stderr, and the output
    folder (out). read(path) is an output file as text."""

    def __init__(self, extra=None):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="theme-test-"))
        atexit.register(shutil.rmtree, tmp, True)
        root = tmp / "site"
        shutil.copytree(FIXTURE, root)
        shutil.copytree(THEME, root / "theme")
        for rel, text in (extra or {}).items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        self.out = tmp / "out"
        done = subprocess.run([str(REPO / "build.sh"), "--root", str(root), "--out", str(self.out)],
                              capture_output=True, text=True)
        self.returncode, self.stdout, self.stderr = done.returncode, done.stdout, done.stderr

    def read(self, path):
        return (self.out / path).read_text(encoding="utf-8")


_BUILT = []


def fixture_build(test):
    """The fixture, built once per run with the theme as it is; skips the
    test when no tilder is at hand."""
    why = builder_missing()
    if why:
        raise unittest.SkipTest(why)
    if not _BUILT:
        _BUILT.append(Build())
    build = _BUILT[0]
    test.assertEqual(build.returncode, 0, build.stderr)
    return build
```

`tests/test_build.py`:

````python
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
````

`tests/test_theme_toml.py`:

```python
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
```

- [ ] **Step 2: Run them to see them fail**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest tests.test_build tests.test_theme_toml -v`
Expected: ERROR in every build test (`FileNotFoundError: .../build.sh`) except `test_layout_comments_hold_no_placeholder`, which errors on the missing `theme/layout.html`; ERROR in the `theme.toml` tests (`FileNotFoundError`).

- [ ] **Step 3: Write the build script**

`TILDER_VERSION`, one line:

```
1.1.0
```

`build.sh` (`chmod +x build.sh`):

```sh
#!/bin/sh
# Build the site with tilder, after the theme's checks. Fails on any
# build warning.
#
#   ./build.sh                          content/ -> public/
#   ./build.sh --out DIR                somewhere else
#   ./build.sh --root DIR --out DIR     another project laid out the same way
#                                       (the theme's tests build tests/site)
#   ./build.sh --watch                  rebuild on every change (checks once)
#
# tilder comes from its Docker image, ghcr.io/thosted/tilder, at the tag in
# TILDER_VERSION. A local checkout instead (before the image exists, or to
# work on tilder itself):
#
#   TILDER_BUILD=/path/to/tilder/build.py ./build.sh
#
# DOCKER=podman picks another container engine.
set -eu

here=$(cd "$(dirname "$0")" && pwd)
root=$here
out=$here/public
watch=""
while [ $# -gt 0 ]; do
	case $1 in
		--root) root=$(cd "$2" && pwd); shift 2 ;;
		--out) mkdir -p "$2"; out=$(cd "$2" && pwd); shift 2 ;;
		--watch) watch=--watch; shift ;;
		*) echo "usage: build.sh [--root DIR] [--out DIR] [--watch]" >&2; exit 2 ;;
	esac
done

# The theme contract: the checkout's own docs/theme.md, else the copy of
# the pinned version's (the image ships no docs/).
if [ -n "${TILDER_BUILD:-}" ]; then
	contract=$(dirname "$TILDER_BUILD")/docs/theme.md
else
	contract=$here/tools/tilder-theme.md
fi
python3 "$here/tools/check-theme.py" "$root/theme/style.css" "$contract"
python3 "$here/tools/check-contrast.py" "$root/theme/style.css"

if [ -n "${TILDER_BUILD:-}" ]; then
	set -- python3 -B "$TILDER_BUILD" --root "$root" --out "$out"
else
	version=$(tr -d ' \n' < "$here/TILDER_VERSION")
	set -- "${DOCKER:-docker}" run --rm -u "$(id -u):$(id -g)" \
		-v "$root:/site:ro" -v "$out:/out" \
		"ghcr.io/thosted/tilder:${version#v}" \
		python3 -B /tilder/build.py --root /site --out /out
fi

if [ -n "$watch" ]; then
	exec "$@" --watch
fi

log=$(mktemp)
trap 'rm -f "$log"' EXIT
status=0
"$@" 2>"$log" || status=$?
cat "$log" >&2
if [ "$status" -ne 0 ]; then
	exit "$status"
fi
if grep -Eq '^(warning|seo):' "$log"; then
	echo "error: build.sh: the build printed warnings (above). A build prints none" >&2
	exit 1
fi
```

- [ ] **Step 4: Write the theme's words**

`theme/theme.toml`:

```toml
# The theme's own words and colours, in English. A site overrides any of
# them in its content/site.toml; theme.fr.toml holds the French.

[search]
label = "Search the documentation"     # the search field's label (search.js)
placeholder = "search"                 # the field's placeholder
none = "No page matches."              # a search that finds nothing
count = "{n} pages found"              # {n}: how many pages match

[doc]
contents = "Contents"                  # the sidebar's summary on small screens
on_this_page = "On this page"          # the right column, over the [TOC]

[share]                                # the link preview and the browser UI
theme_color = "#00707e"
background_color = "#fcfcfa"
text_color = "#1c1e21"
muted_color = "#4f565d"
rule_color = "#d4d4cd"
```

`theme/theme.fr.toml`:

```toml
# The theme's words in French (theme.toml holds the English). A site that
# does not declare "fr" in [site] languages must delete this file: tilder
# stops on a theme.<lang>.toml of an undeclared language.

[search]
label = "Rechercher dans la documentation"
placeholder = "rechercher"
none = "Aucune page ne correspond."
count = "{n} pages trouvées"

[doc]
contents = "Sommaire"
on_this_page = "Sur cette page"
```

- [ ] **Step 5: Write the base layout**

`theme/layout.html`. No `{{` inside a comment (Global Constraints). `layouts/home.html` and `layouts/doc.html` (Task 8) repeat its head, header and footer:

```html
<!DOCTYPE html>
<!-- The theme's base layout: every page reads as a man page. tilder fills
     the double-brace placeholders (tilder docs/theme.md). layouts/home.html and
     layouts/doc.html repeat this head, header and footer: keep them alike. -->
<html lang="{{ site.lang }}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ page.description }}">
<link rel="preload" href="{{ root }}fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{{ root }}style.css">
<link rel="icon" href="{{ root }}favicon.ico" sizes="48x48">
<link rel="icon" href="{{ root }}logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{{ root }}apple-touch-icon.png">
<link rel="manifest" href="{{ root }}site.webmanifest">
<link rel="canonical" href="{{ canonical }}">{{ feeds }}
<meta name="theme-color" content="{{ share.theme_color }}">
{{ head }}
</head>
<body class="layout-base type-{{ type }}">
<div class="page" id="top">

<a class="skip" href="#contenu">{{ labels.skip }}</a>

<header>
<!-- The man-page rule is decoration: hidden from screen readers. -->
<div class="manline manline--head" aria-hidden="true">
	<span>{{ page.man }}</span>
	<span>{{ site.manual }}</span>
	<span>{{ page.man }}</span>
</div>
<div class="bar">
{{ brand }}
<nav class="nav" aria-label="{{ labels.nav }}">
{{ nav }}
</nav>
{{ languages }}
</div>
<p class="tagline">{{ page.tagline }}</p>
</header>

<main id="contenu" lang="{{ content_lang }}">
{{ body }}
<div class="pager">{{ prev }}{{ next }}</div>
</main>

<p class="to-top"><a href="#top">{{ labels.to_top }}</a></p>

<footer class="manline manline--foot">
	<span><a href="{{ home }}{{ footer.left_link }}">{{ footer.left }}</a></span>
	<span>{{ site.updated }}</span>
	<span>{{ footer.right }}</span>
</footer>

</div>
{{ script }}</body>
</html>
```

- [ ] **Step 6: Write the fixture site**

`tests/site/content/site.toml`:

```toml
# The theme's fixture site: every layout, type and class of the theme, in
# two languages. English, neutral; no real person or site.

[site]
name = "fixture docs"
url = "https://docs.example"
lang = "en"
locale = "en_GB"
languages = ["en", "fr"]
manual = "Fixture Manual"
updated = 2026-09-01
title_suffix = " - fixture docs"

[footer]
left = "FIXTURE"
left_link = ""
right = "FIXTURE(1)"

[languages]
en = "English"
fr = "Français"

[[nav]]
label = "home"
href = ""

[[nav]]
label = "docs"
href = "docs/"

[[nav]]
label = "showcase"
href = "showcase/"

[seo]
organization = "Fixture Docs"

[share]
image_alt = "~/fixture docs"
card = ["a documentation theme", "in two languages"]
short_name = "fixture"

[collections.docs]
type = "doc"

[collections.showcase]
type = "showcase"
```

`tests/site/content/site.fr.toml`:

```toml
# The fixture in French: only what differs from site.toml. The theme's
# own French words come from theme/theme.fr.toml.

[site]
lang = "fr"
locale = "fr_FR"
manual = "Manuel du site de test"

[labels]
collection_nav = "Dans cette section"
prev = "précédent"
next = "suivant"

[[nav]]
label = "accueil"
href = ""

[[nav]]
label = "docs"
href = "docs/"

[[nav]]
label = "vitrine"
href = "showcase/"
```

`tests/site/content/index.md` (Task 8 replaces it with the landing page):

```markdown
---
man: FIXTURE(7)
title: fixture docs
description: The landing page of the theme's fixture site, in the base layout for now.
tagline: a fixture for the documentation theme
nav:
---

## Name

fixture - the landing page
```

`tests/site/content/404.md`:

```markdown
---
man: FIXTURE(7)
title: Not found
description: No manual entry for this page: the fixture's not-found page, never indexed.
tagline: 404
nav: -
robots: noindex
---

## Name

not found
```

`tests/site/assets/logo.svg` (tilder draws the icons and `share.png` from it):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
	<rect width="64" height="64" rx="8" fill="#00707e"/>
	<path d="M14 40 L26 24 M30 40 L42 24" stroke="#fcfcfa" stroke-width="6" stroke-linecap="round"/>
</svg>
```

- [ ] **Step 7: Run the tests**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest tests.test_build tests.test_theme_toml -v`
Expected: 12 tests, OK.
Also, without `TILDER_BUILD` (and no image pulled): `python3 -m unittest tests.test_build -v` reports the build tests as skipped, "no TILDER_BUILD and no local image ghcr.io/thosted/tilder:1.1.0 (docker pull ...)". Once the image is published: `docker pull ghcr.io/thosted/tilder:1.1.0 && python3 -m unittest tests.test_build -v` passes through Docker too.

- [ ] **Step 8: Commit**

```bash
git add build.sh TILDER_VERSION theme/layout.html theme/theme.toml theme/theme.fr.toml tests/helpers.py tests/test_build.py tests/test_theme_toml.py tests/site
git commit -m "feat(theme): man-page base layout, theme words, build script and fixture site"
```

---

### Task 8: The landing and documentation layouts

**Files:**
- Create: `theme/layouts/home.html`, `theme/layouts/doc.html`, `tests/site/content/docs/index.md`, `tests/site/content/docs/start.md`, `tests/site/content/docs/cli.md`, `tests/site/content/docs/cli.fr.md`, `tests/test_layouts.py`
- Modify: `tests/site/content/index.md` (whole file below)

**Interfaces:**
- Consumes: `{{ page.search_index }}` (Task 5's `doc.defaults`), `{{ search.* }}`, `{{ doc.* }}` (Task 7), `fixture_build`.
- Produces: the markup the scripts rely on — `<details class="doc-side" open data-doc-side>` (nav.js), `<div class="doc-search" data-search-index data-home data-label data-placeholder data-none data-count>` (search.js), `<div class="doc-toc" data-doc-toc hidden>` inside `<div class="doc">` (nav.js adds `doc--toc` to that div), `<main class="doc-main">`; `<main class="home">` with `<p class="home-tagline">`. `doc.html` links `{{ root }}nav.js` and `{{ root }}search.js` with `defer` (the files come in Tasks 10-11; until then the links are harmless 404s).

- [ ] **Step 1: Write the failing tests**

`tests/test_layouts.py`:

```python
"""The home and doc layouts, the doc type's pages and search index, and
the theme's words in both languages, on the built fixture."""

import json
import unittest

from tests.helpers import fixture_build


class Home(unittest.TestCase):
    def setUp(self):
        self.build = fixture_build(self)

    def test_the_landing_page_uses_the_home_layout(self):
        html = self.build.read("index.html")
        self.assertIn('class="layout-home type-page"', html)
        self.assertIn('<main id="contenu" class="home" lang="en">', html)
        self.assertIn('<p class="home-tagline">a fixture for the documentation theme</p>', html)
        self.assertNotIn('<p class="tagline">', html)

    def test_features_and_panes_are_grids(self):
        html = self.build.read("index.html")
        self.assertEqual(html.count('<div class="b grid">'), 2)
        self.assertIn('<pre class="code" data-lang="console"', html)


class Doc(unittest.TestCase):
    def setUp(self):
        self.build = fixture_build(self)

    def test_three_columns_in_the_markup(self):
        html = self.build.read("docs/start.html")
        self.assertIn('class="layout-doc type-doc"', html)
        side = html.index('<details class="doc-side" open data-doc-side>')
        main = html.index('<main id="contenu" class="doc-main" lang="en">')
        toc = html.index('<div class="doc-toc" data-doc-toc hidden>')
        self.assertLess(side, main)
        self.assertLess(main, toc)
        self.assertIn('<nav class="collection-nav"', html[side:main])
        self.assertIn('<a href="start" aria-current="page">Getting started</a>', html)

    def test_the_search_field_s_words_come_from_theme_toml(self):
        html = self.build.read("docs/start.html")
        self.assertIn('data-search-index="docs/search-index.json" data-home="../"', html)
        self.assertIn('data-label="Search the documentation"', html)
        self.assertIn('data-count="{n} pages found"', html)
        self.assertIn("<summary>Contents</summary>", html)
        self.assertIn('<p class="doc-toc-label" aria-hidden="true">On this page</p>', html)

    def test_french_words_from_theme_fr_toml(self):
        html = self.build.read("fr/docs/cli.html")
        self.assertIn('data-home="../"', html)
        self.assertIn('data-label="Rechercher dans la documentation"', html)
        self.assertIn("<summary>Sommaire</summary>", html)
        self.assertIn('<p class="doc-toc-label" aria-hidden="true">Sur cette page</p>', html)

    def test_scripts_are_linked_from_the_root(self):
        html = self.build.read("fr/docs/cli.html")
        self.assertIn('<script src="../../nav.js" defer></script>', html)
        self.assertIn('<script src="../../search.js" defer></script>', html)

    def test_prev_next_and_the_text_mirror_line(self):
        html = self.build.read("docs/start.html")
        self.assertIn('<a class="next" rel="next" href="cli">', html)
        self.assertIn("next: Command line", self.build.read("txt/docs/start.txt"))

    def test_the_docs_list_is_grouped(self):
        html = self.build.read("docs/index.html")
        self.assertIn('<div class="entry entry--link">', html)
        self.assertIn('<div class="entry entry--group entry--link">', html)
        self.assertIn('data-search-index="docs/search-index.json"', html)

    def test_tech_article(self):
        self.assertIn('"@type":"TechArticle"', self.build.read("docs/cli.html"))


class SearchIndex(unittest.TestCase):
    def setUp(self):
        self.build = fixture_build(self)

    def index(self, path):
        return json.loads(self.build.read(path))

    def test_one_index_per_language(self):
        en, fr = self.index("docs/search-index.json"), self.index("fr/docs/search-index.json")
        self.assertEqual([r["t"] for r in en], ["Getting started", "Command line"])
        # The French pass: a translated page, and an English fallback.
        self.assertEqual([r["t"] for r in fr], ["Getting started", "Ligne de commande"])
        self.assertEqual([r["u"] for r in fr], ["docs/start", "docs/cli"])
        self.assertEqual(sorted(en[0]), ["d", "h", "t", "u", "x"])

    def test_the_index_is_not_a_page(self):
        self.assertNotIn("search-index", self.build.read("sitemap.txt"))
```

- [ ] **Step 2: Add the fixture's documentation and landing page**

`tests/site/content/index.md`, whole file:

````markdown
---
man: FIXTURE(7)
title: fixture docs
description: The landing page of the theme's fixture site, laid out by the home layout.
tagline: a fixture for the documentation theme
nav:
layout: home
---

## Name

fixture - the hero, in large type, under the tagline

## Features {grid}

### Search

  A search field over the documentation, one index per language.

### Sidebar

  The collection's pages, grouped, the current one marked.

## One source, two outputs {grid}

```text
## Name

hello - a page
```

```console
$ curl docs.example
NAME
     hello - a page
```
````

`tests/site/content/docs/index.md` (the collection's own page: a plain page asking for the doc layout, Resolution 6):

```markdown
---
man: FIXTURE-DOCS(7)
title: Documentation
description: Every page of the fixture's documentation, grouped, with a search field.
tagline: the manual
nav: docs/
layout: doc
search_index: docs/search-index.json
---

## Pages {docs}
```

`tests/site/content/docs/start.md`:

````markdown
---
title: Getting started
description: The first page of the fixture's documentation, with no group at all.
order: 10
---

## Name

getting started - the **first** page {mono}

[TOC]

## Install {#install}

Run `build.sh` and read the [cli](docs/cli) page.

```sh
./build.sh
## not a heading
```
````

`tests/site/content/docs/cli.md`:

```markdown
---
title: Command line
description: The second page of the fixture's documentation, in the Reference group.
order: 20
group: Reference
---

## Name

cli - the Élan of options
```

`tests/site/content/docs/cli.fr.md` (only this page is translated; `start` falls back to English on `/fr/`):

```markdown
---
title: Ligne de commande
description: La deuxième page de la documentation du site de test, groupe Référence.
order: 20
group: Référence
---

## Nom

cli - l'élan des options
```

- [ ] **Step 3: Run the tests to see them fail**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest tests.test_layouts -v`
Expected: FAIL in every test, at `fixture_build`: the build stops with `error: content/...: layout "home" names no theme/layouts/home.html` (or `"doc"`), because the fixture's front matter now asks for layouts that do not exist yet.

- [ ] **Step 4: Write the layouts**

`theme/layouts/home.html`:

```html
<!DOCTYPE html>
<!-- The landing page (layout: home in its front matter): the base layout
     airier, wider, the tagline as the hero's headline. Keep the head,
     header and footer like layout.html. -->
<html lang="{{ site.lang }}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ page.description }}">
<link rel="preload" href="{{ root }}fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{{ root }}style.css">
<link rel="icon" href="{{ root }}favicon.ico" sizes="48x48">
<link rel="icon" href="{{ root }}logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{{ root }}apple-touch-icon.png">
<link rel="manifest" href="{{ root }}site.webmanifest">
<link rel="canonical" href="{{ canonical }}">{{ feeds }}
<meta name="theme-color" content="{{ share.theme_color }}">
{{ head }}
</head>
<body class="layout-home type-{{ type }}">
<div class="page page--home" id="top">

<a class="skip" href="#contenu">{{ labels.skip }}</a>

<header>
<!-- The man-page rule is decoration: hidden from screen readers. -->
<div class="manline manline--head" aria-hidden="true">
	<span>{{ page.man }}</span>
	<span>{{ site.manual }}</span>
	<span>{{ page.man }}</span>
</div>
<div class="bar">
{{ brand }}
<nav class="nav" aria-label="{{ labels.nav }}">
{{ nav }}
</nav>
{{ languages }}
</div>
</header>

<main id="contenu" class="home" lang="{{ content_lang }}">
<p class="home-tagline">{{ page.tagline }}</p>
{{ body }}
</main>

<p class="to-top"><a href="#top">{{ labels.to_top }}</a></p>

<footer class="manline manline--foot">
	<span><a href="{{ home }}{{ footer.left_link }}">{{ footer.left }}</a></span>
	<span>{{ site.updated }}</span>
	<span>{{ footer.right }}</span>
</footer>

</div>
{{ script }}</body>
</html>
```

`theme/layouts/doc.html`:

```html
<!DOCTYPE html>
<!-- Documentation pages: the doc type's LAYOUT, or layout: doc. Three
     columns: the search and the collection's sidebar, the text, the
     page's [TOC] (moved there by nav.js on wide screens). Keep the head,
     header and footer like layout.html. -->
<html lang="{{ site.lang }}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ page.description }}">
<link rel="preload" href="{{ root }}fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{{ root }}style.css">
<link rel="icon" href="{{ root }}favicon.ico" sizes="48x48">
<link rel="icon" href="{{ root }}logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{{ root }}apple-touch-icon.png">
<link rel="manifest" href="{{ root }}site.webmanifest">
<link rel="canonical" href="{{ canonical }}">{{ feeds }}
<meta name="theme-color" content="{{ share.theme_color }}">
{{ head }}
</head>
<body class="layout-doc type-{{ type }}">
<div class="page page--wide" id="top">

<a class="skip" href="#contenu">{{ labels.skip }}</a>

<header>
<!-- The man-page rule is decoration: hidden from screen readers. -->
<div class="manline manline--head" aria-hidden="true">
	<span>{{ page.man }}</span>
	<span>{{ site.manual }}</span>
	<span>{{ page.man }}</span>
</div>
<div class="bar">
{{ brand }}
<nav class="nav" aria-label="{{ labels.nav }}">
{{ nav }}
</nav>
{{ languages }}
</div>
<p class="tagline">{{ page.tagline }}</p>
</header>

<div class="doc">
<!-- Open without JavaScript; nav.js folds it on small screens. -->
<details class="doc-side" open data-doc-side>
<summary>{{ doc.contents }}</summary>
<div class="doc-search" data-search-index="{{ page.search_index }}" data-home="{{ home }}"
	data-label="{{ search.label }}" data-placeholder="{{ search.placeholder }}"
	data-none="{{ search.none }}" data-count="{{ search.count }}"></div>
{{ collection_nav }}
</details>

<main id="contenu" class="doc-main" lang="{{ content_lang }}">
{{ body }}
<div class="pager">{{ prev }}{{ next }}</div>
</main>

<div class="doc-toc" data-doc-toc hidden>
<p class="doc-toc-label" aria-hidden="true">{{ doc.on_this_page }}</p>
</div>
</div>

<p class="to-top"><a href="#top">{{ labels.to_top }}</a></p>

<footer class="manline manline--foot">
	<span><a href="{{ home }}{{ footer.left_link }}">{{ footer.left }}</a></span>
	<span>{{ site.updated }}</span>
	<span>{{ footer.right }}</span>
</footer>

</div>
<script src="{{ root }}nav.js" defer></script>
<script src="{{ root }}search.js" defer></script>
{{ script }}</body>
</html>
```

- [ ] **Step 5: Run the tests**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest tests.test_layouts tests.test_build -v`
Expected: 20 tests, OK (the base-layout checks now also cover the two new layouts: one `<h1>`, `lang`, canonical, no `{{` left).

- [ ] **Step 6: Commit**

```bash
git add theme/layouts tests/test_layouts.py tests/site/content
git commit -m "feat(theme): landing layout and three-column documentation layout"
```

---

### Task 9: The kitchen sink and the showcase fixture

**Files:**
- Create: `tests/site/content/kitchen-sink.md`, `tests/site/content/kitchen-sink-figure.svg`, `tests/site/content/showcase/index.md`, `tests/site/content/showcase/example/index.md`, `tests/site/content/showcase/example/shot.svg`, `tests/site/content/members/ada-example.md`, `tests/test_kitchen_sink.py`

**Interfaces:**
- Consumes: `fixture_build`, `load_tool("check-theme")`, the `showcase` type (Task 6).
- Produces: a fixture that writes every contract class but `.icon` (Resolution 14); `kitchen-sink.md` is the page sub-project C copies to `content/`.

- [ ] **Step 1: Write the failing tests**

`tests/test_kitchen_sink.py`:

```python
"""The fixture shows every class of tilder's contract, so the theme is
reviewed on all of them (README.md, "Review by eye")."""

import re
import unittest

from tests.helpers import REPO, fixture_build, load_tool

# Written only when the theme ships icons/<network>.svg; this theme ships none.
NOT_SHOWN = {"icon"}


class KitchenSink(unittest.TestCase):
    def setUp(self):
        self.build = fixture_build(self)

    def test_every_contract_class_appears_in_the_fixture(self):
        check = load_tool("check-theme")
        classes = check.contract_classes((REPO / "tools" / "tilder-theme.md").read_text())
        written = set()
        for path in self.build.out.rglob("*.html"):
            for value in re.findall(r'class="([^"]*)"', path.read_text()):
                written.update(value.split())
        self.assertEqual([c for c in classes if c not in written and c not in NOT_SHOWN], [])

    def test_the_kitchen_sink_is_not_indexed(self):
        html = self.build.read("kitchen-sink.html")
        self.assertIn('<meta name="robots" content="noindex', html)
        self.assertNotIn("kitchen-sink", self.build.read("sitemap.txt"))

    def test_the_showcase_grid_and_page(self):
        html = self.build.read("showcase/index.html")
        self.assertIn('<div class="b showcase grid">', html)
        page = self.build.read("showcase/example.html")
        self.assertIn('<img src="example/shot.svg" alt="Example site"', page)
        self.assertIn('"about":{"@type":"WebSite","name":"Example site","url":"https://example.org/"}', page)
```

- [ ] **Step 2: Run them to see them fail**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest tests.test_kitchen_sink -v`
Expected: FAIL, `test_every_contract_class_appears_in_the_fixture` lists the missing classes (`entry--next`, `callout--info`, `hl-k`, `tasks`, `members`, `profiles`...); ERROR (`FileNotFoundError`) for `kitchen-sink.html` and `showcase/index.html`.

- [ ] **Step 3: Write the kitchen sink**

`tests/site/content/kitchen-sink.md` (every construct of tilder's `docs/markdown.md`; lists are separated by blank lines, else they merge; the code blocks are chosen so every `.hl-*` token appears; `### Rendered {example}` is Resolution 3's frame):

````markdown
---
man: KITCHEN-SINK(7)
title: Kitchen sink
description: Every construct and every class of the theme, on one page, to review by eye.
tagline: every construct, light and dark
nav: -
robots: noindex
---

[TOC]

## Name

kitchen sink - every construct of the dialect, as this theme draws it {mono}

## Paragraphs

A paragraph with **bold**, *italic*, _italic too_, ~~struck~~, ++underlined++,
`inline code`, an [internal link](docs/) and an [external one ↗](https://example.org/).

A small muted line. {small muted}

A faint line. {faint}

A warning line. {warn}

A monospace line. {mono}

*Nothing here yet: the empty state.*

---

## Lists

- a bullet
- another, with a nested list
  - nested

1. first
2. second

- [x] a done task
- [ ] a task to do

## Boxes

> A plain inset: a live example is framed like this.
>
> Its second paragraph.

### Rendered {example}

  | a live | example |
  |---|---|
  | of a | table |

> [!INFO]
> An information callout.

> [!WARNING]
> A warning callout.

> [!ERROR]
> An error callout.

## Entries

### A plain entry

  - 2026-09-01 | Tuesday 1 September 2026
  - a place
  - `tag`

  The entry's body, indented two spaces.

### The next one {next}

  - `next`

### A full one {full}

  - `full`

## Cards {grid}

### First card

  - `grid`

  A card in a grid.

### Second card

  A second card.

## Code

```python
@decorator
def fold(text, width=75):
    """Fold the text."""  # a comment
    return text[:width] + "é"
```

```sh
echo "$HOME" ${PATH} 42
```

```console
$ curl example.org
the text mirror
```

```diff
@@ -1,2 +1,2 @@
-old line
+new line
```

```html
<!DOCTYPE html>
<!-- a comment -->
<p class="x">&amp;</p>
```

```
no language, no label
```

## Tables

| left | centre | right |
|:-----|:------:|------:|
| a    | b      | c     |

## Figures

![A grey rectangle, the kitchen sink's figure](kitchen-sink-figure.svg "A caption under the figure.")

## Posts {posts}

## Upcoming {upcoming}

## Past {past}

## Next event {next-event}

## Members {members}
````

`tests/site/content/kitchen-sink-figure.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 120" width="320" height="120"><rect width="320" height="120" fill="#888"/></svg>
```

- [ ] **Step 4: Write the showcase and the member**

`tests/site/content/showcase/index.md`:

```markdown
---
man: FIXTURE-SHOWCASE(7)
title: Showcase
description: The sites the fixture lists as built with the documented project, as a grid.
tagline: built with it
nav: -
---

## Sites {showcase}
```

`tests/site/content/showcase/example/index.md`:

```markdown
---
title: Example site
url: https://example.org/
description: A site built with the documented project, listed in the fixture's showcase.
image: shot.svg
---

## Name

example - a showcased site
```

`tests/site/content/showcase/example/shot.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 100" width="160" height="100"><rect width="160" height="100" fill="#888"/></svg>
```

`tests/site/content/members/ada-example.md` (tilder's built-in `members` collection, for `.profiles` and a `{members}` card):

```markdown
---
title: Ada Example
description: A member of the fixture, to show a card with profile links in the theme.
first_name: Ada
last_name: Example
category: admin
github: https://github.com/example
website: https://ada.example.org/
---

## Name

ada example - a fixture member
```

- [ ] **Step 5: Run the whole suite**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest -v`
Expected: 74 tests, OK. If a contract class is reported missing, add the construct that writes it to the kitchen sink (never drop it from the check).

- [ ] **Step 6: Commit**

```bash
git add tests/site/content tests/test_kitchen_sink.py
git commit -m "test: kitchen sink and showcase fixture covering every contract class"
```

---

### Task 10: The documentation search (`search.js`)

**Files:**
- Create: `theme/search.js`, `tests/js/search-dom.js`, `tests/test_scripts.py`

**Interfaces:**
- Consumes: the markup of `layouts/doc.html` (`[data-search-index]` with `data-home`, `data-label`, `data-placeholder`, `data-none`, `data-count`) and the index records `{t, u, d, h, x}` (Task 5).
- Produces: under node (`module.exports`): `fold(s) -> str`, `prepare(index) -> list`, `search(prepared, query) -> [record]` (every word must match; weights title 8, headings 4, description 2, text 1; ties keep the index order), `MAX = 10`. In a browser: `label.doc-search-label`, `input#doc-search-input.doc-search-input` (combobox), `p.doc-search-status` (`aria-live="polite"`), `ul#doc-search-results.doc-search-results` (listbox; options `#doc-search-result-<i>`, `aria-selected`), links `data-home + u`; the container gets `data-search-ready="true"`.

- [ ] **Step 1: Write the failing tests**

`tests/js/search-dom.js` (a stand-in DOM, run by node; no package):

```js
/* Runs theme/search.js twice against a tiny stand-in for the DOM, as the
   doc layout and a {docs} list both link it, and prints what it built as
   JSON. Used by tests/test_scripts.py, under node; no dependency. */
"use strict";
var fs = require("fs");
var vm = require("vm");

function Element(tag) {
	this.nodeName = tag.toUpperCase();
	this.attrs = {};
	this.children = [];
	this.hidden = false;
	this.textContent = "";
	this.value = "";
	this.className = "";
	this.listeners = {};
}
Element.prototype.getAttribute = function (k) {
	return Object.prototype.hasOwnProperty.call(this.attrs, k) ? this.attrs[k] : null;
};
Element.prototype.setAttribute = function (k, v) { this.attrs[k] = String(v); };
Element.prototype.removeAttribute = function (k) { delete this.attrs[k]; };
Element.prototype.appendChild = function (c) { this.children.push(c); return c; };
Element.prototype.addEventListener = function (type, fn) { this.listeners[type] = fn; };
Object.defineProperty(Element.prototype, "innerHTML", {
	set: function () { this.children = []; }, get: function () { return ""; }
});

var box = new Element("div");
var words = JSON.parse(process.argv[3]);
Object.keys(words).forEach(function (k) { box.setAttribute(k, words[k]); });
var document = {
	querySelector: function (sel) { return sel === "[data-search-index]" ? box : null; },
	createElement: function (tag) { return new Element(tag); }
};
var source = fs.readFileSync(process.argv[2], "utf8");
var requested = [];
function XMLHttpRequest() {}
XMLHttpRequest.prototype.open = function (method, url) { requested.push(url); };
XMLHttpRequest.prototype.send = function () {
	this.status = 200;
	this.responseText = process.argv[4] || "[]";
	this.onload();
};
var context = { document: document, window: {}, XMLHttpRequest: XMLHttpRequest, String: String };
vm.runInNewContext(source, context);
vm.runInNewContext(source, context);
var input = box.children[1], list = box.children[3], status = box.children[2];
if (input && process.argv[5] !== undefined) {
	input.listeners.focus();
	input.value = process.argv[5];
	input.listeners.input();
}
console.log(JSON.stringify({
	requested: requested,
	status: status ? status.textContent : null,
	results: list ? list.children.map(function (li) { return li.children[0].href; }) : [],
	ready: box.getAttribute("data-search-ready"),
	children: box.children.map(function (c) {
		return { tag: c.nodeName, cls: c.className, text: c.textContent,
			placeholder: c.placeholder || null, id: c.id || null };
	})
}));
```

`tests/test_scripts.py`:

```python
"""The theme's scripts: ES5, no storage, no network but the index, no
words of their own; search.js's matching and its DOM under node, when
node is installed (no package, no framework)."""

import json
import re
import shutil
import subprocess
import unittest

from tests.helpers import REPO, THEME

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

```

- [ ] **Step 2: Run them to see them fail**

Run: `python3 -m unittest tests.test_scripts -v`
Expected: FAIL `test_there_are_scripts_to_check` (`'search.js' not found in []`); ERROR in `SearchUnderNode` (node: `Cannot find module .../theme/search.js`). If node is not installed, `SearchUnderNode` is skipped: install it (`sudo dnf install nodejs`) to run them; the plan's review requires them green once.

- [ ] **Step 3: Write the script**

`theme/search.js`:

```js
/* Documentation search. The doc layout's left column holds an empty
   <div data-search-index>: this script fills it with a labelled search
   field and a list of results, and reads the collection's index (written
   by the doc type, one per language) on first focus. Every word comes
   from the div's data-* attributes; without JavaScript nothing is shown.
   ES5, same-origin, no storage. */
(function () {
	"use strict";

	var MAX = 10;
	var WEIGHTS = [["t", 8], ["h", 4], ["d", 2], ["x", 1]];

	/* Lower case, accents removed: "Élan" and "elan" match. */
	function fold(s) {
		s = String(s).toLowerCase();
		if (s.normalize) {
			s = s.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
		}
		return s;
	}

	/* Each record's fields folded once: title, headings, description, text. */
	function prepare(index) {
		var out = [], i;
		for (i = 0; i < index.length; i++) {
			out.push({
				item: index[i],
				t: fold(index[i].t || ""),
				h: fold((index[i].h || []).join(" ")),
				d: fold(index[i].d || ""),
				x: fold(index[i].x || "")
			});
		}
		return out;
	}

	/* The records every word of the query appears in, best first: a word
	   in the title outweighs one in a heading, then the description, then
	   the text. Ties keep the index's order, the collection's. */
	function search(prepared, query) {
		var words = fold(query).split(/\s+/), hits = [], i, j, k, score, best;
		words = words.filter(function (w) { return w !== ""; });
		if (!words.length) {
			return [];
		}
		for (i = 0; i < prepared.length; i++) {
			score = 0;
			for (j = 0; j < words.length; j++) {
				best = 0;
				for (k = 0; k < WEIGHTS.length; k++) {
					if (prepared[i][WEIGHTS[k][0]].indexOf(words[j]) !== -1) {
						best = WEIGHTS[k][1];
						break;
					}
				}
				if (!best) {
					score = 0;
					break;
				}
				score += best;
			}
			if (score) {
				hits.push({ item: prepared[i].item, score: score, order: i });
			}
		}
		hits.sort(function (a, b) { return b.score - a.score || a.order - b.order; });
		return hits.map(function (h) { return h.item; });
	}

	if (typeof module === "object" && module.exports) {   /* the tests, under node */
		module.exports = { fold: fold, prepare: prepare, search: search, MAX: MAX };
		return;
	}

	var box = document.querySelector("[data-search-index]");
	/* No index on this page, or already done (the script is linked by the
	   layout and, on a page that lists docs, by the type too). */
	if (!box || !box.getAttribute("data-search-index") || box.getAttribute("data-search-ready")) {
		return;
	}
	box.setAttribute("data-search-ready", "true");

	var home = box.getAttribute("data-home") || "";
	var url = home + box.getAttribute("data-search-index");
	var countText = box.getAttribute("data-count") || "{n}";
	var noneText = box.getAttribute("data-none") || "";
	var prepared = null, loading = false, selected = -1, links = [];

	function make(tag, cls) {
		var el = document.createElement(tag);
		if (cls) {
			el.className = cls;
		}
		return el;
	}

	var label = make("label", "doc-search-label");
	var input = make("input", "doc-search-input");
	var status = make("p", "doc-search-status");
	var list = make("ul", "doc-search-results");
	label.htmlFor = "doc-search-input";
	label.textContent = box.getAttribute("data-label") || "";
	input.type = "search";
	input.id = "doc-search-input";
	input.placeholder = box.getAttribute("data-placeholder") || "";
	input.autocomplete = "off";
	input.spellcheck = false;
	input.setAttribute("role", "combobox");
	input.setAttribute("aria-autocomplete", "list");
	input.setAttribute("aria-expanded", "false");
	input.setAttribute("aria-controls", "doc-search-results");
	status.setAttribute("aria-live", "polite");
	list.id = "doc-search-results";
	list.setAttribute("role", "listbox");
	list.hidden = true;
	box.appendChild(label);
	box.appendChild(input);
	box.appendChild(status);
	box.appendChild(list);

	/* The index cannot be read (offline, blocked): the field goes away. */
	function give_up() {
		box.innerHTML = "";
		box.hidden = true;
	}

	function load() {
		if (prepared || loading) {
			return;
		}
		loading = true;
		var req = new XMLHttpRequest();
		req.open("GET", url);
		req.onload = function () {
			try {
				if (req.status !== 200) {
					throw new Error(String(req.status));
				}
				prepared = prepare(JSON.parse(req.responseText));
			} catch (e) {
				give_up();
				return;
			}
			run();
		};
		req.onerror = give_up;
		req.send();
	}

	function choose(i) {
		var items = list.children, k;
		selected = i;
		for (k = 0; k < items.length; k++) {
			items[k].setAttribute("aria-selected", k === i ? "true" : "false");
		}
		if (i >= 0) {
			input.setAttribute("aria-activedescendant", items[i].id);
		} else {
			input.removeAttribute("aria-activedescendant");
		}
	}

	function run() {
		var query = input.value, hits, i, li, a, span;
		list.innerHTML = "";
		links = [];
		selected = -1;
		input.removeAttribute("aria-activedescendant");
		if (!prepared || !query.replace(/\s+/g, "")) {
			list.hidden = true;
			input.setAttribute("aria-expanded", "false");
			status.textContent = "";
			return;
		}
		hits = search(prepared, query);
		for (i = 0; i < hits.length && i < MAX; i++) {
			li = make("li");
			li.id = "doc-search-result-" + i;
			li.setAttribute("role", "option");
			li.setAttribute("aria-selected", "false");
			a = make("a");
			a.href = home + hits[i].u;
			a.textContent = hits[i].t;
			if (hits[i].d) {
				span = make("span");
				span.textContent = hits[i].d;
				a.appendChild(span);
			}
			li.appendChild(a);
			list.appendChild(li);
			links.push(a);
		}
		list.hidden = !links.length;
		input.setAttribute("aria-expanded", links.length ? "true" : "false");
		status.textContent = hits.length ? countText.replace("{n}", String(hits.length)) : noneText;
	}

	input.addEventListener("focus", load);
	input.addEventListener("input", run);
	input.addEventListener("keydown", function (e) {
		var key = e.key || "";
		if ((key === "ArrowDown" || e.keyCode === 40) && links.length) {
			choose(selected + 1 < links.length ? selected + 1 : 0);
			e.preventDefault();
		} else if ((key === "ArrowUp" || e.keyCode === 38) && links.length) {
			choose(selected > 0 ? selected - 1 : links.length - 1);
			e.preventDefault();
		} else if ((key === "Enter" || e.keyCode === 13) && selected >= 0) {
			window.location.href = links[selected].href;
			e.preventDefault();
		} else if (key === "Escape" || key === "Esc" || e.keyCode === 27) {
			input.value = "";
			run();
		}
	});
})();
```

- [ ] **Step 4: Run the tests**

Run: `python3 -m unittest tests.test_scripts -v`
Expected: 10 tests, OK.

- [ ] **Step 5: Commit**

```bash
git add theme/search.js tests/js/search-dom.js tests/test_scripts.py
git commit -m "feat(theme): documentation search, accent-insensitive, one index per language"
```

---

### Task 11: The sidebar and contents (`nav.js`) and the copy button (`code.js`)

**Files:**
- Create: `theme/nav.js`, `theme/code.js`
- Modify: `tests/test_scripts.py` (the import line, and a `Loaded` class at the end)

**Interfaces:**
- Consumes: `[data-doc-side]`, `[data-doc-toc]`, `main .toc`, `.doc` (Task 8); `pre.code` and the `<script src="code.js" data-copy data-copied>` tag tilder writes on pages with code.
- Produces: nav.js: the sidebar `open` below 45rem only until a link is followed, always open wider; the `[TOC]` moved into `[data-doc-toc]` at 60rem and wider (`.doc--toc` on `.doc`, the slot's `hidden` removed, its `<details>` opened), put back after a comment marker when narrower. code.js: each `pre.code` wrapped in `div.code-box` with `button.code-copy` (`aria-live="polite"`), text from `data-copy`, then `data-copied` for 2 s after a copy.

- [ ] **Step 1: Write the failing tests**

In `tests/test_scripts.py`, change the import line to:

```python
from tests.helpers import REPO, THEME, fixture_build
```

and append:

```python
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
```

- [ ] **Step 2: Run them to see them fail**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest tests.test_scripts -v`
Expected: FAIL `test_code_js_on_pages_with_code_with_its_words` (tilder links `code.js` only when the theme ships it) and `test_the_three_scripts_are_served` (`code.js`).

- [ ] **Step 3: Write the scripts**

`theme/nav.js`:

```js
/* The doc layout on screens of every width. The sidebar (<details
   data-doc-side>) is open in the markup, so it works without JavaScript:
   on a small screen this script folds it, and folds it again once a link
   in it is followed. On a wide screen it moves the page's [TOC] into the
   right column (data-doc-toc) and opens it; narrower, it puts it back.
   ES5, no text of its own, no storage. */
(function () {
	"use strict";

	if (!window.matchMedia) {
		return;
	}
	var narrow = window.matchMedia("(max-width: 45rem)");
	var wide = window.matchMedia("(min-width: 60rem)");

	function watch(query, fn) {
		if (query.addEventListener) {
			query.addEventListener("change", fn);
		} else if (query.addListener) {
			query.addListener(fn);
		}
	}

	/* The sidebar: folded on small screens, always open on the others. */
	var side = document.querySelector("[data-doc-side]");
	if (side) {
		var fit = function () {
			side.open = !narrow.matches;
		};
		fit();
		watch(narrow, fit);
		side.addEventListener("click", function (e) {
			var t = e.target;
			while (t && t !== side && t.nodeName !== "A") {
				t = t.parentNode;
			}
			if (t && t.nodeName === "A" && narrow.matches) {
				side.open = false;
			}
		});
	}

	/* The [TOC]: in the right column on wide screens, in the text else. */
	var slot = document.querySelector("[data-doc-toc]");
	var toc = document.querySelector("main .toc");
	if (slot && toc) {
		var home = document.createComment("toc");
		var box = slot.parentNode;
		var details = toc.querySelector("details");
		toc.parentNode.insertBefore(home, toc);
		var place = function () {
			if (wide.matches) {
				slot.appendChild(toc);
				slot.hidden = false;
				if (details) {
					details.open = true;
				}
				box.className += /\bdoc--toc\b/.test(box.className) ? "" : " doc--toc";
			} else {
				home.parentNode.insertBefore(toc, home.nextSibling);
				slot.hidden = true;
				if (details) {
					details.open = false;
				}
				box.className = box.className.replace(/\s*\bdoc--toc\b/, "");
			}
		};
		place();
		watch(wide, place);
	}
})();
```

`theme/code.js`:

```js
/* A copy button on every code block (tilder's code.js: loaded only on
   pages with code). Its words come from its own <script> tag, data-copy
   and data-copied (labels.copy, labels.copied in site.toml). It copies the
   code as plain text, without the highlighting. ES5, no storage. */
(function () {
	"use strict";

	var me = document.currentScript || document.querySelector("script[data-copy]");
	if (!me) {
		return;
	}
	var copy = me.getAttribute("data-copy") || "";
	var copied = me.getAttribute("data-copied") || copy;

	function fallback(text, done) {
		var area = document.createElement("textarea");
		area.value = text;
		area.setAttribute("readonly", "");
		area.className = "sr-only";
		document.body.appendChild(area);
		area.select();
		try {
			if (document.execCommand("copy")) {
				done();
			}
		} catch (e) {
			/* nothing copied: the reader selects the code by hand */
		}
		document.body.removeChild(area);
	}

	function write(text, done) {
		if (navigator.clipboard && window.isSecureContext) {
			navigator.clipboard.writeText(text).then(done, function () {
				fallback(text, done);
			});
		} else {
			fallback(text, done);
		}
	}

	function add(pre) {
		var box = document.createElement("div");
		var button = document.createElement("button");
		var timer = null;
		box.className = "code-box";
		button.type = "button";
		button.className = "code-copy";
		button.textContent = copy;
		button.setAttribute("aria-live", "polite");
		pre.parentNode.insertBefore(box, pre);
		box.appendChild(pre);
		box.appendChild(button);
		button.addEventListener("click", function () {
			var code = pre.querySelector("code") || pre;
			write(code.textContent, function () {
				button.textContent = copied;
				clearTimeout(timer);
				timer = setTimeout(function () {
					button.textContent = copy;
				}, 2000);
			});
		});
	}

	if (!copy) {
		return;
	}
	var blocks = document.querySelectorAll("pre.code");
	for (var i = 0; i < blocks.length; i++) {
		add(blocks[i]);
	}
})();
```

- [ ] **Step 4: Run the tests**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest tests.test_scripts -v`
Expected: 13 tests, OK (the ES5 and rules checks now cover the three scripts).
Also: `node --check theme/nav.js && node --check theme/code.js` (syntax only), when node is installed.

- [ ] **Step 5: Commit**

```bash
git add theme/nav.js theme/code.js tests/test_scripts.py
git commit -m "feat(theme): foldable doc sidebar, contents column, copy button on code"
```

---

### Task 12: The link preview, the README and the licence; review

**Files:**
- Create: `theme/share.svg`, `theme/README.md`, `theme/LICENSE`, `tests/test_share.py`, `tests/test_readme.py`

**Interfaces:**
- Consumes: tilder's `share.svg` fields (`logo`, `manual_upper`, `wordmark`, `domain`, `card_1`, `card_2`, and any configuration value such as `share.background_color`); `tools/check-contrast.py --markdown`.
- Produces: the theme's documentation, which sub-project C links to and copies from.

- [ ] **Step 1: Write the failing tests**

`tests/test_share.py`:

```python
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
```

`tests/test_readme.py`:

```python
"""The theme's README stays true: its contrast table, its list of files,
its licence."""

import subprocess
import sys
import unittest

from tests.helpers import REPO, THEME

README = THEME / "README.md"


class Readme(unittest.TestCase):
    def test_the_contrast_table_is_the_script_s(self):
        table = subprocess.run([sys.executable, str(REPO / "tools" / "check-contrast.py"),
                                str(THEME / "style.css"), "--markdown"],
                               capture_output=True, text=True, check=True).stdout.strip()
        self.assertIn(table, README.read_text())

    def test_every_file_of_the_theme_is_named(self):
        text = README.read_text()
        for path in sorted(THEME.iterdir()):
            if path.name.startswith(".") or path.name in ("README.md", "__pycache__"):
                continue
            name = path.name + ("/" if path.is_dir() else "")
            self.assertIn(f"`{name}`", text, name)

    def test_licence(self):
        self.assertIn("MIT License", (THEME / "LICENSE").read_text())
        self.assertIn("Théau TROVA", (THEME / "LICENSE").read_text())
```

- [ ] **Step 2: Run them to see them fail**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest tests.test_share tests.test_readme -v`
Expected: ERROR (`FileNotFoundError`) for `share.svg`, `README.md`, `LICENSE`; `test_the_build_draws_it` fails on the missing `share.png` (no template, no preview).

- [ ] **Step 3: Write the link preview**

`theme/share.svg` (a man page's first lines; fonts by family name, which tilder's Docker image renders with the theme's own woff2):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
	<!-- The link preview, 1200x630, drawn to share.png at every build: a
	     man page's first lines. The double-brace fields are filled by
	     tilder from the site's configuration ([share], [site]); "logo" is
	     the site's assets/logo.svg. -->
	<rect width="1200" height="630" fill="{{ share.background_color }}"/>
	<text x="80" y="92" font-family="JetBrains Mono, monospace" font-size="24" fill="{{ share.muted_color }}">{{ manual_upper }}</text>
	<rect x="80" y="118" width="1040" height="2" fill="{{ share.rule_color }}"/>
	<image x="80" y="220" width="160" height="160" href="{{ logo }}"/>
	<text x="280" y="300" font-family="JetBrains Mono, monospace" font-weight="700" font-size="72" fill="{{ share.text_color }}"><tspan fill="{{ share.theme_color }}">~/</tspan>{{ wordmark }}</text>
	<text x="282" y="360" font-family="Inter, sans-serif" font-size="34" fill="{{ share.muted_color }}">{{ card_1 }}</text>
	<text x="282" y="406" font-family="Inter, sans-serif" font-size="34" fill="{{ share.muted_color }}">{{ card_2 }}</text>
	<rect x="80" y="510" width="1040" height="2" fill="{{ share.rule_color }}"/>
	<text x="80" y="556" font-family="JetBrains Mono, monospace" font-size="24" fill="{{ share.muted_color }}">{{ domain }}</text>
</svg>
```

- [ ] **Step 4: Write the README and the licence**

`theme/README.md`. Its last table is the output of `python3 tools/check-contrast.py theme/style.css --markdown`, pasted as is (the test compares them; regenerate it whenever a token changes):

````markdown
# A documentation theme for tilder

A theme for [tilder](https://github.com/thosted/tilder) sites that
document something: a manual with a sidebar, previous/next links and a
search, a landing page, a showcase. Every page but the landing page reads
as a man page; the landing page is airier. It names no project and holds
no site text: copy this folder into any tilder project as `theme/`.

It needs tilder 1.1.0 or later (collection navigation, `LOCALIZED_OUTPUTS`).
It speaks English and French out of the box.

## Files

| File | What |
|---|---|
| `layout.html` | the base layout: a man page (header rule, wordmark, navigation, one text column, previous/next, footer rule) |
| `layouts/` | `home.html`, the landing page (`layout: home`); `doc.html`, documentation pages (the `doc` type's layout, or `layout: doc`) |
| `style.css` | tokens, fonts, every class tilder writes (checked by `tools/check-theme.py`), light and dark |
| `fonts/` | Inter and JetBrains Mono, latin subsets, woff2, with their licences (OFL) |
| `share.svg` | the link preview, drawn to `share.png` (1200x630) |
| `code.js` | the copy button on code blocks |
| `search.js` | the documentation search, in the doc layout's sidebar |
| `nav.js` | the doc layout on small and wide screens: folds the sidebar, moves the `[TOC]` |
| `types/` | `doc.py` and `showcase.py`, the two content types below |
| `theme.toml` | the theme's words in English, and the `[share]` colours |
| `theme.fr.toml` | the theme's words in French |
| `LICENSE` | MIT |

## Using it

Declare the collections in `content/site.toml`:

```toml
[collections.docs]          # content/docs/, listed by {docs}
type = "doc"

[collections.showcase]      # content/showcase/, listed by {showcase}
type = "showcase"
```

The landing page asks for its layout: `layout: home` in its front matter.
Its `tagline` is the headline, and its first section the text under it.
A `## Features {grid}` section of `###` entries becomes cards; code
blocks in a `{grid}` section sit side by side.

### `doc`: documentation pages

| Front matter | |
|---|---|
| `title`, `description` | as on any page; the description is the card's text and the search's |
| `order` | a whole number, the page's place in the manual (default 1000; then the file name) |
| `group` | the sidebar's group, written the same way on every page of a language |

| Setting | Default | |
|---|---|---|
| `man` | `"SITE-DOCS(7)"` | the pages' man-page name |
| `nav` | `"docs/"` | the navigation entry marked current |
| `empty` | `"No page yet."` | a `{docs}` list with nothing in it |
| `index` | `"search-index.json"` | the search index, written in the collection's folder, one per language (`fr/docs/search-index.json`) |

A section marked `{docs}` lists every page, grouped. The collection's own
page (`docs/index.md`) is a plain page: give it `layout: doc` for the
sidebar, and `search_index: docs/search-index.json` for the search field.
`[TOC]` on a page goes to the right column on wide screens.

### `showcase`: sites built with the project

| Front matter | |
|---|---|
| `title` | the site's name |
| `url` | **required**, the site's address |
| `description` | one sentence |
| `image` | optional, a screenshot next to the item (`showcase/<slug>/index.md` and `showcase/<slug>/shot.png`) |
| `order` | a whole number (default 1000) |

Settings: `man` (`"SITE-SHOWCASE(7)"`), `nav` (`"showcase"`), `empty`
(`"No site listed yet."`), `visit` (`"visit ↗"`, the link on an item's
page). `{showcase}` lists every item as a grid of cards.

## The theme's words

`theme.toml` and `theme.fr.toml` hold them; a site overrides any of them
in its `site.toml` or `site.fr.toml`:

| Key | English |
|---|---|
| `search.label` | the search field's label |
| `search.placeholder` | its placeholder |
| `search.none` | a search that finds nothing |
| `search.count` | how many pages match: `{n}` is the number |
| `doc.contents` | the sidebar's summary on small screens |
| `doc.on_this_page` | over the `[TOC]` in the right column |

The rest (copy, previous, next, the sidebar's name...) are tilder's
`[labels]`.

## What the site must do

- **Declare French, or delete `theme.fr.toml`.** tilder stops on a
  `theme.<lang>.toml` of a language the site does not declare.
- **Let the search read its index.** The page's Content-Security-Policy
  needs `connect-src 'self'`; tilder's `examples/Caddyfile` has
  `default-src 'none'` and no `connect-src`, which blocks it. Without it,
  the search field removes itself and the rest of the page works.
- Ship `assets/logo.svg` (tilder draws the icons and `share.png` from it).

## Scripts

ES5, same-origin files, no storage, no cookie, no words of their own
(they arrive through `data-*`), progressive enhancement: without
JavaScript the sidebar is open, the `[TOC]` stays in the text, and there
is no search field. `tests/test_scripts.py` checks the rules, and runs
`search.js` under node when it is installed.

By hand, before a release, in a browser (the fixture built and served
over HTTP, `python3 -m http.server` in its output):

- [ ] The search field appears on a doc page; typing `elan` in French
      finds the page with "élan"; the count reads in the page's language.
- [ ] Arrow down and up move through the results; Enter follows the
      selected one; Escape clears the field.
- [ ] With the index missing (rename it), the field goes away.
- [ ] At 360px the sidebar is folded, opens on its summary, and folds
      again after a link is followed.
- [ ] At 1440px the `[TOC]` is in the right column, open, and follows
      the scroll; at 800px it is back in the text, folded.
- [ ] The copy button copies a code block without the language label;
      its word changes to "copied", then back.
- [ ] With JavaScript off, every page reads completely.

## Review by eye

`tests/site/content/kitchen-sink.md` uses every construct; the fixture as
a whole writes every class of tilder's contract but `.icon` (no network
icons are shipped). Review it in light and dark, at 360px and 1440px.

## Fonts

Self-hosted, never from a CDN. Latin and Latin Extended, subset from the
official releases with fonttools' `pyftsubset`; neither licence declares a
Reserved Font Name, so the subsets keep their names.

| Files | Upstream | Licence |
|---|---|---|
| `inter-regular.woff2`, `inter-italic.woff2`, `inter-bold.woff2` | Inter 4.1, `web/Inter-*.woff2` of `Inter-4.1.zip`, github.com/rsms/inter/releases | `fonts/OFL-Inter.txt` (the release's `LICENSE.txt`) |
| `jetbrains-mono-regular.woff2`, `jetbrains-mono-bold.woff2` | JetBrains Mono 2.304, `fonts/webfonts/*.woff2` of `JetBrainsMono-2.304.zip`, github.com/JetBrains/JetBrainsMono/releases | `fonts/OFL-JetBrainsMono.txt` (the release's `OFL.txt`) |

Unicode ranges kept: `U+0000-024F, U+0259, U+02BB-02BC, U+02C6, U+02DA,
U+02DC, U+0300-036F, U+1E00-1EFF, U+2000-206F, U+20A0-20C0, U+2100-214F,
U+2190-21FF, U+2212, U+2215, U+2500-257F, U+25A0-25FF, U+FEFF, U+FFFD`.

## Contrast

Every text colour on both backgrounds, in both schemes, WCAG AA (4.5:1).
`tools/check-contrast.py theme/style.css --markdown` prints this table;
a test keeps it in step.

| scheme | foreground | background | ratio | minimum |
|---|---|---|---:|---:|
| light | `--text` | `--bg` | 16.26 | 4.5 |
| light | `--text` | `--surface` | 14.62 | 4.5 |
| light | `--muted` | `--bg` | 7.25 | 4.5 |
| light | `--muted` | `--surface` | 6.51 | 4.5 |
| light | `--faint` | `--bg` | 5.93 | 4.5 |
| light | `--faint` | `--surface` | 5.33 | 4.5 |
| light | `--accent` | `--bg` | 5.65 | 4.5 |
| light | `--accent` | `--surface` | 5.08 | 4.5 |
| light | `--info` | `--bg` | 5.65 | 4.5 |
| light | `--info` | `--surface` | 5.08 | 4.5 |
| light | `--warning` | `--bg` | 6.22 | 4.5 |
| light | `--warning` | `--surface` | 5.59 | 4.5 |
| light | `--error` | `--bg` | 6.36 | 4.5 |
| light | `--error` | `--surface` | 5.72 | 4.5 |
| dark | `--text` | `--bg` | 14.62 | 4.5 |
| dark | `--text` | `--surface` | 13.11 | 4.5 |
| dark | `--muted` | `--bg` | 8.34 | 4.5 |
| dark | `--muted` | `--surface` | 7.48 | 4.5 |
| dark | `--faint` | `--bg` | 6.48 | 4.5 |
| dark | `--faint` | `--surface` | 5.81 | 4.5 |
| dark | `--accent` | `--bg` | 9.34 | 4.5 |
| dark | `--accent` | `--surface` | 8.37 | 4.5 |
| dark | `--info` | `--bg` | 9.34 | 4.5 |
| dark | `--info` | `--surface` | 8.37 | 4.5 |
| dark | `--warning` | `--bg` | 9.16 | 4.5 |
| dark | `--warning` | `--surface` | 8.21 | 4.5 |
| dark | `--error` | `--bg` | 8.36 | 4.5 |
| dark | `--error` | `--surface` | 7.50 | 4.5 |
````

`theme/LICENSE`:

```text
MIT License

Copyright (c) 2026 Théau TROVA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 5: Run the whole suite and the build by hand**

Run: `TILDER_BUILD=/home/theau/Git/tilder/build.py python3 -m unittest -v`
Expected: 93 tests, OK, none skipped when node is installed.

Build the fixture by hand for review:

```bash
review=$(mktemp -d)
cp -r tests/site "$review/site" && cp -r theme "$review/site/theme"
TILDER_BUILD=/home/theau/Git/tilder/build.py ./build.sh --root "$review/site" --out "$review/out"
grep -rn 'Rechercher' "$review/out/fr/docs/cli.html" | head -1     # the French words
awk '{ if (length($0) > 75) print FILENAME }' $(find "$review/out/txt" -name '*.txt') ; echo "(expected: nothing)"
```

Expected: `theme: 69 classes...`, `contrast: 28 pairs...`, tilder's summary, no `warning:` line.

- [ ] **Step 6: Review by eye (owner)**

Serve the review build: `(cd "$review/out" && python3 -m http.server 8000)`, then open `http://localhost:8000/kitchen-sink.html`, `/docs/start.html`, `/fr/docs/cli.html`, `/docs/`, `/showcase/`, `/` in light and dark, at 360px and 1440px, and walk the README's "Scripts" check list. Screenshots headless, if useful: `firefox --headless --window-size=1440,1000 --screenshot "$review/doc.png" http://localhost:8000/docs/start.html` (and `380,1400` for the phone width). Record anything to fix as a follow-up task; do not change the plan's tests to fit a bug.

- [ ] **Step 7: Commit**

```bash
git add theme/share.svg theme/README.md theme/LICENSE tests/test_share.py tests/test_readme.py
git commit -m "docs(theme): link preview, README with contrast ratios, MIT licence"
```

---

## Self-review

- **Spec coverage.** §1 generic, bilingual, hybrid: Global Constraints, Tasks 7-8. §2 rules: Tasks 4 (every class, a11y), 10-11 (scripts), 3 (fonts), 7 (layout invariants). §3 files: every file has a task (README/LICENSE/share.svg Task 12). §4 layouts: Tasks 7-8, `nav.js` Task 11 (Resolution 8). §5 look: tokens, type, live examples, home grid and panes: Task 4, fixture Tasks 8-9 (Resolution 3). §6 `doc`: Task 5 (Resolutions 4-7, 10). §7 `showcase`: Task 6 (Resolution 9). §8 scripts: Tasks 10-11. §9 words: Task 7, tested in both languages in Task 8. §10 checks: `check-theme.py` Task 1 (in `build.sh`, Task 7), kitchen sink Task 9 (Resolution 14), no warning Task 7, `check-contrast.py` Task 2 with the README table Task 12.
- **Placeholders.** Every code step holds the file; the only copied-in content is `tools/tilder-theme.md` (tilder's file, by command) and the fonts (upstream, by command).
- **Names across tasks.** `search_index` (Task 5 `defaults`, Task 8 `doc.html`, fixture `docs/index.md`); `data-doc-side` / `data-doc-toc` / `.doc--toc` (Tasks 4, 8, 11); `doc-search-*` classes (Tasks 4, 10); `code-box` / `code-copy` (Tasks 4, 11); `entry--group` (Tasks 4, 5), `entry--example` (Tasks 4, 9); `load_tool`, `load_type`, `STUB`, `Build`, `fixture_build` (Tasks 1, 5, 7).
- **Review Focus.** Each of the five lines names its test and its task.
- **Verified before writing.** Every file and test of this plan was run against tilder `main` (v1.1.0 features) on 2026-09-27: 93 tests OK, the fixture built with no warning, the font archives' paths and licences checked, the pages looked at headless at 1440px and 380px.
