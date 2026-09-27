---
title: The Markdown reference
description: tilder's Markdown dialect on one page: its principles, a quick reference of every construct, and what it leaves out on purpose.
order: 10
---

## Name

markdown - the dialect tilder reads, construct by construct

Every page of a tilder site is a Markdown file, written in a small,
strict dialect with a few additions for the man-page layout. This page
sums it up; the five pages after it take each family of constructs in
turn, and show each one twice: its source, then the construct itself,
rendered on the page by the same build that renders the rest of the site.

[TOC]

## Principles

- **A short list, not CommonMark.** tilder reads the constructs listed in
  this reference and nothing else. Anything else is printed as plain
  text, as it was written, never guessed at.
- **Two renderings.** Every construct is rendered twice from the same
  source: as HTML for the site, and as ASCII text, 75 columns wide, for
  the [text mirror](docs/reference/text-mirror) a terminal receives.
  Each page of this reference says what both look like.
- **Blocks are separated by a blank line.** A `##` or `###` heading
  stands on its own, blank line or not; every other block ends at the
  next blank line.
- **A page is a man page.** `##` headings are its sections, `###`
  headings the entries inside them, and it opens with `## Name`
  ([writing pages](docs/guide/writing)).

## Quick reference

| Source | HTML | Text mirror |
|---|---|---|
| `## Title {#id} {html} {text} {grid}` | `<section class="s">`, `<h2>` | `TITLE` at the left edge |
| `## Title {posts}`, `{upcoming:name}`... | the section, filled with a collection's cards | the cards, as entries |
| `### Title {next} {full}` | `.entry`, `.entry--next`, `.entry--full` | the title, indented, its first tag on the right |
| a list right after `###` | the entry's `.meta` line | one line per item |
| `- YYYY-MM-DD \| date` in the meta line | `<time>` | the human date |
| `- item`, `1. item`, nested by indentation | `<ul>`, `<ol>` | `  - item`, `  1. item` |
| `- [ ] to do`, `- [x] done` | `.tasks`, a box | `  - [ ] to do` |
| `[TOC]` alone on a line | `.toc`, folded | a numbered list of the sections |
| `---` alone on a line | `<hr>` | a line of dashes |
| `> text` | `.inset` | indented |
| `> [!INFO]`, `[!WARNING]`, `[!ERROR]` | `.callout` | an ASCII box, the label in its top rule |
| a fence of backquotes, with a language | `<pre class="code">`, highlighted | framed, verbatim |
| `\| a \| b \|` then `\|---\|---\|` | `<table>` in a scrolling wrapper | padded columns, or records |
| `![alt](file "caption")` alone on a line | `<figure>`, `<img>` | `[ image ] alt`, the caption, the path |
| `*text*`, the whole paragraph | `.empty` | plain |
| `text {small muted}` | `<p class="small muted">` | plain |
| `<!-- ... -->` | copied as it is | left out |
| `[label](target)` | `<a>` | the label, and an external URL |
| `**b**`, `*i*`, `_i_` | `<b>`, `<em>` | the text |
| `~~s~~`, `++u++` | `<del>`, `<u class="u">` | `~~s~~`, the text |
| a word in backquotes | `<code>` | the word |

## The pages

[Sections](docs/reference/markdown/sections): `##` headings, the id each
one gets, and the markers in braces that change a section: `{#id}`,
`{html}`, `{text}`, `{grid}` and the list markers.

[Blocks](docs/reference/markdown/blocks): paragraphs and their classes,
the empty state, lists and task lists, the table of contents, rules,
insets and callouts, code blocks, tables and comments.

[Entries](docs/reference/markdown/entries): `###` headings, their meta
line of dates and tags, their indented body, and their markers.

[Inline markup](docs/reference/markdown/inline): bold, italic, struck
and underlined text, code, and what stays literal.

[Links and images](docs/reference/markdown/links-and-images): link
targets written from the site root, anchors, links across languages and
to other sites; images, their alternative text and their captions.

## What is not supported

On purpose: every construct costs two renderings, and each one tilder
reads must look right in a browser and in a terminal.

- Headings other than `##` and `###`: a line starting with `#` or `####`
  is an ordinary paragraph, printed as written.
- Footnotes, definition lists, reference-style links and bare URLs: an
  address is a link only when it is written as `[label](target)`.
- Images inside a sentence, and raw HTML: an image is a block of its
  own, and HTML in the text is shown as text, escaped. Only a block
  starting with `<!--` goes into the page as it is.
- Escaping with a backslash: `\*` prints the backslash too. Rephrase
  instead. The one exception is `\|`, a pipe inside a table cell.
- Inline markup inside inline markup: `**[a link](docs/)**` is bold
  text, not a bold link.
- Lists, code or tables inside an inset: an inset holds paragraphs.
- Scripts in content. The theme's scripts are attached by the build,
  on the pages that need them ([scripts](docs/themes/scripts)).

## See also

- [writing pages](docs/guide/writing)
- [the text mirror](docs/reference/text-mirror)
- [classes](docs/themes/classes)
