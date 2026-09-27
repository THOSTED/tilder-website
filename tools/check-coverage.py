"""Coverage check: the site's documentation (content/docs/) must name every
key, setting, front-matter key, class, placeholder and CLI option of the
pinned tilder tree.

A "term" is one of these facts of tilder (a namedtuple Term(kind, name,
groups)); it is "covered" when some one documentation file contains, for at
least one of its `groups` (a list of alternative regex lists), every regex
of that group. Facts come from:

- defaults.toml: every table, leaf key and array-of-tables (tomllib).
- types/*.py: every key of each type's DEFAULTS dict.
- docs/markdown.md: the front-matter keys of its "Front matter" table.
- docs/theme.md: the classes of its "The HTML the builder writes" table
  (or, from tilder 1.2, CLASSES of src/contract.py), and the placeholders
  of its `layout.html` table.
- src/build.py: every `--option` found in a string constant (its docstring
  included).

Run against a tilder checkout or an image's tree copied out to a folder:

    python3 tools/check-coverage.py --tilder /path/to/tilder [--docs DIR]

`--tilder` is required: a checkout's directory (see Recipe C in the plan's
globals.md for extracting one from a tag with `git archive`), or `/tilder`
copied out of the pinned Docker image. `--docs` defaults to this
repository's content/docs. Exit 0 when every term is documented in both
English and French docs, 1 when a term is missing (each is named on
stderr), 2 when a required tilder or docs input is missing.
"""

import argparse
import ast
import collections
import pathlib
import re
import sys
import tomllib

Term = collections.namedtuple("Term", "kind name groups")

REPO = pathlib.Path(__file__).resolve().parent.parent


# --- regex helpers ---------------------------------------------------------

def lit(s):
    """A literal `s`, with a boundary before/after when the edge character
    could otherwise glue to more identifier text."""
    out = re.escape(s)
    if s and re.match(r"[\w.-]", s[0]):
        out = r"(?<![\w.-])" + out
    if s and re.match(r"[\w-]", s[-1]):
        out = out + r"(?![\w-])"
    return out


def code(k):
    """`k` in backticks, or as a TOML line (key = ...) in a code block."""
    e = re.escape(k)
    return rf"(?:`{e}`|(?m:^[ \t]*{e}[ \t]*=))"


# --- markdown table helper --------------------------------------------------

def _table_rows(md, heading):
    """Data rows (each a list of cell strings) of the first markdown table
    found right after the given heading line, until the next heading or the
    end of the text. The header row and the `|---|---|` separator are not
    included."""
    lines = md.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    if start is None:
        return []
    rows = []
    in_table = False
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        if not in_table:
            in_table = True
            continue
        rows.append(cells)
    return rows


# --- term extraction --------------------------------------------------------

def _kind(value):
    if isinstance(value, dict):
        return "table"
    if isinstance(value, list) and value and all(isinstance(v, dict) for v in value):
        return "array"
    return "leaf"


def defaults_terms(text):
    data = tomllib.loads(text)
    terms = []

    def walk(table, path):
        leaves, subtables, arrays = [], [], []
        for k, v in table.items():
            kind = _kind(v)
            if kind == "table":
                subtables.append((k, v))
            elif kind == "array":
                arrays.append((k, v))
            else:
                leaves.append((k, v))

        if path:
            bracket = f"[{path}]"
            if leaves or not (leaves or subtables or arrays):
                terms.append(Term("table", bracket, [[lit(bracket)]]))
            for k, v in leaves:
                name = f"{path}.{k}"
                terms.append(Term("key", name,
                                   [[lit(name)], [lit(bracket), code(k)]]))
        else:
            for k, v in leaves:
                terms.append(Term("key", k, [[lit(k)]]))

        for k, v in subtables:
            walk(v, f"{path}.{k}" if path else k)

        for k, v in arrays:
            newpath = f"{path}.{k}" if path else k
            bracket = f"[[{newpath}]]"
            terms.append(Term("table", bracket, [[lit(bracket)]]))
            keys = []
            for item in v:
                for kk, vv in item.items():
                    if _kind(vv) == "leaf" and kk not in keys:
                        keys.append(kk)
            for kk in keys:
                name = f"{newpath}.{kk}"
                terms.append(Term("key", name,
                                   [[lit(name)], [lit(bracket), code(kk)]]))

    walk(data, "")
    return terms


def type_terms(types_dir):
    terms = []
    for path in sorted(pathlib.Path(types_dir).glob("*.py")):
        stem = path.stem
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            if not any(isinstance(t, ast.Name) and t.id == "DEFAULTS" for t in node.targets):
                continue
            defaults = ast.literal_eval(node.value)
            for key in defaults:
                terms.append(Term("setting", f"{stem}.{key}", [[code(key)]]))
    return terms


def front_matter_terms(markdown_md):
    terms = []
    for row in _table_rows(markdown_md, "## Front matter"):
        for word in re.findall(r"`([^`]+)`", row[0]):
            terms.append(Term("front matter", word, [[code(word)]]))
    return terms


def class_terms(theme_md, contract_py):
    names = []
    if contract_py is not None:
        tree = ast.parse(contract_py)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            if not any(isinstance(t, ast.Name) and t.id == "CLASSES" for t in node.targets):
                continue
            names.extend(ast.literal_eval(node.value))
    else:
        for row in _table_rows(theme_md, "## The HTML the builder writes"):
            cell = row[0]
            found = re.findall(r"\.([a-z][a-z0-9-]*)", cell)
            names.extend(found)
            base = None
            for n in found:
                if "--" in n:
                    base = n.split("--", 1)[0]
            for m in re.finditer(r"(?<![\w.])--([a-z][a-z0-9-]*)", cell):
                if base:
                    names.append(f"{base}--{m.group(1)}")

    seen, terms = set(), []
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        terms.append(Term("class", name, [[r"\." + re.escape(name) + r"(?![\w-])"]]))
    return terms


def placeholder_terms(theme_md):
    terms = []
    for row in _table_rows(theme_md, "## `layout.html`"):
        for name in re.findall(r"\{\{ ?([a-z_]+) ?\}\}", row[0]):
            terms.append(Term("placeholder", name,
                               [[r"\{\{\s*" + re.escape(name) + r"\s*\}\}"]]))
    return terms


def option_terms(build_py):
    tree = ast.parse(build_py)
    seen, terms = set(), []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for m in re.finditer(r"(?<![\w-])(--[a-z][a-z-]*[a-z])", node.value):
                opt = m.group(1)
                if opt not in seen:
                    seen.add(opt)
                    terms.append(Term("option", opt, [[lit(opt)]]))
    return terms


def docs_texts(docs_dir):
    out = {"en": [], "fr": []}
    for path in sorted(pathlib.Path(docs_dir).rglob("*.md")):
        lang = "fr" if path.name.endswith(".fr.md") else "en"
        out[lang].append(path.read_text(encoding="utf-8"))
    return out


def covered(term, texts):
    for group in term.groups:
        for text in texts:
            if all(re.search(rx, text) for rx in group):
                return True
    return False


# --- entry point -------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(
        description="the documentation names every term of the pinned tilder")
    parser.add_argument("--tilder", required=True)
    parser.add_argument("--docs", default=str(REPO / "content" / "docs"))
    args = parser.parse_args(argv)

    tilder = pathlib.Path(args.tilder)
    docs_dir = pathlib.Path(args.docs)

    required = [
        tilder / "defaults.toml",
        tilder / "docs" / "theme.md",
        tilder / "docs" / "markdown.md",
        tilder / "src" / "build.py",
        tilder / "types",
        docs_dir,
    ]
    for path in required:
        if not path.exists():
            print(f"error: check-coverage: {path} not found", file=sys.stderr)
            return 2

    contract_path = tilder / "src" / "contract.py"
    contract_py = contract_path.read_text(encoding="utf-8") if contract_path.is_file() else None

    terms = (
        defaults_terms((tilder / "defaults.toml").read_text(encoding="utf-8"))
        + type_terms(tilder / "types")
        + front_matter_terms((tilder / "docs" / "markdown.md").read_text(encoding="utf-8"))
        + class_terms((tilder / "docs" / "theme.md").read_text(encoding="utf-8"), contract_py)
        + placeholder_terms((tilder / "docs" / "theme.md").read_text(encoding="utf-8"))
        + option_terms((tilder / "src" / "build.py").read_text(encoding="utf-8"))
    )

    texts = docs_texts(docs_dir)
    missing = 0
    for lang in ("en", "fr"):
        for term in terms:
            if not covered(term, texts.get(lang, [])):
                print(f"error: coverage: {lang}: {term.kind} {term.name} is not documented",
                      file=sys.stderr)
                missing += 1

    if missing:
        print(f"error: coverage: {missing} missing", file=sys.stderr)
        return 1

    print(f"coverage: {len(terms)} terms, all documented in en and fr")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
