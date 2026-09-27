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
