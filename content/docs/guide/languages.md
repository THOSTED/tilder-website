---
title: Languages
description: Serve a site in several languages: declare them, translate the configuration and the pages, and know what happens to a page not yet translated.
order: 40
---

## Name

languages - a site in several languages

A site may be served in several languages: the default one at the root,
each other one under its own prefix, `/fr/`. Every declared language is a
complete site: a page not yet translated is still served, in the language
it is written in. Translations are files beside the originals, for the
pages and for the configuration alike.

[TOC]

## Declare the languages

```toml
# content/site.toml
[site]
lang = "en"                 # the default language, at the root
languages = ["en", "fr"]    # all served, the default first

[languages]                 # the names the language switcher shows
en = "English"
fr = "Français"
```

`site.languages` is empty by default: one language, no prefix, and no
file name is read as a translation. It must contain `site.lang`, or the
build stops. A language missing from `[languages]` shows its code.

## Translate the configuration

`content/site.fr.toml` holds only what differs in French, over
`site.toml`: `[site] lang`, `locale` and `manual`, the `[labels]` a reader
sees, `[[nav]]` (a list, so replaced as a whole: repeat every entry), the
words of each `[collections.<name>]`, `[dates]`, the texts of `[share]`.
The name of the site is a brand: keep `title_suffix` as it is.

```toml
# content/site.fr.toml
[site]
lang = "fr"
locale = "fr_FR"
manual = "Manuel de mon site"

[labels]
skip = "aller au contenu"
languages = "Langues"
```

A declared language without its file gets the default language's words,
so a site can be translated one word at a time. A `site.<lang>.toml` for a
language the site does not declare stops the build, and so does one whose
`[site] lang` names another language.

A theme may carry its own words the same way, in `theme/theme.fr.toml`.
The layers, the last winning:

```text
defaults.toml
  < theme/theme.toml < theme/theme.fr.toml
  < content/site.toml < content/site.fr.toml
```

A `theme.<lang>.toml` for a language the site does not declare is ignored,
neither read nor served: a theme is shared between sites and may know
more languages than any one of them.

## Translate a page

Put `about.fr.md` next to `about.md`. The same goes for a folder's page,
`blog/index.fr.md`, and for the items of a collection,
`blog/2026-01-01-hello.fr.md`. The translation keeps the English file
name: the address is `/fr/about`, the same slug under the prefix.

A suffix that names no declared language stops the build, so a typo never
becomes a page nobody meant: `about.fe.md` is an error. For the same
reason, a name whose last part is a word of two or three letters is read
as a suffix, `readme.txt.md` included; `notes.v2.md` is a plain name.

A site in one language reads no suffix at all: there, `notes.old.md` is
the page `notes.old`.

## Fallback

To build a page in French, tilder takes the first of these files that
exists:

1. `about.fr.md`;
2. `about.<default>.md`, the default language's own suffix;
3. `about.md`;
4. `about.<other>.md`, the other declared languages in their order.

So `/fr/about` exists even when only `about.md` does: the French
interface, the navigation and the labels, around the English text. The
language of the file chosen is the page's content language: the layout
gets it as `{{ content_lang }}`, for `<main lang="...">`, so a screen
reader reads the English text with an English voice.

## Links

A link written from the site root stays in the language of the page: on a
French page, `about` leads to `/fr/about`. A target that starts with `/`
leaves it: `[in English](/about)`, `[en français](/fr/about)`. A file, an
image or a stylesheet, is written once at the root and every language
links the same one. The [writing](docs/guide/writing#links) page has
every kind of target.

## The switcher

The layout's `{{ languages }}` placeholder is a `<nav class="languages">`
with one link per declared language, each to the same page in that
language; the current one is marked `aria-current="page"`. It is empty
on a site in one language. The region is named by `labels.languages`.

The names come from `[languages]` in `content/site.toml`: every language
is named the same way on every page, each in its own words. A
`[languages]` table in `site.fr.toml` is not read.

Two other placeholders tell a layout where things are: `{{ root }}` is the
site root, even under `/fr/`, for the stylesheet and the icons, written
once; `{{ home }}` is the landing page of the page's language, for links
to pages.

## What the build writes

| Output | Default language | French |
|---|---|---|
| pages | `about.html` | `fr/about.html` |
| text mirror | `txt/about.txt` | `txt/fr/about.txt` |
| RSS feed | `blog/feed.xml` | `fr/blog/feed.xml` |
| 404 page | `404.html` | `fr/404.html` |
| calendar, sitemap, `robots.txt`, manifest, icons | once, at the root | - |

- Every page carries a `<link rel="alternate" hreflang="...">` for each
  language, plus `x-default` for the default one, and the other
  languages' `og:locale:alternate`.
- One `sitemap.xml` lists every address of every language, each with its
  alternates.
- Each language has its own RSS feed, with its own title and description
  from `[collections.<name>]`. A page's `<link rel="alternate">` names the
  feed of its language.
- The iCalendar file of a collection of events is written once: a
  calendar has no interface language.
- The text mirror names the languages under its header rule:
  `LANGUAGES: en fr`.

The server must know each prefix, for its 404 page: see
[deployment](docs/guide/deployment).

## Limits

- The text mirror folds every character to ASCII and counts one column
  per character: it suits languages written in the Latin alphabet.
- tilder knows no language by name and holds no text: every word comes
  from the language's file. A language nobody translated shows the
  default language's words.
- An item kept as one file in one language and as a folder in another is
  not supported: choose one shape per item.

## See also

- [writing pages](docs/guide/writing)
- [the configuration reference](docs/reference/configuration)
- [deployment](docs/guide/deployment)
