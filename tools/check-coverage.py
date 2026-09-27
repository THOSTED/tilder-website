"""Coverage check: the site's documentation (content/docs/) must name every
key, setting, front-matter key, class, placeholder and CLI option of the
pinned tilder tree.

A "term" is one of these facts of tilder (a namedtuple Term(kind, name,
groups)); it is "covered" when some one documentation file contains, for at
least one of its `groups` (a list of alternative regex lists), every regex
of that group. A class needs its dot and a real boundary (not glued to a
longer dotted name, e.g. `labels.nav`), except through the handful of
element/chain prefixes the contract's own markup uses (`.b.grid`,
`pre.code`). A type's setting needs either its dotted name, or its bare key
together with a mention of its own type in the same file (a bare key alone
would just as well cover another type's key of the same name). Facts come
from:

- defaults.toml: every table, leaf key and array-of-tables (tomllib).
- types/*.py: every key of each type's DEFAULTS dict.
- Front-matter keys, from several sources, merged by name:
  - docs/markdown.md: its "Front matter" table (every page), its
    "Collections" table (the per-type fields: `author`, `place`...) and
    its "Members" table (`first_name`, `pronouns`...) - each picked out,
    among any other table under the same heading, by its header ("Key" or
    "Field");
  - docs/seo.md: its "What contributors control" table (`image_alt`,
    `updated`, `robots`...);
  - docs/types.md: the collection-config keys of its "keys a collection
    may set" paragraph (`dir`, `nav_label`) - prose, not a table;
  - src/*.py and types/*.py: every literal key read from a page's `meta`
    dict (`meta.get("k"`, `meta["k"]`), across tilder's own modules (a
    theme adds its own types/*.py). A key the code only ever *assigns*
    (`meta["k"] = ...`, e.g. the builder's own computed `_dir`) is not a
    front-matter key a person writes, and is excluded, along with any
    key starting with `_`.
- docs/theme.md: the classes of its "The HTML the builder writes" table
  (or, from tilder 1.2, CLASSES of src/contract.py), and the placeholders
  of its `layout.html` table.
- src/build.py: every `--option`, and `-h`, found in a string constant
  (its docstring included).

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

def _tables_under(md, heading):
    """Every markdown table under the given heading line, until the next
    heading or the end of the text, as (header cells, data rows) pairs -
    a heading section may hold more than one table."""
    lines = md.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    if start is None:
        return []
    tables = []
    header, rows = None, None
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        stripped = line.strip()
        if not stripped.startswith("|"):
            if header is not None:
                tables.append((header, rows))
                header, rows = None, None
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue  # the `|---|---|` separator
        if header is None:
            header, rows = cells, []
        else:
            rows.append(cells)
    if header is not None:
        tables.append((header, rows))
    return tables


def _table_rows(md, heading, first_header=None):
    """Data rows (each a list of cell strings) of a table under the given
    heading: the first one found, or, when given, the first whose header's
    first cell is `first_header` (a heading may hold more than one table,
    e.g. docs/markdown.md's "Collections")."""
    for header, rows in _tables_under(md, heading):
        if first_header is None or (header and header[0] == first_header):
            return rows
    return []


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


def _type_mention(stem):
    """A mention of the type itself in the same file as its setting's key:
    the type's name in backticks, or a TOML `type = "<stem>"` line (as a
    [collections.*] example would show it)."""
    e = re.escape(stem)
    return rf'(?:`{e}`|type[ \t]*=[ \t]*"{e}")'


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
                name = f"{stem}.{key}"
                # A bare key in backticks is not enough - it would cover
                # any type's key of the same name. Covered by the dotted
                # name, or by the key together with a mention of its own
                # type, in one file.
                terms.append(Term("setting", name,
                                   [[lit(name)], [code(key), _type_mention(stem)]]))
    return terms


def _key_table_terms(md, heading, first_header):
    terms = []
    for row in _table_rows(md, heading, first_header):
        for word in re.findall(r"`([^`]+)`", row[0]):
            terms.append(Term("front matter", word, [[code(word)]]))
    return terms


def front_matter_terms(markdown_md):
    """Front-matter keys of docs/markdown.md: its "Front matter" table
    (every page), plus the per-type fields of its "Collections" table
    ("every front-matter key read by the builder") and its "Members"
    table - each a "key table" (first column "Key" or "Field"), picked
    out from any other table under the same heading by that header."""
    return (_key_table_terms(markdown_md, "## Front matter", "Key")
            + _key_table_terms(markdown_md, "## Collections", "Field")
            + _key_table_terms(markdown_md, "## Members", "Field"))


def seo_front_matter_terms(seo_md):
    """Front-matter keys of docs/seo.md's "What contributors control"
    table (`image_alt`, `updated`, `robots`... some already named by
    docs/markdown.md; duplicates are harmless, main() merges by name)."""
    return _key_table_terms(seo_md, "## What contributors control", "Field")


def collection_key_terms(types_md):
    """The collection-config keys named in docs/types.md's "keys a
    collection may set" paragraph (`dir`, `nav_label`): not a table - a
    sentence - so found by anchoring on it and taking every backticked,
    all-lowercase word in its paragraph. `` `DEFAULTS` `` (the type's own
    settings dict, already covered by type_terms) is not taken: it is
    not all-lowercase."""
    m = re.search(r"keys a collection may set are.*?\n\n", types_md, re.S)
    if not m:
        return []
    return [Term("front matter", w, [[code(w)]])
            for w in re.findall(r"`([a-z_]+)`", m.group(0))]


def _meta_key(node):
    """The literal string key of `meta[...]` or `meta.get(...)`, else
    None (a dynamic key, e.g. a loop variable, is not a documentable
    literal)."""
    if (isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name)
            and node.value.id == "meta" and isinstance(node.slice, ast.Constant)
            and isinstance(node.slice.value, str)):
        return node.slice.value, isinstance(node.ctx, ast.Store)
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get" and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "meta" and node.args
            and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str)):
        return node.args[0].value, False
    return None


def meta_read_terms(pytexts):
    """Front-matter keys the code reads from a page's `meta` dict, across
    tilder's own modules (src/*.py, types/*.py; a theme's own types/*.py
    would add its own): a literal string given to `meta.get(...)` or read
    from `meta[...]`. A key the code itself assigns (`meta["k"] = ...`,
    e.g. the builder's own computed `_dir`) is the builder setting it,
    not a front-matter key a person writes - excluded, along with any
    key starting with `_` (tilder's own convention for such internal,
    computed fields), belt and suspenders."""
    read, written = set(), set()
    for text in pytexts:
        for node in ast.walk(ast.parse(text)):
            found = _meta_key(node)
            if found is None:
                continue
            key, is_write = found
            (written if is_write else read).add(key)
    names = sorted(k for k in read - written if not k.startswith("_"))
    return [Term("front matter", k, [[code(k)]]) for k in names]


def _merge_terms(terms):
    """`terms`, with same-named same-kind entries merged (their `groups`
    unioned): the same front-matter key may be named by more than one of
    docs/markdown.md, docs/seo.md, docs/types.md and the code scan."""
    order, groups_by = [], {}
    for t in terms:
        key = (t.kind, t.name)
        if key not in groups_by:
            order.append(key)
            groups_by[key] = list(t.groups)
        else:
            groups_by[key].extend(g for g in t.groups if g not in groups_by[key])
    return [Term(kind, name, groups_by[(kind, name)]) for kind, name in order]


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

    # Element/chain prefixes the contract's markup actually uses: a class
    # chained onto another (`.b.grid`), or a class on a specific tag
    # (`pre.code`, `th.center`, `td.foo`, `u.u`). Without this, a class
    # mention needs its dot not glued to more identifier text before it
    # (`(?<![\w.])`), else a dotted name like `labels.nav` would falsely
    # cover a class `nav`.
    prefixes = r"\.b|pre|th|td|u"

    seen, terms = set(), []
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        esc = re.escape(name)
        pattern = (rf"(?<![\w.])\.{esc}(?![\w-])"
                   rf"|(?<![\w.])(?:{prefixes})\.{esc}(?![\w-])")
        terms.append(Term("class", name, [[pattern]]))
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
            for m in re.finditer(r"(?<![\w-])(--[a-z][a-z-]*[a-z]|-h)(?![\w-])", node.value):
                opt = m.group(1)
                if opt not in seen:
                    seen.add(opt)
                    terms.append(Term("option", opt, [[lit(opt)]]))
    return terms


def docs_texts(docs_dir):
    docs_dir = pathlib.Path(docs_dir)
    out = {"en": [], "fr": []}
    for path in sorted(docs_dir.rglob("*.md")):
        # A file or folder starting with `_` is never rendered by tilder
        # (docs/markdown.md, "Files and URLs"): its text can never cover a
        # term for a real reader, so it must not count as documentation.
        if any(part.startswith("_") for part in path.relative_to(docs_dir).parts):
            continue
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
        tilder / "docs" / "seo.md",
        tilder / "docs" / "types.md",
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

    pytexts = [p.read_text(encoding="utf-8") for p in sorted((tilder / "src").glob("*.py"))
               + sorted((tilder / "types").glob("*.py"))]

    front_matter = _merge_terms(
        front_matter_terms((tilder / "docs" / "markdown.md").read_text(encoding="utf-8"))
        + seo_front_matter_terms((tilder / "docs" / "seo.md").read_text(encoding="utf-8"))
        + collection_key_terms((tilder / "docs" / "types.md").read_text(encoding="utf-8"))
        + meta_read_terms(pytexts))

    terms = (
        defaults_terms((tilder / "defaults.toml").read_text(encoding="utf-8"))
        + type_terms(tilder / "types")
        + front_matter
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
