---
title: Scripts
description: The scripts a tilder theme may ship, code.js, members.js and a type's own, where the build loads each one, and the rules every script follows.
order: 40
---

## Name

scripts - what a theme's scripts may do, and where they load

Scripts belong to the theme: tilder writes none and needs none. It knows
two by name, `code.js` for the copy button and `members.js` for the
members' search, and any script a content type names. It loads each only
on the pages it serves, and only if the theme ships the file. Every
script improves a page that is complete without it.

[TOC]

## code.js

A copy button on code blocks. The build adds its tag to every page that
has a code block, anywhere in its sections, when the theme has `code.js`:

```html
<script src="../code.js" defer
	data-copy="copy" data-copied="copied"></script>
```

The words of the button come from `labels.copy` and `labels.copied`,
through the tag's `data-copy` and `data-copied`: the script holds no text
of its own, so it speaks every language of the site. The blocks it works
on are the `pre.code` elements ([classes](docs/themes/classes)); the
language label, `data-lang`, is not part of the code, so a script that
copies the `<code>` inside copies the code alone.

## members.js and a type's script

A content type may name a script in its `SCRIPT` attribute: the build adds
its tag to every page that has a section listing the type, when the theme
ships the file. The built-in `member` type names `members.js`, for the
search and filter of a `{members}` list ([members](docs/content-types/member)):

```html
<script src="members.js" defer></script>
```

The list gives the script what it needs, as data: the section's body, a
`<div class="b members grid">`, carries the words of the member
collection (`data-search_label`, `data-search_placeholder`, `data-all`,
`data-one`, `data-many`, `data-none`), and each card, a `<div
class="entry">`, its `data-category` and `data-search`, the member's names
in lowercase ASCII.

A theme's own type does the same: this site's `doc` type names
`search.js`, loaded on the pages that list the documentation. A type
writes the `data-*` of the section that lists it with its `list_data`
function ([custom types](docs/content-types/custom-types)).

## Where the tags go

`{{ script }}` holds every tag the page needs: first the scripts the
listed types name, each once, then `code.js`. Each has `defer`, so it runs
once the page is parsed, and a `src` relative to the page. Place
`{{ script }}` at the end of the `<body>` of every layout; a layout
without it loads none of these scripts.

A layout may also load a script of its own, on every page it serves, with
a tag of its own:

```html
<script src="{{ root }}nav.js" defer></script>
```

This site's documentation layout loads its sidebar script that way. Like
every theme file, a script in the site's `assets/` replaces the theme's of
the same name ([files](docs/themes/files)).

## The rules

A theme's scripts follow the rules of tilder's own contract (its
`AGENTS.md`, "Scripts"), which the server's Content-Security-Policy
enforces:

<!-- 1.2 -->

- **A file, never inline.** ES5, no dependency, a file the site serves:
  never a `<script>` with code in the page, never a CDN. The example
  Caddyfile's policy allows scripts with `script-src 'self'` alone, so a
  browser would refuse both. The one inline `<script>` is the JSON-LD the
  build writes, which is data, not code.
- **Enhancement only.** The page is complete without the script: every
  text readable, every link followed. The script creates its own
  controls, the copy button, the search field, so a reader without
  JavaScript sees none of them rather than a control that does nothing.
- **No text of its own.** Its words come from the configuration, through
  `data-*` attributes the build or the layout writes: `labels.copy` for
  the copy button, a theme's `[search]` for its search.
- **No storage, no cookie.**
- **Same-origin requests only.** A script may fetch the site's own files,
  a search index for example, and nothing else: no other host. The policy
  grants `connect-src 'self'`; under a policy that lacks it, the browser
  blocks the request, and the script should then remove its control, as
  this site's search does.

The same policy has `style-src 'self'`: a script shows and hides with
classes and the `hidden` attribute rather than with inline styles. The
[deployment](docs/guide/deployment) page gives the whole policy.

## See also

- [custom types](docs/content-types/custom-types)
- [deployment](docs/guide/deployment)
- [classes](docs/themes/classes)
