---
title: Navigation
description: The order of a collection's pages, their groups and sections, the sidebar, the links to the previous and next page, and their line in the text mirror.
order: 60
---

## Name

navigation - the order of a collection, its sidebar and its neighbours

The pages of a collection have an order, set by their type. A theme shows
it three ways: a sidebar of every page, grouped and nested, links to the
previous and the next page, and, in the text mirror, a line naming both.
This manual is built that way: the sidebar on the left, the links at the
foot of each page.

[TOC]

## The order

A collection's order is its type's `sort_key`, applied to every item;
without one, the order of the slugs. Posts and events are named by their
date, so their slugs sort by date; their lists then read that order
backwards, newest first. Members sort by category, then last name. The
sidebar, the neighbours, the text line and the lists all start from this
order.

This site's documentation uses the `doc` type of its theme, whose order
is the `order` front-matter key, a whole number, then the slug:

```markdown
---
title: Getting started
description: Install tilder, build the starter site, look around.
order: 10
---
```

A page without `order` counts as `1000`, after the numbered ones.
`order` is the `doc` type's key, not tilder's: another type sorts by
whatever its `sort_key` reads
([types of your own](docs/content-types/custom-types)). A translation
keeps the `order` of its original, so both languages list the pages
alike.

## Groups

An item may set `group` in its front matter. The sidebar then gathers the
items of each group under the group's label: the items without a group
first, then each group in the order of its first item, the items of a
group in the collection's order.

```markdown
---
title: Deployment
description: Put a site online: Docker, compose, Caddy, others.
group: Serving
---
```

A group's label is compared as written, language by language: every
French file of a group must spell its `group` the same way, or the
sidebar shows two groups. The neighbours ignore groups.

## Sections

In a recursive collection (tilder 1.2), the folders are sections, as the
sections of this manual are. The order is depth first: within a folder,
its items and its sections are sorted by `sort_key`, a section by its own
page, its `index.md` or a `<name>.md` beside the folder (a section without
one comes after them, by folder name); a section's own page comes first,
then the pages it holds. So
`order: 20` in `content/docs/content-types/index.md` places the whole
section, and `order: 10` in `content/docs/content-types/page.md` places
the page inside it.

The sidebar nests the sections, each labelled by its own page's title,
linked, or by its folder's name when it has none. `group` works at every
level. The neighbours and the text line follow the same depth-first
order: the last page of a section leads on to whatever follows it, the
next page of the folder above or the next section's own page.

## The sidebar

The layout's `{{ collection_nav }}` placeholder is the collection's
sidebar: every item, in order, grouped, the current page marked with
`aria-current="page"`. It appears on the collection's items and, with
nothing marked, on the collection's own page; it is empty elsewhere.

```html
<nav class="collection-nav" aria-label="In this section">
<ul>
	<li><a href="start">Getting started</a></li>
	<li class="collection-group"><span class="collection-group-label">Serving</span>
	<ul>
		<li><a href="deployment" aria-current="page">Deployment</a></li>
	</ul>
	</li>
</ul>
</nav>
```

With sections (tilder 1.2), a section is a list item of class
`.collection-section` holding its label and a nested list; the section of
the current page adds `.collection-section--open`, so a theme can fold
the others. The label, `.collection-section-label`, is a link to the
section's own page, or a `<span>` for a section without one.

The `<nav>` is named for screen readers by the collection's `nav_label`,
else by `labels.collection_nav`, `"In this section"` by default:

```toml
[collections.docs]
type = "doc"
nav_label = "In the manual"
```

Its classes are `.collection-nav`, `.collection-group` and
`.collection-group-label`, and the neighbours below add `.prev`,
`.prev-label`, `.next` and `.next-label`: the
[classes](docs/themes/classes) page lists them all, and
[layouts](docs/themes/layouts) says where the placeholders go.

## Previous and next

`{{ prev }}` and `{{ next }}` link a page to its neighbours in the order,
groups ignored:

```html
<a class="prev" rel="prev" href="writing"><span class="prev-label">previous</span> Writing pages</a>
<a class="next" rel="next" href="deployment"><span class="next-label">next</span> Deployment</a>
```

Each is empty at its end of the collection, on the collection's own page,
and on every page outside a collection. The labels are `labels.prev`,
`"previous"`, and `labels.next`, `"next"`, translated in each language's
`site.<lang>.toml` ([configuration](docs/reference/configuration)).

## The text line

A type that sets `SEQUENTIAL = True` gives each item's text mirror one
more line, just before the footer: the previous page on the left, the
next one on the right, both with their labels.

```text
previous: Writing pages                                     next: Languages
```

The line is 75 columns at most, in ASCII. When both do not fit, each
side keeps half the width and a title that overflows its half is cut
with `...`; a short side leaves its room to the other. The first page has
only `next:`, the last only `previous:`. The `doc` type of this site sets
`SEQUENTIAL`, so `curl` can walk the manual from page to page.

## See also

- [collections](docs/content-types)
- [types of your own](docs/content-types/custom-types)
- [layouts](docs/themes/layouts)
- [the text mirror](docs/reference/text-mirror)
