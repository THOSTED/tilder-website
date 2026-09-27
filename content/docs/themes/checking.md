---
title: Checking a theme
description: build.py --check checks a theme against the tilder that runs it: a rule for every class it writes, and the contrast of the colour pairs.
order: 50
---

## Name

checking - build.py --check, the classes and the contrast of a theme

`build.py --check` checks the site's theme against the tilder that runs
it, and builds nothing. Two checks: every class the build writes has a
rule in `style.css`, and every pair of colours the theme declares reaches
its contrast minimum, in the light scheme and in the dark one. It prints
one line per problem and exits 1 when there is one, so it fits before a
build, in a Makefile or in CI.

[TOC]

## The command

From the project, with Python:

```sh
python3 ../tilder/build.py --check
python3 ../tilder/build.py --check --markdown   # and the table
```

With Docker, the project mounted read-only, since nothing is written:

```sh
docker run --rm -v "$PWD:/site:ro" ghcr.io/thosted/tilder:1.4.1 \
  python3 -B /tilder/build.py --root /site --check
```

It prints one `error:` line per problem, in the shape of the build's own
errors, the file, what is wrong, then what to do, and a summary line for
each check it ran: with contrast pairs declared but no `style.css`, the
contrast check has an error instead of a summary. The exit code is 0
when every check passes or is skipped, 1 when a problem was found. The
normal build never runs these checks: run them when the theme changes,
or before every build.

For example, tilder 1.2.0 checking the theme of this site as it was
written for tilder 1.1, before it styled the three section classes of
1.2 and before its `theme.toml` declared contrast pairs:

```console
$ python3 ../tilder/build.py --check
error: theme/style.css: no rule for .collection-section. Style it, or name it in [check] unstyled (theme/theme.toml)
error: theme/style.css: no rule for .collection-section--open. Style it, or name it in [check] unstyled (theme/theme.toml)
error: theme/style.css: no rule for .collection-section-label. Style it, or name it in [check] unstyled (theme/theme.toml)
classes: 3 of 72 not styled
contrast: skipped, no [check] contrast in theme/theme.toml
$ echo $?
1
```

## The classes

tilder holds the list of every class it writes, `CLASSES` in its
`src/contract.py`: the classes of the [classes](docs/themes/classes) page.
The check looks for each one in `style.css`, the site's
`assets/style.css` if it has one, else the theme's: a class counts when
`.name` appears with no name character after it, comments and the
contents of strings aside. So `.toc` does not count for `.toc-label`,
and a class named only in a comment is missing.

A theme that leaves a class unstyled on purpose names it in `[check]
unstyled`, and the check skips it: a theme without profile logos, say,
has nothing to style in `.icon`. Without `style.css`, the check is skipped
with a note.

```text
classes: 72 of the contract, all styled
classes: 3 of 72 not styled
classes: skipped, no theme/style.css
```

Since the list comes from the tilder that runs the check, a new version
of tilder that writes a new class makes the check name it: the theme
learns what to style before a page shows it unstyled.

## The contrast

The theme declares the pairs of colours that carry text, foreground then
background, as custom properties of its `style.css`, in `[check]
contrast`. The check computes the WCAG 2 contrast ratio of each pair and
reports each one below `contrast_min`, 4.5 by default, the WCAG AA
minimum for text, with its ratio.

It reads the colours where a browser would:

- **light**: the custom properties of the `:root` rule of `style.css`;
- **dark**: those of the `:root` rule inside `@media
  (prefers-color-scheme: dark)`, over the light ones, so a dark scheme only
  sets what differs. Without such a rule, only the light scheme is checked.

Only a rule whose selector is exactly `:root` counts: not `:root, .dark`,
not one inside `@supports` or `@layer`. A colour a pair uses must be
written in hex, `#rgb` or `#rrggbb`; a property that is not set, or is not
a hex colour (`rgb()`, a `var()`, a name), is an error naming it. Without
pairs, the check is skipped; with pairs and no `style.css`, it is an
error.

```text
error: theme/style.css: dark: --muted on --bg is 3.87:1, below 4.5:1. Darken or lighten one of them
error: theme/style.css: light: --accent is rgb(0 112 126), not a hex colour. Write it #rrggbb, or leave its pairs out of [check] contrast
```

Its summary line says how many pairs it measured, and in which schemes:

```text
contrast: 20 pairs (light, dark), all at or above 4.5:1
contrast: 1 of 18 pairs below 4.5:1, 1 unreadable
contrast: skipped, no [check] contrast in theme/theme.toml
```

## The [check] table

The three keys live in the theme's `theme.toml`, under `[check]`. They
are read from `defaults.toml`, then the theme's `theme.toml`, then the
site's `site.toml`, the last one winning: a site may change them in its
own `site.toml` without touching the theme.

| Key | Default | |
|---|---|---|
| `unstyled` | `[]` | classes of the contract the theme leaves unstyled on purpose (the dot is optional) |
| `contrast` | `[]` | pairs of custom properties of `style.css`, foreground then background; empty: not checked |
| `contrast_min` | `4.5` | the least contrast ratio of every pair |

```toml
# theme/theme.toml
[check]
unstyled = ["icon"]              # no profile logos in this theme
contrast = [
	["--fg", "--bg"], ["--fg", "--bg-inset"],
	["--fg-muted", "--bg"], ["--fg-muted", "--bg-inset"],
	["--accent", "--bg"],
]
contrast_min = 4.5
```

A malformed table is an error of its own: `unstyled` must be a list of
names, `contrast` a list of pairs of names starting with `--`,
`contrast_min` a number.

## A table for the README

With `--markdown`, the check also prints the contrast table as Markdown,
on standard output, and its summary lines on standard error: redirect the
output to a file and paste the table in the theme's README, so its users
see the ratios without running anything.

```sh
python3 ../tilder/build.py --check --markdown > contrast.md
```

The table begins with the light scheme, then the dark one, each pair in
the order of `[check] contrast`. The first rows for the starter's theme:

```markdown
| scheme | foreground | background | ratio | minimum |
|---|---|---|---:|---:|
| light | `--fg` | `--bg` | 17.40 | 4.5 |
| light | `--fg` | `--bg-inset` | 15.68 | 4.5 |
| light | `--fg-muted` | `--bg` | 7.46 | 4.5 |
| light | `--fg-muted` | `--bg-inset` | 6.72 | 4.5 |
```

The starter's theme passes both checks and declares its pairs in
`starter/theme/theme.toml`: a model for a theme of your own.

## See also

- [classes](docs/themes/classes)
- [the command line](docs/reference/cli)
- [the files of a theme](docs/themes/files)
