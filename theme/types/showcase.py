"""Showcase: sites built with the documented project, one item each, with
an optional screenshot next to it. A theme type (tilder docs/types.md)."""

from seo import page_title, site_ref

NAME = "showcase"
DEFAULTS = {
    "man": "SITE-SHOWCASE(7)",      # items' man-page name, unless one sets its own
    "nav": "showcase/",             # items' nav entry
    "empty": "No site listed yet.", # a {showcase} list with nothing in it
    "visit": "visit ↗",             # the link to the site, on its page
}


def defaults(item, conf):
    meta = item["meta"]
    url = meta.get("url", "")
    if not url.startswith(("https://", "http://")):
        raise ValueError(f'url must be the site\'s address, https://..., not "{url}"')
    if meta.get("image") and not (item["src"].parent / meta["image"]).is_file():
        raise ValueError(f'image "{meta["image"]}" is not next to {item["src"].name}')
    meta.setdefault("man", conf["man"])
    meta.setdefault("nav", conf["nav"])
    meta.setdefault("tagline", url.split("://", 1)[1].rstrip("/"))
    meta.setdefault("description", "")


def sort_key(item, conf):
    value = item["meta"].get("order", "1000")
    try:
        return (int(value), item["slug"])
    except ValueError:
        raise ValueError(f'order must be a whole number, not "{value}"') from None


def image_src(item):
    """The screenshot's path from content/, like the builder's own images:
    next to the item's file (showcase/<slug>/shot.png, or showcase/shot.png
    for a flat showcase/<slug>.md)."""
    folder = item["path"][:-5] if item["src"].stem.split(".")[0] == "index" \
        else item["path"].rsplit("/", 1)[0]
    return f"{folder}/{item['meta']['image']}"


def entry(item, link, conf):
    """The card: the title, the address, the description, the screenshot.
    On its own page, a link to the site too."""
    meta = item["meta"]
    blocks = []
    if meta.get("description"):
        blocks.append({"k": "para", "text": meta["description"], "cls": []})
    if meta.get("image"):
        blocks.append({"k": "image", "src": image_src(item), "alt": meta["title"], "caption": ""})
    if not link:
        blocks.append({"k": "para", "text": f"[{conf['visit']}]({meta['url']})", "cls": []})
    return {"k": "entry", "id": None, "cls": ["link"] if link else [],
            "title": f"[{meta['title']}]({item['path'][:-5]})" if link else meta["title"],
            "meta": [meta["url"]], "blocks": blocks, "own": not link}


def showcase(items, conf):
    """{showcase}: every site, in order, as a grid."""
    return {"items": [(it, []) for it in items], "empty": conf.get("empty", ""), "cls": ["grid"]}


MARKERS = {"showcase": showcase}


def json_ld(item, conf):
    """The page is about another site: a WebPage whose subject is that
    WebSite. The builder sets the node's own url and inLanguage."""
    meta = item["meta"]
    return {"@type": "WebPage", "name": page_title(meta), "description": meta["description"],
            "isPartOf": site_ref(),
            "about": {"@type": "WebSite", "name": meta["title"], "url": meta["url"]}}
