---
title: Classes
description: Every class tilder writes in its HTML, grouped as in its contract, with the element each lands on, and the accessibility a theme owns.
order: 30
---

## Name

classes - every class the build writes, for the theme to style

The build writes semantic HTML with a fixed set of class names and never
an inline style, a colour or a font: those are the theme's. This page is
that set, grouped as in tilder's own contract, with the element each
class lands on. A theme that styles all of them shows every page tilder
can build; `build.py --check` tells it which ones it misses.

[TOC]

## The page

| Class | On | What |
|---|---|---|
| `.sr-only` | `<span>` | required: text for screen readers only, to hide visually. The separators of the wordmark, the words that replace the arrow of an external link, a profile's network, "opens in a new tab" |
| `.wordmark` | `<h1>` | the page's heading, the wordmark as a path: `~/site/section/title` |
| `.tilde` | `<span>` | the `~/` at its start, hidden from screen readers |
| `.slash` | `<span>` | each `/` between segments, hidden from screen readers |
| `.here` | `<span>` | the page's own segment, the last one |
| `.cursor` | `<span>` | an empty element after it, hidden from screen readers, for a cursor |
| `.nav` | `<nav>` | the site's navigation, around `{{ nav }}`; the layout writes this element (the starter: `<nav class="nav">`) |
| `.sep` | `<span>` | between two links of `{{ nav }}`, a middle dot hidden from screen readers |
| `.languages` | `<nav>` | the language switcher, `{{ languages }}`: one `<a>` per language, the current one `aria-current="page"` |

The segments of the wordmark between the site's name and the page's own
link to the pages they name: a folder's `index.md`, else the page beside
it. A section of a recursive collection without its own page is named
by its folder, not linked. On the landing page, the wordmark is `~/site`
and the cursor.

## A collection's navigation

| Class | On | What |
|---|---|---|
| `.collection-nav` | `<nav>` | the collection's sidebar, `{{ collection_nav }}`, around a `<ul>` of links; the current page's link is `aria-current="page"` |
| `.collection-group` | `<li>` | a group of items (their `group:`), holding its label and a `<ul>` |
| `.collection-group-label` | `<span>` | the group's name: a label, not a heading |
| `.prev`, `.next` | `<a>` | `{{ prev }}` and `{{ next }}`, the links to the neighbours, with `rel="prev"` and `rel="next"` |
| `.prev-label`, `.next-label` | `<span>` | inside them, the words `labels.prev` and `labels.next`, before the neighbour's title |

A recursive collection nests its folders in the sidebar, as sections:

| Class | On | What |
|---|---|---|
| `.collection-section` | `<li>` | a section: its label, then a `<ul>` of its pages |
| `.collection-section--open` | `<li>` | added to the section that holds the current page, so the theme may fold the others |
| `.collection-section-label` | `<a>` or `<span>` | the section's name: a link to its own page (its `index.md`, or a `<name>.md` beside the folder), titled like it; without one, a `<span>` with the folder's name |

The sidebar of this manual on its page `docs/guide/writing`, shortened
(`<!-- ... -->` stands for the lines left out); the build makes every
link relative to the page:

```html
<nav class="collection-nav" aria-label="In this section">
<ul>
	<li class="collection-section collection-section--open"><a class="collection-section-label" href="../guide">Guide</a>
	<ul>
		<li><a href="getting-started">Getting started</a></li>
		<li><a href="project">The project</a></li>
		<li><a href="writing" aria-current="page">Writing pages</a></li>
		<!-- ... -->
	</ul>
	</li>
	<li class="collection-section"><a class="collection-section-label" href="../content-types">Content types</a>
	<ul>
		<li><a href="../content-types/page">page</a></li>
		<!-- ... -->
	</ul>
	</li>
	<!-- ... -->
</ul>
</nav>
```

## Sections and lists

| Class | On | What |
|---|---|---|
| `.s` | `<section>` | a `##` section of the page, holding its `<h2>` and its body |
| `.b` | `<div>` | the section's body, after the `<h2>` |
| `.b.grid` | `<div>` | a body marked `{grid}`, or a list of members: entries as a grid of cards |
| `.members`, `.posts` | `<div class="b">` | a body marked `{members}` or `{posts}`, listing that collection |
| `.upcoming`, `.past`, `.next-event` | `<div class="b">` | a body marked `{upcoming}`, `{past}` or `{next-event}`, listing events |
| `.entry` | `<div>` | an entry: a `###` of the page, or an item's card in a list, its title an `<h3>`; on an item's own page, its card has no `<h3>`, the `<h1>` being the title |
| `.entry--next` | `<div class="entry">` | the next event: the first card of `{upcoming}`, the card of `{next-event}` |
| `.entry--full` | `<div class="entry">` | a member at capacity, `full: yes` |
| `.entry--link` | `<div class="entry">` | a card whose title is a link to the item's page; the theme may make the link cover the whole card |
| `.meta` | `<p>` | an entry's meta line: a date, an author, a place, a pronoun..., each in a `<span>` |
| `.tag` | `<span>` | a tag in the meta line: a post's `tag`, an event's upcoming or past, a member's category |
| `.tag--next`, `.tag--full` | `<span class="tag">` | the tags of a `.entry--next` or `.entry--full` card |

A marker naming a collection, `{upcoming:meetups}`, gives the class
without its name: `upcoming`. The words of tags and states are always
written: a full mentor's card says "full", never only by a colour.

## Text

| Class | On | What |
|---|---|---|
| `.small`, `.muted`, `.faint`, `.mono`, `.warn` | `<p>` | the paragraph classes a writer adds at the end of a paragraph: `{small muted}` |
| `.empty` | `<p>` | the empty state: a list with nothing in it, or a paragraph in `*...*` alone |
| `.inset` | `<div>` | a `>` inset, holding paragraphs |
| `.callout` | `<div role="note">` | a callout, `> [!INFO]`, `[!WARNING]` or `[!ERROR]` |
| `.callout--info`, `.callout--warning`, `.callout--error` | `<div class="callout">` | its kind |
| `.callout-label` | `<p>` | its first line, the word of its kind (`labels.info`...) |
| `u.u` | `<u>` | `++underlined++` text |

The [Markdown reference](docs/reference/markdown) shows each of these
constructs, its source and its rendering.

## Code

| Class | On | What |
|---|---|---|
| `pre.code` | `<pre tabindex="0">` | a code block, around a `<code>`; focusable, so a keyboard can scroll it |
| `pre.code[data-lang]` | `<pre class="code">` | a highlighted block: `data-lang` holds the language as written, in lowercase, for the theme to show (`content: attr(data-lang)`); the `<code>` inside is `language-<lang>` |
| `.hl-k` | `<span>` | a keyword |
| `.hl-b` | `<span>` | a builtin, a type, a literal |
| `.hl-s` | `<span>` | a string |
| `.hl-c` | `<span>` | a comment |
| `.hl-n` | `<span>` | a number |
| `.hl-v` | `<span>` | a variable |
| `.hl-p` | `<span>` | a prompt, `$` or `#` |
| `.hl-t` | `<span>` | a tag, a section, a key |
| `.hl-gi`, `.hl-gd`, `.hl-gh` | `<span>` | a diff's inserted line, deleted line, hunk header |

A block in no language, or in one tilder does not know, is a plain
`<pre class="code">` without `data-lang` and without tokens. A diff keeps
its `+` and `-`: colour is never the only sign.

## Tables, lists, figures

| Class | On | What |
|---|---|---|
| `.table` | `<div tabindex="0" role="region">` | the wrapper of every table, named by `labels.table`, so a wide table scrolls on its own instead of the page |
| `th.center`, `td.center` | `<th>`, `<td>` | a column aligned `:---:` |
| `th.right`, `td.right` | `<th>`, `<td>` | a column aligned `---:`; left alignment has no class |
| `.tasks` | `<ul>` or `<ol>` | a list with task items |
| `.task` | `<span role="img">` | the box of a task, empty, named for screen readers by `labels.task_done` or `labels.task_todo` |
| `.task--done`, `.task--todo` | `<span class="task">` | its state, `[x]` or `[ ]` |
| `.figure` | `<figure>` | an image alone on its line, with its `<figcaption>` when it has a title |
| `.toc` | `<nav>` | a `[TOC]`: a `<details>` holding an `<ol>` of the page's sections, closed by default |
| `.toc-label` | `<summary>` | the `[TOC]`'s label, `labels.toc`, which opens it |
| `.profiles` | `<p>` | a member's profile links |
| `.icon` | `<svg>` | a network's logo in a profile link, from `icons/<network>.svg`, hidden from screen readers |

## Accessibility the theme owns

The build writes the markup: one `<h1>`, `<h2>` for sections and `<h3>`
for entries, alt text (it warns when an image has none), labels and
`aria-*` attributes, focusable scrolling regions, a word next to every
colour. The rest is the theme's:

- **Contrast**: 4.5:1 at least for text, against its background, in each
  colour scheme the theme offers. [Checking a
  theme](docs/themes/checking) measures the pairs a theme declares.
- **Focus**: a visible outline on everything that takes the focus, links,
  the `[TOC]`'s summary, and the focusable `pre.code` and `.table`.
- **Hidden text**: `.sr-only` is hidden visually, and still read.
  `display: none` would hide it from screen readers too; the usual rule:

```css
.sr-only {
	position: absolute; width: 1px; height: 1px; overflow: hidden;
	clip-path: inset(50%); white-space: nowrap;
}
```

- **Reduced motion**: no animation, or none under `@media
  (prefers-reduced-motion: reduce)`, for the cursor of the wordmark as for
  anything else.

## See also

- [checking a theme](docs/themes/checking)
- [layouts and placeholders](docs/themes/layouts)
- [the Markdown reference](docs/reference/markdown)
