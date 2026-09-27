---
title: The text mirror
description: Every page as text: 75 columns, folded to ASCII, plain in txt/ and coloured in ansi/, with framed code, boxed callouts and the plain-text host.
order: 30
---

## Name

text-mirror - every page as text, for terminals

Every page tilder builds comes out twice: as HTML for browsers, and as
text for terminals, from the same source, so the two cannot drift apart.
The text is 75 columns wide and folded to ASCII. It is written twice
too: plain in `txt/`, and coloured with ANSI escape sequences in `ansi/`.
A terminal that asks the site for a page gets the coloured one.

[TOC]

## Where it is

Each page's text sits under `txt/` and `ansi/`, at the page's address
with `.txt`. A folder's page is named after the folder.

| Page | Plain | Coloured |
|---|---|---|
| `index.html` | `txt/index.txt` | `ansi/index.txt` |
| `about.html` | `txt/about.txt` | `ansi/about.txt` |
| `blog/index.html` | `txt/blog.txt` | `ansi/blog.txt` |
| `blog/2026-01-01-hello.html` | `txt/blog/2026-01-01-hello.txt` | `ansi/blog/2026-01-01-hello.txt` |
| `fr/about.html` | `txt/fr/about.txt` | `ansi/fr/about.txt` |

Served by the example Caddyfile, `curl example.org/about` returns
`ansi/about.txt`, with a 200 and no redirect; `?plain` returns
`txt/about.txt` instead, to save or pipe; and the plain-text host serves
`txt/` to every client, at the same paths
([deployment](docs/guide/deployment)). The files are also there to read
from the disk:

```sh
less -R public/ansi/about.txt
curl example.org/about
curl "example.org/about?plain" > about.txt
```

`robots.txt` keeps search engines out of `/txt/` and `/ansi/`, and
`txt/robots.txt` out of the whole plain-text host: the text duplicates
the pages ([SEO](docs/reference/seo)).

## The page as text

The text follows the page's sections, in the manner of a man page
(shortened here: the real rules are 75 columns wide):

```text
MYSITE(1)                 My Site Manual                 MYSITE(1)

LANGUAGES: en fr

NAME
     about - who we are

     A paragraph, wrapped at 75 columns, indented five spaces.

SEE ALSO
     ...

previous: Getting started                         next: Deployment

MYSITE                    2026-01-01                     MYSITE(1)
```

- The header rule: the page's `man:` on both sides, `site.manual` in the
  middle.
- On a site with several languages, a `LANGUAGES:` line lists them.
- Each `##` section: its title in capitals at the first column, its body
  indented five spaces.
- Before the footer, the line of a sequential collection's neighbours,
  from `labels.prev` and `labels.next` ([navigation](docs/content-types/navigation)).
- The footer rule: `footer.left`, `site.updated`, `footer.right`
  ([configuration](docs/reference/configuration)).

What is left out: anything before the first `##`, a section marked
`{html}`, and a comment block. A section marked `{text}` appears only
here, not on the page ([sections](docs/reference/markdown/sections)).
Trailing spaces are dropped, and never more than one blank line follows
another.

## 75 columns

Every line fits in 75 columns: an 80-column terminal, the default since
the VT100, with room left for a scrollbar, the gutter of `less` or a
diff, or the `>` of a quoted email. Paragraphs are wrapped on spaces,
greedily. A word is never cut, a URL or a command neither, so a single
word longer than the line is the one thing that can pass the edge.

## ASCII

`txt/` is ASCII: the source keeps its accents and typography, the mirror
folds them. First these characters are replaced:

| Character | Becomes |
|---|---|
| em dash, en dash | `-` |
| curly single quotes | `'` |
| curly double quotes, guillemets | `"` |
| middle dot | `-` |
| ellipsis | `...` |
| right arrow | `->` |
| north-east arrow, U+2197 | nothing |
| the ligatures of o and e, a and e, in either case | `oe`, `OE`, `ae`, `AE` |
| no-break space, narrow no-break space | a space |
| multiplication sign | `x` |

Then every letter loses its accents and other marks: an e with an acute
accent becomes e, a c with a cedilla becomes c. In prose,
runs of spaces become one; in code, spacing is kept exactly. A character
that is neither in the table nor an accented letter, an emoji or another
arrow, is not folded: it passes into `txt/` as it is, so keep such
characters out of text meant for the mirror.

## Blocks as text

| Block | In the text mirror |
|---|---|
| paragraph | wrapped; its classes, `{small muted}`, affect the page only |
| list | `- item`, `1. item`, `- [x] item`, `- [ ] item`; wrapped lines and nested lists align under the item's text |
| quote | indented two more spaces |
| callout | a box, its label in the top rule: `+- WARNING ---+`, from `labels.info`, `labels.warning` or `labels.error` |
| code block | framed by two rules, see below |
| table | padded columns, like `column -t`; if they do not fit in 75 columns, one record per row, a `Header: value` line per cell |
| horizontal rule | a line of dashes |
| image | `[ image ] alt text`, from `labels.image`, then the caption, then the file's path from the site root |
| `[TOC]` | `labels.toc` in capitals, then the numbered section titles |
| entry | its title, the first tag right-aligned on the same line, `[ tag ]`; the meta line below it, a date in words only; its body indented four more spaces |

Inline: a link keeps its label, and an external one adds its address in
parentheses, `archive (https://example.org/)`; an internal address is
left out, since a terminal visits it with `curl` rather than copying it.
Bold and italic are plain text; struck text keeps its `~~` marks, since
dropping them would change the sense. The full dialect, block by block,
is in [the Markdown reference](docs/reference/markdown).

## Code frames

A code block is framed by two rules that say which end is which: the top
one opens with `.`, carries the language and closes with `.`; the bottom
one opens and closes with `'`. The code is indented inside, with nothing
added to its own lines, so it copies clean from a terminal. Shortened:

```text
.-- sh ------------------------------.
  curl example.org/about
'------------------------------------'
```

The code keeps its spacing exactly; a tab moves to the next tab stop,
every four columns. A line past
the 75th column is cut and continued on the next line, indented two
spaces, the cut marked with `\`: a shell reads it as a continuation.

## Colours

`ansi/` is the same text with ANSI escape sequences: eight colours, or a
256-colour accent the site chose (`text.accent`), never a background, so
it reads on light and dark terminals alike. Colour follows the markup,
never a guess from the words: the build marks inline code, list markers,
code-block lines and, in a highlighted code block, each token, where it
renders them, and colours exactly those, across line breaks.

| What | Colour |
|---|---|
| the header and footer rules | dim |
| a section's title, when it holds only letters, digits, spaces and `-()'` | bold |
| the page's name, on the first line of the first section | bold |
| inline `code` | the accent, as far as its backquotes go |
| list markers | the accent |
| URLs | the accent, underlined |
| `[ tags ]` | bold, in the accent |
| a code block's rules | dim |
| a command line in a code block with no language, or in `text` | the accent |
| an information callout's box and label | the accent, the label bold |
| a warning callout | yellow |
| an error callout | red |

The accent is `text.accent`: `"cyan"` by default, or any of the eight
colour names or a 256-colour index from 16 to 255, such as `208` for
orange, set in `site.toml` (a `site.<lang>.toml` may set its own)
([configuration](docs/reference/configuration)). A URL's or a command
line's closing punctuation - a final `.,;:!?`, a quote left unpaired, a
bracket never opened - is left uncoloured: in a sentence such as (see
https://example.org/a_(b)), only the address is coloured, not the `).`
that ends it.

A command line is a code-block line that starts with one of the words of
`text.commands`, alone or after a prompt, `$` or `#` and a space; by default only
`curl`. A site adds its own:

```toml
[text]
commands = ["curl", "docker", "python3"]
```

Callouts are recognised by the label in their top rule, so the colours
follow `labels.info`, `labels.warning` and `labels.error` in every
language. Remove the escape sequences from a file of `ansi/`, and what
is left is its twin in `txt/`, byte for byte. `txt/` has no escape
sequence at all: it survives `curl > file`.

## Highlighted code blocks

A code block in a language `highlight.py` knows is highlighted in
`ansi/` too, each token in its kind's colour, by the same rules as the
HTML page: `ansi/` never disagrees with what a browser shows. Colour
only, never a character added: the spaces around a token are left
uncoloured, and stripped of its escapes, the block is the one of `txt/`.
A line cut at the 75th column keeps its colours on the next line.

| Token | Colour |
|---|---|
| keyword; in `sh` and `console`, the command word; in `markdown`, `[!INFO]` and the like, `[TOC]` | bold, in the accent |
| builtin or type; in `sh` and `console`, an option (`-s`, `--out`); in `markdown`, a list marker, a task box, emphasis | the accent |
| string, a `diff` `+` line; in `markdown`, inline `code`, a link's title | green |
| comment, a `console` prompt (`$ `, `# `); in `markdown`, a fence line, a rule, a table's pipes, the `>` of an inset, the front matter's `---` | dim |
| number, variable; in `markdown`, a link's target, the `{markers}` ending a line | magenta |
| tag, key, section, a `diff` hunk header (`@@`); in `markdown`, a heading, a front matter key | bold |
| a `diff` `-` line | red |

The command word is the first word of a command: at the start of a
line (after a `$ ` prompt in `console`), after `|`, `||`, `&&`, `;`,
`&`, `(`, `$(`, after a prefix such as `sudo` or `env`, and after a
variable assignment.

The languages highlighted are `sh`, `python`, `js`, `c`, `go`, `rust`,
`sql`, `json`, `jsonc`, `yaml`, `kyaml`, `ini`, `conf`, `dockerfile`,
`html`, `css` and `make`, each by its own token rules, plus `console`,
`diff` and `markdown`, coloured line by line; the full list of names
and their aliases is in [code
blocks](docs/reference/markdown/blocks). A block with no language, in
`text`, or in a language tilder does not know is not highlighted: only
its command lines (`text.commands`) are in the accent, and `txt/` stays
plain either way.

## Leaving a page out

`text: no` in a page's front matter writes no text for it, in `txt/` or
in `ansi/`. The starter's 404 page does it: a terminal gets a short
message from the server instead ([writing pages](docs/guide/writing),
[deployment](docs/guide/deployment)).

```markdown
---
title: 404
description: Page not found.
text: no
robots: noindex
---
```

## See also

- [deployment](docs/guide/deployment)
- [the Markdown reference](docs/reference/markdown)
- [configuration](docs/reference/configuration)
