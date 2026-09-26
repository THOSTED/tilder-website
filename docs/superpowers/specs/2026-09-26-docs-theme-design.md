# Documentation theme - design

Date: 2026-09-26. Status: approved in conversation, awaiting review of this
document. Depends on tilder `v1.1.0` (collection navigation,
`tilder/docs/superpowers/specs/2026-09-26-collection-nav-design.md`).
Followed by the site's content (`2026-09-26-site-content-design.md`).

---

## 1. Goal

A tilder theme for documentation sites, in `theme/` of this repository.
**Generic**: it names no project and holds no site text; any tilder
project that documents something can copy the folder. Bilingual out of the
box (English, French) through `theme.toml` / `theme.fr.toml`.

Look: **hybrid**. The landing page is airy and modern; every other page
reads as a man page.

### Not in this work

- A logo (none exists yet; see the site spec).
- Search beyond the documentation collection, fuzzy matching, or
  highlighting in the target page.
- Any site content.

---

## 2. Rules it follows

From tilder's `AGENTS.md` and `docs/theme.md`:

- styles **every** class of `docs/theme.md` (v1.1.0), light and dark;
- scripts: ES5, same-origin files, progressive enhancement, no network but
  same-origin JSON, no storage, no text of their own (`data-*`);
- no third-party request; fonts self-hosted;
- WCAG AA contrast, visible focus, `prefers-reduced-motion`, `.sr-only`;
- `layout.html` keeps `lang`, one `{{ brand }}`, `<main id="contenu">`
  (`lang="{{ content_lang }}"`), `<link rel="canonical">`.

## 3. Files

```
theme/
  README.md            what it is, the files, the collections and front matter it expects
  LICENSE              MIT
  layout.html          the man-page base
  layouts/home.html    the landing page
  layouts/doc.html     documentation pages
  style.css            tokens, base, man-page, home, doc, every contract class
  fonts/               two OFL woff2 families + their licences
  share.svg            the link preview (1200x630)
  code.js              copy button on code blocks (tilder contract)
  search.js            documentation search
  nav.js               collapsible sidebar on small screens
  types/doc.py         the "doc" type
  types/showcase.py    the "showcase" type
  theme.toml           [share] colours, the theme's words in English
  theme.fr.toml        the theme's words in French
```

## 4. Layouts

**`layout.html` (base, man-page).** A header rule (`site.manual` centred,
the page's `man` name on both sides), `{{ brand }}`, `{{ nav }}`,
`{{ languages }}`; one text column of ~75ch; `{{ prev }}{{ next }}` after
the body (a blog then gets them); the footer rule (`footer.left`,
`site.updated`, `footer.right`).

**`layouts/home.html`.** Same header, navigation and footer. The main area
is wide, and the page's sections are laid out as blocks. The page's first
section is the hero: large type, the tagline from `page.tagline`. Chosen by
`layout: home` in the landing page's front matter.

**`layouts/doc.html`** (the `doc` type's `LAYOUT`). Three columns on wide
screens:

| left | centre | right |
|---|---|---|
| search field (created by `search.js`) + `{{ collection_nav }}` | the body, then `{{ prev }}{{ next }}` | the page's `[TOC]` if it has one, sticky |

- Below ~60rem the right column folds into the body flow.
- Below ~45rem the left column becomes a `<details>` ("contents"). It is
  open by default in CSS, so it works without JS. `nav.js` closes it on
  load and after a link is followed.

## 5. Look

- **Tokens** on `:root`: background, surface, text, muted, faint, rule,
  accent (the terminal cyan of the text mirror, darkened for AA on light),
  info/warning/error. Redefined under `prefers-color-scheme: dark`.
- **Type**: a monospace family for the wordmark, headings, navigation,
  code and tags, and a sans-serif family for body text. The proposal is
  JetBrains Mono and Inter, both OFL, woff2, latin + latin-ext subsets. The
  `<h2>` are small caps / upper case with letter spacing, like man-page
  sections.
- **Live examples.** A documentation page shows a construct's source in a
  code block, then the construct itself inside an `.inset` (tilder's box).
  The theme draws `.inset` as a framed box with a dashed rule. Any label
  ("Rendered:") is written by the page in its own language, so the theme
  needs no word for it and the text mirror says it too.
- **Home**: generous spacing and larger type. Features are shown as a grid
  of `.entry` cards. Side-by-side panes (source, HTML, terminal) are built
  from existing classes: `pre.code` with `data-lang` and a two-column
  `.b.grid`.

## 6. The `doc` type (`types/doc.py`)

| | |
|---|---|
| `NAME` | `"doc"` |
| `ARTICLE` | `True` |
| `SEQUENTIAL` | `True` (prev/next in the text mirror) |
| `LOCALIZED_OUTPUTS` | `True` |
| `LAYOUT` | `"doc"` |
| `SCRIPT` | `"search.js"`: loaded on pages that list docs. `doc.html` also links it directly, from `{{ root }}`, `defer` |
| `DEFAULTS` | `man` = `"SITE-DOCS(7)"`, `nav` = `"docs/"`, `empty` = `"No page yet."`, `index` = `"search-index.json"` |

- Front matter:
  - `title`, `description`
  - `order` (an integer; default 1000)
  - `group` (read by tilder's collection nav)
- `sort_key`: `(order, slug)`.
- `entry`: a card with the title and the description. Used by `{docs}`,
  the marker that lists every page, grouped by `group` in the same order,
  as a documentation index.
- `json_ld`: `TechArticle`, with `headline`, `description`, `inLanguage`
  (`content_lang`) and `publisher`.
- `outputs(items, conf)` writes `{conf.dir}/{conf.index}`: a JSON array with
  one object per item, `{"t": title, "u": clean URL, "d": description,
  "h": [h2 titles], "x": plain text, first 2000 characters}`. It is read
  from `item["src"]`, with the front matter and Markdown punctuation
  stripped by a small local function, since the type may not import the
  builder's parser. Because of `LOCALIZED_OUTPUTS`, the French pass writes
  `fr/docs/search-index.json`.

## 7. The `showcase` type (`types/showcase.py`)

| | |
|---|---|
| `NAME` | `"showcase"` |
| `DEFAULTS` | `man` = `"SITE-SHOWCASE(7)"`, `nav` = `"showcase"`, `empty` = `"No site listed yet."`, `visit` = `"visit ↗"` |

- Front matter:
  - `title`, `url` (required, the site)
  - `description`
  - `image` (optional screenshot, next to the item in `<slug>/index.md`)
  - `order`
- `entry`: a card with the title, `url` as a meta line, the description,
  and the image if any (an `image` block with the alt text `title`).
- The marker `{showcase}` lists every item as a `grid`.
- `json_ld`: `WebSite` with `url`.
- Items have their own page (with the image, description, and link).

## 8. Scripts

**`search.js`**
- Finds `[data-search-index]` on the doc layout's left column. The URL is
  built from `{{ home }}` and the collection's `index`; the labels come from
  `data-label`, `data-placeholder`, `data-none` and `data-count`, from
  `theme.toml` through `{{ search.* }}` placeholders.
- Creates a labelled `<input type="search">` and a results `<ul>`
  announced by a `aria-live="polite"` region.
- Fetches the index on first focus, then does case- and accent-insensitive
  matching (NFD, then marks removed) on title, headings, description and
  text, ranked in that order, 10 results at most.
- Keyboard: the arrows move through the results and Enter follows the
  selected one.
- Without JS, nothing is created.

**`nav.js`**: see §4.

**`code.js`**: the copy button of tilder's contract. Its labels are
`labels.copy` and `labels.copied`, from `data-*`.

## 9. The theme's words

`theme.toml` (English) and `theme.fr.toml` (French) hold, under
`[search]`, `[doc]` and `[share]`:

- `label`, `placeholder`, `none`, `count`;
- `contents` (the mobile `<details>` summary) and `on_this_page` (the right
  column);
- the share colours.

A site overrides any of them in `site.toml`.

## 10. Checks

- `tools/check-theme.py`: every class listed in tilder's `docs/theme.md`
  (read from the pinned image, or passed as a path) appears in
  `style.css`. It runs in the build script.
- `content/kitchen-sink.md`, in the site, with `robots: noindex` and no
  navigation entry (`_`-prefixed files are not built). It uses every
  construct and every class, and is reviewed by eye in light and dark, at
  360px and at 1440px.
- The build must emit no warning.
- Contrast is checked for every token pair (text/background,
  muted/background, accent/background, both schemes) by `tools/check-contrast.py`, with the ratios recorded in the README.
