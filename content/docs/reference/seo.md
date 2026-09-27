---
title: SEO
description: What tilder writes for search engines and link previews: title, description, canonical, Open Graph, JSON-LD, sitemaps, robots.txt, checks.
order: 40
---

## Name

seo - titles, meta tags, structured data, sitemaps and the build's checks

Everything a search engine or a link preview shows of a page comes from
its front matter and from `site.toml`. The build writes the tags in the
`<head>`, the structured data, the sitemaps and `robots.txt`, then checks
every title and description and warns about what search engines cut or
penalise. There is nothing to install and nothing to fill in by hand.

[TOC]

## What a page controls

| Key | Becomes |
|---|---|
| `title` | the `<title>`, with `site.title_suffix`; `og:title` and `twitter:title`, without it |
| `name` | the page's name in the `<h1>` path, and in `og:title` instead of the title |
| `description` | `<meta name="description">`, `og:description`, `twitter:description`, the structured data, the feeds |
| `image` | the preview image, `og:image` and `twitter:image`, relative to the page's folder |
| `image_alt` | `og:image:alt`; default `share.image_alt` |
| `updated` | `<lastmod>` in `sitemap.xml`, and a post's `dateModified` |
| `robots` | `<meta name="robots">`; default `seo.robots`. With `noindex`, the page leaves the sitemaps and the checks |

Every front-matter key is described in [writing pages](docs/guide/writing).
Write for people first: a title that says what the page is, a description
that says why to open it.

## Title and description

The `<title>`, the layout's `{{ title }}`, is the page's `title` followed
by `site.title_suffix`, unless the title already contains `site.name`, in
any case. With the defaults, `title: about` gives `about - my site`.

The description is the page's `description`, one sentence. The starter's
layout writes it as `<meta name="description">` from `{{ page.description }}`;
the build writes it again for Open Graph and Twitter Card.

## Canonical URL

Every page has one address, on the site's origin, without `.html`:
`https://example.org/about`, `https://example.org/blog/`. The layout
writes it as `<link rel="canonical">` from `{{ canonical }}`, and the
build uses it for `og:url`, the structured data and the sitemaps. It is
built from `site.url`, which must be the address the site is served at.

On a site with several languages, each page also lists its siblings,
`<link rel="alternate" hreflang="...">`, one per declared language, and
`hreflang="x-default"` for the default one
([languages](docs/guide/languages)).

## The head

`{{ head }}` holds, in this order ([layouts](docs/themes/layouts)):

- the language alternates, on a site with several languages;
- `<meta name="robots">`: the page's `robots`, else `seo.robots`,
  `index, follow, max-image-preview:large`;
- the type's own name tags: a post with an `author` gets
  `<meta name="author">`;
- Open Graph;
- the type's own property tags: a post's `article:published_time`, and
  `article:tag` when it has a `tag`;
- Twitter Card;
- the structured data.

## Open Graph

What a link preview reads, on social networks and in chat apps:

| Property | Value |
|---|---|
| `og:site_name` | `site.name` |
| `og:locale` | `site.locale` |
| `og:locale:alternate` | each other declared language's `locale`, once |
| `og:type` | the type's: `article` for posts, `website` for every other built-in type |
| `og:title` | the page's `name`, else its title without the suffix |
| `og:description` | the description |
| `og:url` | the canonical URL |
| `og:image` | the page's `image`; else `share.png`, when the theme has a `share.svg`; else the icon, `share.logo` |
| `og:image:alt` | the page's `image_alt`, else `share.image_alt` |
| `og:image:width`, `og:image:height` | the image's size, read from the file, when it is known |

An `image` is a PNG or a JPEG of 1200x630 at best: social platforms
mostly ignore SVG. How `share.png` and the icons are drawn is in
[feeds and images](docs/reference/feeds-and-images).

## Twitter Card

| Name | Value |
|---|---|
| `twitter:card` | `summary_large_image` when the image is at least 600 pixels wide and wider than tall; else `summary` |
| `twitter:title` | as `og:title` |
| `twitter:description` | the description |
| `twitter:image` | as `og:image` |

## Structured data

Every page carries one `<script type="application/ld+json">`: inert
data, never run, which the site's security policy lets through. It is a
graph of up to four nodes.

- `Organization`: `seo.organization`, the site's address, and the logo,
  `share.logo`.
- `WebSite`: `site.name`, the site's address, its language, and the
  organization as publisher.
- The page's own node, given by its type, with the page's address and
  language.
- `BreadcrumbList`: the first `[[nav]]` entry, then the entry the page
  marks with `nav:`, when it is a page of the site and not the page
  itself, then the page. The landing page has none.

The page's node, per type:

| Type | Node | Carries |
|---|---|---|
| `page` | `WebPage` | the `<title>`, the description, the site it is part of |
| `post` | `BlogPosting` | headline, description, `datePublished` (the file's date), `dateModified` (`updated`, else the date), the organization as publisher, the image, and `author` as a `Person` when the post names one |
| `event` | `Event` | name, description, `startDate`, `endDate` (`end`, else the date), scheduled, in person, the `place` as a `Place` with `geo` when `lat` and `lon` are given, the organization as organizer, the image |
| `member` | `ProfilePage` | the `<title>`, and a `Person`: the member's name, member of the organization, the profile links as `sameAs`, the `affiliation` |

A type a theme adds gives its own node, or gets a `WebPage`
([custom types](docs/content-types/custom-types)). Check the result with
a structured-data validator after changing a type.

## Sitemaps

Two sitemaps at the root, one for every language:

- `sitemap.xml`: every page, sorted by address, with its `<lastmod>`: the
  page's `updated`, else its date for a post or an event, else
  `site.updated`. On a site with several languages, each address lists
  its siblings in every language, and `x-default`.
- `sitemap.txt`: the same addresses, one per line.

A page whose `robots` contains `noindex` is left out of both, as the
starter's 404 page is. `robots.txt` points to `sitemap.xml`: give that
address to the search engines' consoles too.

## robots.txt

The build writes two, from two tables of the configuration
([configuration](docs/reference/configuration)):

- `robots.txt`, for the site, from `[robots]`: one `Disallow:` line per
  path of `robots.disallow`, by default `/txt/` and `/ansi/`, then the
  sitemap's address;
- `txt/robots.txt`, the `robots.txt` of the plain-text host, which serves
  `txt/` as its root, from `[robots_man]`: by default `robots_man.disallow`
  is `/`, the whole host.

An empty list writes `Allow: /` instead. With the defaults:

```text
User-agent: *
Disallow: /txt/
Disallow: /ansi/

Sitemap: https://example.org/sitemap.xml
```

The text mirrors duplicate the pages: search engines are asked to index
the pages only ([the text mirror](docs/reference/text-mirror)).

## The build's checks

After each language's pages, the build checks every page but those
marked `noindex`, and prints a line on its error output for each
problem:

```text
seo: [en] about.html: title is 64 characters (max 60)
seo: [en] about.html: description is 38 characters (50-160)
seo: [en] blog/index.html: same title as about.html
seo: [fr] about.html: same description as index.html
```

| Warning | When |
|---|---|
| `title is N characters` | the `<title>`, suffix included, is longer than `seo.title_max`, `60` |
| `description is N characters` | the description is shorter than `seo.description_min`, `50`, or longer than `seo.description_max`, `160` |
| `same title as` | two pages of one language share a `<title>` |
| `same description as` | two pages of one language share a description |

The sample above is from a site in two languages, where each line names the
language of the pass, the default one included, `[en]`, `[fr]`; a site in
one language writes the lines without it, `seo: about.html: ...`. A warning does not stop the build nor change its exit
code: a site that wants it to, as this one does, fails on any `seo:`
line in its own build script ([the command line](docs/reference/cli)).
Change the limits in `[seo]`:

```toml
[seo]
title_max = 65
description_max = 155
```

## See also

- [writing pages](docs/guide/writing)
- [feeds and images](docs/reference/feeds-and-images)
- [configuration](docs/reference/configuration)
