"""Documentation pages: one page of a manual, in order, grouped, with prev/
next links, a sidebar, and a search index per language. A theme type
(tilder docs/types.md)."""

import json
import re

from paths import clean_url
from seo import org_ref, page_heading

NAME = "doc"
ARTICLE = True
SEQUENTIAL = True           # previous/next line in the text mirror
LOCALIZED_OUTPUTS = True    # one search index per language, fr/docs/...
LAYOUT = "doc"
SCRIPT = "search.js"        # pages that list docs; doc.html links it itself
DEFAULTS = {
    "man": "SITE-DOCS(7)",          # items' man-page name, unless one sets its own
    "nav": "docs/",                 # items' nav entry
    "empty": "No page yet.",        # a {docs} list with nothing in it
    "index": "search-index.json",   # the search index, in the collection's folder
    # tilder 1.2: the collection reads its subfolders too, at any depth:
    # content/docs/guide/writing.md is the page docs/guide/writing, in the
    # section guide, whose own page is guide/index.md (docs/guide).
    "recursive": True,
}
TEXT_MAX = 2000                     # characters of body text per page in the index


def defaults(item, conf):
    meta = item["meta"]
    meta.setdefault("man", conf["man"])
    meta.setdefault("nav", conf["nav"])
    meta.setdefault("tagline", "")
    meta.setdefault("description", "")
    # The layout's search field reads it: {{ page.search_index }}.
    meta.setdefault("search_index", f"{conf['dir']}/{conf['index']}")


def order(item):
    value = item["meta"].get("order", "1000")
    try:
        return int(value)
    except ValueError:
        raise ValueError(f'order must be a whole number, not "{value}"') from None


def sort_key(item, conf):
    return (order(item), item["slug"])


def entry(item, link, conf):
    """The card: the title, the group (in a tree of folders, the section:
    by_section), the description. None on the page itself: a
    documentation page shows no card of its own."""
    if not link:
        return None
    meta = item["meta"]
    group = item["section_title"] if "section_title" in item else meta.get("group")
    blocks = [{"k": "para", "text": meta["description"], "cls": []}] if meta.get("description") else []
    return {"k": "entry", "id": None, "cls": ["link"],
            "title": f"[{meta['title']}]({item['path'][:-5]})",
            "meta": [group] if group else [],
            "blocks": blocks, "own": False}


def grouped(items):
    """The items, the ungrouped first, then each group in the order of its
    first item: the sidebar's order ({{ collection_nav }})."""
    loose, named = [], {}
    for it in items:
        g = it["meta"].get("group") or ""
        (named.setdefault(g, []) if g else loose).append(it)
    return loose + [it for its in named.values() for it in its]


def by_section(items):
    """[(item, cls)] for {docs} in a recursive collection: tilder's
    depth-first order kept, each card a copy of its item with its
    section's title (section_title, for entry's meta line), a card whose
    section is not the previous card's marked "group". A section's own page
    (the item whose slug is the section) belongs to it; its title is that
    page's, else the folder's name. A top-level page has none (""), and no
    group either."""
    sections = set()  # every folder holding a page, and the folders above it
    for it in items:
        parts = it.get("section", "").split("/") if it.get("section") else []
        sections.update("/".join(parts[:i + 1]) for i in range(len(parts)))
    titles = {it["slug"]: it["meta"]["title"] for it in items if it["slug"] in sections}
    out, previous = [], None
    for it in items:
        key = it["slug"] if it["slug"] in sections else it.get("section", "")
        card = dict(it, section_title=titles.get(key, key.rpartition("/")[2]) if key else "")
        out.append((card, ["group"] if previous is not None and key != previous else []))
        previous = key
    return out


def docs(items, conf):
    """{docs}: every page, grouped; the first card of a group is marked
    (entry--group) so the theme can space the groups apart. In a tree of
    folders the groups are its sections (by_section), not group:."""
    if any(it.get("section") for it in items):
        return {"items": by_section(items), "empty": conf.get("empty", "")}
    out, seen = [], set()
    for it in grouped(items):
        g = it["meta"].get("group") or ""
        out.append((it, ["group"] if g and g not in seen else []))
        seen.add(g)
    return {"items": out, "empty": conf.get("empty", "")}


MARKERS = {"docs": docs}


def json_ld(item, conf):
    meta = item["meta"]
    return {"@type": "TechArticle", "headline": page_heading(meta),
            "description": meta["description"], "publisher": org_ref()}


# --- the search index ---------------------------------------------------------

FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
# A fence may be indented under an entry (`### Rendered {example}`): the
# closing fence shares the opening one's indent, not necessarily column 0.
FENCE = re.compile(r"^([ \t]*)(`{3,})[^\n]*\n.*?^\1\2`*[ \t]*$", re.S | re.M)
COMMENT = re.compile(r"<!--.*?-->", re.S)
MARKERS_RE = re.compile(r"\s*\{[^}\n]*\}[ \t]*$", re.M)
LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
H2 = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)
# `## Title {text}`: rendered in the text mirror only, never in the HTML
# page (docs/markdown.md); it must not be searchable either.
TEXT_ONLY = re.compile(r"^##[ \t]+[^\n]*\{text\}[^\n]*\n.*?(?=^##[ \t]|\Z)", re.S | re.M)


def strip_text_only(body):
    """A Markdown body with every `{text}`-marked section removed. No
    replacement text: the next heading must stay at column 0 for H2 to
    find it, and `plain`'s whitespace collapses regardless."""
    return TEXT_ONLY.sub("", body)


def headings(src):
    """The ## titles, markers removed, outside code blocks and {text}
    sections."""
    body = strip_text_only(FENCE.sub("", FRONT.sub("", src, count=1)))
    return [MARKERS_RE.sub("", h).strip() for h in H2.findall(body)]


def plain(src):
    """The words of a Markdown source: no front matter, code blocks,
    comments, markers, link targets, {text} sections or punctuation of the
    syntax. The builder's parser is not a type's to import (docs/types.md)."""
    text = strip_text_only(FENCE.sub(" ", FRONT.sub("", src, count=1)))
    text = COMMENT.sub(" ", text)
    text = MARKERS_RE.sub("", text)
    text = LINK.sub(r"\1", text)
    text = re.sub(r"^\s*\[TOC\]\s*$", " ", text, flags=re.M | re.I)
    text = re.sub(r"^[ \t]*(#{2,3}|>|[-*]|\d+[.)])[ \t]+(\[[ xX]\][ \t]+)?", "", text, flags=re.M)
    text = re.sub(r"^[ \t]*\[!\w+\][ \t]*", "", text, flags=re.M)
    text = re.sub(r"^\s*\|?[-:| ]+\|?\s*$", " ", text, flags=re.M)   # table rules
    text = re.sub(r"(\*\*|\+\+|~~|`|\*|\|)", " ", text)
    text = re.sub(r"(?<!\w)_|_(?!\w)", " ", text)
    return " ".join(text.split())


def url(item):
    """The page's clean URL from the language's landing page ("docs/start",
    not "/fr/docs/start"): search.js puts the layout's {{ home }} before it,
    so the links work under any prefix and from any page."""
    return clean_url(item["path"])[len(clean_url("index.html")):]


def record(item):
    src = item["src"].read_text(encoding="utf-8")
    meta = item["meta"]
    return {"t": meta["title"], "u": url(item), "d": meta.get("description", ""),
            "h": headings(src), "x": plain(src)[:TEXT_MAX]}


def outputs(items, conf):
    """The search index of the collection, in the language of the pass:
    {dir}/{index}, under the language's prefix (LOCALIZED_OUTPUTS)."""
    data = [record(it) for it in items]
    return {f"{conf['dir']}/{conf['index']}":
            json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"}
