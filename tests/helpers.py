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
