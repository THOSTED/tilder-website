---
title: Content types
description: Collections of pages of one type: declaring them, their items, the list markers, their RSS feeds and iCalendar files, and the four built-in types.
order: 20
---

## Name

content types - collections, and the types that give them their shape

A collection is a folder of `content/` whose files are items of one type:
the posts of a blog, the events of a calendar, the members of a group.
The type says what an item is: which front-matter keys it reads, its card
in a list, its structured data, its feed. tilder ships four types, and a
theme adds its own in Python. This page declares collections and lists
them; the pages after it describe each type.

[TOC]

## The types

| Type | Items | Lists | Feeds | Page |
|---|---|---|---|---|
| `page` | every page outside a collection | - | - | [page](docs/content-types/page) |
| `post` | articles, notes, release notes | newest first | RSS | [post](docs/content-types/post) |
| `event` | meetups, talks, releases | upcoming and past, by the date of the build | RSS and iCalendar | [event](docs/content-types/event) |
| `member` | people | by category, then last name | - | [member](docs/content-types/member) |

A theme adds types in `theme/types/`, written exactly as the built-in ones
are ([types of your own](docs/content-types/custom-types)). This manual
is itself a collection of the theme's `doc` type, and its showcase one of
a `showcase` type.

## Declaring a collection

A collection is a table of `site.toml`, `[collections.<name>]`. The name
is how markers and the `feed:` front-matter key refer to it.

```toml
[collections.talks]         # {upcoming:talks}, {past:talks}
type = "event"
dir = "talks"               # content/talks/, served at /talks/...
feed = "talks.xml"
calendar = "talks.ics"
upcoming_tag = "soon"
```

| Key | Meaning |
|---|---|
| `type` | the type of its items: `post`, `event`, `member`, or a type of the theme; default `post`. Types are singular: `type = "posts"` stops the build |
| `dir` | its folder under `content/`; default: the collection's name. Two collections cannot share a folder, nor nest one inside the other |
| `nav_label` | the accessible name of its sidebar, `{{ collection_nav }}`; default `labels.collection_nav` ([navigation](docs/content-types/navigation)) |
| `recursive` | `true` to read the subfolders too (tilder 1.2); default `false`, unless the type's settings say otherwise |
| every setting of its type | the words and options of the type, each with a default in the type's module: a collection sets only what differs |

Each type's settings are listed on its page. A French `site.fr.toml` may
repeat `[collections.<name>]` with only the words that change: tables are
merged key by key, so the French feed gets a French title while `type`
and `dir` stay as `site.toml` sets them
([languages](docs/guide/languages)).

A type that no module defines stops the build and names the types
loaded:

```text
error: content/site.toml: collection "talks" has type "tlak", which no type defines. Types loaded: event, member, page, post (types/)
```

## Three collections by default

tilder's `defaults.toml` declares the three collections most sites have:

```toml
[collections.blog]
type = "post"
dir = "blog"
feed = "blog/feed.xml"

[collections.events]
type = "event"
dir = "events"
nav = "events"
feed = "events.xml"
calendar = "calendar.ics"

[collections.members]
type = "member"
dir = "members"
```

A collection whose folder does not exist is inactive: no item, no feed, no
calendar, and a list marker naming it shows its empty text. So a site
starts a blog by creating `content/blog/`, and needs no configuration for
it. A `[collections.blog]` in `site.toml` is merged over the default one:
this site sets its man-page name and its feed's words. The build's
summary says which collections are active:

```text
collections: blog (post, 3 items), events (event, no folder), members (member, no folder)
```

## Items

An item is one file in the collection's folder, or a folder of its own:

| Source | Item | Page |
|---|---|---|
| `content/talks/2099-03-01-first-talk.md` | `2099-03-01-first-talk` | `/talks/2099-03-01-first-talk` |
| `content/talks/2099-03-01-first-talk/index.md` | the same, with its images beside it | the same |
| `content/talks/2099-03-01-first-talk.fr.md` | its French translation | `/fr/talks/2099-03-01-first-talk` |
| `content/talks/_template.md` | none: a name starting with `_` is never built | - |
| `content/talks/index.md` | none: the collection's own page | `/talks/` |

- A dated type, `post` or `event`, reads its date from the file's name,
  `YYYY-MM-DD-slug.md` ([post](docs/content-types/post)).
- The collection's own page is `<dir>/index.md`, or a page named like the
  folder beside it (`talks.md` for `talks/`). It is a plain page: it sets
  its own `man`, `tagline` and `nav`, and holds the list.
- With the built-in types, an item's front matter may leave out `man`,
  `nav` and, for dated types, `tagline`: the type fills them from the
  collection's settings.

## Recursive collections

<!-- 1.2 -->

With `recursive = true` (tilder 1.2), a collection also reads its
subfolders, at any depth. `content/docs/guide/writing.md` is the item
`guide/writing`, served at `/docs/guide/writing`, in the section `guide`.
A subfolder's `index.md` is the item named like the folder, served beside
it: `content/docs/guide/index.md` is `/docs/guide`, the section's own
page. A `guide.md` beside the folder may be that page instead; a section
with neither has no page, and its folder's name stands for it. The
documentation you are reading is such a collection.

<!-- 1.2 -->

`recursive` is `false` unless the collection or its type's settings set
it, and it is `true` or `false`, nothing else. A dated type cannot be
recursive, and two files for one item (`guide.md` and `guide/index.md`)
stop the build. The order of the pages, depth first, is on the
[navigation](docs/content-types/navigation) page.

## Lists

A section heading that ends with a type's marker is filled with the
collection's cards, one per item, each clickable as a whole:

```text
## Posts {posts}

## Coming up {upcoming:talks}
```

| Marker | Type | Fills the section with |
|---|---|---|
| `{posts}` | `post` | every post, newest first |
| `{upcoming}` | `event` | the events dated today or later, nearest first, the first one highlighted |
| `{past}` | `event` | the events before today, latest first |
| `{next-event}` | `event` | the next event only |
| `{members}` | `member` | every member, as a grid, by category then last name |

- `{marker:name}` names the collection to list: `{posts:news}`,
  `{upcoming:talks}`. A name that is not a collection of the marker's
  type stops the build.
- A bare `{marker}` lists the page's own collection of that type, the
  one whose folder the page is in or is named like; else the first
  collection of that type.
- A list with nothing in it shows the collection's empty text: `empty`
  for posts and members, `none_upcoming` and `none_past` for events.
- Blocks written under the heading stay, after the cards.
- The marker's word is also a class of the section's body (`.posts`,
  `.upcoming`), and a member grid adds `.grid`
  ([classes](docs/themes/classes)).

A theme's type brings its own markers, as this site's `{docs}` and
`{showcase}` do.

## Feeds and calendars

Each collection may write two files, both named by a path from the site
root in its settings; an empty path writes nothing.

- `feed`: an RSS feed of every item, in the reverse of the collection's
  order (newest first for posts and events), for types that give feed
  items (`post` and `event`, not `member`). The feed is written in
  every language, under its prefix: `blog/feed.xml` and
  `fr/blog/feed.xml`, with the words of `feed_title` and
  `feed_description` in that language. A page's `feed:` front-matter key,
  a collection's name or `all`, advertises the feed in its `<head>`
  ([writing pages](docs/guide/writing)).
- `calendar`: an iCalendar file of every event, for the `event` type. It
  is written once, in the default language: a calendar has no interface
  language ([event](docs/content-types/event)).

Every calendar of the site shares the `[calendar]` table:

| Key | Default | Meaning |
|---|---|---|
| `calendar.name` | `"events"` | the calendar's name in calendar apps (`X-WR-CALNAME`), and the suffix of each event's summary, `First talk - events` |
| `calendar.description` | `"Events."` | the calendar's description (`X-WR-CALDESC`) |
| `calendar.prodid` | `"-//site//events//EN"` | the product identifier (`PRODID`) |
| `calendar.timezone` | `"UTC"` | the calendar's time zone (`X-WR-TIMEZONE`) |
| `calendar.uid_domain` | `"example.org"` | the domain of each event's identifier, `<slug>@<uid_domain>`: set your own |

```toml
[calendar]
name = "talks"
description = "Talks of the group."
prodid = "-//example.org//talks//EN"
uid_domain = "example.org"
```

Since the calendar is written in the default language, it takes these
values from `site.toml`; a `[calendar]` in `site.fr.toml` is not used.

## See also

- [page](docs/content-types/page), [post](docs/content-types/post),
  [event](docs/content-types/event), [member](docs/content-types/member)
- [types of your own](docs/content-types/custom-types)
- [navigation](docs/content-types/navigation)
- [feeds and images](docs/reference/feeds-and-images)
