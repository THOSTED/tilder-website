---
title: Configuration
description: Every key of tilder's defaults.toml, table by table: its default value, what it does, and an example of setting it in site.toml.
order: 20
---

## Name

configuration - every key of defaults.toml

tilder reads every setting of a site, and every word a reader sees
outside the pages, from TOML. Its own `defaults.toml` holds each key with
a neutral, English default; the theme's `theme.toml` and the site's
`content/site.toml` are merged over it, and state only what differs. This
page lists every key of `defaults.toml`, table by table, with its default
exactly as the file writes it.

[TOC]

## How the files merge

Each file is merged over the one before, the last one winning:
`defaults.toml`, then `theme/theme.toml`, then `content/site.toml`. On a
site with several languages, `theme/theme.<lang>.toml` comes after
`theme.toml`, and `content/site.<lang>.toml` after `site.toml`, for the
pass of that language ([the project](docs/guide/project),
[languages](docs/guide/languages)).

- Tables merge key by key: a file that sets `[site] manual` keeps every
  other key of `[site]`.
- A value that is not a table, a list included, replaces the one before
  as a whole. So does a list of tables, `[[nav]]`: a file that sets it
  repeats every entry.
- A collection's settings start from its type's own defaults, in the
  type's module, with `[collections.<name>]` over them
  ([content types](docs/content-types)).

The files are read again at every build, and none of them is ever served.
A key tilder does not read is ignored, except the few removed tables that
stop the build with a message saying where their keys went
([the command line](docs/reference/cli)).

## Site

The `[site]` table: who the site is, where it lives, its language.

| Key | Default | Meaning |
|---|---|---|
| `site.name` | `"my site"` | the wordmark, `~/my site`; `og:site_name`; the `WebSite` of the structured data; the web manifest's `name` |
| `site.url` | `"https://example.org"` | the canonical origin, without a trailing slash: every absolute address the build writes starts with it |
| `site.lang` | `"en"` | the default language, served at the root: `lang` of the page, the feeds, the manifest |
| `site.locale` | `"en_GB"` | `og:locale`, for Open Graph |
| `site.manual` | `"My Site Manual"` | the centre of the man-page header rule, on the page and in the text mirror |
| `site.updated` | `2026-01-01` | a TOML date, not a string: the date in the footer rule, the feeds' `lastBuildDate`, the sitemap's last resort for `<lastmod>` |
| `site.title_suffix` | `" - my site"` | appended to every `<title>` that does not already contain `site.name` |
| `site.languages` | `[]` | every language served, the default (`lang`) first; empty: one language, no prefix |

`site.url` must be the address the site is served at: the canonical
links, `og:url`, the sitemaps, the feeds and the calendar are built from
it. `site.title_suffix` is added only when the title does not name the
site already, in any case: a page titled `About my site` keeps its title
as it is.

```toml
[site]
name = "my site"
url = "https://example.org"
lang = "en"
locale = "en_GB"
manual = "My Site Manual"
updated = 2026-05-16
title_suffix = " - my site"
languages = ["en", "fr"]
```

## Footer

The `[footer]` table: the man-page footer rule at the bottom of every
page, with `site.updated` in its middle.

| Key | Default | Meaning |
|---|---|---|
| `footer.left` | `"SITE"` | the left of the footer rule; in the starter's layout, a link |
| `footer.left_link` | `""` | where `footer.left` links, from the language's landing page: `""` is the landing page itself |
| `footer.right` | `"SITE(1)"` | the right of the footer rule |

The text mirror writes the footer rule from these keys itself. On the
page, the layout places them where it wants: the starter writes
`<a href="{{ home }}{{ footer.left_link }}">{{ footer.left }}</a>`
([layouts](docs/themes/layouts)).

```toml
[footer]
left = "MYSITE"
left_link = "about"
right = "MYSITE(1)"
```

## Labels

The `[labels]` table: the words of the interface, many of them heard only
through a screen reader. Translate them in `site.<lang>.toml`.

| Key | Default | Meaning |
|---|---|---|
| `labels.skip` | `"skip to content"` | the skip link, first in the page (a layout placeholder) |
| `labels.nav` | `"Main navigation"` | the name of the navigation landmark (a layout placeholder) |
| `labels.info` | `"INFO"` | the label of an information callout, on the page and in the text mirror's box |
| `labels.warning` | `"WARNING"` | the label of a warning callout |
| `labels.error` | `"ERROR"` | the label of an error callout |
| `labels.image` | `"image"` | the text mirror's line for an image: `[ image ] alt text` |
| `labels.task_done` | `"done"` | a done item of a task list, read by screen readers |
| `labels.task_todo` | `"to do"` | an open item of a task list, read by screen readers |
| `labels.to_top` | `"↑ back to top"` | the link back to the top of the page (a layout placeholder) |
| `labels.copy` | `"copy"` | the copy button on code blocks, given to the theme's `code.js` |
| `labels.copied` | `"copied"` | the same button once it has copied |
| `labels.external` | `"external site"` | said by screen readers after an external link marked with the arrow, instead of the arrow |
| `labels.new_tab` | `"opens in a new tab"` | said by screen readers on a link that opens a new tab |
| `labels.table` | `"table"` | the name of a table's scrollable region |
| `labels.toc` | `"contents"` | the title of the `[TOC]` block; in capitals in the text mirror |
| `labels.website` | `"website"` | a member's own site, among the profile links |
| `labels.languages` | `"Languages"` | the name of the language switcher, `{{ languages }}` |
| `labels.collection_nav` | `"In this section"` | the name of the `{{ collection_nav }}` sidebar; a collection may set its own `nav_label` |
| `labels.prev` | `"previous"` | the label of `{{ prev }}`, and of the text mirror's line of a sequential type |
| `labels.next` | `"next"` | the label of `{{ next }}`, and of that line |

The three callout labels also pick the colour of the callout's box in the
coloured mirror: the box whose top rule carries `labels.info` follows
`text.accent`, `labels.warning` is yellow, `labels.error` red
([the text mirror](docs/reference/text-mirror)). The layout placeholders
work only where the theme's `layout.html` writes them, as the starter's
does.

```toml
# content/site.fr.toml
[labels]
skip = "aller au contenu"
toc = "sommaire"
prev = "précédent"
next = "suivant"
```

## Links

The `[links]` table: whether external links open in a new tab.

| Key | Default | Meaning |
|---|---|---|
| `links.new_tab` | `false` | `true`: every external link, `http://` or `https://`, opens in a new tab |
| `links.same_tab` | `[]` | with `new_tab` on, the hosts whose links stay in the same tab, their subdomains too |

A link that opens a new tab gets `target="_blank"` and `rel="noopener"`,
and tells screen readers so with `labels.new_tab`. The rule covers links
in pages, the navigation and a member's profile links
([writing pages](docs/guide/writing)).

```toml
[links]
new_tab = true
same_tab = ["example.com"]    # and its subdomains
```

## Languages

The `[languages]` table is empty by default: it maps a language's code
to the name the language switcher shows. A language without a name shows
its code.

```toml
[languages]
en = "English"
fr = "Français"
```

The names are read from the default language's configuration only, so
they are written once, in `site.toml`, each in its own language
([languages](docs/guide/languages)).

## Navigation

The `[[nav]]` list of tables: the navigation, in order, one table per
link. The default has one entry.

| Key | Default | Meaning |
|---|---|---|
| `nav.label` | `"home"` | the link's text |
| `nav.href` | `""` | the target, written from the site root: `""` is the landing page, `docs/` a folder's page, `about` a page; `https://` is an external link |

A page marks its entry as the current one with its `nav:` front-matter
key, equal to the entry's `href` ([writing pages](docs/guide/writing)).
The first entry is also the first step of every page's breadcrumb in the
structured data, and the entry a page marks, unless it is the landing
page or an external link, is the second one ([SEO](docs/reference/seo)). Links stay inside the current language:
`about` from a French page leads to `/fr/about`.

A list of tables is replaced as a whole: a site that adds one link
writes them all, the first one included.

```toml
[[nav]]
label = "home"
href = ""

[[nav]]
label = "blog"
href = "blog/"

[[nav]]
label = "source ↗"
href = "https://example.com/my-site"
```

## SEO

The `[seo]` table: structured data, the default for robots, and the
limits of the build's checks ([SEO](docs/reference/seo)).

| Key | Default | Meaning |
|---|---|---|
| `seo.organization` | `"My Site"` | the publisher: the `Organization` node of every page's structured data |
| `seo.robots` | `"index, follow, max-image-preview:large"` | `<meta name="robots">` of a page that sets no `robots:` |
| `seo.title_max` | `60` | a `<title>` longer than this, suffix included, is a warning |
| `seo.description_min` | `50` | a description shorter than this is a warning |
| `seo.description_max` | `160` | a description longer than this is a warning |

```toml
[seo]
organization = "Example Group"
title_max = 65
```

## Sharing

The `[share]` table: the icons, the link preview and the web manifest.
The icons are drawn at every build from `assets/logo.svg`, and
`share.png` from the theme's `share.svg`, filled with values from here
([feeds and images](docs/reference/feeds-and-images)).

| Key | Default | Meaning |
|---|---|---|
| `share.logo_svg` | `"logo.svg"` | the source of every icon, a file of `assets/` |
| `share.image` | `"share.png"` | the default preview's file, 1200x630, drawn from the theme's `share.svg`: the `og:image` of every page that sets no `image:`, when the theme has one |
| `share.logo` | `"icon-512.png"` | the logo of the structured data, and the preview of a theme without `share.svg`; the name of an icon the build draws |
| `share.image_alt` | `"my site"` | `og:image:alt` of a page that sets no `image_alt:` |
| `share.card` | `["a man-page website"]` | the preview's lines under the name, one or two: `{{ card_1 }}` and `{{ card_2 }}` in `share.svg` |
| `share.theme_color` | `"#0F6E68"` | the colour of the browser's interface: the manifest's `theme_color`, the starter's `<meta name="theme-color">`, and the preview |
| `share.background_color` | `"#FDF6E3"` | the manifest's `background_color`, and the preview's background |
| `share.text_color` | `"#073642"` | the preview's text |
| `share.muted_color` | `"#506C75"` | the preview's secondary text |
| `share.rule_color` | `"#DED7C3"` | the preview's rules |
| `share.short_name` | `"site"` | the manifest's `short_name`, the name under an icon on a home screen |

The five colours are for the theme's `share.svg`, which reads them as
`{{ share.text_color }}` and the like; a theme usually sets them in its
`theme.toml`, to match its palette. Only `theme_color` and
`background_color` are also written by the build itself, in the
manifest.

```toml
[share]
image_alt = "~/my site"
card = ["meetups and talks", "in Exampleville"]
short_name = "mysite"
```

## Collections

`[collections.<name>]` declares a folder of `content/` whose files are
items of one type ([content types](docs/content-types)). Its keys are the
type's settings, each listed on the type's page, plus these:

| Key | Default | Meaning |
|---|---|---|
| `type` | `"post"` | the type: `page`, `post`, `event`, `member`, or one the theme adds |
| `dir` | the collection's name | the folder, under `content/` |

From tilder 1.2, `recursive = true` makes the subfolders of `dir`
sections of the collection, and their files its items, in the sidebar's
tree ([navigation](docs/content-types/navigation)). It is `false` unless
the collection or its type's `DEFAULTS` sets it; a dated type, such as
`post` or `event`, cannot be recursive, and the build stops if one is.

`defaults.toml` declares the three collections most sites have. Each one
is inactive until its folder exists: no page, no feed, no calendar.

| Key | Default |
|---|---|
| `collections.blog.type` | `"post"` |
| `collections.blog.dir` | `"blog"` |
| `collections.blog.feed` | `"blog/feed.xml"` |
| `collections.events.type` | `"event"` |
| `collections.events.dir` | `"events"` |
| `collections.events.nav` | `"events"` |
| `collections.events.feed` | `"events.xml"` |
| `collections.events.calendar` | `"calendar.ics"` |
| `collections.members.type` | `"member"` |
| `collections.members.dir` | `"members"` |

A site sets only what differs from them, or declares its own:

```toml
[collections.blog]
man = "MYSITE-BLOG(7)"
feed_title = "my site blog"

[collections.talks]
type = "event"
feed = "talks.xml"
calendar = "talks.ics"
```

The settings of each built-in type are on its page:
[post](docs/content-types/post), [event](docs/content-types/event),
[member](docs/content-types/member), [page](docs/content-types/page).

## Dates

The `[dates]` table: how a date is written out in words, on a post's or an
event's card and as the tagline of a post or an event.

| Key | Default | Meaning |
|---|---|---|
| `dates.weekdays` | `["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]` | the days, Monday first |
| `dates.months` | `["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]` | the months, January first |
| `dates.first` | `"1"` | how the first day of a month is written |
| `dates.format` | `"{weekday} {day} {month} {year}"` | the pattern |

`dates.format` takes four names in braces: `{weekday}`, `{day}` (the day's
number, without a leading zero, or `dates.first` on the first of the
month), `{month}` and `{year}`. With the defaults, `2026-11-21` is
Saturday 21 November 2026. A French site writes "samedi 1er novembre":

```toml
# content/site.fr.toml
[dates]
weekdays = ["lundi", "mardi", "mercredi", "jeudi", "vendredi",
            "samedi", "dimanche"]
months = ["janvier", "février", "mars", "avril", "mai", "juin",
          "juillet", "août", "septembre", "octobre", "novembre",
          "décembre"]
first = "1er"
format = "{weekday} {day} {month} {year}"
```

## Calendar

The `[calendar]` table: what every iCalendar file of the site shares, for
the collections that set `calendar` ([event](docs/content-types/event)).

| Key | Default | Meaning |
|---|---|---|
| `calendar.name` | `"events"` | the calendar's name in calendar apps, and the end of each event's summary |
| `calendar.description` | `"Events."` | the calendar's description |
| `calendar.prodid` | `"-//site//events//EN"` | the product identifier, `PRODID` |
| `calendar.timezone` | `"UTC"` | the calendar's time zone |
| `calendar.uid_domain` | `"example.org"` | the domain of each event's identifier, `<slug>@<uid_domain>`: set your own |

```toml
[calendar]
name = "my site events"
prodid = "-//example.org//events//EN"
uid_domain = "example.org"
```

## Text

The `[text]` table: the coloured text mirror's colours.

| Key | Default | Meaning |
|---|---|---|
| `text.commands` | `["curl"]` | the words that start a command line worth highlighting, in a code block of the coloured mirror |
| `text.accent` | `"cyan"` | the one accent colour of `ansi/`: links, `[ tags ]`, list markers, inline `code`, command lines, the INFO box, and (in a highlighted code block) keywords and builtins |

A code-block line that starts with one of `text.commands`, alone or after a
prompt, `$` or `#` and a space, is coloured in the accent in `ansi/`; `txt/` has no
colour at all ([the text mirror](docs/reference/text-mirror)).

`text.accent` is one of the eight colour names `black`, `red`, `green`,
`yellow`, `blue`, `magenta`, `cyan` (the default), `white`, or a
256-colour index from 16 to 255, such as `208` for orange. Anything else
stops the build. A `site.<lang>.toml` may set its own accent for that
language.

```toml
[text]
commands = ["curl", "docker", "python3"]
accent = 208
```

## Robots

Two tables, one per `robots.txt` the build writes
([SEO](docs/reference/seo)).

| Key | Default | Meaning |
|---|---|---|
| `robots.disallow` | `["/txt/", "/ansi/"]` | the site's `robots.txt`: the paths search engines are asked to leave out, the text mirrors |
| `robots_man.disallow` | `["/"]` | `txt/robots.txt`, the `robots.txt` of the plain-text host: everything |

Each path becomes a `Disallow:` line; an empty list writes `Allow: /`
instead. The site's `robots.txt` also points to `sitemap.xml`.

```toml
[robots]
disallow = ["/txt/", "/ansi/", "/drafts/"]
```

## Theme checks

The `[check]` table is the theme's, read by `build.py --check` (tilder
1.2) and set in `theme/theme.toml`; `content/site.toml` may set it too,
merged over the theme's as every other table: `unstyled`, the classes
the theme leaves unstyled on purpose (default `[]`); `contrast`, the pairs of
colours to check (default `[]`, nothing checked); `contrast_min`, the
least ratio of every pair (default `4.5`). Every key is described in
[checking a theme](docs/themes/checking).

## See also

- [the project](docs/guide/project)
- [content types](docs/content-types)
- [layouts](docs/themes/layouts)
- [the command line](docs/reference/cli)
