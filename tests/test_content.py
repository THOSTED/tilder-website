"""The site's content: every page has its French twin, links reach only
allowed hosts, code blocks name only languages tilder highlights."""

import pathlib
import re
import unittest

from tests.helpers import REPO

CONTENT = REPO / "content"
ENGLISH_ONLY = {"kitchen-sink.md"}          # the theme's test page (ledger Ruling)
ALLOWED = re.compile(r"https?://(tilder\.thosted\.fr|github\.com/THOSTED/tilder"
                     r"|([\w-]+\.)*example\.(org|com|net)|[\w.-]+\.example|localhost)"
                     r"(?=[/:)\s`\"'>]|$)")
URL = re.compile(r"https?://[^\s)`\"'>]+")
FENCE = re.compile(r"^[ \t]*(`{3,})([^`\n]*)$", re.M)
# Every name src/highlight.py accepts at v1.1.0: its LANGS keys, ALIASES
# keys (aliases resolving to a LANGS entry), SPECIAL (handled line by
# line: console, diff, text, plain, txt) and SPECIAL_ALIASES keys; plus ""
# for a bare/closing fence, which is not a language at all.
LANGS = {"", "sh", "bash", "shell", "zsh", "console", "shell-session", "terminal", "python",
         "py", "toml", "ini", "cfg", "systemd", "yaml", "yml", "json", "html", "xml", "svg",
         "css", "js", "javascript", "ts", "typescript", "node", "make", "makefile", "caddy",
         "caddyfile", "conf", "nginx", "dockerfile", "docker", "containerfile", "diff", "patch",
         "text", "plain", "txt", "sql", "c", "h", "cpp", "c++", "go", "golang", "rust", "rs",
         "postgres", "postgresql"}


def pages():
    return sorted(p for p in CONTENT.rglob("*.md") if not p.name.startswith("_"))


def toml_pages():
    return sorted(CONTENT.glob("site*.toml"))


def front(path):
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    return dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l) if m else {}


class Content(unittest.TestCase):
    def test_every_english_page_has_its_french_twin(self):
        for p in pages():
            if p.name.endswith(".fr.md") or p.name in ENGLISH_ONLY:
                continue
            twin = p.with_name(p.name[:-3] + ".fr.md")
            self.assertTrue(twin.is_file(), f"{p.relative_to(REPO)} has no {twin.name}")

    def test_every_french_page_has_its_english_original(self):
        for p in pages():
            if p.name.endswith(".fr.md"):
                self.assertTrue(p.with_name(p.name[:-6] + ".md").is_file(), p.name)

    def test_twins_share_their_order_and_layout(self):
        for p in pages():
            if not p.name.endswith(".fr.md"):
                continue
            en, fr = front(p.with_name(p.name[:-6] + ".md")), front(p)
            for key in ("order", "layout", "nav"):
                self.assertEqual(en.get(key, "").strip(), fr.get(key, "").strip(),
                                 f"{p.relative_to(REPO)}: {key}")

    def test_links_reach_only_allowed_hosts(self):
        for p in pages() + toml_pages():
            for url in URL.findall(p.read_text(encoding="utf-8")):
                self.assertRegex(url, ALLOWED, f"{p.relative_to(REPO)}: {url}")

    def test_code_blocks_name_a_language_tilder_knows(self):
        for p in pages():
            for _, lang in FENCE.findall(p.read_text(encoding="utf-8")):
                self.assertIn(lang.strip().lower(), LANGS, f"{p.relative_to(REPO)}: {lang}")
