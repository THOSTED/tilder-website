---
title: member
description: The member type: one page per person, a searchable grid by {members}, categories, pronouns, public profiles with their logos, and members.js.
order: 40
---

## Name

member - people, one page each, in a searchable grid

A member is a person described once, in the front matter of one file, in
a collection of type `member`: the people of a group, a team, a list of
mentors. Each gets a page and a card with their names, pronouns,
affiliation and public profiles; a section marked `{members}` shows them
all as a grid that the theme's `members.js` can search and filter.

[TOC]

## Settings

A `member` collection may set these keys under `[collections.<name>]`;
each has its default in the type's module, `types/member.py`.

| Key | Default | Meaning |
|---|---|---|
| `member.man` | `"SITE-MEMBERS(7)"` | the man-page name of its items, unless one sets its own |
| `member.nav` | `"members"` | the `[[nav]]` entry its items mark as current |
| `member.categories` | `["admin", "member"]` | the categories, in the order of the grid and of the filter's buttons |
| `member.default_category` | `"member"` | a member's category when the front matter sets none |
| `member.empty` | `"No member listed yet."` | the text of a `{members}` list with nothing in it |
| `member.search_label` | `"search"` | the label of the search field |
| `member.search_placeholder` | `"first or last name"` | the placeholder of the search field |
| `member.all` | `"all"` | the filter's button that shows every category |
| `member.one` | `"entry"` | the count's noun, for one |
| `member.many` | `"entries"` | the count's noun, for several |
| `member.none` | `"No entry matches."` | what a search that finds nothing says |
| `member.full` | `"full"` | said on the card of a member whose capacity is reached |

The six words from `search_label` to `none` are for `members.js`, which
holds no text of its own. `defaults.toml` already declares
`[collections.members]`, on `content/members/`; a site with mentors
adds its category and its words:

```toml
[collections.members]
type = "member"
categories = ["admin", "mentor", "member"]
search_placeholder = "name"
```

## A file per member

A member is `content/members/<slug>.md`, or a folder with its `index.md`.
The type is not dated: any slug will do, `jane-doe.md`. Start from a
`_template.md` in the folder that lists every field; its name keeps it
from being built.

## Front matter

```text
---
title: Jane Doe
description: Jane Doe, who runs the project and answers its mail.
tagline: admin
first_name: Jane
last_name: Doe
pronouns: she/her
category: admin
affiliation: Example Corp
website: https://jane.example
mastodon: https://social.example/@jane
---
```

| Key | Meaning |
|---|---|
| `first_name`, `last_name` | the person's names; `last_name` sorts the grid |
| `display_name` | the name to show when it is not first and last name: a chosen name, a pseudonym, a single name. When set, it is the only name shown; the others stay searchable |
| `pronouns` | as the person writes them (`she/her`, `they/them`, `iel`); ask, never guess, and leave it out if they prefer |
| `category` | one of the collection's `categories`; default `default_category`. The card's tag, and the filter's |
| `affiliation` | a company, a school or a project, if they want one shown |
| `capacity` | a note on what they can still take on, `2 per term`, for a category that tracks one, such as mentors |
| `full` | `yes` when that capacity is reached: the tag turns to the warning colour and `full` is said in words |
| `linkedin`, `github`, `gitlab`, `mastodon`, `bluesky`, `website` | the addresses of public profiles (below) |
| `man`, `nav` | default: the collection's `man` and `nav` |

Leave empty what does not apply: an empty field shows nothing. There is
deliberately no field for gender, age or a photo. `title` and
`description` are the page's own, as on every page; the card shows the
member's name, not the title.

## The grid

A section marked `{members}` lists every member of the collection as a
grid (`.grid`), in this order: by category, in the order of
`categories` (a category not listed there comes after them); then by last
name, accents and case ignored; then by file name.

```text
## Members {members}
```

Each card shows the name (`display_name`, else first and last name), a
line with the pronouns, the affiliation, the capacity and, when `full`,
the word `full`, the category as a tag, and the profile links. In the
grid the name links to the member's page; on that page the same card,
without the link, closes the first section.

## Profiles

Six keys hold public profiles, shown in this order: `linkedin`, `github`,
`gitlab`, `mastodon`, `bluesky`, `website`. Each holds an address, or
several separated by spaces, a personal and a work account; each is then
named with the last part of its address, `GitHub (jane)`.

- **Logos.** A link shows the theme's `theme/icons/<network>.svg`,
  `icons/github.svg` for `github`, inlined in the page (its paths only,
  classed `.icon`, for the theme to colour) and hidden from screen
  readers, which hear the network's name instead. Without the icon, the
  link shows the name followed by `↗`. `website` is named by
  `labels.website`, `"website"` by default
  ([configuration](docs/reference/configuration)).
- **Verification.** Every link has `rel="me"`, which lets a profile that
  links back to the page verify it, and the addresses are the `sameAs`
  of the member's structured data.
- **Text mirror.** Each profile is a line, `GitHub: <address>`.

## Search and filter

A page with a `{members}` section loads the theme's `members.js`, if the
theme ships one: the type names it in its `SCRIPT`. The script is the
theme's own; the one tilder describes adds a search field (first, last
and display name, accents and case ignored, every word must match) and
one button per category. Without JavaScript, the whole grid is simply
shown ([scripts](docs/themes/scripts)).

It finds what it needs in the page. Each card carries
`data-category` and `data-search` (the member's names, in lower-case
ASCII), and the section carries the collection's six words as
`data-search_label`, `data-search_placeholder`, `data-all`, `data-one`,
`data-many` and `data-none`, so the script speaks the page's language.

## Search engines

A member's page is a `ProfilePage` whose `mainEntity` is a `Person`: the
member's name, the site's organisation as `memberOf`, the profiles as
`sameAs`, and the `affiliation` as an `Organization`. A member collection
has no RSS feed: the type gives no feed items.

## See also

- [collections](docs/content-types)
- [scripts](docs/themes/scripts)
- [the files of a theme](docs/themes/files)
