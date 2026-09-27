#!/usr/bin/env python3
"""Check the WCAG contrast of a theme's colour tokens, light and dark.

The tokens are the custom properties of the first `:root { }` block of
style.css (light) and of the `:root { }` block inside
`@media (prefers-color-scheme: dark)` (dark). Colours are #rrggbb.

    python3 tools/check-contrast.py theme/style.css            # check
    python3 tools/check-contrast.py theme/style.css --markdown # the README table

Exit 0 when every pair reaches its minimum, 1 otherwise, 2 when the
tokens cannot be read.
"""

import re
import sys

# (foreground, background, minimum): text is 4.5:1 (WCAG 1.4.3); the
# accent is also the focus outline, and is text (links) too.
PAIRS = [(fg, bg, 4.5)
         for fg in ("text", "muted", "faint", "accent", "info", "warning", "error")
         for bg in ("bg", "surface")]
TOKEN = re.compile(r"--([\w-]+)\s*:\s*([^;]+);")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def _block(css, start):
    """The text between the brace that opens at `start` and its match."""
    depth, i = 0, css.index("{", start)
    for j in range(i, len(css)):
        depth += {"{": 1, "}": -1}.get(css[j], 0)
        if depth == 0:
            return css[i + 1:j]
    raise ValueError("unbalanced braces")


def tokens(css):
    """{"light": {name: "#rrggbb"}, "dark": {...}} from style.css."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    media = re.search(r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)", css)
    if not media:
        raise ValueError("no @media (prefers-color-scheme: dark) block")
    root = re.search(r":root\s*\{", css)
    if not root or root.start() > media.start():
        raise ValueError("no :root { } block before the dark scheme")
    dark_root = re.search(r":root\s*\{", _block(css, media.start()))
    if not dark_root:
        raise ValueError("no :root { } block in the dark scheme")
    light = dict(TOKEN.findall(_block(css, root.start())))
    dark = dict(TOKEN.findall(_block(_block(css, media.start()), dark_root.start())))
    return {"light": light, "dark": dark}


def luminance(hex_colour):
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def results(schemes):
    """[(scheme, fg, bg, ratio, minimum)], or ValueError on a missing or
    malformed token."""
    out = []
    for scheme in ("light", "dark"):
        t = schemes[scheme]
        for fg, bg, minimum in PAIRS:
            for name in (fg, bg):
                value = t.get(name, "").strip()
                if not HEX.match(value):
                    raise ValueError(f"{scheme}: --{name} must be #rrggbb, not {value or 'missing'}")
            out.append((scheme, fg, bg, ratio(t[fg].strip(), t[bg].strip()), minimum))
    return out


def markdown(rows):
    lines = ["| scheme | foreground | background | ratio | minimum |",
             "|---|---|---|---:|---:|"]
    lines += [f"| {s} | `--{fg}` | `--{bg}` | {r:.2f} | {m} |" for s, fg, bg, r, m in rows]
    return "\n".join(lines)


def main(argv):
    args = [a for a in argv[1:] if a != "--markdown"]
    if len(args) != 1:
        print("usage: check-contrast.py STYLE_CSS [--markdown]", file=sys.stderr)
        return 2
    try:
        with open(args[0], encoding="utf-8") as f:
            rows = results(tokens(f.read()))
    except (OSError, ValueError) as e:
        print(f"error: check-contrast: {e}", file=sys.stderr)
        return 2
    if "--markdown" in argv:
        print(markdown(rows))
    low = [r for r in rows if r[3] < r[4]]
    for s, fg, bg, r, m in low:
        print(f"error: {args[0]}: {s}: --{fg} on --{bg} is {r:.2f}:1, below {m}:1. "
              f"Darken or lighten one of them", file=sys.stderr)
    if not low and "--markdown" not in argv:
        print(f"contrast: {len(rows)} pairs, all at or above their minimum")
    return 1 if low else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
