---
title: Sections
description: The ## headings of a page: the man-page rows they draw, the id each one gets, and every marker in braces that changes a section.
order: 10
---

## Name

sections - `##` headings, their ids and their markers

A page is a list of sections, as a man page is. Each one starts at a `##`
heading and runs to the next; markers in braces at the end of the heading
give it an id, keep it to one output, lay it out as a grid of cards or
fill it from a collection. The sections of this page are themselves the
live examples: each marker below is used by a section you can see, or,
for one of them, not see.

[TOC]

## A section

A `##` heading starts a section, and everything down to the next `##`
belongs to it. On the web page, the section is a row of the man page: its
name in the left margin, its content beside it. In the text mirror, the
name is printed in capitals at the left edge and the content indented
five spaces under it.

```text
## Name

sections - `##` headings, their ids and their markers

A page is a list of sections, as a man page is.
```

That source is the opening of this page. Pages start with `## Name`, a
line `name - summary`, then a paragraph that sums the page up
([writing pages](docs/guide/writing)); tilder does not require it, but a
man page reads that way.

A `##` heading stands on its own, with or without a blank line around it.
Only `##` and `###` are headings: a line starting with `#` or `####` is a
paragraph, printed as written.

Whatever comes before the first `##` of a file is rendered at the top of
the web page, outside any section, and left out of the text mirror.

## Ids {#ids}

Every section gets an id, so a link can lead to it. By default, the id
comes from the title: accents folded to ASCII, lower case, every run of
other characters turned into one hyphen. `## Section ids` gets
`section-ids`; a second section with the same title gets
`section-ids-2`.

`{#id}` at the end of the heading sets the id instead:

```text
## Ids {#ids}
```

This section is written that way: its id is `ids`, and
[this link](#ids) leads to it, from this page, as
`docs/reference/markdown/sections#ids` does from any other. A fixed id
keeps links working when the title is reworded or translated.

## Markers

A heading may end with markers in braces: one marker per pair of braces,
or several separated by spaces, in any order.

```text
## Contact {#write}
## Members {members} {#team}
## Coming up {upcoming:talks grid}
```

| Marker | Effect |
|---|---|
| `{#id}` | the section's id, instead of one made from the title |
| `{html}` | on the web page only: the text mirror leaves the section out |
| `{text}` | in the text mirror only: the web page leaves the section out |
| `{grid}` | lays the section's entries out as a grid of cards |
| `{posts}`, `{upcoming}`, `{past}`, `{next-event}`, `{members}` | fills the section from a collection (below) |
| a marker of a theme's type | fills the section from a collection of that type, such as this site's `{docs}` |
| any other word | a class on the section's body |

The next section of this page is written `## Cards {grid}`: its three
entries are laid out as cards, side by side where the page is wide
enough, one under the other on a phone. Every block of a grid section is
a cell of the grid, so such a section usually holds entries only. In
the text mirror, a grid is a list of entries like any other.

## Cards {grid}

### First card

  Each `###` entry of a `{grid}` section is a card.

### Second card

  The cards share the width of the column.

### Third card

  An [entry](docs/reference/markdown/entries) keeps its meta line and
  its body in a card.

## One output only

`{text}` keeps a section for the text mirror, and `{html}` for the web
page. Use them for what makes sense in one output only: a note about
`curl` for terminal readers, a section built around an image for the
browser.

```text
## In the terminal {text}

You are reading the text mirror.

## In the browser {html}

This section is not in the text mirror.
```

These two sections follow, written as above. On this web page you see
only the second; in a terminal,
`curl tilder.thosted.fr/docs/reference/markdown/sections` prints only the
first. The table of contents of each output lists only its own sections.

## In the terminal {text}

You are reading the text mirror: the web page has no such section.

## In the browser {html}

This section is on the web page only: the text mirror leaves it out.

## List markers

A section whose heading ends with a type's marker is filled by the build
with a collection's cards, one per item: the section heading and its
marker are all you write.

```text
## Posts {posts}

## Coming up {upcoming:talks}

## Pages {docs}
```

| Marker | Fills the section with |
|---|---|
| `{posts}` | the posts, newest first |
| `{upcoming}` | the events dated today or later, nearest first |
| `{past}` | the events before today, latest first |
| `{next-event}` | the next event only |
| `{members}` | the members, as a grid |

A marker may name its collection, `{upcoming:talks}`; a bare marker lists
the page's own collection of that type, else the first one declared.
Blocks written under the heading stay, after the cards. The last line of
the source above is how the [documentation's home page](docs/) lists
these pages: `{docs}` is the marker of this site's theme type. Every
marker, and what an empty list shows, is on the
[content types](docs/content-types) page.

## Classes

A marker that means nothing to tilder becomes a class on the section's
body, the `<div class="b">` beside the heading, for the theme to style.
`{grid}` is such a class too, and a list marker adds its own word, without
the collection's name: `{upcoming:talks}` gives `.upcoming`.

```text
## Sponsors {wide}
```

The body of that section is `<div class="b wide">`. The classes a theme
styles are listed on the [classes](docs/themes/classes) page.

## See also

- [entries](docs/reference/markdown/entries), the `###` headings inside
  a section
- [writing pages](docs/guide/writing)
- [content types](docs/content-types), for the list markers
