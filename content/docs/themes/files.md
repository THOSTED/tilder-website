---
title: The files of a theme
description: Every file a tilder theme may provide, what the build does with each one, what it serves, and how assets/ overrides the theme.
order: 10
---

## Name

files - what a theme folder may hold, and what is served

A theme needs `layout.html` and nothing else. Every other file has a job
the build knows, or is copied to the site as it is. The files the build
only reads, the layouts, the types, the configuration, are never served;
and a file of the same name in the site's `assets/` wins over the theme's.

[TOC]

## The files

| File | | Used for |
|---|---|---|
| `layout.html` | required | the page around the content, filled with placeholders ([layouts](docs/themes/layouts)) |
| `style.css` | expected | copied to the site root; the layout links it. It styles the classes the build writes ([classes](docs/themes/classes)) |
| `code.js` | optional | a copy button on code blocks, loaded only on pages that have code ([scripts](docs/themes/scripts)) |
| `members.js` | optional | search and filter on a `{members}` list, loaded only there |
| `fonts/` | optional | web fonts; its `*.woff2` files also draw the text of `share.png` |
| `icons/<network>.svg` | optional | the logo of a member's profile link; without it, the network's name is shown |
| `share.svg` | optional | the link preview, drawn to `share.png` (1200x630); without it, `og:image` is the icon |
| `layouts/<name>.html` | optional | a layout for the pages of a type, or asked for by `layout:` in a page's front matter; the same placeholders as `layout.html` |
| `types/<name>.py` | optional | a content type the theme adds, or a built-in one it replaces ([custom types](docs/content-types/custom-types)) |
| `theme.toml` | optional | the theme's configuration values, under the site's `site.toml`: the `[share]` colours, the theme's own words, and `[check]` for `build.py --check` |
| `theme.<lang>.toml` | optional | the per-language twin of `theme.toml`, between it and the site's `site.toml` |

Any other file, a second script, an image the stylesheet uses, a
`.well-known/` folder, is copied to the site root at the same path.

## What is served

Everything in `theme/` is copied to the root of the site as it is, but:

- what the build reads: `layout.html`, `layouts/`, `share.svg`, `icons/`,
  `types/`, `theme.toml` and every `theme.<lang>.toml`;
- what belongs to the theme's own repository rather than to the site:
  `.git`, and every file or folder whose name starts with `.git`
  (`.gitignore`, `.gitmodules`), at any depth; a `README.md`, and any file
  whose name starts with `LICENSE`, at the top of the folder.

So `theme/style.css` is served at `/style.css`, `theme/fonts/mono.woff2`
at `/fonts/mono.woff2`, and the layout, which the build has already
turned into pages, is not served at all. The layout links these files
through `{{ root }}`, the relative path to the site root
([placeholders](docs/themes/layouts)).

`assets/` follows the same rules. The [project](docs/guide/project) page
shows them for the three folders of a site.

## assets/ wins over theme/

For every theme file the build reads or serves, it looks in `assets/`
first, then in `theme/`. A site can so replace one file of a theme it did
not write, without touching the theme:

| The site adds | It replaces |
|---|---|
| `assets/style.css` | `theme/style.css` |
| `assets/layout.html` | `theme/layout.html` |
| `assets/layouts/doc.html` | the theme's `layouts/doc.html` |
| `assets/share.svg` | the theme's link preview |
| `assets/icons/github.svg` | the theme's logo for that network |
| `assets/code.js` | the theme's copy button |

Three exceptions: content types are read from `theme/types/` only, the
fonts that draw `share.png` from `theme/fonts/` only, and the
configuration from `theme/theme.toml`; a site changes the configuration in
its own `site.toml` instead.

## theme.toml

The theme's layer of the configuration, merged over tilder's
`defaults.toml` and under the site's `site.toml`: tables key by key, so a
site overrides one value and keeps the others. It holds what the theme
needs a value for:

- `[share]`: the colours of the link preview and of the browser's
  interface (`theme_color`, `background_color`...), documented in the
  [configuration reference](docs/reference/configuration);
- the theme's own words, in tables of its own, which its layouts read
  through placeholders (`{{ search.label }}`);
- `[check]`: what `build.py --check` checks ([checking a
  theme](docs/themes/checking)).

```toml
# theme/theme.toml
[search]
label = "Search the documentation"
none = "No page matches."

[share]
theme_color = "#2e6b34"
background_color = "#f7f8f3"
```

A layout that reads `{{ search.label }}` needs the key to exist: a
placeholder naming a key that no layer sets stops the build. The theme's
`theme.toml` is the place to give every key it uses a value.

### theme.<lang>.toml

  One file per language the theme speaks: `theme.fr.toml` holds the French
  of the theme's words. It is ignored when the site does not declare that
  language, so a theme may ship languages a site lacks
  ([languages](docs/guide/languages)). It comes between `theme.toml` and
  the site's files, in this order, the last winning:

```text
defaults.toml
  < theme/theme.toml < theme/theme.fr.toml
  < content/site.toml < content/site.fr.toml
```

## share.svg and the fonts

`share.svg` is the template of the link preview: the build fills it and
draws it to `share.png`, 1200 by 630 pixels, the image social networks
show next to a link. Its placeholders are `{{ logo }}` (the site's
`assets/logo.svg`, as a `data:` URL), `{{ manual_upper }}`, `{{ wordmark }}`,
`{{ domain }}`, `{{ card_1 }}`, `{{ card_2 }}` and any `site.toml` value
(`{{ site.name }}`), XML-escaped. The
[feeds and images reference](docs/reference/feeds-and-images) describes
them, and the tools that draw the image.

The text of `share.png` is drawn with the theme's own fonts: every
`fonts/*.woff2`, converted for the renderer when `woff2_decompress` is
installed (the Docker image has it). Without it, the renderer falls back
to the fonts of the system.

## icons/

`icons/<network>.svg` is the logo of a member's profile link, for the
networks a member page may list: `linkedin`, `github`, `gitlab`,
`mastodon`, `bluesky`, `website`. The build inlines it in the page as an
`<svg class="icon">`, hidden from screen readers (the link keeps the
network's name as text for them). It keeps the file's `viewBox` and the
`d` of its `<path>` elements, nothing else: an icon is paths, it must
have a `viewBox`, and the theme colours it (`.icon { fill: currentColor;
}` draws it in the text colour). Without the file, the link shows the
network's name.

## See also

- [layouts and placeholders](docs/themes/layouts)
- [the project](docs/guide/project)
- [members](docs/content-types/member)
