---
title: post
description: The post type: dated articles named by their date, listed newest first by {posts}, with an RSS feed, article metadata and BlogPosting data.
order: 20
---

## Name

post - dated articles, newest first, with an RSS feed

A post is a Markdown file named by its date, in a collection of type
`post`: a blog, news, release notes. The collection lists its posts
newest first wherever a section says `{posts}`, writes an RSS feed of
them, and tells search engines and link previews that each one is an
article, with its date and its author.

[TOC]

## Settings

A `post` collection may set these keys under `[collections.<name>]`;
each has its default in the type's module, `types/post.py`.

| Key | Default | Meaning |
|---|---|---|
| `man` | `"SITE-BLOG(7)"` | the man-page name of its items, unless one sets its own |
| `nav` | `"blog/"` | the `[[nav]]` entry its items mark as current, and the link of the feed |
| `empty` | `"No post yet."` | the text of a `{posts}` list with nothing in it |
| `feed` | `""` | the RSS feed's path from the site root, `"blog/feed.xml"`; empty for none |
| `feed_title` | `"posts"` | the feed's title |
| `feed_description` | `"Posts."` | the feed's description |

This site's blog, for instance:

```toml
[collections.blog]
type = "post"
man = "TILDER-BLOG(7)"
feed = "blog/feed.xml"
feed_title = "tilder blog"
feed_description = "Release notes of tilder."
```

`defaults.toml` already declares `[collections.blog]` with `dir = "blog"`
and `feed = "blog/feed.xml"`: creating `content/blog/` is enough to start
one ([collections](docs/content-types)).

## A file per post

A post's file is named `YYYY-MM-DD-slug.md`: its date, a hyphen, then a
slug of lower-case letters, digits and hyphens. The name is the post's
address, and its date is the post's date; there is no `date:` key.

| Source, in `content/blog/` | Address |
|---|---|
| `2026-01-01-hello.md` | `/blog/2026-01-01-hello` |
| `2026-01-01-hello.fr.md` | `/fr/blog/2026-01-01-hello` |
| `2026-03-01-release/index.md` | `/blog/2026-03-01-release` |
| `2026-03-01-release/flow.svg` | `/blog/2026-03-01-release/flow.svg` |

- A post that shows images is a folder, with `index.md` and the images
  beside it.
- A file of the folder whose name does not start with a date is not a
  post: it is built as an ordinary page, which states its own `man`,
  `tagline` and `nav`.
- A name whose date does not exist stops the build:
  `"2026-02-30" is not a date`.
- `index.md` is the blog's own page, and `_template.md` is never built.

## Front matter

```markdown
---
title: Hello
description: The first post, in a file named by its date: all a post needs.
author: Me
tag: news
---
```

| Key | Meaning |
|---|---|
| `title` | the post's title |
| `description` | one sentence: the card's text in a list, the feed's summary, the link preview |
| `author` | a named author, on the card, in `<meta name="author">` and in the structured data |
| `tag` | one word, the card's tag and the `article:tag` |
| `man` | default: the collection's `man` |
| `nav` | default: the collection's `nav` |
| `tagline` | default: the date in words, `Thursday 1 January 2026`, written with `[dates]` |
| `updated` | a date, `2026-03-01`: the last change, in the sitemap and the structured data; default: the post's date |

Every other key of [writing pages](docs/guide/writing) applies too:
`image`, `robots`, `group`...

## The card

A post's card shows its date, its author and its tag, the date as a
`<time>` element. In a list the card also shows the description, and its
title links to the post; on the post's own page the same card, without
the link, closes the first section. In the text mirror:

```text
     Hello                                                         [ news ]
     Thursday 1 January 2026
     Me

         The first post, in a file named by its date: all a post needs.
```

## The list

A section marked `{posts}` lists every post of the collection, newest
first. The blog's own page is usually just that:

```markdown
---
man: MYSITE-BLOG(7)
title: blog
description: Posts, newest first, one Markdown file each, named by date.
tagline: posts
nav: blog/
feed: blog
---

## Posts {posts}
```

`{posts:news}` lists the collection `news` from any page; an empty list
shows the collection's `empty` text. `feed: blog` advertises the blog's
feed in the page's `<head>`.

## RSS

With `feed` set, the build writes the collection's RSS 2.0 feed at that
path: every post, newest first, each with its title, its address (also
its `guid`), its date and its description. The channel's title is
`feed_title`, its description `feed_description`, and its link the page
that `nav` names.

Each language has its own feed, under its prefix: `blog/feed.xml` in
English, `fr/blog/feed.xml` in French, with the words that
`site.fr.toml` gives the collection
([languages](docs/guide/languages)). An empty `feed`, the default of the
type, writes none.

## Search engines

A post is an article, in every sense the page can say it:

- its body is wrapped in `<article>`, which reader modes look for;
- `og:type` is `article`, with `article:published_time` (the date) and
  `article:tag` (the `tag`), and `<meta name="author">` when an author is
  named;
- its JSON-LD node is a `BlogPosting`: `headline`, `description`,
  `datePublished`, `dateModified` (`updated`, else the date), the site's
  organisation as `publisher`, the preview `image`, and the `author` as a
  `Person` when named.

The [SEO reference](docs/reference/seo) shows the whole `<head>`.

## See also

- [collections](docs/content-types)
- [event](docs/content-types/event)
- [feeds and images](docs/reference/feeds-and-images)
