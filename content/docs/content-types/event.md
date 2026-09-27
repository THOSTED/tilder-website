---
title: event
description: The event type: dated items with a place, upcoming or past by the build's date, the {upcoming}, {past} and {next-event} lists, RSS and iCalendar.
order: 30
---

## Name

event - dated items with a place, upcoming or past

An event is a Markdown file named by its date, in a collection of type
`event`: meetups, talks, releases. Its card says when and where; it is
upcoming until its date has passed, then past, with no one touching the
file. The collection lists its events in three ways, writes an RSS feed
and an iCalendar file that calendar apps subscribe to.

[TOC]

## Settings

An `event` collection may set these keys under `[collections.<name>]`;
each has its default in the type's module, `types/event.py`.

| Key | Default | Meaning |
|---|---|---|
| `man` | `"SITE-EVENTS(7)"` | the man-page name of its items, unless one sets its own |
| `nav` | `"events"` | the `[[nav]]` entry its items mark as current, and the link of the feed |
| `upcoming_tag` | `"upcoming"` | the tag of an upcoming event's card |
| `past_tag` | `"past"` | the tag of a past event's card |
| `none_upcoming` | `"No upcoming event."` | the text of an `{upcoming}` or `{next-event}` list with nothing in it |
| `none_past` | `"No past event."` | the text of a `{past}` list with nothing in it |
| `link_label` | `"event website ↗"` | the link to the event's own site, on its page |
| `map_label` | `"see on OpenStreetMap ↗"` | the link to the place on the map, on its page |
| `feed` | `""` | the RSS feed's path from the site root, `"events.xml"`; empty for none |
| `feed_title` | `"events"` | the feed's title |
| `feed_description` | `"Upcoming and past events."` | the feed's description |
| `calendar` | `""` | the iCalendar file's path from the site root, `"events.ics"`; empty for none |

An empty tag, `upcoming_tag = ""`, leaves the card without one.
`defaults.toml` already declares `[collections.events]`, with `feed =
"events.xml"` and `calendar = "calendar.ics"`: creating `content/events/`
is enough to start. A second collection names its own:

```toml
[collections.talks]
type = "event"
nav = "talks"
feed = "talks.xml"
calendar = "talks.ics"
upcoming_tag = "soon"
none_upcoming = "No talk planned yet."
```

## A file per event

An event's file is named `YYYY-MM-DD-slug.md`, the date the event starts,
as a post's is ([post](docs/content-types/post)): the same folder form
for images, the same `.fr.md` translations, the same errors for a date
that does not exist.

An event lasts whole days. There is no key for an hour: write it in the
description or in the page, and give the last day in `end` when it lasts
more than one.

## Front matter

```text
---
title: Spring meetup
description: Talks and a workshop on documentation, then dinner.
place: 1 Example Street, Exampleton
link: https://meetup.example/spring
end: 2099-03-02
lat: 48.8566
lon: 2.3522
---
```

| Key | Meaning |
|---|---|
| `title` | the event's name |
| `description` | one sentence: the card's text in a list, the feed's summary, the calendar's `DESCRIPTION` |
| `place` | where: an address or a venue, on the card, in the calendar's `LOCATION` and the structured data |
| `link` | the event's own site, linked from its page with `link_label` |
| `end` | `YYYY-MM-DD`, the last day of an event over several days |
| `lat`, `lon` | coordinates of the place: an exact map marker, the calendar's `GEO`, the structured data's `geo` |
| `man`, `nav` | default: the collection's `man` and `nav` |
| `tagline` | default: the date in words, written with `[dates]` |

Every other key of [writing pages](docs/guide/writing) applies too. Give
coordinates only when you know them: without them, the map link searches
for the `place` instead.

## The card

The card shows the date as a `<time>`, running to `end` in words when the
event lasts several days (`Sunday 1 March 2099 - Monday 2 March 2099`),
the place, and the tag: `upcoming_tag` when the event starts today or
later, `past_tag` once that day has gone by. In a list it shows the
description and links to the event.

On the event's own page, the card also links to the event's site
(`link`, labelled `link_label`) and to the place on the map
(`map_label`): a marker at `lat` and `lon` when both are given, else a
search for `place`. It is a link, not an embedded map, so no reader's
browser calls another site unless they click it. The text mirror keeps
the event's site and leaves the map link out: the address is on the card
already, and the map's URL would not fit in 75 columns.

## Upcoming and past

Three markers list a collection of events, all by the date of the build:

| Marker | Lists |
|---|---|
| `{upcoming}` | the events that start today or later, nearest first; the first is marked as the next one (`.entry--next`, `.tag--next`) |
| `{past}` | the events that started before today, latest first |
| `{next-event}` | the next event only, marked the same way |

```text
## Upcoming {upcoming}

## Past {past}
```

Each takes a collection's name, `{upcoming:talks}`, as every marker does
([collections](docs/content-types)). An empty list shows `none_upcoming`
or `none_past`.

"Today" is the day the site is built. An event moves from one list to the
other only when the site is built again, so a site with events must be
rebuilt every day. In watch mode, tilder rebuilds at midnight for this
reason alone, even when no file has changed; the compose file of the
[deployment](docs/guide/deployment) runs it that way. A site built by
hand, or in CI, needs a daily build of its own. The build reads the day
from the `BUILD_TODAY` environment variable when it is set,
`BUILD_TODAY=2099-03-01`, which is how to preview the lists as they will
be on another day.

## RSS

With `feed` set, the collection's RSS feed lists every event, upcoming
and past, the latest date first, each with its title, address, date and
description; `feed_title` and `feed_description` name the channel. Each
language has its own, under its prefix, as for posts
([post](docs/content-types/post)).

## iCalendar

With `calendar` set, the build writes an iCalendar file (RFC 5545) that
calendar apps can subscribe to. It is written once, in the default
language, and holds every event of the collection:

- each event as a whole-day `VEVENT`, from its date to its `end` or its
  date (`DTEND` is the day after, as the format wants), with its `UID`, the event's title
  followed by the calendar's name as `SUMMARY`, the `place` as
  `LOCATION`, `lat` and `lon` as `GEO`, its address as `URL` and its
  description;
- the calendar's own name, description, product identifier and time
  zone, from the `[calendar]` table: `calendar.name`,
  `calendar.description`, `calendar.prodid`, `calendar.timezone`, and
  `calendar.uid_domain` for the identifiers. Their defaults are on the
  [collections](docs/content-types) page.

The text is folded to ASCII and cut into lines of 75 octets, as the
format requires.

## Search engines

An event's body is wrapped in `<article>`. Its JSON-LD node is an
`Event`: `name`, `description`, `startDate` (the date), `endDate` (`end`,
else the date), a scheduled, in-person event, its `location` as a
`Place` named by `place` (with `geo` from `lat` and `lon`), the site's
organisation as `organizer`, and the preview `image`. Its `og:type` is
`website`.

## See also

- [collections](docs/content-types)
- [post](docs/content-types/post)
- [feeds and images](docs/reference/feeds-and-images)
- [the command line](docs/reference/cli)
