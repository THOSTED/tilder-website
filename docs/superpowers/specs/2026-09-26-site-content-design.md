# tilder website - design

Date: 2026-09-26, revised 2026-09-27. Status: revision awaiting review.
Depends on tilder `v1.2.0` (nested collections, `--check`: tilder's
`docs/superpowers/specs/2026-09-27-v1.2-nested-collections-and-theme-checks-design.md`)
and on the documentation theme (`2026-09-26-docs-theme-design.md`, done).

Revision 2026-09-27 (the owner's choices): the documentation is a tree of
folders; a `Makefile` replaces `build.sh`; a compose stack serves the site
locally and in production; the theme's own checks move into tilder
(`--check`).

---

## 1. Goal

The website of tilder, at `https://tilder.thosted.fr`:

- a presentation of the project;
- an **exhaustive** documentation of what the generator can do (Markdown
  dialect, content types, languages, themes, configuration, SEO, feeds,
  images, text mirror, CLI, deployment);
- a "why tilder" page, a showcase of sites built with tilder, and a blog
  for release notes.

English is the default language, at the root. French is second, under
`/fr/`. The site is built by tilder itself with the theme of this
repository, so it is its own demonstration: `curl tilder.thosted.fr`
returns the text mirror.

### Decisions taken

- **Source of truth.** The documentation is **rewritten** here, in tilder's
  dialect, for users. `tilder/docs/` stays the contributors' reference.
  Drift is watched by hand (§8).
- **Tilder is fetched as a Docker image only** (`ghcr.io/thosted/tilder`),
  pinned by tag. No submodule. A local checkout may replace it for
  development (`make TILDER_BUILD=…`).
- **Make, not shell scripts**: a `Makefile` is the one entry point.
- **Served by Caddy in a compose stack**, with tilder's
  `examples/Caddyfile` contract, the same stack locally and in production.
- **No logo yet.** A provisional `assets/logo.svg`, a `~/` glyph in the
  theme's monospace outlined as paths, because tilder draws the icons and
  `share.png` from it. It is replaced when a logo exists.

### Not in this work

- A logo or brand identity.
- Automatic synchronisation with `tilder/docs/`.
- Any language other than English and French.
- Analytics of any kind (tilder forbids them).

---

## 2. Repository

```
tilder-website/
  content/            the site (§3)
  theme/              the documentation theme (its own spec)
  assets/logo.svg     provisional
  Makefile            build, check, watch, serve, test, clean (§6)
  compose.yaml        the build and Caddy (§6)
  Caddyfile           from tilder/examples, hosts from the environment
  .env.example        the hosts and ports, local defaults
  TILDER_VERSION      the pinned image tag, 1.2.0
  tools/check-coverage.py   the documentation's exhaustiveness check (§8)
  tests/              the theme's tests and fixture (already there)
  README.md
  .gitignore          public/
  docs/superpowers/   specs and plans
```

## 3. Content

Slugs are English in both languages. A translation is the same file with
`.fr` (`markdown.fr.md`).

| Page | Layout / type | Contents |
|---|---|---|
| `index.md` | `layout: home` | The hero: "a man-page site builder", one Markdown file in and two outputs out. Next to it, the source of a short page, its HTML, and its `curl` output. Then the features as cards (text mirror, types, languages, SEO, themes, accessibility, no dependency), a quick start (`docker run …`, the starter), links to the docs and to GitHub. |
| `why.md` | base | The principles: 75 columns and why, two renderings of everything, no third party, no JS required, no tracking, the standard library only, accessibility. An honest comparison with Hugo, Jekyll and Eleventy: what tilder does not do. |
| `docs/index.md` | base (collection index) | What the documentation covers, then `{docs}` grouped. |
| `docs/*.md` | `doc` | §4 |
| `showcase/index.md` | base | `{showcase}`, and how to be listed (a pull request). |
| `showcase/<slug>/index.md` | `showcase` | The sites built with tilder that the owner agrees to list. The seed is Théau's own sites that use it, to be confirmed. |
| `blog/index.md`, `blog/YYYY-MM-DD-*.md` | `post` | Release notes. The first post announces the site and v1.1.0. Feed at `blog/feed.xml`. |
| `404.md` | base | A man-page style "No manual entry for…". |
| `kitchen-sink.md` | base, `noindex` | The theme's test page (theme spec §10). |

Navigation (`[[nav]]`): home, docs, why, showcase, blog, GitHub ↗.

## 4. Documentation

`content/docs/`, type `doc`, **recursive** (tilder 1.2): the folders are
the sections of the sidebar, each with its own `index.md` (the section's
overview), in the order of `order:`. Each page opens with a one-paragraph
summary, and uses `[TOC]` when it has more than three sections.

```
docs/
  index.md                    what the documentation covers; {docs}
  guide/                      10  Guide
    index.md                      the path through the guide
    getting-started.md        10  Docker, or Python 3.11+ (rsvg-convert optional); the starter; the first build; --watch; public/
    project.md                20  content/, theme/, assets/; the three configuration layers; what is served; nothing generated is committed
    writing.md                30  pages, every front-matter key; sections as man-page sections; links (relative, cross-language, external, new tab); images next to a page
    languages.md              40  declaring languages, site.<lang>.toml, translated files, fallback, the switcher, hreflang, sitemaps and feeds per language, limits
    deployment.md             50  Docker and compose, the Caddyfile contract (clean URLs, curl gets the mirror, plain-text host, CSP incl. connect-src, caching), other servers and what is lost
  content-types/              20  Content types
    index.md                      collections: [collections.*], dir, recursive, markers, feeds, calendars
    page.md                   10
    post.md                   20  every DEFAULTS key, front matter, {posts}, RSS
    event.md                  30  {upcoming} {past} {next-event}, iCalendar
    member.md                 40  {members}, categories, profiles, members.js
    custom-types.md           50  the module, attributes (SEQUENTIAL, LOCALIZED_OUTPUTS...), functions, the item, the entry node, markers, imports, errors; a worked example
    navigation.md             60  order, group:, nested folders, nav_label, prev/next, the text line
  themes/                     30  Themes
    index.md                      using a theme; what a theme is
    files.md                  10  the files a theme may provide, what is served
    layouts.md                20  layout.html, layouts/, every placeholder
    classes.md                30  every class the builder writes
    scripts.md                40  code.js, a type's SCRIPT, the rules for scripts
    checking.md               50  build.py --check: classes, [check] contrast, the Markdown table
  reference/                  40  Reference
    index.md
    markdown/                 10  the dialect, one page per family, each construct's source then the construct rendered live (an .inset, or an {example} entry for blocks)
      index.md
      sections.md             10
      blocks.md               20
      entries.md              30
      inline.md               40
      links-and-images.md     50
    configuration.md          20  every key of defaults.toml, section by section: default, meaning, example; every labels.*
    text-mirror.md            30  75 columns, ASCII folding, txt/ and ansi/, colours and their markup, code frames, callouts, the plain-text host, text: no
    seo.md                    40  <title>, description, canonical, Open Graph, Twitter Card, JSON-LD per type, sitemaps, robots.txt, the build's checks and warnings
    feeds-and-images.md       50  RSS, iCalendar, icons and share.png: sources, tools, fallbacks
    cli.md                    60  build.py and every option (--root, --out, --watch and the midnight rebuild, --check, --debug, --version), errors, warnings, exit codes
```

"Exhaustive" means that every key of `defaults.toml`, every built-in type
setting, every front-matter key read by the builder, every placeholder,
every class, every Markdown construct and every CLI option appears on some
page; `tools/check-coverage.py` proves it (§8).

## 5. Configuration

`content/site.toml`:
- `site.name` = `"tilder"`, `url` = `"https://tilder.thosted.fr"`,
  `lang` = `"en"`, `languages` = `["en", "fr"]`;
- `manual` = `"tilder manual"`;
- `footer`: `TILDER(1)`, with a link to the repository;
- `[languages]` en = "English", fr = "Français";
- `[links] new_tab` = `false`;
- `[collections.docs]` type `doc` (recursive by the type's default),
  `[collections.showcase]` type `showcase`, `[collections.blog]` `post`
  with its feed;
- `[share]` card lines;
- `[text] commands` = `["curl", "docker", "python3"]`.

`content/site.fr.toml`: every word that differs, and the French `[dates]`.

## 6. Build and serve

**`Makefile`** (GNU make; every recipe is a few lines of POSIX shell):

| Target | Does |
|---|---|
| `make` / `make build` | `check`, then builds `content/` into `public/`; fails on any `warning:` or `seo:` line |
| `make check` | tilder's `--check` on the theme (classes, contrast), and `tools/check-coverage.py` |
| `make watch` | rebuilds on every change (checks once first) |
| `make serve` | `docker compose up`: the site at `http://localhost:8080`, `curl localhost:8080` gets the text mirror |
| `make test` | the theme's tests (`python3 -m unittest`) |
| `make clean` | removes `public/` |

- tilder runs from `ghcr.io/thosted/tilder:$(TILDER_VERSION)` (read from
  `TILDER_VERSION`), as `python3 -B /tilder/build.py --root /site --out
  /out`, the site mounted read-only, as the calling user. `DOCKER=podman`
  works. `make TILDER_BUILD=/path/to/tilder/build.py` uses a checkout
  instead.
- `build.sh` is removed; the theme's tests that built through it build
  through `make` (or tilder directly) instead.

**`compose.yaml`**, one stack for local and production:

- `build`: the tilder image, builds the site into a volume, then exits
  (`make serve` runs it first; `docker compose run build` rebuilds).
- `web`: `caddy:2` with the site's `Caddyfile` (tilder's
  `examples/Caddyfile`, hosts and ports from the environment), serving the
  volume: clean URLs, `curl` gets the ANSI mirror, the plain-text host, the
  CSP with `connect-src 'self'`, caching, compression.
- `.env.example`: `SITE_HOST=localhost:8080`, `TEXT_HOST=localhost:8081`
  locally; production sets `SITE_HOST=tilder.thosted.fr` and the text host,
  and Caddy fetches the certificates.

**The theme** drops what tilder now does: `tools/check-theme.py`,
`tools/check-contrast.py`, `tools/tilder-theme.md` and their tests go;
`theme/theme.toml` declares `[check] contrast` (its 28 pairs); the
README's contrast table comes from `--check --markdown`.

## 7. Translation

- Every page exists in French.
- The French is written, not machine-output. Code, option names, keys and
  class names stay as they are.
- A page not yet translated falls back to English, which tilder does
  natively, so the site is shippable at any point.

## 8. Keeping it true

- The site pins one tilder version, and the docs describe that version.
- When the pin is bumped, the tilder changelog (git log between tags) and
  the diffs of `tilder/docs/` and `defaults.toml` are reviewed, and the
  pages updated.
- The exhaustiveness checklist lives in the plan. A small script
  (`tools/check-coverage.py`) greps the site's content for every key of the
  pinned `defaults.toml`, every class and placeholder of `docs/theme.md`,
  and every CLI option, and fails on a miss. It runs in `make check`.

## 9. Done when

- `make` passes, with no warning and every check green.
- `make serve`: `curl localhost:8080` returns the landing page's text
  mirror, and a browser returns HTML; the docs' sidebar shows the folder
  tree.
- Every page exists in both languages.
- The kitchen sink passes review in light and dark, on phone and desktop.
