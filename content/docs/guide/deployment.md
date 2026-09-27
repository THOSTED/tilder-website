---
title: Deployment
description: Put a tilder site online with Docker, compose and Caddy: clean URLs, the text mirror for curl, a plain-text host, headers, and other servers.
order: 50
---

## Name

deployment - serve the site, to browsers and to terminals

`public/` is a static site: any web server can serve it. tilder ships a
compose file and a Caddy configuration that serve it the way it is meant
to be: addresses without `.html`, the text mirror for `curl` at the same
address as the page, a host that serves only text, strict headers. This
page explains that contract, then what other servers can keep of it.

[TOC]

## Docker and compose

tilder's repository has both files in `examples/`: `compose.yaml` and
`Caddyfile`. Copy them next to `content/`, `theme/` and `assets/`, then:

```sh
docker compose up -d
```

The stack has two services. `build` runs the tilder image: it builds the
site into a volume, then watches the sources and rebuilds on every change
and at midnight. `web` is Caddy, serving that volume; it starts once the
first build has written `index.html`.

```yaml
services:
  build:
    image: ghcr.io/thosted/tilder:1
    volumes:
      - ./content:/site/content:ro
      - ./theme:/site/theme:ro
      - ./assets:/site/assets:ro
      - site:/out
    healthcheck:
      test: ["CMD", "test", "-f", "/out/index.html"]
  web:
    image: caddy:2-alpine
    depends_on:
      build:
        condition: service_healthy
    ports:
      - "8080:80"
      - "8081:81"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - site:/srv:ro
volumes:
  site:
```

This excerpt leaves out the healthcheck's timings and the environment.
The image tag `1` follows the latest 1.x release; pin a full version,
`1.4.0`, to choose when a site changes generator.

The hosts come from the environment of `web`. Locally, the defaults serve
the site at `site.localhost:8080` and its text at
`man.site.localhost:8080`; ports 8080 and 8081 also answer any host, so
`localhost:8080` serves the site and `localhost:8081` its text, and so
does the machine's address on the network. In production:

| Variable | Production value | What it is |
|---|---|---|
| `SITE_HOST` | `example.org` | the site, the same host as `site.url` |
| `WWW_HOST` | `www.example.org` | redirected to the site, never served |
| `MAN_HOST` | `man.example.org` | the plain-text host |
| `SITE_ORIGIN` | `https://example.org` | where the `www` host redirects to |
| `AUTO_HTTPS` | `ignore_loaded_certs` | Caddy obtains and renews the certificates |

`AUTO_HTTPS` fills Caddy's `auto_https` option, which has no `on`: any
value but `off` and `disable_certs` keeps automatic HTTPS, and
`ignore_loaded_certs` changes nothing else. With it, publish Caddy's ports
80 and 443 rather than 8080 and 8081, and point the three names at the
machine.

## Clean URLs

Pages are files ending in `.html` on disk, and addresses without it:
`/about` serves `about.html`, `/blog/` serves `blog/index.html`. Every
page has exactly one address; the others redirect to it, permanently:

- `/about.html` goes to `/about`;
- `/index` and `/index.html` go to `/`, and the same for each folder's
  page listed in the `@index` matcher, `/blog/index` and `/fr/index` in
  the example: add your own folders there;
- `/blog` goes to `/blog/` when `blog/index.html` exists.

The rules, from the example's `handle` block for browsers (its headers
are left out here):

```caddyfile
@index path /index /index.html /blog/index /blog/index.html /fr/index /fr/index.html
redir @index {http.request.uri.path.dir} permanent
@noslash {
  file {path}/index.html
  not path */
}
redir @noslash {path}/ permanent
@html path_regexp html ^/(.*)\.html$
redir @html /{re.html.1} permanent
try_files {path} {path}.html {path}/index.html
file_server
```

The links tilder writes are already in this form, so a reader never meets
a redirect by following them.

## Terminals get the text

A request from `curl`, `wget` or `httpie`, recognised by its
`User-Agent`, for a page (an address without a dot) gets the text
mirror, coloured, from `ansi/`, as `text/plain`, with a 200: no redirect
to follow, no `-L`. The one redirect drops a trailing slash, `/blog/` to
`/blog`, the address of the folder's text. Add `?plain` for the bare
ASCII of `txt/`, to save or to pipe: a twin block does the same from
`txt/`, not shown here.

```caddyfile
@terminal {
  header_regexp User-Agent (?i)^(curl|wget|httpie)/
  path_regexp ^/[^.]*$
  not path /LICENSE
  not query plain= plain=1 plain=true
}
handle @terminal {
  root * /srv/ansi
  header Content-Type "text/plain; charset=utf-8"
  header Cache-Control "public, max-age=300"
  @slash path_regexp slash ^(/.+)/$
  redir @slash {re.slash.1} permanent
  rewrite / /index.txt
  try_files {path}.txt {path} {path}/index.txt
  file_server
}
```

An address with a dot, `style.css` or `blog/feed.xml`, is served as it is,
so `curl -O` downloads files as usual. The same address answers a browser
with HTML and a terminal with text, so every response of the site carries
`Vary: User-Agent`: without it, a shared cache could hand one to the
other.

```console
$ curl example.org/about
$ curl "example.org/about?plain" > about.txt
```

## The plain-text host

`MAN_HOST` serves `txt/` only: the bare ASCII of every page, at the same
paths, whatever the client. It sniffs nothing, which makes it the
interface for scripts. Its pages carry `X-Robots-Tag: noindex`, and its
`robots.txt`, written from `[robots_man]`, asks search engines to stay
out: the site is what they index. The site's own `robots.txt`, from
`[robots]`, keeps them out of `/txt/` and `/ansi/`.

## Headers

**Content Security Policy.** Pages may load styles, fonts, images, the
manifest and scripts from the site itself, and nothing from anywhere
else; an inline script never runs. `connect-src 'self'` lets a theme's
script fetch a file of the same site, such as this manual's search index,
and no other host. The Caddyfile writes the policy on one line:

```text
default-src 'none'; style-src 'self'; font-src 'self';
img-src 'self'; manifest-src 'self'; script-src 'self';
connect-src 'self'; form-action 'none'; base-uri 'none';
frame-ancestors 'none'
```

An SVG file gets a policy of its own that lets it style itself with a
`<style>` element, and still run no script.

**Caching.** Fonts are kept a year (`immutable`: a font never changes
under the same name); styles, scripts and images a day; pages and the
coloured text served to terminals five minutes, so a rebuild shows
quickly.

**Compression.** Responses are compressed with zstd or gzip.

**The rest.** `X-Content-Type-Options: nosniff`,
`X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, a
`Permissions-Policy` that turns off location, microphone and camera; no
`Server` header. Calendars, feeds and the manifest get their content
types.

**Logs.** Access logs are discarded, `log { output discard }`: a site
built with tilder does not track its readers. Keep it that way.

## Error pages

A missing page gets the site's `404.html`, or its language's
(`/fr/404.html`) under a language's prefix. Each prefixed language takes
one line in `handle_errors`; a prefix the site does not declare gets the
default 404. A terminal gets a short text instead: edit the example's
`SITE(1)` and `curl example.org` to name your site.

```caddyfile
handle_errors {
  @terminalerror header_regexp User-Agent (?i)^(curl|wget|httpie)/
  respond @terminalerror "SITE(1)

Page not found.

See: curl example.org
" 404
  @fr path /fr/*
  rewrite @fr /fr/404.html
  rewrite * /404.html
  file_server
}
```

## Other servers

nginx, Apache or a static host serve `public/` as it is. What they keep
depends on what they can be told:

- **Clean URLs.** The links tilder writes have no `.html`, and neither
  have the canonical addresses of its pages, sitemap and feeds. Without a
  rule that maps `/about` to `about.html`, they lead nowhere. Most
  servers and many static hosts can do it; do it before anything else.
- **The text for curl.** It needs a rule on the `User-Agent`. Without
  it, `curl` gets the HTML; the text is still at `/txt/about.txt` and
  `/ansi/about.txt`. If you add the rule, add `Vary: User-Agent` with it.
- **Headers.** The policy, the cache lifetimes, compression and the
  discarded logs are the server's to set. A host that sets no headers
  serves the site without them: it works, with less protection.
- **Error pages.** One `404.html` is common; a 404 page per language needs
  a rule per prefix.

Every link between pages is relative, and every page is complete without
its scripts. The absolute addresses come from `site.url`: the canonical
link, `og:url`, the sitemaps and the feeds. Set it to the address the
site is served at.

## See also

- [getting started](docs/guide/getting-started)
- [the text mirror](docs/reference/text-mirror)
- [SEO](docs/reference/seo)
