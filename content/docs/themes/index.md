---
title: Themes
description: What a tilder theme is, how to use one, and the pages that describe its files, layouts, classes, scripts and checks.
order: 30
---

## Name

themes - how a tilder site looks

tilder writes HTML with stable class names and no style of its own; the
site's `theme/` folder decides how it looks. A theme is a layout with
placeholders, a stylesheet, and whatever else it chooses to add: fonts,
scripts, a link preview, content types. tilder ships no theme but the
starter's, a minimal one to copy and grow.

[TOC]

## What a theme is

A theme is a folder, `theme/`, next to `content/` and `assets/`. It needs
one file, `layout.html`: the HTML around every page, in which the build
replaces `{{ title }}`, `{{ body }}` and the other placeholders. Everything
else is optional:

- `style.css`, which styles the classes the build writes;
- other layouts, for one type of page or asked for by a page;
- fonts, profile logos, the template of the link preview;
- scripts, which improve a page without being needed to read it;
- content types, in Python, that add kinds of pages to the site;
- `theme.toml`, the theme's own settings and words, under the site's.

The build fills the layout, copies what is meant to be served, and never
serves what it only reads. The theme owns the look and part of the
accessibility (contrast, focus, the visually hidden text); the build owns
the markup: headings, alt text, labels, `aria-*` attributes.

## Using a theme

A site uses the theme in its `theme/` folder, and nothing else: there is
no setting to name a theme. To use one, copy it there.

### the starter's

  The starter's site comes with its theme, `starter/theme/` in tilder's
  repository: a layout, a stylesheet and a link preview, on system fonts,
  with no script. It styles every class the build writes and meets WCAG
  AA contrast in light and dark. Starting from the starter
  ([getting started](docs/guide/getting-started)) gives you this theme to
  change as you like.

### this site's

  The site you are reading uses a theme of its own, and shows what a
  larger theme does: two more layouts (`layouts/home.html` for the landing
  page, `layouts/doc.html` for the documentation), two content types in
  `types/` (`doc` and `showcase`), three scripts (the copy button, the
  sidebar on small screens, the search), self-hosted fonts, and its words
  in English and French in `theme.toml` and `theme.fr.toml`.

### another one

  Copy its folder as `theme/`, then read its README: a theme that adds
  content types says which collections to declare in `site.toml`, and a
  theme may need a version of tilder or a server setting (a search reads
  its index, which needs `connect-src 'self'` in the page's
  Content-Security-Policy).

```sh
rm -rf theme
cp -r ../other-theme theme
```

A theme can live in its own git repository, cloned as `theme/`: its
`.git` folder, its git files, and a `README.md` or `LICENSE` at its top
are never served.

## Changing a theme you did not write

Two ways to change a theme and still take its next version as it is:

- **Its words and settings**: set them in `content/site.toml` (or
  `site.<lang>.toml`), which has the last word over the theme's
  `theme.toml` ([configuration](docs/reference/configuration)).
- **One file**: put a file of the same name in `assets/`. It wins over the
  theme's: `assets/style.css` replaces `theme/style.css`,
  `assets/layouts/doc.html` replaces the theme's layout of that name.

## Trust

A theme's `types/` are Python modules, run by the build with the rights of
whoever runs it. A theme is part of the site, like tilder itself: read one
before you use it, as you would any code you run. A theme without
`types/` runs nothing at build time; its scripts run in the reader's
browser, under the rules of [scripts](docs/themes/scripts).

## The pages of this section

[Files](docs/themes/files): every file a theme may provide, what the
build does with it, and what is served.

[Layouts](docs/themes/layouts): `layout.html` and `layouts/`, how a page's
layout is chosen, every placeholder and what the layout must keep.

[Classes](docs/themes/classes): every class the build writes, the element
it lands on, and the accessibility the theme is responsible for.

[Scripts](docs/themes/scripts): `code.js`, `members.js`, a type's script,
where each is loaded and the rules they follow.

[Checking a theme](docs/themes/checking): `build.py --check`, which checks
a theme's classes and colour contrast against the tilder that runs it.

## See also

- [the project](docs/guide/project)
- [custom types](docs/content-types/custom-types)
- [the configuration reference](docs/reference/configuration)
