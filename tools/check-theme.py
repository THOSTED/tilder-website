#!/usr/bin/env python3
"""Check that a theme's style.css styles every class tilder writes.

The classes are read from tilder's theme contract, docs/theme.md: the
first column of the table under "## The HTML the builder writes".

    python3 tools/check-theme.py theme/style.css path/to/docs/theme.md

Exit 0 when every class appears in a selector, 1 with one line per
missing class, 2 when the contract cannot be read.
"""

import re
import sys

SECTION = "## The HTML the builder writes"
CLASS = re.compile(r"\.([A-Za-z_][\w-]*)")
COMMENT = re.compile(r"/\*.*?\*/", re.S)


def contract_classes(text):
    """Every class of the contract's table, in order, without duplicates.
    A cell token like `--warning` completes the block of the class before
    it that has a modifier: `.callout--info`, `--warning` -> callout--warning."""
    if SECTION not in text:
        raise ValueError(f'no "{SECTION}" section')
    rows = text.split(SECTION, 1)[1].split("\n## ", 1)[0].splitlines()
    out, block = [], None
    for row in rows:
        if not row.startswith("| ") or row.startswith("|---"):
            continue
        first = row.split("|")[1]
        for token in re.findall(r"`([^`]+)`", first):
            if token.startswith("--"):
                if block is None:
                    raise ValueError(f"modifier {token} has no class before it")
                names = [block + token]
            else:
                names = CLASS.findall(token)
                for name in names:
                    if "--" in name:
                        block = name.split("--", 1)[0]
            for name in names:
                if name not in out:
                    out.append(name)
    if not out:
        raise ValueError("the table lists no class")
    return out


def missing(css, classes):
    """The classes that no selector of `css` names."""
    css = COMMENT.sub("", css)
    return [c for c in classes
            if not re.search(r"\." + re.escape(c) + r"(?![\w-])", css)]


def main(argv):
    if len(argv) != 3:
        print("usage: check-theme.py STYLE_CSS THEME_MD", file=sys.stderr)
        return 2
    try:
        with open(argv[2], encoding="utf-8") as f:
            classes = contract_classes(f.read())
        with open(argv[1], encoding="utf-8") as f:
            css = f.read()
    except (OSError, ValueError) as e:
        print(f"error: check-theme: {e}", file=sys.stderr)
        return 2
    gone = missing(css, classes)
    for name in gone:
        print(f"error: {argv[1]}: .{name} is written by tilder and not styled. "
              f"Add a rule for it (docs/theme.md)", file=sys.stderr)
    if not gone:
        print(f"theme: {len(classes)} classes of the contract, all styled")
    return 1 if gone else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
