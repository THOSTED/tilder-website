---
title: Entries
description: The ### headings inside a section: an event, a person, a card. Their meta line of dates and tags, their indented body, and their markers.
order: 30
---

## Name

entries - `###` headings, their meta line, their body and their markers

An entry is a `###` heading inside a section: a talk in a programme, a
person in a list, a card in a grid. It may carry a meta line of dates,
places and tags, and a body of blocks indented under it. The cards that
a collection writes into a list are entries too, built the same way.
Each example below is followed by the entry it renders.

[TOC]

## An entry

A `###` heading starts an entry in the current section. The blocks of
its body are indented two spaces; the first block that is not indented
ends the entry, and the page goes back to the section.

```text
### Spring meetup

  Three talks and a workshop, open to everyone.

Back in the section, after the entry.
```

That source renders as follows.

### Spring meetup

  Three talks and a workshop, open to everyone.

Back in the section, after the entry.

The title may hold inline markup, such as a link. An entry has no id of
its own, and a `{#id}` on its heading is dropped: to link to it, link to
its section. Entries do not nest: a
`####` heading is not one.

In the text mirror, the title is printed at the section's indent and the
body indented four spaces further.

## The meta line

A list right after the heading, indented like the body, is the entry's
meta line rather than a list. Each item is one of three kinds:

| Item | On the web page | In the text mirror |
|---|---|---|
| a word in backquotes | a tag, in a small frame | the first tag, on the right of the title line |
| `YYYY-MM-DD \| human date` | `<time datetime="YYYY-MM-DD">`, showing the human date | the human date |
| anything else | a plain item | a line of its own |

```text
### Autumn meetup

  - 2026-10-17 | Saturday 17 October 2026
  - Main hall, 1 Example Street, Exampleville
  - `talks`

  Two talks, then questions.
```

That source renders as follows.

### Autumn meetup

  - 2026-10-17 | Saturday 17 October 2026
  - Main hall, 1 Example Street, Exampleville
  - `talks`

  Two talks, then questions.

On the web page, the items are set on one line, separated by dots. The
part before ` | ` goes into the `datetime` attribute as it is: write the
date as `YYYY-MM-DD`. Meta items are plain text: a link or bold text in
one is shown as written. Only the first tag goes to the text mirror.

For an item of a collection, the build writes this line itself, from the
front matter ([content types](docs/content-types)).

## Markers

Like a section, an entry's heading may end with markers in braces. Each
one becomes a class on the entry, `entry--<marker>`; three of them mean
something to tilder and to every theme.

| Marker | Class | Effect |
|---|---|---|
| `{next}` | `.entry--next` | the entry's tag in the accent colour: the next event |
| `{full}` | `.entry--full` | the entry's tag in the warning colour: a mentor with no room left |
| `{link}` | `.entry--link` | a card whose title link covers the whole card |
| any other word | `.entry--<word>` | a class for the theme |

```text
### Winter meetup {next}

  - `next`

### Office hours {full}

  - `full`

### [Content types](docs/content-types) {link}

  Collections, and the types that shape them.
```

That source renders as follows.

### Winter meetup {next}

  - `next`

### Office hours {full}

  - `full`

### [Content types](docs/content-types) {link}

  Collections, and the types that shape them.

`{next}` and `{full}` change the tag only; the card itself looks like any
other. The build sets them on the cards it writes: `{next}` on the first
event of an `{upcoming}` list and on the one card of `{next-event}`,
`{full}` on a member whose front matter says `full: yes`. It sets `{link}` on the cards of posts and events in
a list, whose title links to the item's page; the last entry above is
such a card, clickable anywhere. In a section marked `{grid}`, entries
are laid out as cards side by side
([sections](docs/reference/markdown/sections#cards)).

This site's theme styles one more marker, `{example}`, as the dashed
frame labelled `Rendered` around every live example of the
[blocks](docs/reference/markdown/blocks) page.

```text
### Rendered {example}

  | a live | example |
  |---|---|
  | of a | table |
```

## The body

Every block may go into an entry's body: paragraphs, lists, boxes, code,
tables, images. Each is indented two spaces, including its continuation
lines, and blank lines separate them as anywhere else.

```text
### Version 2.0

  - `release`

  A new layout for the programme.

  > [!INFO]
  > Read the notes before you upgrade.

  - a list after the first block is a list
  - not a meta line
```

That source renders as follows.

### Version 2.0

  - `release`

  A new layout for the programme.

  > [!INFO]
  > Read the notes before you upgrade.

  - a list after the first block is a list
  - not a meta line

A list is the meta line only when it comes first, right after the
heading. A body that must open with a list starts with another block
before it: a sentence, or a [comment](docs/reference/markdown/blocks#comment),
which nobody sees.

## See also

- [sections](docs/reference/markdown/sections)
- [blocks](docs/reference/markdown/blocks)
- [content types](docs/content-types), for the cards of a list
- [classes](docs/themes/classes)
