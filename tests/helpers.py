"""What the theme's tests share: load a tool or a theme type as a module,
and build or check the fixture site (tests/site) with the theme through
tilder, the way the Makefile runs it.

Standard library only. The build needs tilder: TILDER_BUILD pointing to a
checkout's build.py, or the pinned Docker image already pulled (DOCKER
picks another engine). Without either, the build tests are skipped, and
say why."""

import atexit
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import types
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
THEME = REPO / "theme"
FIXTURE = REPO / "tests" / "site"


def load_tool(name):
    """tools/<name>.py ("check-coverage") as a module."""
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


def image():
    """The pinned image, ghcr.io/thosted/tilder:<TILDER_VERSION>."""
    version = (REPO / "TILDER_VERSION").read_text().strip().removeprefix("v")
    return f"ghcr.io/thosted/tilder:{version}"


def builder_missing():
    """Why the fixture cannot be built here, or None when it can."""
    local = os.environ.get("TILDER_BUILD")
    if local:
        return None if pathlib.Path(local).is_file() else f"TILDER_BUILD={local} is not a file"
    engine = os.environ.get("DOCKER", "docker")
    if not shutil.which(engine):
        return f"no TILDER_BUILD and no {engine}"
    found = subprocess.run([engine, "image", "inspect", image()], capture_output=True)
    return None if found.returncode == 0 else f"no TILDER_BUILD and no local image {image()} ({engine} pull {image()})"


def tilder(root, *args, out=None):
    """Run tilder on the project at `root` (--root), with `args` (--check),
    into `out` when given (--out): the Makefile's $(RUN) $(OUTARG)."""
    local = os.environ.get("TILDER_BUILD")
    if local:
        argv = [sys.executable, "-B", local, "--root", str(root)]
        if out is not None:
            argv += ["--out", str(out)]
    else:
        argv = [os.environ.get("DOCKER", "docker"), "run", "--rm",
                "-u", f"{os.getuid()}:{os.getgid()}", "-v", f"{root}:/site:ro"]
        if out is not None:
            pathlib.Path(out).mkdir(parents=True, exist_ok=True)
            argv += ["-v", f"{out}:/out"]
        argv += [image(), "python3", "-B", "/tilder/build.py", "--root", "/site"]
        if out is not None:
            argv += ["--out", "/out"]
    return subprocess.run(argv + list(args), capture_output=True, text=True)


def contract_classes():
    """CLASSES of the tilder that builds: every class it writes
    (src/contract.py of the checkout, or of the image)."""
    local = os.environ.get("TILDER_BUILD")
    if local:
        source = (pathlib.Path(local).resolve().parent / "src" / "contract.py").read_text()
    else:
        source = subprocess.run([os.environ.get("DOCKER", "docker"), "run", "--rm", image(),
                                 "cat", "/tilder/src/contract.py"],
                                capture_output=True, text=True, check=True).stdout
    scope = {}
    exec(compile(source, "contract.py", "exec"), scope)
    return list(scope["CLASSES"])


def project(extra=None):
    """A throwaway project: the fixture with theme/ copied in (tests/site
    ships no theme of its own), plus `extra` ({path: text}). Its folder."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="theme-test-"))
    atexit.register(shutil.rmtree, tmp, True)
    root = tmp / "site"
    shutil.copytree(FIXTURE, root)
    shutil.copytree(THEME, root / "theme")
    for rel, text in (extra or {}).items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    return root


class Build:
    """One build of the fixture: returncode, stdout, stderr, and the output
    folder (out). read(path) is an output file as text."""

    def __init__(self, extra=None):
        root = project(extra)
        self.out = root.parent / "out"
        done = tilder(root, out=self.out)
        self.returncode, self.stdout, self.stderr = done.returncode, done.stdout, done.stderr

    def read(self, path):
        return (self.out / path).read_text(encoding="utf-8")


_BUILT = []


def fixture_build(test):
    """The fixture, built once per run with the theme as it is; skips the
    test when no tilder is at hand."""
    why = builder_missing()
    if why:
        raise unittest.SkipTest(why)
    if not _BUILT:
        _BUILT.append(Build())
    build = _BUILT[0]
    test.assertEqual(build.returncode, 0, build.stderr)
    return build
