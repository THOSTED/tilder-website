# tilder website - design

Date: 2026-09-26. Status: approved in conversation, awaiting review of this
document. Depends on tilder `v1.1.0` and on the documentation theme
(`2026-09-26-docs-theme-design.md`).

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
  pinned by tag. No submodule.
- **Served by Caddy**, with tilder's `examples/Caddyfile` contract.
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
  build.sh            the build (§6)
  compose.yaml        Caddy + a build service, from tilder/examples
  Caddyfile           from tilder/examples, hosts from the environment
  TILDER_VERSION      the pinned image tag, e.g. v1.1.0
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

`content/docs/`, type `doc`, grouped. Each page opens with a one-paragraph
summary, and uses `[TOC]` when it has more than three sections.

**Guide**

| order | slug | Covers |
|---|---|---|
| 10 | `getting-started` | What you need: Docker, or Python 3.11+ with `rsvg-convert` optional. Copying the starter, the first build, `--watch`, what `public/` holds. |
| 20 | `project` | The layout of a project (`content/`, `theme/`, `assets/`), the three configuration layers, what is served and what is not, "nothing generated is committed". |
| 30 | `writing` | Pages, front matter (every key the builder and the built-in types read), sections as man-page sections, links (relative, cross-language, external, new tab), images next to a page. |
| 40 | `collections` | Collections, and the four built-in types with every setting (`DEFAULTS` tables), front matter, markers (`{posts}`, `{upcoming}`, `{past}`, `{next-event}`, `{members}`), feeds and calendars. |
| 50 | `languages` | Declaring languages, `site.<lang>.toml`, translated files, fallback, the switcher, `hreflang`, sitemaps and feeds per language, limits. |
| 60 | `themes` | Using and writing a theme: files, layouts, placeholders, classes, scripts, fonts, `share.svg`, `theme.toml`, and the rules (a11y, no third party). |
| 70 | `custom-types` | Writing a type: the module, attributes (`SEQUENTIAL`, `LOCALIZED_OUTPUTS` included), functions, the item, the entry node, markers, what a type may import, errors. With a worked `talk` example. |
| 80 | `deployment` | Docker and compose, the Caddyfile contract (clean URLs, `curl` gets the mirror, plain-text host, CSP, caching), other static servers and what is lost there. |

**Reference**

| order | slug | Covers |
|---|---|---|
| 110 | `markdown` | Every construct of `tilder/docs/markdown.md`: its source in a code block, then the construct rendered live in an `.inset`. A note on the text mirror links to the page's own mirror. |
| 120 | `configuration` | Every key of `defaults.toml`, section by section: its default, its meaning, and an example. Every `labels.*`. |
| 130 | `text-mirror` | 75 columns, ASCII folding, `txt/` and `ansi/`, colours and the markup that drives them, code frames, callouts, the plain-text host, `text: no`. |
| 140 | `seo` | `<title>`, description, canonical, Open Graph and Twitter Card, JSON-LD per type, sitemaps, `robots.txt`, the build's checks and warnings. |
| 150 | `feeds-and-images` | RSS, iCalendar, the icons and `share.png`: sources, tools (`rsvg-convert`, `woff2_decompress`, ImageMagick fallback), what is skipped and when. |
| 160 | `cli` | `build.py` and its options, `--root` resolution, `--watch` (and the midnight rebuild), `--debug`, the shape of errors and warnings, exit codes. |

"Exhaustive" means that every key of `defaults.toml`, every built-in type
setting, every front-matter key read by the builder, every placeholder,
every class, every Markdown construct and every CLI option appears on some
page. A checklist in the implementation plan tracks this (§8).

## 5. Configuration

`content/site.toml`:
- `site.name` = `"tilder"`, `url` = `"https://tilder.thosted.fr"`,
  `lang` = `"en"`, `languages` = `["en", "fr"]`;
- `manual` = `"tilder manual"`;
- `footer`: `TILDER(1)`, with a link to the repository;
- `[languages]` en = "English", fr = "Français";
- `[links] new_tab` = `false`;
- `[collections.docs]` type `doc`, `[collections.showcase]` type
  `showcase`, `[collections.blog]` `post` with its feed;
- `[share]` card lines;
- `[text] commands` = `["curl", "docker", "python3"]`.

`content/site.fr.toml`: every word that differs, and the French `[dates]`.

## 6. Build and serve

`build.sh`:

```sh
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/site" -w /site \
  ghcr.io/thosted/tilder:"$(cat TILDER_VERSION)" --root /site --out /site/public "$@"
```

- `./build.sh --watch` rebuilds on every change.
- The exact entrypoint is settled against the image when the plan is
  written.
- It then runs the theme check (theme spec §10) and fails on any build
  warning.
- `compose.yaml` serves `public/` with Caddy and the `Caddyfile`, for local
  preview and for production. The hosts come from the environment:
  `tilder.thosted.fr`, plus the plain-text host of the Caddyfile contract.

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
  and every CLI option, and fails on a miss. It runs in `build.sh`.

## 9. Done when

- `./build.sh` passes, with no warning and both checks green.
- `curl localhost` through the compose stack returns the landing page's
  text mirror, and a browser returns HTML.
- Every page exists in both languages.
- The kitchen sink passes review in light and dark, on phone and desktop.
