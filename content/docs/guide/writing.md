---
title: Writing pages
description: From a Markdown file to a page: its address, every front-matter key, man-page sections, links inside and across languages, and images.
order: 30
---

## Name

writing - pages, front matter, sections, links and images

A page is one Markdown file under `content/`: a front matter that says
what the page is, then sections in the manner of a man page. Its path
gives its address. Links are written from the site root and the build makes
them relative; images sit next to the page that shows them.

[TOC]

## Pages and addresses

A file's path under `content/` is its address, without the `.md`. A
folder's `index.md` is the folder's own page, with a trailing slash.

| Source | Address | Text mirror |
|---|---|---|
| `content/index.md` | `/` | `txt/index.txt` |
| `content/about.md` | `/about` | `txt/about.txt` |
| `content/blog/index.md` | `/blog/` | `txt/blog.txt` |
| `content/blog/2026-01-01-hello.md` | `/blog/2026-01-01-hello` | `txt/blog/2026-01-01-hello.txt` |
| `content/blog/2026-01-01-hello/index.md` | the same | the same |

- The build writes `about.html`; the server answers `/about` with it
  ([deployment](docs/guide/deployment)).
- Name files in English, in lower case, with hyphens:
  `code-of-conduct.md`. The page itself may be in any language, and its
  translations keep the same name ([languages](docs/guide/languages)).
- A file or a folder whose name starts with `_` is never built:
  `_draft.md`, `blog/_template.md`.
- An item of a collection may be a folder, `<slug>/index.md`, to keep its
  images beside it; its page is still `/blog/<slug>`.
- Every page is listed in `sitemap.xml` and `sitemap.txt`, unless its
  `robots` says `noindex`.

In a recursive collection, such as the documentation you are reading,
folders nest: `content/docs/guide/writing.md` is the page
`/docs/guide/writing`, and a folder's `index.md` is that section's own
page, beside it: `content/docs/guide/index.md` is `/docs/guide`. The
[collections](docs/content-types) page explains the switch, `recursive`.

## Front matter

The front matter opens the file, between two `---` lines: one `key: value`
per line. Values are plain text, never quoted: `nav: ""` would be two
quote marks, so the landing page writes `nav:` with nothing after it.

```text
---
man: MYSITE-ABOUT(7)
title: About
description: Who writes this site and why, and how to reach them.
tagline: who, why and how to write
nav: about
---

## Name

about - who writes this site
```

These keys apply to every page. The ones marked required stop the build
when they are missing; `man`, `tagline` and `nav` come from the collection
for its items, which may leave them out.

| Key | Meaning |
|---|---|
| `man` | required: the man-page name, `MYSITE-ABOUT(7)`, in the header rule of the page and of its text mirror |
| `title` | required: the page's title. The `<title>` adds `site.title_suffix` unless the title already names the site. The build warns past `seo.title_max` characters, suffix included (60) |
| `description` | required: one sentence, for search engines, link previews and feeds. The build warns outside `seo.description_min` to `seo.description_max` characters (50 to 160) |
| `name` | the page's last segment in the `<h1>` path, `~/my site/<name>`; default: the title without the suffix. On a folder's page, it also names that folder's segment on every page inside. `heading` is its older spelling |
| `tagline` | the line under the wordmark, for the layout's `{{ page.tagline }}`; a post's or an event's defaults to its date |
| `nav` | the `[[nav]]` entry marked current, by its `href`: `about`, `blog/`, nothing for the landing page, `-` for none |
| `feed` | a collection's name, or `all`: adds the `<link rel="alternate">` of that collection's RSS feed |
| `text` | `text: no` builds no text mirror for the page (the 404 page does this) |
| `image` | the link preview, relative to the page's folder; default `share.image`. A PNG or a JPEG, ideally 1200x630: social platforms mostly ignore SVG |
| `image_alt` | the preview's alternative text; default `share.image_alt` |
| `updated` | a date, `2026-03-01`: the page's last change in the sitemap; default: an item's date, else `site.updated` |
| `robots` | the page's `<meta name="robots">`; default `seo.robots`. With `noindex`, the page leaves the sitemaps and the build's SEO checks |
| `layout` | `layout: home` renders the page with the theme's `layouts/home.html`, which must exist |
| `group` | in a collection, the item's group in the theme's sidebar |
| `order` | read by this site's theme, not by tilder: a whole number, the page's place among the documentation pages (default 1000) |

Each type reads keys of its own: a post's `author` and `tag`, an event's
`place` and `end`, a member's names and profiles. They are listed with
their type, under [content types](docs/content-types). Any other key is
kept, and a layout shows it with `{{ page.<key> }}`
([layouts](docs/themes/layouts)).

## Sections

A section is a `##` heading and what follows it. It is laid out as a row
of a man page: the name in the left margin, the text beside it. In the
text mirror, the name is printed in capitals at the left edge and the
text indented under it.

Pages open with `## Name`, as a man page does: the page's name, a dash
and one line that says what it is, then a paragraph that sums the page
up. The other sections follow in the order a reader needs them.

```text
## Name

about - who writes this site

A paragraph that sums up the page.

## Contact {#write}

Write to the address below.
```

A heading may end with markers in braces. `{#write}` gives the section
the id `write`, so `about#write` links to it; without one, the id comes
from the title. `{text}` keeps a section out of the HTML page and `{html}`
out of the text mirror. `{grid}` lays its entries out as cards, a list
marker such as `{posts}` fills it from a collection, and any other word
becomes a class. `###` headings inside a section are entries, whose text
is indented two spaces. The
[sections reference](docs/reference/markdown/sections) has every marker.

## Links

Write the target of a link from the site root: no leading slash, no
`.html`. The build rewrites it relative to the page, so the same source
works on any page, however deep.

| Target | Leads to |
|---|---|
| `blog/2026-01-01-hello` | a page |
| `blog/` | a folder's page: keep the slash |
| empty, or `./` | the landing page |
| `about#write` | a section of a page |
| `#write` | a section of this page |
| `blog/feed.xml`, `logo.svg` | a file, served under its own name |
| `https://example.org/` | another site, left as it is |

This page links the next one as `[languages](docs/guide/languages)`; the
build writes `languages`, since both are in `/docs/guide/`.

**Across languages.** On a site in several languages, a target stays in
the language of the page: `docs/guide/languages` on a French page is the
French page, `/fr/docs/guide/languages`. A target that starts with `/`
leaves the language: `[in English](/about)` from a French page,
`[en français](/fr/about)` from an English one. A file is written once,
at the root, and every language links the same file. RSS feeds are
written per language, but a link to `blog/feed.xml` in a page is still
the default language's feed: write `/fr/blog/feed.xml` for the French one
([languages](docs/guide/languages)).

**External links.** End the label of a link to another site with the
north-east arrow, U+2197: `[archive ↗](https://example.org/)`. Screen
readers skip the arrow and hear `labels.external` instead; the text
mirror drops it. Whether external links open a new tab is decided once for
the site, in `site.toml`:

```toml
[links]
new_tab = true                # external links: a new tab
same_tab = ["example.com"]    # except these hosts, subdomains too
```

The defaults are `new_tab = false` and `same_tab = []`. A link that opens
a new tab tells screen readers so beforehand, with `labels.new_tab`. In
the text mirror, an internal link keeps only its label, while an external
one prints its address in parentheses after it.

## Images

An image stands alone on its line, as in Markdown; the quoted text after
the path, optional, is its caption:

```text
![A page's two outputs](flow.svg "One source, two renderings.")
```

- The path is relative to the page's folder, unlike links: put the image
  next to the page. For a post, use a folder, `blog/2026-01-01-hello/`,
  with `index.md` and the image inside.
- The alternative text is required: it is what a screen reader says and
  what the text mirror shows, `[ image ] A page's two outputs`.
- The build reads the width and height from the file (PNG, JPEG, GIF,
  WebP, SVG), so the page does not jump while it loads.
- An image from another site is allowed by the syntax, but the
  recommended server policy only lets pages load images from their own
  site: it will not display.

The build warns, and goes on, when the file is missing or the alternative
text is empty:

```text
warning: image not found: content/blog/2026-01-01-hello/flow.svg
warning: image without alt text: blog/2026-01-01-hello/flow.svg
```

Prefer SVG for diagrams: an SVG file may carry its own dark-mode colours,
and the server lets it style itself, never run a script. The
[links and images reference](docs/reference/markdown/links-and-images)
has the details.

## See also

- [the Markdown reference](docs/reference/markdown)
- [languages](docs/guide/languages)
- [SEO](docs/reference/seo)
