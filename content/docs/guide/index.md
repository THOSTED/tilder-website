---
title: Guide
description: The path through tilder, page by page: install it, lay out a project, write pages, add a language, then put the site online.
order: 10
---

## Name

guide - from the first build to a site online

The guide takes a site from nothing to production in five pages, each
building on the one before. It explains what you do and why; the
reference gives every value and option in full.

## The path

[Getting started](docs/guide/getting-started) installs tilder, with
Docker or with Python, copies the starter site and builds it. It shows the
watch mode, which rebuilds as you write, and what the build leaves in
`public/`.

[The project](docs/guide/project) walks through the three folders of a
site, `content/`, `theme/` and `assets/`, the three layers of the
configuration, and which files end up on the server and which never do.

[Writing pages](docs/guide/writing) turns a Markdown file into a page: its
URL, every front-matter key, sections in the manner of a man page, links
and images.

[Languages](docs/guide/languages) adds a second language: declaring it,
translating the configuration and the pages, what happens to a page not
yet translated, and what the build writes for each language.

[Deployment](docs/guide/deployment) puts the site online: Docker and
compose, the Caddy configuration that serves the text mirror to `curl`,
and what other servers can and cannot do.

## See also

- [the Markdown reference](docs/reference/markdown)
- [the configuration reference](docs/reference/configuration)
- [the command line](docs/reference/cli)
