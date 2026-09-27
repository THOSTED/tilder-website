---
title: The command line
description: build.py and every option, from --root to --check, what the build prints, every warning and error it can give, and its exit codes.
order: 60
---

## Name

cli - build.py, its options, its messages and its exit codes

tilder is one command, `build.py`, run with Python 3.11 or later, or
inside its Docker image. It builds a project into a folder once, or
keeps rebuilding it as you write, or checks the theme without building.
Its messages all have one shape, name the file at fault and say what to
do.

[TOC]

## Synopsis

```text
python3 build.py [--root DIR] [--out DIR] [--watch] [--debug]
python3 build.py [--root DIR] --check [--markdown] [--debug]
python3 build.py --version
python3 build.py -h | --help
```

`build.py` is at the top of a tilder checkout, and at `/tilder/build.py`
in the Docker image, whose default command is a watch of `/site` into
`/out`:

```sh
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD:/site" -v "$PWD/public:/out" \
  ghcr.io/thosted/tilder:1.2.0 \
  python3 -B /tilder/build.py --root /site --out /out
```

Options may come in any order, except `-h` and `--help`, which count only
as the first argument; an argument the build does not know is ignored
([getting started](docs/guide/getting-started)).

## Options

### --root DIR

  The project to build: the folder that holds `content/`, `theme/` and
  `assets/`. Without it, the project is the current folder when it has a
  `content/` folder, else the folder that holds the tilder checkout.

### --out DIR

  Where the site goes, created if needed. Default: `public/` in the
  project. The build writes only the files that changed, each one
  replaced at once, so a server never reads half a file, and deletes
  every file it no longer produces, then the empty folders: the output
  folder belongs to the build, keep nothing else in it.

### --watch

  Build, then keep watching the project and rebuild on every change. The
  sources, `content/`, `theme/`, `assets/`, a `LICENSE` beside them and
  tilder's own files, are looked at every second. A build that fails
  prints its errors, keeps the last good output and waits for the next
  change; if the very first build fails, it tries again every five
  seconds until it succeeds. A change to tilder itself, or to a
  theme's types in `theme/types/`, restarts the process, so the new code
  is loaded.

  The watch also rebuilds at midnight, with no change at all: the date of
  the build decides which events are upcoming and which are past, so an
  event moves to the past list the day after it. Midnight is the
  machine's: in a container, UTC unless the `TZ` variable says otherwise.

<!-- 1.2 -->

### --check

  From tilder 1.2: check the theme against the tilder that runs it, and
  build nothing. Every class the build writes must have a rule in the
  served `style.css` (`assets/style.css` wins over `theme/style.css`),
  but those the theme's `[check] unstyled` names; every pair of colours
  of `[check] contrast` must reach `contrast_min`, in the light scheme,
  and in the dark one when the stylesheet has one. It prints one `error:` line per problem, then a summary
  line per check, and exits 1 when there is a problem, 0 otherwise
  ([checking a theme](docs/themes/checking)).

<!-- 1.2 -->

### --markdown

  From tilder 1.2, with `--check`: also print the contrast table as
  Markdown, a row per pair with its ratio, for a theme's README. The
  table goes to the standard output and the summary lines to the error
  output, so `--check --markdown > contrast.md` keeps only the table.

### --debug

  After each error message, print the Python traceback that caused it.
  The messages are meant to be enough; the traceback is for a bug in
  tilder or in a theme's type.

### --version

  Print tilder's version and exit: the image's release, `1.2.0`, from
  its `TILDER_VERSION` variable; `dev` from a checkout, where the variable
  is not set.

### -h, --help

  Print the usage, the options and the map of tilder's modules, then
  exit.

## Environment

| Variable | Effect |
|---|---|
| `SITE_ROOT` | the project to build, as `--root`, which sets it |
| `BUILD_TODAY` | the build's date, `2026-05-16`, instead of today's: which events are upcoming, for a test or a preview |
| `BUILD_INTERVAL` | with `--watch`, the seconds between two looks at the sources; default `1` |
| `TILDER_VERSION` | what `--version` prints; set by the Docker image |
| `TZ` | the time zone of the date and of the midnight rebuild |

## What the build prints

On the standard output, the first build says what it understood, then
every build lists what it wrote, or `no change`; a file it deleted is
listed with a `-`:

```console
$ python3 ../tilder/build.py
languages: en (default), fr
types: event, member, page, post
collections: blog (post, 1 item), events (event, no folder), ...
[10:42:07] built /home/me/my-site/public: 404.html, blog/feed.xml, ...
[10:43:12] built /home/me/my-site/public: about.html, txt/about.txt, ansi/about.txt
[10:44:30] built /home/me/my-site/public: -old.html
```

The `languages:` line appears only on a site with several languages;
the `types:` line adds the types that come from the theme,
`; from theme: talk`. With `--watch`, the build also says when it
waits after a failure or restarts on new code. Warnings and errors go to
the error output.

## Errors

An error stops the build. Every message has the same shape:

```text
error: <file>[:<line>]: <what is wrong>. <what to do>
```

The file is named from the project's root, or from tilder's for one of
its own files; the build gathers every problem of a phase before it
stops, so one run shows them all.

```text
error: content/site.toml: collection "blog" has type "posts"; types are singular. Write type = "post"
error: content/blog/2026-02-30-hello.md: "2026-02-30" is not a date. Name the file YYYY-MM-DD-slug.md with the post's date
```

The errors of the configuration and of the languages:

| Message | Cause |
|---|---|
| `[members] is no longer read` | a table an older tilder read; its keys go under `[collections.members]` |
| `[collection_defaults] is no longer read` | the same; a type's words go under each `[collections.<name>]` |
| `collection "..." has type "...s"; types are singular` | a type written in the plural, `posts` |
| `collection "..." has type "...", which no type defines` | an unknown type; the message lists those loaded |
| `collections "..." and "..." share the folder content/...` | two collections with one `dir`, or one whose `dir` is inside the other's |
| `[site] languages does not contain the default language "..."` | `site.lang` missing from `site.languages` |
| `"..." is not a declared language` | a `site.<lang>.toml` or a page `<name>.<lang>.md` for a language not in `site.languages` |
| `[site] lang is "...", not "..."` | a `site.<lang>.toml` that sets another language |

<!-- 1.2 -->

From tilder 1.2, a recursive collection adds three:

| Message | Cause |
|---|---|
| `collection "..." has recursive = ...` | a value other than `true` or `false` |
| `collection "..." is recursive, and its type "..." is dated` | a recursive `post` or `event` collection |
| `is a second file for the item ..., with ...` | one item as both `guide.md` and `guide/index.md` |

The errors of the content and the theme:

| Message | Cause |
|---|---|
| `cannot be built: <error>` | a page the build cannot render, a missing `title:` for instance: the file is named, `--debug` shows the traceback |
| `"..." is not a date` | a post's or an event's file whose name starts with a date that does not exist |
| `{...} names no ... collection` | a list marker naming a collection of another type, or none |
| `no layout.html: a site needs a theme` | `theme/layout.html` is missing |
| `layout "..." names no theme/layouts/....html` | a page's `layout:` names a file the theme does not have |
| `unknown placeholder {{ ... }}` | a layout uses a name that is neither a placeholder nor a configuration key ([layouts](docs/themes/layouts)) |

A theme's types in Python have errors of their own, from a missing
`NAME` to a marker two types claim, listed with
[custom types](docs/content-types/custom-types). The errors of `--check`
are listed with [checking a theme](docs/themes/checking).

In a one-shot build, a file that is not valid TOML, or a bug, ends with
Python's own message and traceback instead of this shape. With
`--watch`, the same problem is one line, `error: <Python error>: <what>`,
and the traceback follows only with `--debug`.

## Warnings

A warning does not stop the build nor change its exit code: the site is
built, with something missing or likely to be cut. Every warning the
build can print:

| Line | Meaning |
|---|---|
| `warning: image not found: content/<path>` | an image whose file does not exist |
| `warning: image without alt text: <path>` | an image with an empty alt text |
| `warning: unknown code language '<lang>', left plain` | a code block's language tilder does not highlight ([blocks](docs/reference/markdown/blocks)) |
| `warning: no <logo> in assets/: no icons, no share.png` | the logo named by `share.logo_svg`, `logo.svg` by default, is missing |
| `warning: no rsvg-convert or magick: icons and share.png not made` | no SVG renderer is installed ([feeds and images](docs/reference/feeds-and-images)) |
| `seo: <page>: title is N characters (max MAX)` | a `<title>` longer than `seo.title_max`, `60` by default |
| `seo: <page>: description is N characters (MIN-MAX)` | a description outside `seo.description_min` and `seo.description_max`, `50-160` by default |
| `seo: <page>: same title as <page>` | two pages of one language share a title |
| `seo: <page>: same description as <page>` | two pages of one language share a description |

On a site with several languages, every `seo:` line names the language
of the pass, the default one included: `seo: [en] about.html: ...`,
`seo: [fr] about.html: ...` ([SEO](docs/reference/seo)). A site
that wants no warning at all makes its own build fail on them, as this
site's build does on any `warning:` or `seo:` line. In a shell script:

```sh
python3 ../tilder/build.py 2> build.log; status=$?
cat build.log >&2
[ "$status" -eq 0 ] && ! grep -Eq '^(warning|seo):' build.log
```

## Exit codes

| Code | When |
|---|---|
| `0` | the site is built, warnings or not; `--check` found no problem; `--version` and `--help` |
| `1` | the build stopped on an error; `--check` found a problem; a Python exception outside the build's own messages |

With `--watch`, a failed build does not exit: the process keeps waiting
for a fix, and runs until it is stopped.

## See also

- [getting started](docs/guide/getting-started)
- [checking a theme](docs/themes/checking)
- [configuration](docs/reference/configuration)
