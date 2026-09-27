---
title: Getting started
description: Install tilder with Docker or Python 3.11, copy the starter site, build it once, rebuild as you write, and find your way in public/.
order: 10
---

## Name

getting started - install tilder and build a first site

tilder runs from its Docker image or from a checkout with Python 3.11 or
later; nothing else is required. This page copies the starter site, a
small bilingual site with its own theme, builds it, keeps it rebuilding as
you write, and tours what the build leaves in `public/`.

[TOC]

## Install

### With Docker

  The image `ghcr.io/thosted/tilder` holds the generator, Python, and the
  tools that draw the icons. It is tagged by version: `1.4.1`, `1.4` and
  `1` follow the releases, `latest` the main branch. Pin a version, so a
  site builds the same way tomorrow:

  ```sh
  docker pull ghcr.io/thosted/tilder:1.4.1
  ```

  The generator is in `/tilder` inside the image, with the reference
  documentation of its version in `/tilder/docs/`.

### With Python

  A checkout of the repository is enough: tilder uses Python's standard
  library only, so there is nothing to install with `pip`. Python 3.11 or
  later is required.

  ```sh
  git clone --branch v1.4.1 https://github.com/THOSTED/tilder
  python3 tilder/build.py --help
  ```

### Icons and the share image

  Every build draws `favicon.ico` and the PNG icons from the site's
  `assets/logo.svg`. When the theme has a `share.svg`, it also draws
  `share.png`, the 1200x630 link preview, from that template, with the
  logo inside; without one, the preview is the largest icon. It needs an
  SVG renderer: `rsvg-convert` first, else ImageMagick's `magick`. The
  Docker image has `rsvg-convert`, and `woff2_decompress` so the preview
  is drawn with the theme's own fonts.

  Without either tool the build goes on and says so, once:

  ```text
  warning: no rsvg-convert or magick: icons and share.png not made
  ```

  The pages are complete, but the icon and preview files they point at
  are missing. Without `assets/logo.svg`, none is made either, and the
  build says:

  ```text
  warning: no logo.svg in assets/: no icons, no share.png
  ```

## Copy the starter

The repository's `starter/` folder is a complete site: a landing page, a
blog with one post, a 404 page, English and French, and a minimal theme
on system fonts. Copy it and make it yours:

```sh
git clone --branch v1.4.1 https://github.com/THOSTED/tilder
cp -r tilder/starter my-site
cd my-site
```

Skip the clone if you already made it to run tilder with Python.

It holds the three folders of every project: `content/` (the pages and
`site.toml`), `theme/` (how it looks) and `assets/` (the logo). The
[project](docs/guide/project) page describes each one.

The starter declares two languages. For a site in one language, delete
`content/site.fr.toml`, every `.fr.md` file, and the `languages` line of
`content/site.toml`.

## The first build

With Docker, from `my-site/`:

```sh
mkdir -p public
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD:/site" -v "$PWD/public:/out" \
  ghcr.io/thosted/tilder:1.4.1 \
  python3 -B /tilder/build.py --root /site --out /out
```

`-u` makes you the owner of what the build writes; creating `public/`
first keeps Docker from creating it as root.

With Python, from `my-site/`, next to the `tilder/` checkout:

```sh
python3 ../tilder/build.py
```

tilder builds the current folder when it has a `content/` folder, into its
`public/`. From anywhere else, name both: `--root` is the project to
build, `--out` where the site goes.

```sh
python3 tilder/build.py --root my-site --out my-site/public
```

The build prints what it found, then every file it wrote:

```console
$ python3 ../tilder/build.py
languages: en (default), fr
types: event, member, page, post
collections: blog (post, 1 item), events (event, no folder), ...
[10:42:07] built /home/me/my-site/public: 404.html, ...
```

A second build writes only what changed, and deletes from the output
folder every file the build no longer produces: the folder belongs to
tilder, keep nothing else in it.

A problem in the content stops the build with a message that names the
file and says what to do; the exit code is then 1. A warning, such as an
image without alt text or a description too long for search engines, does
not stop it. Every message is listed in the
[command-line reference](docs/reference/cli).

## Rebuild as you write

`--watch` builds once, then watches the project and rebuilds on every
change:

```sh
python3 ../tilder/build.py --watch
```

The image's default command is the same watch, on `/site` into `/out`:

```sh
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD:/site" -v "$PWD/public:/out" ghcr.io/thosted/tilder:1.4.1
```

It looks at `content/`, `theme/` and `assets/` every second. A build that
fails keeps the last good output and waits for the next change. A change
to the generator itself, or to a theme's Python types in `theme/types/`,
restarts the process so the new code is loaded.

It also rebuilds at midnight, with no change at all: the build's date
decides which events are upcoming and which are past, so an event moves
to the past list the day after its date. Midnight is the machine's: in a
container, UTC unless the `TZ` variable says otherwise.

## What public/ holds

To browse it, serve the folder: the links have no `.html`, so opening
the files from the disk breaks them, and the compose stack of
[deployment](docs/guide/deployment) serves them as intended. The build
wrote:

| Path | What it is |
|---|---|
| `index.html`, `blog/index.html`, `404.html`... | the pages, for browsers |
| `fr/...` | the same pages in French, under the language's prefix |
| `txt/` | the text mirror, plain ASCII, 75 columns: `txt/index.txt` |
| `ansi/` | the same text, coloured for terminals |
| `blog/feed.xml`, `fr/blog/feed.xml` | the blog's RSS feed, one per language |
| `sitemap.xml`, `sitemap.txt`, `robots.txt` | for search engines |
| `favicon.ico`, `icon-192.png`, `icon-512.png`, `apple-touch-icon.png` | the icons, drawn from `assets/logo.svg` |
| `share.png`, `site.webmanifest` | the link preview, and the web manifest |
| `style.css`, `logo.svg` | the theme's files and the assets, copied |

A site with events also gets their RSS feed and an iCalendar file. None
of this is edited by hand, and none of it is committed: `public/` is
rebuilt from the sources every time.

## See also

- [the project](docs/guide/project)
- [the command line](docs/reference/cli)
- [deployment](docs/guide/deployment)
