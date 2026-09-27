---
man: TILDER-SHOWCASE(7)
title: Showcase
description: Sites built with tilder, and how to have yours listed: an issue or a pull request with its address and one line about it.
tagline: sites built with tilder
nav: showcase/
---

## Name

showcase - sites built with tilder

Sites that tilder builds, each with its address, a line about it and,
when it has one, a screenshot. Built one with tilder? It can be listed
here.

## Sites {showcase}

## Be listed

Open an issue or a pull request on
[THOSTED/tilder ↗](https://github.com/THOSTED/tilder) with:

- the site's address;
- one line that says what the site is;
- if you like, a screenshot.

Each site is one entry file, `showcase/<slug>/index.md`, with its
screenshot next to it. The slug is a short name for the site, in lower
case. A pull request adds that folder; an issue gives what goes in it:

```text
---
title: Example site
url: https://example.org/
description: The notes of a small team, in English and French, with a text mirror for terminals.
image: shot.png
order: 10
---

## Name

example - the notes of a small team
```

| Front matter | |
|---|---|
| `title` | the site's name |
| `url` | **required**, the site's address, `https://example.org` |
| `description` | one sentence, the text of the card |
| `image` | optional, a screenshot next to the file (`showcase/<slug>/shot.png`) |
| `order` | optional, a whole number: the place in the list (default 1000, then the slug) |

## See also

- [why tilder](why)
- [the documentation](docs/)
