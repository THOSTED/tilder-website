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
        self.assertEqual(showcase.DEFAULTS, {"man": "SITE-SHOWCASE(7)", "nav": "showcase/",
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
