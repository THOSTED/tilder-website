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
