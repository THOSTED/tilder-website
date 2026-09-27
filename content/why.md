---
man: TILDER-WHY(7)
title: Why tilder
description: The principles behind tilder, what it deliberately leaves out next to Hugo, Jekyll and Eleventy, and when it is the right tool.
tagline: the principles, and what tilder does not do
nav: why
---

## Name

why - the principles behind tilder

tilder builds sites that read like a man page, for a browser and for a
terminal alike. It does little, on purpose: each page is written once,
rendered twice, and served with nothing from anywhere else. This page says
why, what that costs, and when another tool will serve you better.

[TOC]

## Principles

### 75 columns

  A man page is a column of text a terminal can show without wrapping.
  tilder keeps that line: the text mirror of every page is 75 columns
  wide, code included, which leaves room in an 80-column terminal for a
  scrollbar, a pager's gutter or an email quote. This site's theme keeps
  the same measure in the browser, so a page reads alike in both.

### Two renderings of everything

  Every page is written once, in Markdown, and built twice: HTML for the
  browser, ASCII text for the terminal, with a coloured twin. Both come
  from the same source, so they cannot drift apart. A construct is not
  supported until it renders in both; the text is half the product, not
  an afterthought. `curl` gets the text instead of the HTML, and a braille
  display reads it as easily.

### Nothing from a third party

  A built page loads nothing from another site: no CDN, no font service,
  no remote script, no iframe, no remote image. Fonts, styles and scripts
  are the theme's own files, served by your server. Links to other sites
  are fine; loading from them is not.

### No JavaScript required

  Every page reads in full without JavaScript. Scripts belong to the theme
  and only enhance: on this site, a copy button on code and the search of
  the documentation. Each one creates its own controls, so without it
  nothing is missing or broken.

### No tracking

  No analytics, no cookies, no forms, no server-side code: the output is
  static files. The example Caddyfile goes one step further and discards
  the access logs, so a visit leaves no record on the server either.

### The standard library only

  tilder is written in Python with its standard library alone: nothing to
  install, no package manager, no framework, no preprocessor. The one
  outside tool, `rsvg-convert`, is optional and only draws the icons and
  the share image; the Docker image has it.

### Accessibility

  One `<h1>` per page, headings in order, landmarks, labels, required alt
  text, focusable code blocks and tables. A screen reader hears when a
  link leaves the site or opens a tab, and no meaning is carried by colour
  alone. Contrast and focus are the theme's: the starter theme and this
  site's theme meet WCAG AA.

## What tilder does not do

Hugo, Jekyll and Eleventy are mature, general-purpose static site
generators, each with a large community. They can build almost any site,
and they grow with it. tilder builds one kind of site, and leaves out much
of what they offer:

- **No template language.** A theme's `layout.html` is plain HTML
  with placeholders, such as `{{ title }}`, filled at build time: no
  loops, no conditions, no includes. The others give themes a full template language.
- **No plugin ecosystem.** There is nothing to install. The one way to
  extend tilder is a content type: a Python module in the theme, which
  adds items, lists and markers of its own.
- **No asset pipeline.** No Sass, no bundling, no minification, no image
  resizing. The theme's files and the images next to a page are served as
  they are; the build reads an image's size and draws only the icons and
  the share image.
- **No shortcodes.** The only additions to Markdown are markers in braces,
  such as `{grid}` on a section or `{small}` on a paragraph; a
  collection's markers, such as `{posts}`, place its list on a page.
- **No raw HTML in Markdown.** Anything that is not part of the dialect
  is escaped and shown as text; only an HTML comment passes through, and
  only into the HTML.
- **A restricted dialect.** Headings are `##` and `###` only; there are no
  footnotes, definition lists, reference-style links, bare URLs, inline
  images or escapes. Each construct costs two renderings, so the list
  stays short.
- **No pagination and no tag pages.** A collection is listed in full, in
  the order its type gives: newest first, upcoming then past, or an order
  you set.
- **A plain scheme for languages.** A translation is the same file with a
  language suffix, `why.fr.md` next to `why.md`, and the interface words
  of a language live in its own TOML file. There are no translation keys
  in the pages and no folder per language in `content/`.

If a site needs any of these, one of the others is the better choice.

## When to use it

tilder fits a site that is mostly text: documentation, a project's pages,
release notes, a small association with its events and members, a
personal page. It fits when you want the site to read in a terminal as
well as in a browser, to load nothing from elsewhere, and to build with
nothing but Python.

It does not fit a site that needs rich layouts page by page, embedded
media from other services, client-side applications, or a large catalogue
with pagination and tags. There, the constraints that make tilder simple
get in the way.

## See also

- [getting started](docs/guide/getting-started)
- [the documentation](docs/)
- [tilder on GitHub ↗](https://github.com/THOSTED/tilder)
