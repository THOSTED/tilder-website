"""The theme's README stays true: its contrast table, its list of files,
its licence."""

import unittest

from tests.helpers import THEME, builder_missing, project, tilder

README = THEME / "README.md"


class Readme(unittest.TestCase):
    def test_the_contrast_table_is_tilder_s(self):
        why = builder_missing()
        if why:
            self.skipTest(why)
        done = tilder(project(), "--check", "--markdown")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("| scheme | foreground |", done.stdout)
        self.assertIn(done.stdout.strip(), README.read_text())

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
