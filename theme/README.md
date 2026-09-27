# A documentation theme for tilder

A theme for [tilder](https://github.com/thosted/tilder) sites that
document something: a manual with a sidebar, previous/next links and a
search, a landing page, a showcase. Every page but the landing page reads
as a man page; the landing page is airier. It names no project and holds
no site text: copy this folder into any tilder project as `theme/`.

It needs tilder 1.2.0 or later (a manual as a tree of folders, `--check`).
It speaks English and French out of the box.

## Files

| File | What |
|---|---|
| `layout.html` | the base layout: a man page (header rule, wordmark, navigation, one text column, previous/next, footer rule) |
| `layouts/` | `home.html`, the landing page (`layout: home`); `doc.html`, documentation pages (the `doc` type's layout, or `layout: doc`) |
| `style.css` | tokens, fonts, every class tilder writes (checked by tilder's `build.py --check`), light and dark |
| `fonts/` | Inter and JetBrains Mono, latin subsets, woff2, with their licences (OFL) |
| `share.svg` | the link preview, drawn to `share.png` (1200x630) |
| `code.js` | the copy button on code blocks |
| `search.js` | the documentation search, in the doc layout's sidebar |
| `nav.js` | the doc layout on small and wide screens: folds the sidebar, moves the `[TOC]` |
| `types/` | `doc.py` and `showcase.py`, the two content types below |
| `theme.toml` | the theme's words in English, the `[share]` colours, and `[check]` for tilder's `build.py --check` |
| `theme.fr.toml` | the theme's words in French |
| `LICENSE` | MIT |

## Using it

Declare the collections in `content/site.toml`:

```toml
[collections.docs]          # content/docs/, listed by {docs}
type = "doc"

[collections.showcase]      # content/showcase/, listed by {showcase}
type = "showcase"
```

The landing page asks for its layout: `layout: home` in its front matter.
Its `tagline` is the headline, and its first section the text under it.
A `## Features {grid}` section of `###` entries becomes cards; code
blocks in a `{grid}` section sit side by side.

### `doc`: documentation pages

| Front matter | |
|---|---|
| `title`, `description` | as on any page; the description is the card's text and the search's |
| `order` | a whole number, the page's place in the manual (default 1000; then the file name) |
| `group` | the sidebar's group within a folder, written the same way on every page of a language |

| Setting | Default | |
|---|---|---|
| `man` | `"SITE-DOCS(7)"` | the pages' man-page name |
| `nav` | `"docs/"` | the navigation entry marked current |
| `empty` | `"No page yet."` | a `{docs}` list with nothing in it |
| `index` | `"search-index.json"` | the search index, written in the collection's folder, one per language (`fr/docs/search-index.json`) |
| `recursive` | `true` | the collection reads its subfolders too (tilder's `recursive`) |

The manual may be a tree of folders: `docs/guide/writing.md` is the page
`docs/guide/writing`, in the section `guide`, whose own page is
`docs/guide/index.md` (served at `docs/guide`); `order` sorts the pages
and the sections of each folder. The sidebar nests the sections: the one
holding the page is open, the others fold to their label, a link to
their own page (a section without one stays unfolded).

A section marked `{docs}` lists every page, grouped: by folder in a tree
(each card names its section, the title of the section's own page), else
by `group`. The collection's own
page (`docs/index.md`) is a plain page: give it `layout: doc` for the
sidebar, and `search_index: docs/search-index.json` for the search field.
`[TOC]` on a page goes to the right column on wide screens.

### `showcase`: sites built with the project

| Front matter | |
|---|---|
| `title` | the site's name |
| `url` | **required**, the site's address |
| `description` | one sentence |
| `image` | optional, a screenshot next to the item (`showcase/<slug>/index.md` and `showcase/<slug>/shot.png`) |
| `order` | a whole number (default 1000) |

Settings: `man` (`"SITE-SHOWCASE(7)"`), `nav` (`"showcase/"`), `empty`
(`"No site listed yet."`), `visit` (`"visit ↗"`, the link on an item's
page). `{showcase}` lists every item as a grid of cards.

## The theme's words

`theme.toml` and `theme.fr.toml` hold them; a site overrides any of them
in its `site.toml` or `site.fr.toml`:

| Key | English |
|---|---|
| `search.label` | the search field's label |
| `search.placeholder` | its placeholder |
| `search.none` | a search that finds nothing |
| `search.count` | how many pages match: `{n}` is the number |
| `doc.contents` | the sidebar's summary on small screens |
| `doc.on_this_page` | over the `[TOC]` in the right column |

The rest (copy, previous, next, the sidebar's name...) are tilder's
`[labels]`.

## What the site must do

- **Use tilder 1.2.0 or later.** It ignores `theme.fr.toml` on a site
  that does not declare French, draws the collection sidebar as a tree,
  reads a collection's subfolders, and checks the theme (`--check`).
- **Let the search read its index.** The page's Content-Security-Policy
  needs `connect-src 'self'`, as in tilder's `examples/Caddyfile`. Without
  it, the search field removes itself and the rest of the page works.
- Ship `assets/logo.svg` (tilder draws the icons and `share.png` from it).

## Scripts

ES5, same-origin files, no storage, no cookie, no words of their own
(they arrive through `data-*`), progressive enhancement: without
JavaScript the sidebar is open, the `[TOC]` stays in the text, and there
is no search field. In the theme's source repository (not part of a
copied `theme/` folder), `tests/test_scripts.py` checks the rules, and
runs `search.js` under node when it is installed.

By hand, before a release, in a browser (the fixture built and served
over HTTP, `python3 -m http.server` in its output):

- [ ] The search field appears on a doc page; typing `elan` in French
      finds the page with "élan"; the count reads in the page's language.
- [ ] Arrow down and up move through the results; Enter follows the
      selected one; Escape clears the field.
- [ ] With the index missing (rename it), the field goes away.
- [ ] At 360px the sidebar is folded, opens on its summary, and folds
      again after a link is followed.
- [ ] At 1440px the `[TOC]` is in the right column, open, and follows
      the scroll; at 800px it is back in the text, folded.
- [ ] The copy button copies a code block without the language label;
      its word changes to "copied", then back.
- [ ] With JavaScript off, every page reads completely.

## Review by eye

In the theme's source repository, `tests/site/content/kitchen-sink.md`
uses every construct; the fixture as a whole writes every class of
tilder's contract but `.icon` (no network icons are shipped). Review it
in light and dark, at 360px and 1440px.

## Fonts

Self-hosted, never from a CDN. Latin and Latin Extended, subset from the
official releases with fonttools' `pyftsubset`; neither licence declares a
Reserved Font Name, so the subsets keep their names.

| Files | Upstream | Licence |
|---|---|---|
| `inter-regular.woff2`, `inter-italic.woff2`, `inter-bold.woff2` | Inter 4.1, `web/Inter-*.woff2` of `Inter-4.1.zip`, github.com/rsms/inter/releases | `fonts/OFL-Inter.txt` (the release's `LICENSE.txt`) |
| `jetbrains-mono-regular.woff2`, `jetbrains-mono-bold.woff2` | JetBrains Mono 2.304, `fonts/webfonts/*.woff2` of `JetBrainsMono-2.304.zip`, github.com/JetBrains/JetBrainsMono/releases | `fonts/OFL-JetBrainsMono.txt` (the release's `OFL.txt`) |

Unicode ranges kept: `U+0000-024F, U+0259, U+02BB-02BC, U+02C6, U+02DA,
U+02DC, U+0300-036F, U+1E00-1EFF, U+2000-206F, U+20A0-20C0, U+2100-214F,
U+2190-21FF, U+2212, U+2215, U+2500-257F, U+25A0-25FF, U+FEFF, U+FFFD`.

## Checks

tilder checks the theme against its own contract, and builds nothing:

```sh
python3 builder/build.py --check              # 0: fine, 1: a check failed
python3 builder/build.py --check --markdown   # and the table below, as Markdown
```

Every class tilder writes has a rule in `style.css`, and the colour pairs
`theme.toml` declares under `[check]` reach the minimum in the light and
the dark scheme. The theme leaves no class unstyled on purpose. A site
that ships its own `assets/style.css` is checked on that one.

## Contrast

Every text colour on both backgrounds, in both schemes, WCAG AA (4.5:1,
tilder's default `contrast_min`). tilder's `build.py --check --markdown`
prints this table; in the theme's source repository, a test keeps it in
step.

| scheme | foreground | background | ratio | minimum |
|---|---|---|---:|---:|
| light | `--text` | `--bg` | 18.88 | 4.5 |
| light | `--text` | `--surface` | 16.87 | 4.5 |
| light | `--muted` | `--bg` | 8.45 | 4.5 |
| light | `--muted` | `--surface` | 7.55 | 4.5 |
| light | `--faint` | `--bg` | 7.00 | 4.5 |
| light | `--faint` | `--surface` | 6.26 | 4.5 |
| light | `--accent` | `--bg` | 5.18 | 4.5 |
| light | `--accent` | `--surface` | 4.63 | 4.5 |
| light | `--info` | `--bg` | 5.18 | 4.5 |
| light | `--info` | `--surface` | 4.63 | 4.5 |
| light | `--warning` | `--bg` | 12.63 | 4.5 |
| light | `--warning` | `--surface` | 11.29 | 4.5 |
| light | `--error` | `--bg` | 17.40 | 4.5 |
| light | `--error` | `--surface` | 15.55 | 4.5 |
| dark | `--text` | `--bg` | 15.47 | 4.5 |
| dark | `--text` | `--surface` | 13.94 | 4.5 |
| dark | `--muted` | `--bg` | 9.21 | 4.5 |
| dark | `--muted` | `--surface` | 8.30 | 4.5 |
| dark | `--faint` | `--bg` | 6.78 | 4.5 |
| dark | `--faint` | `--surface` | 6.11 | 4.5 |
| dark | `--accent` | `--bg` | 8.99 | 4.5 |
| dark | `--accent` | `--surface` | 8.10 | 4.5 |
| dark | `--info` | `--bg` | 8.99 | 4.5 |
| dark | `--info` | `--surface` | 8.10 | 4.5 |
| dark | `--warning` | `--bg` | 12.02 | 4.5 |
| dark | `--warning` | `--surface` | 10.84 | 4.5 |
| dark | `--error` | `--bg` | 17.24 | 4.5 |
| dark | `--error` | `--surface` | 15.55 | 4.5 |
