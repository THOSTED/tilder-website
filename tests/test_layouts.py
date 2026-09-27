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
