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
