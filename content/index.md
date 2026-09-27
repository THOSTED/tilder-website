---
man: TILDER(1)
title: tilder - a man-page site builder
description: tilder builds a website from Markdown, an HTML page for browsers and a text mirror for terminals, with Python's standard library alone.
tagline: a man-page site builder
nav:
layout: home
---

## Name

tilder - a man-page site builder

One Markdown file in, two outputs out: an HTML page for browsers and its
text mirror for terminals. tilder is written in Python's standard library;
its pages need no JavaScript and load nothing from a third party.

## One file, two outputs {grid}

```text
---
title: hello
man: HELLO(7)
---

## Name

hello - a page

## Description

One **Markdown** file, two outputs.
```

```html
<section class="s" id="description">
	<h2>Description</h2>
	<div class="b">
		<p>One <b>Markdown</b> file, two outputs.</p>
	</div>
</section>
```

```console
$ curl tilder.thosted.fr/hello
NAME
     hello - a page

DESCRIPTION
     One Markdown file, two outputs.
```

## Features {grid}

### Text mirror

  Every page has a plain-text twin, 75 columns wide, plain or coloured for
  terminals. `curl` gets it instead of the HTML, and a braille display
  reads it as easily.

### Content types

  Pages, posts, events and members, each with its lists, and RSS and
  iCalendar feeds. A theme adds a type of its own in a few lines of Python.

### Languages

  The default language at the root, the others under their prefix, such
  as `/fr/`. An untranslated page falls back to another language, and
  `hreflang`, the sitemap and the feeds follow.

### SEO

  Canonical URLs, Open Graph, Twitter Card, JSON-LD, a sitemap and
  `robots.txt`. The build checks every title and description, and warns
  when one is too long or too short.

### Themes

  tilder writes semantic HTML with stable class names; the site's `theme/`
  decides how it looks. The starter ships a minimal theme to copy; this
  site is drawn by another.

### Accessibility

  One `<h1>` per page, landmarks, labels, alt text and named regions.
  Screen readers hear when a link leaves the site or opens a tab, and
  every page reads in full without JavaScript.

### No dependency

  Python's standard library, nothing to install. One optional tool,
  `rsvg-convert`, draws the icons and the link preview; the Docker image
  has it. No page loads anything from another site.

## Quick start

Copy the starter, a small site with its theme, from the repository's
`starter/` folder, then build it with the Docker image,
`ghcr.io/thosted/tilder`:

```sh
git clone https://github.com/THOSTED/tilder
cp -r tilder/starter my-site && cd my-site
mkdir -p public
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD:/site" -v "$PWD/public:/out" \
  ghcr.io/thosted/tilder \
  python3 -B /tilder/build.py --root /site --out /out
```

The site is in `public/`. Or, with Python rather than Docker, run
`python3 ../tilder/build.py` in `my-site/`. The
[getting started](docs/guide/getting-started) guide goes on from there.

## See also

- [the documentation](docs/)
- [why tilder](why)
- [tilder on GitHub ↗](https://github.com/THOSTED/tilder)
