---
man: TILDER(1)
title: tilder - a man-page site builder
description: tilder builds a website from Markdown, an HTML page for browsers and a text mirror for terminals, with Python's standard library alone.
tagline: a man-page site builder
nav:
layout: home
---

## Name {text}

tilder - a man-page site builder

## Description

One Markdown file in, two outputs out: an HTML page for browsers and its
text mirror for terminals. tilder is written in Python's standard library;
its pages need no JavaScript and load nothing from a third party.

## One file, two outputs {grid}

```markdown
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
$ curl example.org/hello
NAME
     hello - a page

DESCRIPTION
     One Markdown file, two outputs.
```

## Features {grid}

### Text mirror

  Every page has a plain-text twin, 75 columns wide, plain or coloured for
  terminals. `curl` gets it instead of the HTML.

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

  Python's standard library, nothing to install. Outside tools only draw
  the icons and the link preview, and are optional: `rsvg-convert`, with
  `woff2_decompress`, else ImageMagick; without either, those images are
  skipped with a warning. The Docker image has `rsvg-convert` and
  `woff2_decompress`. No page loads anything from another site.

## Quick start

Copy the starter, a small site with its theme, from the repository's
`starter/` folder, then build it with the Docker image,
`ghcr.io/thosted/tilder:1.4.1`:

```sh
git clone --branch v1.4.1 https://github.com/THOSTED/tilder
cp -r tilder/starter my-site && cd my-site
mkdir -p public
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD:/site" -v "$PWD/public:/out" \
  ghcr.io/thosted/tilder:1.4.1 \
  python3 -B /tilder/build.py --root /site --out /out
```

The site is in `public/`. Or, with Python rather than Docker, run
`python3 ../tilder/build.py` in `my-site/`. The
[getting started](docs/guide/getting-started) guide goes on from there.

## See also

- [the documentation](docs/)
- [why tilder](why)
- [tilder on GitHub ↗](https://github.com/THOSTED/tilder)
