---
title: Blocks
description: Paragraphs and their classes, the empty state, lists, tasks, contents, rules, insets, callouts, code blocks, tables and comments, each shown rendered.
order: 20
---

## Name

blocks - paragraphs, lists, boxes, code, tables and comments

A block is a run of lines between two blank lines: a paragraph, a list,
a box, a code block, a table. Each construct below is given as source,
then rendered under a dashed frame marked `Rendered`, exactly as that
source renders on any page of the site.

[TOC]

## Paragraph

Consecutive lines make one paragraph, joined by spaces; a blank line
ends it. Words in braces at the end of a paragraph are classes, applied
on the web page only: the text mirror prints the paragraph plain.

```text
The build joins these two lines
into one paragraph.

A small, muted line. {small muted}

A faint line. {faint}

A line in the monospace font. {mono}

A line in the warning colour. {warn}
```

### Rendered {example}

  The build joins these two lines
  into one paragraph.

  A small, muted line. {small muted}

  A faint line. {faint}

  A line in the monospace font. {mono}

  A line in the warning colour. {warn}

`small`, `muted`, `faint`, `mono` and `warn` are the classes every theme
is expected to style ([classes](docs/themes/classes)). Any other word in
the braces becomes a class too, for a theme that styles it.

## Empty state

A paragraph wrapped entirely in single asterisks is an empty state: the
muted, monospace line that says something is not there yet. A list with
nothing in it shows the same line.

```text
*No talk announced yet.*
```

### Rendered {example}

  *No talk announced yet.*

The asterisks must open and close the whole paragraph. With text after
the closing asterisk, `*Soon.* Check back later.` is an ordinary
paragraph that begins in italics. A paragraph entirely in bold also
starts and ends with asterisks: it becomes an empty state, its text in
italics. Keep bold for words inside a sentence.

## List

A line starting with `- ` or `* ` is a bulleted item; `1. ` or `1) `
starts a numbered one. A numbered list starts at its first number:
`7.` then `8.` counts from 7. Indent an item further than the one above
to nest a list inside it. An indented line that is not an item carries
on the item above it.

```text
1. Copy the starter site
2. Build it, then keep it rebuilding
   while you write
   - `./build.sh`
   - `./build.sh --watch`
3. Write the first page
```

### Rendered {example}

  <!-- The example's first block: a list here would be the entry's meta line. -->

  1. Copy the starter site
  2. Build it, then keep it rebuilding
     while you write
     - `./build.sh`
     - `./build.sh --watch`
  3. Write the first page

In the text mirror, each item is indented two spaces, as `- item` or
`1. item`, and its wrapped lines and nested lists align under the item's
text.

A list does not follow a paragraph without a blank line: the list's
lines would carry on the paragraph. And right after a `###` heading, a
list is the entry's [meta line](docs/reference/markdown/entries), not a
list.

## Task list

`[ ]` or `[x]` right after an item's marker makes a task: an empty box,
or a checked one. Screen readers hear `labels.task_todo` or
`labels.task_done` for the box ("to do", "done").

```text
- [x] move the blog into folders
- [ ] write the first report
```

### Rendered {example}

  <!-- The example's first block: a list here would be the entry's meta line. -->

  - [x] move the blog into folders
  - [ ] write the first report

The text mirror prints the boxes as text: `- [x] item`, `- [ ] item`.

## Table of contents

`[TOC]` alone on a line lists the page's sections, each one linking to
its section. On the web page, it is a `<nav>` named by `labels.toc`,
folded by default in a `<details>` that opens without any script. In the text
mirror it is a numbered list of the section names. Each output lists
only the sections it shows ([sections](docs/reference/markdown/sections)).

```text
[TOC]
```

### Rendered {example}

  [TOC]

Put it where the contents should appear, near the top of a long page.
This page has one under its `## Name`; on a wide screen, this site's
theme moves the first table of contents of a documentation page into
the right-hand column.

## Horizontal rule

`---`, `***` or `___` alone on a line, between blank lines, draws a rule:
`<hr>` on the web page, a line of dashes in the text mirror. At the very
top of a file, `---` opens the front matter instead.

```text
Above the rule.

---

Below the rule.
```

### Rendered {example}

  Above the rule.

  ---

  Below the rule.

## Inset

Every line of an inset starts with `>`. It is drawn as a box on the web
page, and indented in the text mirror. A line holding only `>` separates
two paragraphs. An inset holds paragraphs, with inline markup: a list or
a code block inside it is read as text.

```text
> **Note:** the [archive ↗](https://archive.example.org/) keeps older posts.
>
> A second paragraph.
```

### Rendered {example}

  > **Note:** the [archive ↗](https://archive.example.org/) keeps older posts.
  >
  > A second paragraph.

The pages of this reference use insets to frame the live examples of
[inline markup](docs/reference/markdown/inline).

## Callout

An inset whose first line is `[!INFO]`, `[!WARNING]` or `[!ERROR]` is a
callout, in GitHub's syntax. Text may follow the marker on the same line.
GitHub's other names are accepted, in upper or lower case.

```text
> [!INFO]
> The build runs again at midnight.

> [!WARNING]
> Never edit `public/` by hand: the next build replaces it.

> [!ERROR] A missing `title:` stops the build.
```

### Rendered {example}

  > [!INFO]
  > The build runs again at midnight.

  > [!WARNING]
  > Never edit `public/` by hand: the next build replaces it.

  > [!ERROR] A missing `title:` stops the build.

| Marker | Also accepted | Kind | Label |
|---|---|---|---|
| `[!INFO]` | `[!NOTE]`, `[!TIP]` | info | `labels.info` |
| `[!WARNING]` | `[!IMPORTANT]`, `[!CAUTION]` | warning | `labels.warning` |
| `[!ERROR]` | `[!DANGER]` | error | `labels.error` |

On the web page, a callout is a box with a coloured rule on its left and
its label, marked `role="note"` for screen readers. In the text mirror
it is a box drawn in ASCII, the label in its top rule, and coloured by
kind in the ANSI mirror:

```text
+- WARNING --------------------------------------------------------+
| Never edit public/ by hand: the next build replaces it.          |
+------------------------------------------------------------------+
```

The labels come from `[labels]` in `site.toml`, so they follow the
page's language. Any other word, `[!NOTICE]` say, leaves an ordinary
inset that begins with the marker as written.

## Code block

A code block opens with a fence of three backquotes and closes with
another. A language name right after the opening fence turns on syntax
highlighting, done by the build (no script), and shows the language in
the block's corner. The block keeps its spacing exactly, and a long line
scrolls sideways instead of widening the page.

````text
```python
def fold(text, width=75):
    return textwrap.wrap(text, width)
```
````

### Rendered {example}

  ```python
  def fold(text, width=75):
      return textwrap.wrap(text, width)
  ```

To show a fence inside a code block, as the source above does, open the
outer block with more backquotes: a fence of four closes only on a line
of four or more.

| Language | Also accepted |
|---|---|
| `sh` | `bash`, `shell`, `zsh` |
| `console` | `terminal`, `shell-session` |
| `python` | `py` |
| `js` | `javascript`, `ts`, `typescript`, `node` |
| `c` | `h`, `cpp`, `c++` |
| `go` | `golang` |
| `rust` | `rs` |
| `sql` | `postgres`, `postgresql` |
| `json` | |
| `yaml` | `yml` |
| `ini` | `toml`, `cfg`, `systemd` |
| `conf` | `caddy`, `caddyfile`, `nginx` |
| `dockerfile` | `docker`, `containerfile` |
| `html` | `xml`, `svg` |
| `css` | |
| `make` | `makefile` |
| `diff` | `patch` |
| `text` | `plain`, `txt` |

The name may be written in any case; the label shows it in lower case,
as written: `caddy`, not `conf`. Three languages are
read line by line rather than word by word:

- `console`: a line starting with a prompt, `$ ` or `# `, possibly after
  a user and a host, is a command and is highlighted as shell; any other
  line is output, left plain.
- `diff`: added lines and removed lines are coloured apart, hunk headers
  muted.
- `text`: no highlighting at all, but the label is shown. Every Markdown
  source in this manual is a `text` block.

````text
```console
$ ./build.sh
built public/
```

```diff
-nav = "blog"
+nav = "blog/"
```
````

### Rendered {example}

  ```console
  $ ./build.sh
  built public/
  ```

  ```diff
  -nav = "blog"
  +nav = "blog/"
  ```

A block with no language has no label and no highlighting. A language
tilder does not know prints a build warning and leaves the block plain.

If the theme ships `code.js`, as this one does, every code block gets a
button that copies its code as plain text, worded by `labels.copy` and
`labels.copied`; the script is loaded only on pages with code
([scripts](docs/themes/scripts)). In the text mirror, the block is framed
by two rules, the language in the top one, and its lines are left
untouched; a line longer than the mirror's 75 columns is cut and
continued on the next one, the cut marked with `\`:

```text
.-- python ---------------------------------------------------------------.
  def fold(text, width=75):
      return textwrap.wrap(text, width)
'-------------------------------------------------------------------------'
```

## Table

Pipes separate the cells; the second line, of dashes, separates the
header from the rows. Colons in that line set each column's alignment:
`:---` left, the default, `:---:` centred, `---:` right. Inline markup
works in the cells, and `\|` writes a pipe inside one.

```text
| Output | Format | Width |
|:-------|:------:|------:|
| page   | HTML   | any   |
| mirror | ASCII  | 75    |
| `a \| b` | text | 5 |
```

### Rendered {example}

  | Output | Format | Width |
  |:-------|:------:|------:|
  | page   | HTML   | any   |
  | mirror | ASCII  | 75    |
  | `a \| b` | text | 5 |

The pipes need not line up, and each line of dashes needs at least three.
A row has as many cells as the header: a missing cell is empty, an extra
one is dropped. On the web page, a table wider than the column scrolls
inside its own frame, named by `labels.table` for screen readers. In the
text mirror it becomes padded columns; when those do not fit in 75
columns, each row becomes a record of `Header: value` lines.

## Comment

A block starting with `<!--` is copied into the web page as it is, where
the browser does not show it, and left out of the text mirror. Use it for
notes to the people who edit the page, such as a fact still to find:

```text
<!-- TO FILL: the venue's address. -->

*Venue to be announced.*
```

### Rendered {example}

  <!-- TO FILL: the venue's address. -->

  *Venue to be announced.*

The comment says what is missing, the empty state tells the reader. The
whole block, down to the next blank line, is copied as it is: leave a
blank line after the comment.

## See also

- [sections](docs/reference/markdown/sections)
- [entries](docs/reference/markdown/entries)
- [the text mirror](docs/reference/text-mirror)
- [classes](docs/themes/classes)
