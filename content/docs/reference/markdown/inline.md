---
title: Inline markup
description: Bold, italic, struck and underlined text, code and links inside a sentence: the six inline constructs, what stays literal, and the text mirror.
order: 40
---

## Name

inline - bold, italic, struck, underlined, code and links

Inside a paragraph, a list item, a table cell or a title, tilder reads
six constructs and nothing else. Each is shown below as source, then
rendered in a frame, as it renders in any sentence of the site.

[TOC]

## Bold and italic

Two asterisks on each side make bold text. One asterisk or one
underscore on each side makes italic text.

```text
A **bold** word, an *italic* one, and _another_ one.
```

> A **bold** word, an *italic* one, and _another_ one.

Both are written so that ordinary text is left alone:

- `*italic*` must not touch a space on the inside, so `2 * 3 * 4` stays
  as written;
- `_italic_` works only around whole words, so `snake_case` stays as
  written.

```text
2 * 3 * 4 is 24, and snake_case is not italic.
```

> 2 * 3 * 4 is 24, and snake_case is not italic.

On the web page, bold is `<b>` and italic `<em>`. The text mirror prints
the words alone, without the marks.

A paragraph wrapped entirely in single asterisks is not italic: it is an
[empty state](docs/reference/markdown/blocks#empty-state).

## Struck and underlined

Two tildes on each side strike text through; two plus signs on each side
underline it, with a dotted line, since a plain underline reads as a link
on the web.

```text
The meetup is on ~~Friday~~ Saturday, ++at noon++.
```

> The meetup is on ~~Friday~~ Saturday, ++at noon++.

`++underlined++` follows the same rule as italics: not right after a
letter, and not touching a space on the inside, so `C++` and `1 ++ 2`
stay as written. On the web page they are `<del>` and `<u class="u">`.
The text mirror prints struck text with its tildes, `~~Friday~~`: dropping
them would change the meaning. Underlined text is printed plain.

## Code

A word or a phrase between backquotes is code: set in the monospace
font, and never read for any other markup.

```text
Run `./build.sh`, and keep **`--watch` on** while you write.
```

> Run `./build.sh`, and keep **`--watch` on** while you write.

The end of that example also shows the next rule: no nesting. The bold
text holds the backquotes as they are, not code. Code cannot hold a
backquote either. In the
text mirror, code is printed as it is, and coloured in the ANSI mirror.

## Links

`[label](target)` is a link. The target is written from the site root,
without a leading slash and without `.html`; the build makes it relative
to the page.

```text
Read [the guide](docs/guide), or the [example ↗](https://example.org/).
```

> Read [the guide](docs/guide), or the [example ↗](https://example.org/).

The [links and images](docs/reference/markdown/links-and-images) page
has every kind of target: anchors, links across languages, files and
other sites.

## What stays literal

The six constructs do not nest: the first one found wins, and holds its
content as plain text. There is no escape character: a backslash is
printed, and does not stop the markup after it. Anything else, HTML
included, is printed as written.

```text
**[a link](docs/)** is bold, and <b>this</b> is not.
A \*backslash\* does not escape.
```

> **[a link](docs/)** is bold, and <b>this</b> is not.
> A \*backslash\* does not escape.

The two lines make one paragraph: bold text holding a link's source,
HTML shown as text, then a backslash printed before italics. Rephrase rather
than escape. Inside a table cell, `\|` is a pipe
([tables](docs/reference/markdown/blocks#table)).

## In the text mirror

The text mirror prints the words of every construct and drops their
marks, except the tildes of struck text. An internal link keeps only its
label, since a terminal reader reaches it with `curl`, not by copying it;
a link to another site prints its address in parentheses after the label.
Accents and typographic characters are folded to ASCII: accented
letters lose their accents, typographic quotes and dashes become plain
ones, and the north-east arrow of external links is dropped. Lines are wrapped at 75 columns
([the text mirror](docs/reference/text-mirror)).

## See also

- [links and images](docs/reference/markdown/links-and-images)
- [blocks](docs/reference/markdown/blocks)
- [the text mirror](docs/reference/text-mirror)
