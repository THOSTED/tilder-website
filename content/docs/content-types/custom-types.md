---
title: Types of your own
description: Write a content type in Python in theme/types/: its attributes, its functions, the item, the entry node, markers, imports and errors, with an example.
order: 50
---

## Name

custom types - a content type of your own, in Python

A theme adds a type with one Python module in `theme/types/`, written
exactly as the four built-in types are: a name, a few attributes, and
functions that turn an item into a card, structured data, a feed item or
files of its own. A type never writes HTML. It returns nodes that the
builder renders twice, as HTML and as text, so a new type is right in the
text mirror without any work. This page is the whole contract, then a
complete example, a `recipe` type.

[TOC]

## The module

The builder loads `types/*.py` from tilder first, then
`theme/types/*.py` from the theme. A file whose name starts with `_` is
not loaded. A theme module with the same `NAME` as a built-in type
replaces it; two modules of one folder cannot share a name. A collection
uses a type by its name, `type = "recipe"`.

Only `NAME` and the function `entry` are required. Everything else has a
default:

| Attribute | Default | Meaning |
|---|---|---|
| `NAME` | required | the name `type =` refers to: a string, a valid Python identifier |
| `DATED` | `False` | items are named `YYYY-MM-DD-slug`, and `item["date"]` holds the date |
| `ARTICLE` | `False` | the page's body is wrapped in `<article>` |
| `OG_TYPE` | `"website"` | the page's `og:type`; the `post` type sets `"article"` |
| `LAYOUT` | the `NAME` | the item pages use `theme/layouts/<LAYOUT>.html` if the theme has it, else `layout.html` |
| `SCRIPT` | `""` | a theme script loaded on the pages that list the type, if the theme ships it: `"members.js"` |
| `DEFAULTS` | `{}` | the type's settings and words, English and neutral; a collection overrides any of them |
| `MARKERS` | `{}` | the section markers that list the type: `{"word": function}` |
| `SEQUENTIAL` | `False` | the text mirror of an item gets a `previous: ... next: ...` line before its footer ([navigation](docs/content-types/navigation)) |
| `LOCALIZED_OUTPUTS` | `False` | `outputs()` is called in every language, its files put under the language's prefix, `fr/`; else once, in the default language |

A value of the wrong kind, such as a `DATED` that is not a `bool`, stops
the build.
The settings a collection receives are the type's `DEFAULTS` with
`[collections.<name>]` over them, plus `type` and `dir`.

## The functions

`item` is the dictionary below, `conf` the collection's settings, `link`
a boolean. Only `entry` is required.

```python
def defaults(item, conf): ...
def sort_key(item, conf): ...
def entry(item, link, conf): ...
def json_ld(item, conf): ...
def meta_tags(item, conf): ...
def feed_item(item, conf): ...
def outputs(items, conf): ...
def list_data(conf): ...
```

| Function | Returns | Left out |
|---|---|---|
| `defaults` | nothing: it fills what the front matter left out | nothing is filled |
| `sort_key` | the item's key in the collection's order | the slug |
| `entry` | the card, an entry node, or `None` for no card | required |
| `json_ld` | the page's schema.org node, a `dict`, or `None` | a `WebPage` node |
| `meta_tags` | extra `<meta>` tags, a list of `("name", key, value)` and `("property", key, value)` | none |
| `feed_item` | `{"title", "link", "description", "date"}`, or `None` to leave the item out | no RSS feed |
| `outputs` | extra files, `{"path": text}` | none |
| `list_data` | `{key: value}`, the `data-*` attributes of a section that lists the type | none |

- `defaults` runs on every item once its file is read, before anything
  else: it changes `item["meta"]` in place. The built-in types fill
  `man` and `nav` from `conf` there.
- `sort_key` orders the collection: the lists, the feed, the sidebar and
  the neighbours start from it. Lists may reverse it, as `{posts}` does.
- `entry` is called with `link` true for a card in a list, and false for
  the card at the end of the first section of the item's own page.
- `json_ld` returns the page's own node; the builder adds its `@id`,
  `url` and `inLanguage`, and places it in the graph with the site's
  `Organization` and `WebSite` ([SEO](docs/reference/seo)).
- `feed_item` makes the collection's RSS possible: without it, a `feed`
  setting writes nothing. `date` is an ISO date, so a type with a feed is
  usually `DATED`.
- `outputs` receives every item of the collection and returns files to
  write, by their path from the site root: the event type's iCalendar,
  this site's search index. It runs only when the collection's folder
  exists.

## The item

What `defaults`, `entry` and the others receive:

```python
{"slug": "2099-03-01-first-talk",
 "date": "2099-03-01",
 "meta": {...},
 "src": Path("content/talks/2099-03-01-first-talk.md"),
 "path": "talks/2099-03-01-first-talk.html",
 "collection": "talks",
 "conf": {...},
 "type": <the module>,
 "lang": "en",
 "content_lang": "en",
 "section": ""}
```

| Key | Meaning |
|---|---|
| `slug` | the file's name without `.md`, or the item's folder's name |
| `date` | the date of a `DATED` item, `YYYY-MM-DD`; else `None` |
| `meta` | the front matter, after `defaults()` |
| `src` | the Markdown file read, a `Path` |
| `path` | the page's file from the site root |
| `collection`, `conf`, `type` | the collection's name, its settings, the type's module |
| `lang` | the language being built |
| `content_lang` | the language of the file read, which differs when a page is not translated yet |
| `section` | tilder 1.2: the folder of an item of a recursive collection |

Front-matter values are strings, as written: `meta["serves"]` is `"4"`,
not a number. `item["path"][:-5]`, the path without `.html`, is the link
target of the item's page.

<!-- 1.2 -->

In a recursive collection (tilder 1.2), the slug carries the folders,
`guide/writing`, and `section` holds the folder part, `guide`; it is
`""` at the top, and in every collection that is not recursive.

## The entry node

What `entry` returns, a card:

```python
{"k": "entry", "id": None,
 "title": "[First talk](talks/2099-03-01-first-talk)",
 "meta": ["2099-03-01 | Sunday 1 March 2099",
          "Auditorium", "`upcoming`"],
 "cls": ["link"],
 "blocks": [{"k": "para", "text": "One sentence.", "cls": []}],
 "own": False,
 "data": {"category": "admin"}}
```

| Key | Meaning |
|---|---|
| `title` | inline Markdown: a link to the item in a list, its bare title on its own page |
| `meta` | the card's line, one string per part (below) |
| `cls` | the card's classes, each written `entry--<cls>`: `link` makes the card clickable as a whole |
| `blocks` | what follows the line, as block nodes |
| `own` | true on the item's own page: no `<h3>`, since the page's `<h1>` is the title |
| `data` | optional: `data-*` attributes of the card |

Each part of `meta` is one of three things. A date and its words
joined by a bar, `"2099-03-01 | Sunday 1 March 2099"`, becomes a
`<time>`, and the text mirror keeps the words. A string that opens and
closes with a backtick becomes a tag (`.tag`), which the text mirror sets
at the right edge. Anything else is plain text.

The blocks a card may hold are those of the Markdown dialect: `para`,
`empty`, `list`, `code`, `table`, `image` and `profiles`. A new kind of
block is a new construct of the dialect, added to the builder with both
its renderings. The three that types build most often:

```python
{"k": "para", "text": "One sentence.", "cls": [],
 "txt": "Its wording in the text mirror."}   # txt: optional
{"k": "image", "src": "recipes/soup/bowl.png",
 "alt": "A bowl of soup", "caption": ""}     # src: from content/
{"k": "profiles", "items": [(key, label, url)]}
```

## Markers

`MARKERS` maps a word to a function. A section whose heading ends with
`{word}` or `{word:collection}` calls it with the collection's items, in
order, and its settings:

```python
def recipes(items, conf):
    return {"items": [(it, []) for it in items],
            "empty": conf.get("empty", ""),
            "cls": ["grid"]}
```

- `items` are the items to show, in order, each with a list of extra
  classes for its card; `empty` is the text of a list with nothing in
  it; `cls`, optional, adds classes to the section's body.
- An extra card class of an item, `["next"]`, is added to its card's
  classes: `.entry--next`, and `.tag--next` on its tag, as `{upcoming}`
  does for the nearest event.
- A marker word belongs to one type. A word two types claim stops the
  build; a theme that wants the word replaces the type that owns it.
- The section also gets the word as a class, the type's `SCRIPT` if the
  theme has it, and the `data-*` attributes of `list_data`.

## What a type may import

A type imports what it needs from these, and from nothing else of the
builder: the rest may change in any version.

| Module | Names |
|---|---|
| `config` | `CFG` (the merged configuration), `STATE["today"]` (the build's date, ISO), `apex` (the site's address) |
| `dates` | `human_date`, a date in the words of `[dates]` |
| `paths` | `clean_url`, a page's address without `.html` |
| `fold` | `to_ascii` |
| `seo` | `page_heading`, `page_title`, `share_image`, `org_ref`, `site_ref` |
| `feeds` | `calendar`, the iCalendar of a list of events |
| `contenttypes` | `TYPES`: the built-in types, loaded first, to build on one |

The standard library of Python is available too. A type that extends
another starts from its module:

```python
from contenttypes import TYPES

event = TYPES["event"]

NAME = "talk"
DATED = True
ARTICLE = True
DEFAULTS = {**event.DEFAULTS, "man": "SITE-TALKS(7)",
            "nav": "talks"}
MARKERS = {"talks": event.MARKERS["upcoming"]}
defaults = event.defaults
entry = event.entry
```

## Errors

The builder checks every module and every collection before building,
and reports every problem it finds before it stops: a missing `NAME` or
`entry`, an attribute of the wrong kind, a function that is not callable,
a marker word claimed twice, a module that cannot be imported, a
collection whose `type` no module defines, two collections on one folder.

```text
error: theme/types/talk.py: MARKERS["upcoming"] is already claimed by type "event" (types/event.py). Rename the marker, or replace that type by naming yours "event"
```

An exception raised in a type's function stops the build too, at the
file being built, naming the module and the function:

```text
error: content/talks/2099-03-01-first-talk.md: theme/types/talk.py: entry() failed: KeyError: 'speaker'. Run with --debug for the traceback
```

`--debug` prints the Python traceback of the failure. In watch mode, a
change under `theme/types/` restarts the builder, which loads the modules
again ([the command line](docs/reference/cli)). A type is code that runs
at every build: review a theme's types before you use it.

## A worked example

A `recipe` type: a page per recipe, a grid of cards that say how long
each one takes and how many it serves, sorted by title, and a `Recipe`
node for search engines. The collection, in `content/site.toml`:

```toml
[collections.recipes]       # content/recipes/, {recipes}
type = "recipe"
serves = "for {}"
```

The module, `theme/types/recipe.py`:

```python
"""Recipes: a page each, a grid of cards, the time they take."""

from fold import to_ascii
from seo import org_ref, page_heading

NAME = "recipe"
DEFAULTS = {
    "man": "SITE-RECIPES(7)",   # the items' man-page name
    "nav": "recipes/",          # the items' nav entry
    "empty": "No recipe yet.",  # a {recipes} list, empty
    "minutes": "{} min",        # the time, on a card
    "serves": "serves {}",      # the servings, on a card
}


def defaults(item, conf):
    meta = item["meta"]
    meta.setdefault("man", conf["man"])
    meta.setdefault("nav", conf["nav"])
    meta.setdefault("description", "")
    if meta.get("minutes"):
        time = conf["minutes"].format(meta["minutes"])
        meta.setdefault("tagline", time)


def sort_key(item, conf):
    """By title, accents and case ignored."""
    title = to_ascii(item["meta"].get("title", "")).lower()
    return (title, item["slug"])


def entry(item, link, conf):
    """The card: time, servings, a tag; the description."""
    meta = item["meta"]
    line = []
    if meta.get("minutes"):
        line.append(conf["minutes"].format(meta["minutes"]))
    if meta.get("serves"):
        line.append(conf["serves"].format(meta["serves"]))
    if meta.get("veggie") == "yes":
        line.append("`veggie`")
    blocks = []
    if link and meta.get("description"):
        blocks.append({"k": "para", "text": meta["description"],
                       "cls": []})
    title = meta["title"]
    if link:
        title = f"[{title}]({item['path'][:-5]})"
    return {"k": "entry", "id": None, "title": title,
            "meta": line, "blocks": blocks, "own": not link,
            "cls": ["link"] if link else []}


def recipes(items, conf):
    """{recipes}: every recipe, in order, as a grid."""
    return {"items": [(it, []) for it in items],
            "empty": conf.get("empty", ""), "cls": ["grid"]}


MARKERS = {"recipes": recipes}


def json_ld(item, conf):
    meta = item["meta"]
    node = {"@type": "Recipe", "name": page_heading(meta),
            "description": meta["description"],
            "author": org_ref()}
    if meta.get("minutes"):
        node["totalTime"] = f"PT{meta['minutes']}M"
    if meta.get("serves"):
        node["recipeYield"] = meta["serves"]
    return node
```

The collection's page, `content/recipes/index.md`, and a recipe,
`content/recipes/leek-soup.md`:

```text
---
man: SITE-RECIPES(7)
title: Recipes
description: Every recipe of the site, by title, with its time.
tagline: what we cook
nav: recipes/
---

## Name

recipes - what we cook

## Recipes {recipes}
```

```text
---
title: Leek soup
description: A leek and potato soup, for a cold winter evening.
minutes: 40
serves: 4
veggie: yes
---

## Name

leek soup - for a cold evening

## Ingredients

- 3 leeks
- 2 potatoes
```

The build names the new type and its collection, and `/recipes` reads,
in a terminal:

```text
types: event, member, page, post; from theme: recipe
collections: blog (post, no folder), events (event, no folder), members (member, no folder), recipes (recipe, 1 item)
```

```text
RECIPES
     Leek soup                                                   [ veggie ]
     40 min
     for 4

         A leek and potato soup, for a cold winter evening.
```

The page of the soup ends its first section with the same card, without
the link, and carries a `Recipe` node with `"totalTime":"PT40M"` and
`"recipeYield":"4"`. The words are the collection's: `serves = "for {}"`
replaced the type's `"serves {}"`, and a `site.fr.toml` would give them in
French.

## See also

- [collections](docs/content-types)
- [navigation](docs/content-types/navigation)
- [layouts](docs/themes/layouts)
- [scripts](docs/themes/scripts)
