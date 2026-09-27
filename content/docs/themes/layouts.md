---
title: Layouts and placeholders
description: layout.html and layouts/, how tilder chooses a page's layout, every placeholder with its value and escaping, and what a layout must keep.
order: 20
---

## Name

layouts - the page around the content, and its placeholders

A layout is an HTML file in which the build replaces each `{{ name }}`
with a value: the page's title, its sections, the navigation, a value of
`site.toml`. `layout.html` serves every page; `layouts/<name>.html` serves
the pages of a type, or a page that asks for it. An unknown placeholder
stops the build, so a layout never ships with a hole in it.

[TOC]

## layout.html and layouts/

`theme/layout.html` is the one file a theme must have: without it, the
build stops with `no layout.html: a site needs a theme`. Other layouts sit
in `theme/layouts/`, one file each, named after what they serve:
`layouts/home.html` for a landing page, `layouts/post.html` for posts.
Every layout takes the same placeholders.

The starter's `layout.html` is a complete, short example. Stripped to its
bones:

```html
<!DOCTYPE html>
<html lang="{{ site.lang }}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ page.description }}">
<link rel="stylesheet" href="{{ root }}style.css">
<link rel="canonical" href="{{ canonical }}">{{ feeds }}
{{ head }}
</head>
<body>
<a class="skip" href="#contenu">{{ labels.skip }}</a>
<nav class="nav" aria-label="{{ labels.nav }}">
{{ nav }}
</nav>
{{ languages }}
{{ brand }}
<main id="contenu" lang="{{ content_lang }}">
{{ body }}
{{ prev }}
{{ next }}
</main>
<footer>{{ footer.right }}</footer>
{{ script }}</body>
</html>
```

## Which layout a page gets

The build takes the first of these that applies:

1. `layout:` in the page's front matter: `layout: home` uses
   `layouts/home.html`. The file must exist; if it does not, the build
   stops and names the page.
2. The layout of the page's type, its `LAYOUT`, which defaults to the
   type's name: a post uses `layouts/post.html`, an event
   `layouts/event.html`, if the theme has the file. A theme's type may
   name another one ([custom types](docs/content-types/custom-types)).
3. `layout.html`.

So a theme gives posts their own page by adding `layouts/post.html`,
without any setting. As with every theme file, a layout in the site's
`assets/` wins over the theme's ([files](docs/themes/files)).

## The placeholders

A placeholder is a name between double braces; the spaces inside are
optional (`{{title}}` works). Each is replaced by its value:

| Placeholder | Value |
|---|---|
| `{{ title }}` | the text of the `<title>`: the page's title followed by `site.title_suffix`, unless the title already holds the site's name |
| `{{ type }}` | the page's type: `page`, `post`, `event`, `member`, or a theme's |
| `{{ page.<key> }}` | a value of the page's front matter: `{{ page.description }}`, `{{ page.man }}`, `{{ page.tagline }}`; empty when the page does not set it |
| `{{ <section>.<key> }}` | a value of the configuration: `{{ site.lang }}`, `{{ site.manual }}`, `{{ footer.left }}`, `{{ labels.skip }}`, a theme's `{{ search.label }}` |
| `{{ root }}` | the relative path from the page to the site root (`./`, `../`), for `style.css`, the icons, the manifest, the fonts: the site root even on a page under `/fr/` |
| `{{ home }}` | the relative path to the landing page of the page's language, for links to pages: `{{ home }}{{ footer.left_link }}`; the same as `root` on a site in one language |
| `{{ canonical }}` | the page's absolute URL, for `<link rel="canonical">` |
| `{{ feeds }}` | a `<link rel="alternate">` for each RSS feed the page names |
| `{{ head }}` | the rest of the `<head>`: robots, author, Open Graph, Twitter Card, JSON-LD ([SEO](docs/reference/seo)) |
| `{{ brand }}` | the page's `<h1>`: the wordmark as a path, `~/<site>/<section>/<title>` |
| `{{ nav }}` | the links of `[[nav]]`, the current one marked `aria-current="page"` |
| `{{ languages }}` | the language switcher, a `<nav>` with one link per declared language, the current one marked `aria-current="page"`; empty on a site in one language |
| `{{ collection_nav }}` | the sidebar of the page's collection: its items in the collection's order, grouped by their `group:`, the current one marked `aria-current="page"`; on the collection's own page the same list, nothing marked; empty elsewhere |
| `{{ prev }}`, `{{ next }}` | links to the page's neighbours in its collection, labelled with `labels.prev` and `labels.next`; empty at either end, on the collection's own page, and outside a collection |
| `{{ content_lang }}` | the language of the page's content: the same as `site.lang`, unless the page is served as a fallback, in the language of the file that stands in for the translation |
| `{{ body }}` | the sections of the page, wrapped in an `<article>` for a type that is an article (posts, events) |
| `{{ script }}` | the `<script>` tags the page needs, if the theme has the files ([scripts](docs/themes/scripts)) |

<!-- 1.2 -->

In a recursive collection, such as this documentation, `{{ collection_nav }}`
is a tree: each folder is a section, an `<li class="collection-section">`
with its label and a list of its own, and the section that holds the page
is also `collection-section--open`, so the theme may fold the others
([classes](docs/themes/classes)).

### page.<key>

  Any key of the front matter, as the page writes it, after the type has
  filled its defaults: an event's `{{ page.man }}` is the collection's
  `man` when the event does not set its own. A key the page does not set
  gives an empty value, never an error, so a layout may read keys that
  only some pages have (`{{ page.tagline }}`).

### <section>.<key>

  Any value of the merged configuration, `defaults.toml` then the theme's
  `theme.toml` then the site's `site.toml`, in the page's language: the
  French pages read `theme.fr.toml` and `site.fr.toml` too. A name no
  layer sets stops the build with `unknown placeholder`, naming the
  layout: a theme gives every key its layouts read a value in its own
  `theme.toml` ([files](docs/themes/files)).

## Escaping

Front-matter and configuration values, `{{ page.<key> }}` and
`{{ <section>.<key> }}`, are HTML-escaped: `<`, `>`, `&` and quotes come
out as entities, so a value is safe inside an attribute as in text.
`{{ title }}` is escaped too.

The values the build computes go in as they are, being HTML already or a
path: `type`, `root`, `home`, `canonical`, `brand`, `nav`, `languages`,
`collection_nav`, `prev`, `next`, `content_lang`, `feeds`, `head`, `body`,
`script`.

## What the layout must keep

The build writes accessible, indexable markup; four things of it live in
the layout, and a theme keeps them:

- `lang="{{ site.lang }}"` on `<html>`: the language of the page, which
  screen readers and search engines read.
- One `{{ brand }}`: it is the page's only `<h1>`. The body's headings
  start at `<h2>`.
- A `<main id="contenu">`, or another target with the id the skip link
  points to: the first link of the page lets a keyboard skip the
  navigation.
- `<link rel="canonical" href="{{ canonical }}">`: the page's one address
  for search engines.

On a site with several languages, `<main lang="{{ content_lang }}">` is
recommended: a page served as a fallback, not yet translated, then
keeps the language of its text inside a page of another language.

Everything else is the theme's choice: where the navigation goes, whether
`{{ collection_nav }}` is a sidebar, whether `{{ prev }}` and `{{ next }}`
show at all. A layout that leaves out `{{ script }}` loads no script the
build names; one that leaves out `{{ head }}` loses the page's metadata.

## See also

- [the files of a theme](docs/themes/files)
- [classes](docs/themes/classes)
- [navigation in a collection](docs/content-types/navigation)
- [writing pages](docs/guide/writing)
