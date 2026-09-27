"""The fixture shows every class of tilder's contract, so the theme is
reviewed on all of them (README.md, "Review by eye")."""

import re
import unittest

from tests.helpers import contract_classes, fixture_build

# Written only when the theme ships icons/<network>.svg; this theme ships none.
NOT_SHOWN = {"icon"}


class KitchenSink(unittest.TestCase):
    def setUp(self):
        self.build = fixture_build(self)

    def test_every_contract_class_appears_in_the_fixture(self):
        classes = contract_classes()
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
