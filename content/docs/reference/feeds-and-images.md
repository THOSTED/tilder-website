---
title: Feeds and images
description: The files tilder writes besides the pages: RSS feeds, iCalendar, the icons and share.png drawn from SVG at every build, and the web manifest.
order: 50
---

## Name

feeds-and-images - RSS, iCalendar, icons, the link preview and the manifest

Besides the pages, the build writes the files that other programs read: an
RSS feed per collection that asks for one, in every language; an
iCalendar file for events; the icons and the link preview, drawn from
SVG at every build; and the web manifest. None of them is committed or
edited by hand: they come from the content and from `site.toml`.

[TOC]

## RSS

A collection writes an RSS 2.0 feed when its `feed` setting names a path
and its type gives feed items: `post` and `event` do, `member` and `page`
do not ([content types](docs/content-types)). `defaults.toml` sets
`blog/feed.xml` for the blog and `events.xml` for the events.

The feed is written in every language, under the language's prefix:
`blog/feed.xml` and `fr/blog/feed.xml`, each with that language's words
([languages](docs/guide/languages)).

| Element | Value |
|---|---|
| `<title>` | the collection's `feed_title` |
| `<link>` | the collection's page, its `nav` setting, as an absolute address in the language |
| `<atom:link rel="self">` | the feed's own address |
| `<description>` | the collection's `feed_description` |
| `<language>` | the language of the pass, `site.lang` |
| `<lastBuildDate>` | `site.updated` |
| one `<item>` per item | newest first: the title, the address as `<link>` and `<guid>`, the date as `<pubDate>`, the description |

Every item is in the feed, a past event as an upcoming one. A page
advertises a feed in its `<head>` with the `feed:` front-matter key, the
collection's name or `all` ([writing pages](docs/guide/writing)).

```toml
[collections.blog]
feed = "blog/feed.xml"
feed_title = "my site blog"
feed_description = "News of my site."
```

## iCalendar

An `event` collection writes an iCalendar file (RFC 5545) when its
`calendar` setting names a path; `defaults.toml` sets `calendar.ics` for
the events. Calendar apps subscribe to it. It is written once, at the
root, in the default language: a calendar has no interface language.

Each event is an all-day `VEVENT`: from its date to its `end`, or the same
day; a summary made of the title and `calendar.name`; the `place` as its
location, `lat` and `lon` as its `GEO`; its address and description. The
text is folded to ASCII, lines are cut at 75 octets as the standard asks,
and each event's identifier is `<slug>@<uid_domain>`. The calendar's own
name, description, product identifier and time zone come from the
`[calendar]` table ([event](docs/content-types/event),
[configuration](docs/reference/configuration)).

## Icons

The build draws the icons from one SVG, `assets/logo.svg` (the file
`share.logo_svg` names, in `assets/`), at every build:

| File | Size | Used by |
|---|---|---|
| `favicon.ico` | 16, 32 and 48 pixels, in one file | browsers' tabs |
| `apple-touch-icon.png` | 180x180 | a phone's home screen |
| `icon-192.png` | 192x192 | the web manifest |
| `icon-512.png` | 512x512 | the web manifest, the structured data's logo (`share.logo`) |

`logo.svg` itself is served as it is, from `assets/`, for the browsers
that take an SVG icon. The layout links the icons
([layouts](docs/themes/layouts)); the starter's writes:

```html
<link rel="icon" href="{{ root }}favicon.ico" sizes="48x48">
<link rel="icon" href="{{ root }}logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{{ root }}apple-touch-icon.png">
<link rel="manifest" href="{{ root }}site.webmanifest">
```

## The link preview

`share.png` is the image a link to the site shows on social networks and
in chat apps, 1200x630. The build draws it from the theme's `share.svg`
(or `assets/share.svg`, which wins), a template it fills first:

| Placeholder | Value |
|---|---|
| `{{ logo }}` | `assets/logo.svg`, embedded as a `data:` URI |
| `{{ wordmark }}` | `site.name`, in lowercase |
| `{{ manual_upper }}` | `site.manual`, in capitals |
| `{{ domain }}` | the host of `site.url` |
| `{{ card_1 }}`, `{{ card_2 }}` | the lines of `share.card`; empty when it has only one |
| `{{ section.key }}` | any value of the configuration: `{{ share.text_color }}`, `{{ site.name }}` |

An unknown placeholder stops the build. The text is drawn with the
theme's fonts, from its `fonts/` folder: the renderer reads TrueType,
not WOFF2, so each `*.woff2` is first decompressed with
`woff2_decompress`, when it is installed ([the files of a theme](docs/themes/files)).

Every page's `og:image` is `share.png`, unless the page sets `image:` or the theme draws a card per page (below).
The file is named by `share.image`. Without a `share.svg`, no preview is
drawn, and `og:image` is the icon, `icon-512.png`, with the small
`summary` card ([SEO](docs/reference/seo)).

## A card per page

With a `share-page.svg` in the theme, every other page gets its own
card: drawn at every build from the page's fields, written at
`/previews/<key>.png`, and named by `og:image`, `twitter:image` and the
`image` of a post's or an event's structured data. The key is a hash of
the filled template and the fonts: a page that does not change keeps its
file and its address. `share-<type>.svg`, `share-event.svg` for
instance, wins for the pages of that type. The landing page keeps
`share.png`; so does a page marked `noindex`, the 404. A page that sets
`image:` shows that image.

Besides the placeholders above, the template reads the page's own:

| Placeholder | Value |
|---|---|
| `{{ man }}` | the page's `man`, else `footer.right` |
| `{{ path }}` | the page's place, after `~/<site>`: `/events` for an event, `/mentoring` for a page, `/blog` for the blog's page |
| `{{ url }}` | the address of that place, without the scheme: `example.org/events` |
| `{{ title_1 }}`, `{{ title_2 }}` | the page's `share_title`, else its `title`, on `share.title_lines` lines of `share.title_columns` characters |
| `{{ title_shift }}` | how far up, in pixels, what follows the title moves when the title leaves a line empty: a `translate` |
| `{{ detail_1 }}` | the page's `tagline`; a post's or an event's is its date in words |
| `{{ detail_2 }}` | the page's `share_detail`, else an event's `place`, else a post's `author` |
| `{{ tags }}` | the post's `tag`, then the page's `share_tags`, each in an outlined box: SVG drawn from (0, 0) in `currentColor`, for a group that places it and gives its font and `color` |

The text is fitted by character count, so the template suits a
monospace face. A title breaks at spaces; what does not fit on its last
line is cut, ending with `...`, three dots. A detail line is cut at
`share.detail_columns`. Tags go left to right, as many on a line as
`share.tag_room` pixels hold, on up to `share.tag_lines` lines; the
second only when the title leaves its second line empty. A tag longer
than a line is cut; one that no longer fits is left out, with those
after it: a card never overflows.

An event gives its card tags with `share_tags`, comma-separated, and
may shorten its place for the card with `share_detail`:

```markdown
share_tags: stand all day, technical interview workshop
share_detail: Library · Downtown
```

They are for the card only: a page already says them in its text, and
an event's card on the site has its upcoming or past tag. `og:image:alt` is the card's text,
`~/my site/events - Meetup - Saturday 21 November 2026 - Library`,
unless the page sets `image_alt`. Like diagrams, cards are cached: in
memory while `--watch` runs, in `TILDER_CACHE`, and in the previous
output. tilder's starter theme ships a `share-page.svg`.

## Tools and fallbacks

Drawing needs an SVG renderer. The build uses the first one it finds:

1. `rsvg-convert`: it draws the text with the theme's fonts;
2. `magick`, ImageMagick 7.

tilder's Docker image has `rsvg-convert` and `woff2_decompress`, so a
build in Docker draws everything. With Python on its own, install one of
them from your system's packages. Without either, the build still works
and says so once:

```text
warning: no rsvg-convert or magick: icons and share.png not made
```

The layout's links to the icons then lead nowhere, and previews point
to a missing image: install a renderer before deploying. Without the logo,
the file `share.logo_svg` names, the build says so too, and draws
nothing:

```text
warning: no logo.svg in assets/: no icons, no share.png
```

Every warning is listed in [the command line](docs/reference/cli).

## The web manifest

`site.webmanifest`, written once at the root, tells a browser how to
install the site as an app. With the defaults, laid out shorter:

```json
{
  "name": "my site",
  "short_name": "site",
  "lang": "en",
  "start_url": "./",
  "display": "browser",
  "background_color": "#FDF6E3",
  "theme_color": "#0F6E68",
  "icons": [
    {"src": "logo.svg", "type": "image/svg+xml", "sizes": "any"},
    {"src": "icon-192.png", "type": "image/png", "sizes": "192x192"},
    {"src": "icon-512.png", "type": "image/png", "sizes": "512x512"}
  ]
}
```

The values are `site.name`, `share.short_name`, `site.lang`,
`share.background_color` and `share.theme_color`, in the default
language.

## See also

- [content types](docs/content-types)
- [SEO](docs/reference/seo)
- [the files of a theme](docs/themes/files)
