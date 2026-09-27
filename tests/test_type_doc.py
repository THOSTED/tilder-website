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

# A fenced block indented under an entry (`### Rendered {example}`): the
# closing fence shares the opening one's indent, not column 0.
INDENTED_FENCE = """---
title: Guide
---

## Name

before the fence

### An example {example}

  ```toml
  ## not a heading
  secret_code = 1
  ```

after the fence
"""

# A `{text}` section: rendered in the text mirror only, never in the HTML
# page, so it must not be searchable either.
TEXT_ONLY_SECTION = """---
title: Guide
---

## Visible

visible words here

## Hidden {text}

secretword only for the text mirror

## After

after words here
"""


def item(slug, src=None, **meta):
    meta.setdefault("title", slug.title())
    return {"slug": slug, "meta": meta, "path": f"docs/{slug}.html", "src": src,
            "section": slug.rpartition("/")[0]}


class Attributes(unittest.TestCase):
    def test_the_type_s_contract(self):
        self.assertEqual(doc.NAME, "doc")
        self.assertTrue(doc.ARTICLE)
        self.assertTrue(doc.SEQUENTIAL)
        self.assertTrue(doc.LOCALIZED_OUTPUTS)
        self.assertEqual(doc.LAYOUT, "doc")
        self.assertEqual(doc.SCRIPT, "search.js")
        self.assertEqual(doc.DEFAULTS, {"man": "SITE-DOCS(7)", "nav": "docs/",
                                        "empty": "No page yet.", "index": "search-index.json",
                                        "recursive": True})

    def test_a_docs_collection_reads_its_subfolders(self):
        # tilder 1.2: content/docs/guide/writing.md is the item guide/writing.
        self.assertIs(doc.DEFAULTS["recursive"], True)


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

    def test_docs_lists_by_section_when_the_pages_have_sections(self):
        # tilder's depth-first order, kept: a section's own page (the item
        # whose slug is the section) opens it, then its pages; a section in
        # a section is a section of its own; group: is not used.
        its = [item("start"), item("guide", title="The guide"), item("guide/one", group="X"),
               item("guide/two"), item("ref", title="Reference"), item("ref/cli", title="Cli"),
               item("ref/cli/opts"), item("ref/seo"), item("cli", group="X")]
        out = doc.MARKERS["docs"](its, {"empty": ""})
        self.assertEqual([(it["slug"], cls) for it, cls in out["items"]],
                         [("start", []), ("guide", ["group"]), ("guide/one", []),
                          ("guide/two", []), ("ref", ["group"]), ("ref/cli", ["group"]),
                          ("ref/cli/opts", []), ("ref/seo", ["group"]), ("cli", ["group"])])
        cards = [doc.entry(it, True, {})["meta"] for it, _ in out["items"]]
        self.assertEqual(cards, [[], ["The guide"], ["The guide"], ["The guide"],
                                 ["Reference"], ["Cli"], ["Cli"], ["Reference"], []])

    def test_a_section_without_its_own_page_is_named_by_its_folder(self):
        its = [item("start"), item("misc/a"), item("misc/b")]
        out = doc.MARKERS["docs"](its, {"empty": ""})
        self.assertEqual([cls for _, cls in out["items"]], [[], ["group"], []])
        self.assertEqual([doc.entry(it, True, {})["meta"] for it, _ in out["items"]],
                         [[], ["misc"], ["misc"]])

    def test_the_marker_leaves_the_items_as_they_are(self):
        its = [item("guide"), item("guide/one")]
        before = [dict(it, meta=dict(it["meta"])) for it in its]
        doc.MARKERS["docs"](its, {"empty": ""})
        self.assertEqual(its, before)


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

    def test_an_indented_fence_under_an_entry_leaks_no_code(self):
        # The closing fence shares the opening one's indent (not column 0):
        # the whole block, not just its first line, must be dropped.
        self.assertEqual(doc.headings(INDENTED_FENCE), ["Name"])
        text = doc.plain(INDENTED_FENCE)
        self.assertNotIn("secret_code", text)
        self.assertNotIn("not a heading", text)
        self.assertIn("before the fence", text)
        self.assertIn("after the fence", text)

    def test_text_only_sections_are_excluded_from_headings_and_text(self):
        self.assertEqual(doc.headings(TEXT_ONLY_SECTION), ["Visible", "After"])
        text = doc.plain(TEXT_ONLY_SECTION)
        self.assertNotIn("secretword", text)
        self.assertIn("visible words here", text)
        self.assertIn("after words here", text)
