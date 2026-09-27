---
title: The project
description: The three folders of a tilder site, content/, theme/ and assets/, the three layers of its configuration, and what is served.
order: 20
---

## Name

project - the folders of a site and its configuration

A tilder project is three folders: `content/` for what you write,
`theme/` for how it looks, `assets/` for the files served as they are. The
configuration comes in three layers, from tilder's defaults to your own
`site.toml`. The build reads all of it and serves only what belongs on a
website.

[TOC]

## The three folders

```text
my-site/
  content/          the pages, and the site's configuration
    site.toml         the settings and the words of the site
    site.fr.toml      what differs in French (optional)
    index.md          the landing page
    404.md            the page for a missing address
    blog/             a collection: one file per post
  theme/            how it looks
    layout.html       the page around the content (required)
    style.css
    theme.toml        the theme's own configuration (optional)
  assets/           served as they are
    logo.svg          the source of every icon and of share.png
  public/           the built site: never edited, never committed
```

### content/

  Every Markdown file is a page, at the address its path gives
  ([writing pages](docs/guide/writing)). A folder declared as a
  collection in `site.toml` holds items of one type: posts, events,
  members, or a type the theme adds ([content types](docs/content-types)).
  Any other file, an image or a PDF, is copied to the site at the same
  path, so an image lives next to the page that shows it.

### theme/

  `layout.html` is the only file a theme must have: the HTML around every
  page, filled with placeholders. The rest is optional: `style.css`,
  scripts, fonts, other layouts, content types in Python, and
  `theme.toml`. The starter's theme is a complete, minimal one to begin
  with ([themes](docs/themes)).

### assets/

  The project's own files, served at the root of the site as they are:
  `assets/logo.svg` is `/logo.svg`. It is also the source the build draws
  the icons and the link preview from. A file in `assets/` wins over the
  theme's file of the same name, so a site can replace one file of a
  theme it did not write, `style.css` or `layout.html`, without touching
  the theme.

## Configuration

The settings of a site, and every word a reader sees outside the pages,
come from TOML files. tilder holds no text of its own. Three layers, each
merged over the one before, so each only states what differs:

1. `defaults.toml`, in tilder: every key it reads, with its default and
   a comment. The [configuration reference](docs/reference/configuration)
   documents each one.
2. `theme/theme.toml`: the theme's own values, such as the colours of
   the link preview.
3. `content/site.toml`: your site. It has the last word.

```toml
# content/site.toml: only what differs from the defaults
[site]
name = "my site"
url = "https://example.org"
title_suffix = " - my site"

[footer]
right = "MYSITE(1)"
```

Each additional language adds a file to the theme's layer and to the
site's, read in this order, the last winning:

```text
defaults.toml
  < theme/theme.toml < theme/theme.fr.toml
  < content/site.toml < content/site.fr.toml
```

Tables are merged key by key: a `site.fr.toml` that sets `[site] manual`
keeps every other key of `[site]`. A list of tables, such as the
navigation's `[[nav]]`, is replaced as a whole: a file that sets it
repeats every entry. The settings of a collection start from its type's
own defaults, in the type's module, with `[collections.<name>]` over
them.

Configuration files are read at every build, so a change applies at the
next one, and none of them is ever served.

## What is served

The build turns `content/` into pages and copies the rest; a few files are
read, never served.

| Folder | Served | Never served |
|---|---|---|
| `content/` | the pages, built from the Markdown; every other file, at its own path | the Markdown sources; `site.toml` and `site.<lang>.toml`; any file or folder whose name starts with `_` |
| `theme/` | everything else, at the site root: `style.css`, scripts, `fonts/`... | `layout.html`, `layouts/`, `share.svg`, `icons/`, `types/`, `theme.toml` and `theme.<lang>.toml`; `.git` and every file whose name starts with `.git`; a `README.md` or a `LICENSE` at its top |
| `assets/` | everything else, at the site root | the same list as `theme/` |

A `LICENSE` file at the top of the project, next to `content/`, is served
at the root of the site.

The `_` prefix keeps drafts and templates in `content/`: `_draft.md` or
`blog/_template.md` is never built. The theme's list lets a theme live in
its own git repository, with its README and licence, without publishing
them.

## Nothing generated is committed

`public/` is built from the sources every time: add it to `.gitignore`.
The icons and `share.png` are drawn again at every build, from
`assets/logo.svg` and the theme's `share.svg`, so they are not committed
either. What goes into version control is `content/`, `theme/`, `assets/`,
and whatever builds and serves them: a compose file, a Caddyfile.

```text
# .gitignore
public/
```

## See also

- [writing pages](docs/guide/writing)
- [the configuration reference](docs/reference/configuration)
- [the files of a theme](docs/themes/files)
