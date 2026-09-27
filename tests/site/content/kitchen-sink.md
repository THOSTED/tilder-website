---
man: KITCHEN-SINK(7)
title: Kitchen sink
description: Every construct and every class of the theme, on one page, to review by eye.
tagline: every construct, light and dark
nav: -
robots: noindex
---

[TOC]

## Name

kitchen sink - every construct of the dialect, as this theme draws it {mono}

## Paragraphs

A paragraph with **bold**, *italic*, _italic too_, ~~struck~~, ++underlined++,
`inline code`, an [internal link](docs/) and an [external one ↗](https://example.org/).

A small muted line. {small muted}

A faint line. {faint}

A warning line. {warn}

A monospace line. {mono}

*Nothing here yet: the empty state.*

---

## Lists

- a bullet
- another, with a nested list
  - nested

1. first
2. second

- [x] a done task
- [ ] a task to do

## Boxes

> A plain inset: a live example is framed like this.
>
> Its second paragraph.

### Rendered {example}

  | a live | example |
  |---|---|
  | of a | table |

> [!INFO]
> An information callout.

> [!WARNING]
> A warning callout.

> [!ERROR]
> An error callout.

## Entries

### A plain entry

  - 2026-09-01 | Tuesday 1 September 2026
  - a place
  - `tag`

  The entry's body, indented two spaces.

### The next one {next}

  - `next`

### A full one {full}

  - `full`

## Cards {grid}

### First card

  - `grid`

  A card in a grid.

### Second card

  A second card.

## Code

```python
@decorator
def fold(text, width=75):
    """Fold the text."""  # a comment
    return text[:width] + "é"
```

```sh
echo "$HOME" ${PATH} 42
```

```console
$ curl example.org
the text mirror
```

```diff
@@ -1,2 +1,2 @@
-old line
+new line
```

```html
<!DOCTYPE html>
<!-- a comment -->
<p class="x">&amp;</p>
```

```
no language, no label
```

## Tables

| left | centre | right |
|:-----|:------:|------:|
| a    | b      | c     |

## Figures

![A grey rectangle, the kitchen sink's figure](kitchen-sink-figure.svg "A caption under the figure.")

## Posts {posts}

## Upcoming {upcoming}

## Past {past}

## Next event {next-event}

## Members {members}
