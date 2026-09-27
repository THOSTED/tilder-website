---
title: page
description: The page type: every Markdown file outside a collection, with no settings, no card and no list, described to search engines as a WebPage.
order: 10
---

## Name

page - the type of every page outside a collection

Every Markdown file that is not an item of a collection is a `page`: the
landing page, an about page, the page of a collection that holds its
list, the 404 page. The type adds nothing to what a page writes.
It has no settings, gives no card to any list and writes no feed.

[TOC]

## Front matter

A page states everything itself: `man`, `title`, `description`,
`tagline` and `nav` are all written in its front matter, since there is
no collection to take them from. Every key of
[writing pages](docs/guide/writing) applies.

```text
---
man: MYSITE-ABOUT(7)
title: About
description: Who writes this site and why, and how to reach them.
tagline: who, why and how to write
nav: about
---
```

## What the type does

- **Layout.** The theme's `layouts/page.html` if it has one, else
  `layout.html`; a page's `layout:` key picks another
  ([layouts](docs/themes/layouts)).
- **Card.** None: a page never appears in a list.
- **Structured data.** A `WebPage` node, with the page's title and
  description, part of the site's `WebSite` ([SEO](docs/reference/seo)).
- **Open Graph.** `og:type` is `website`.

A theme may replace the type, like any built-in one, by shipping a module
named `page` in `theme/types/`
([types of your own](docs/content-types/custom-types)).

## See also

- [writing pages](docs/guide/writing)
- [collections](docs/content-types)
- [post](docs/content-types/post)
