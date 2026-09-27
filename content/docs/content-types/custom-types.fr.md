---
title: Vos propres types
description: Écrire un type de contenu en Python dans theme/types/ : ses attributs, ses fonctions, l'élément, le nœud de carte, les marqueurs, les imports, les erreurs.
order: 50
---

## Nom

custom types - un type de contenu à vous, en Python

Un thème ajoute un type avec un module Python dans `theme/types/`, écrit
exactement comme les quatre types fournis : un nom, quelques attributs, et
des fonctions qui font d'un élément une carte, des données structurées,
une entrée de flux ou des fichiers à lui. Un type n'écrit jamais de HTML.
Il renvoie des nœuds que la construction rend deux fois, en HTML et en
texte : un nouveau type est donc juste dans le miroir en texte sans le
moindre effort. Cette page donne le contrat en entier, puis un exemple
complet, un type `recipe`.

[TOC]

## Le module

La construction charge d'abord les `types/*.py` de tilder, puis les
`theme/types/*.py` du thème. Un fichier dont le nom commence par `_`
n'est pas chargé. Un module du thème qui porte le même `NAME` qu'un type
fourni le remplace ; deux modules d'un même dossier ne peuvent pas
partager un nom. Une collection utilise un type par son nom,
`type = "recipe"`.

Seuls `NAME` et la fonction `entry` sont obligatoires. Tout le reste a une
valeur par défaut :

| Attribut | Défaut | Rôle |
|---|---|---|
| `NAME` | obligatoire | le nom auquel renvoie `type =` : une chaîne, un identifiant Python valide |
| `DATED` | `False` | les éléments se nomment `YYYY-MM-DD-slug`, et `item["date"]` contient la date |
| `ARTICLE` | `False` | le corps de la page est enveloppé dans un `<article>` |
| `OG_TYPE` | `"website"` | l'`og:type` de la page ; le type `post` fixe `"article"` |
| `LAYOUT` | le `NAME` | les pages des éléments utilisent `theme/layouts/<LAYOUT>.html` si le thème l'a, sinon `layout.html` |
| `SCRIPT` | `""` | un script du thème chargé sur les pages qui listent le type, si le thème le fournit : `"members.js"` |
| `DEFAULTS` | `{}` | les réglages et les mots du type, en anglais et neutres ; une collection peut remplacer chacun d'eux |
| `MARKERS` | `{}` | les marqueurs de section qui listent le type : `{"word": function}` |
| `SEQUENTIAL` | `False` | le miroir en texte d'un élément reçoit une ligne `previous: ... next: ...` avant son pied de page ([navigation](docs/content-types/navigation)) |
| `LOCALIZED_OUTPUTS` | `False` | `outputs()` est appelée dans chaque langue, ses fichiers placés sous le préfixe de la langue, `fr/` ; sinon une seule fois, dans la langue par défaut |

Une valeur qui n'est pas du bon type, par exemple un `DATED` qui n'est
pas un `bool`, arrête la construction. Les réglages que reçoit une collection
sont les `DEFAULTS` du type avec `[collections.<name>]` par-dessus, plus
`type` et `dir`.

## Les fonctions

`item` est le dictionnaire décrit plus bas, `conf` les réglages de la
collection, `link` un booléen. Seule `entry` est obligatoire.

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

| Fonction | Renvoie | Si elle manque |
|---|---|---|
| `defaults` | rien : elle complète ce que l'en-tête a omis | rien n'est complété |
| `sort_key` | la clé de l'élément dans l'ordre de la collection | l'identifiant (`slug`) |
| `entry` | la carte, un nœud de carte, ou `None` pour aucune carte | obligatoire |
| `json_ld` | le nœud schema.org de la page, un `dict`, ou `None` | un nœud `WebPage` |
| `meta_tags` | des balises `<meta>` en plus, une liste de `("name", key, value)` et de `("property", key, value)` | aucune |
| `feed_item` | `{"title", "link", "description", "date"}`, ou `None` pour laisser l'élément de côté | pas de flux RSS |
| `outputs` | des fichiers en plus, `{"path": text}` | aucun |
| `list_data` | `{key: value}`, les attributs `data-*` d'une section qui liste le type | aucun |

- `defaults` s'exécute sur chaque élément dès que son fichier est lu,
  avant tout le reste : elle modifie `item["meta"]` sur place. Les types
  fournis y remplissent `man` et `nav` à partir de `conf`.
- `sort_key` ordonne la collection : les listes, le flux, la barre
  latérale et les voisins en partent. Une liste peut l'inverser, comme le
  fait `{posts}`.
- `entry` est appelée avec `link` vrai pour une carte dans une liste, et
  faux pour la carte qui clôt la première section de la page de
  l'élément.
- `json_ld` renvoie le nœud propre à la page ; la construction y ajoute
  son `@id`, son `url` et son `inLanguage`, et le place dans le graphe
  avec l'`Organization` et le `WebSite` du site
  ([référencement](docs/reference/seo)).
- `feed_item` rend possible le flux RSS de la collection : sans elle, le
  réglage `feed` n'écrit rien. `date` est une date ISO, si bien qu'un
  type qui a un flux est en général `DATED`.
- `outputs` reçoit tous les éléments de la collection et renvoie des
  fichiers à écrire, par leur chemin depuis la racine du site : le
  fichier iCalendar du type `event`, l'index de recherche de ce site.
  Elle ne s'exécute que si le dossier de la collection existe.

## L'élément

Ce que reçoivent `defaults`, `entry` et les autres :

<!-- 1.2 -->

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

<!-- 1.2 -->

| Clé | Rôle |
|---|---|
| `slug` | le nom du fichier sans `.md`, ou le nom du dossier de l'élément |
| `date` | la date d'un élément `DATED`, `YYYY-MM-DD` ; sinon `None` |
| `meta` | l'en-tête, après `defaults()` |
| `src` | le fichier Markdown lu, un `Path` |
| `path` | le fichier de la page depuis la racine du site |
| `collection`, `conf`, `type` | le nom de la collection, ses réglages, le module du type |
| `lang` | la langue en cours de construction |
| `content_lang` | la langue du fichier lu, qui diffère quand une page n'est pas encore traduite |
| `section` | tilder 1.2 : le dossier d'un élément d'une collection récursive |

Les valeurs de l'en-tête sont des chaînes, telles qu'écrites :
`meta["serves"]` vaut `"4"`, pas un nombre. `item["path"][:-5]`, le
chemin sans `.html`, est la cible d'un lien vers la page de l'élément.

<!-- 1.2 -->

Dans une collection récursive (tilder 1.2), l'identifiant porte les
dossiers, `guide/writing`, et `section` en contient la partie dossier,
`guide` ; elle vaut `""` au premier niveau, et dans toute collection qui
n'est pas récursive.

## Le nœud de carte

Ce que renvoie `entry`, une carte :

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

| Clé | Rôle |
|---|---|
| `title` | du Markdown en ligne : un lien vers l'élément dans une liste, son titre seul sur sa propre page |
| `meta` | la ligne de la carte, une chaîne par partie (plus bas) |
| `cls` | les classes de la carte, chacune écrite `entry--<cls>` : `link` rend la carte cliquable en entier |
| `blocks` | ce qui suit la ligne, en nœuds de blocs |
| `own` | vrai sur la page de l'élément : pas de `<h3>`, puisque le `<h1>` de la page est le titre |
| `data` | facultatif : des attributs `data-*` de la carte |

Chaque partie de `meta` est l'une de trois choses. Une date et ses mots
joints par une barre, `"2099-03-01 | Sunday 1 March 2099"`, devient un
`<time>`, et le miroir en texte garde les mots. Une chaîne qui s'ouvre et
se ferme sur un accent grave devient une étiquette (`.tag`), que le
miroir en texte place contre la marge de droite. Tout le reste est du
texte simple.

Les blocs qu'une carte peut contenir sont ceux du dialecte Markdown :
`para`, `empty`, `list`, `code`, `table`, `image` et `profiles`. Une
nouvelle sorte de bloc est une nouvelle construction du dialecte, ajoutée
au générateur avec ses deux rendus. Voici les trois que les types
emploient le plus :

```python
{"k": "para", "text": "One sentence.", "cls": [],
 "txt": "Its wording in the text mirror."}   # txt: optional
{"k": "image", "src": "recipes/soup/bowl.png",
 "alt": "A bowl of soup", "caption": ""}     # src: from content/
{"k": "profiles", "items": [(key, label, url)]}
```

## Les marqueurs

`MARKERS` associe un mot à une fonction. Une section dont le titre se
termine par `{word}` ou `{word:collection}` l'appelle avec les éléments
de la collection, dans l'ordre, et ses réglages :

```python
def recipes(items, conf):
    return {"items": [(it, []) for it in items],
            "empty": conf.get("empty", ""),
            "cls": ["grid"]}
```

- `items` sont les éléments à montrer, dans l'ordre, chacun avec une liste
  de classes en plus pour sa carte ; `empty` est le texte d'une liste
  vide ; `cls`, facultatif, ajoute des classes au corps de la section.
- Une classe en plus d'un élément, `["next"]`, s'ajoute aux classes de sa
  carte : `.entry--next`, et `.tag--next` sur son étiquette, comme le fait
  `{upcoming}` pour l'événement le plus proche.
- Un mot de marqueur appartient à un seul type. Un mot que deux types
  revendiquent arrête la construction ; un thème qui veut ce mot remplace
  le type qui le possède.
- La section reçoit aussi le mot comme classe, le `SCRIPT` du type si le
  thème l'a, et les attributs `data-*` de `list_data`.

## Ce qu'un type peut importer

Un type importe ce dont il a besoin parmi ces noms, et rien d'autre de la
construction : le reste peut changer à chaque version.

| Module | Noms |
|---|---|
| `config` | `CFG` (la configuration fusionnée), `STATE["today"]` (la date de la construction, ISO), `apex` (l'adresse du site) |
| `dates` | `human_date`, une date dans les mots de `[dates]` |
| `paths` | `clean_url`, l'adresse d'une page sans `.html` |
| `fold` | `to_ascii` |
| `seo` | `page_heading`, `page_title`, `share_image`, `org_ref`, `site_ref` |
| `feeds` | `calendar`, le fichier iCalendar d'une liste d'événements |
| `contenttypes` | `TYPES` : les types fournis, chargés en premier, pour bâtir sur l'un d'eux |

La bibliothèque standard de Python est disponible aussi. Un type qui en
prolonge un autre part de son module :

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

## Erreurs

La construction vérifie chaque module et chaque collection avant de
construire, et signale tous les problèmes qu'elle trouve avant de
s'arrêter : un `NAME` ou une `entry` absents, un attribut qui n'est pas
du bon type, une fonction qui n'en est pas une, un mot de marqueur revendiqué
deux fois, un module qui ne peut pas être importé, une collection dont
aucun module ne définit le `type`, deux collections sur un même dossier.

```text
error: theme/types/talk.py: MARKERS["upcoming"] is already claimed by type "event" (types/event.py). Rename the marker, or replace that type by naming yours "event"
```

Une exception levée dans une fonction d'un type arrête aussi la
construction, au fichier en cours, en nommant le module et la fonction :

```text
error: content/talks/2099-03-01-first-talk.md: theme/types/talk.py: entry() failed: KeyError: 'speaker'. Run with --debug for the traceback
```

`--debug` affiche la trace Python de l'échec. En mode surveillance, un
changement sous `theme/types/` relance la construction, qui recharge les
modules ([la ligne de commande](docs/reference/cli)). Un type est du code
qui s'exécute à chaque construction : relisez les types d'un thème avant
de l'adopter.

## Un exemple complet

Un type `recipe` : une page par recette, une grille de cartes qui disent
combien de temps prend chacune et pour combien de personnes, triées par
titre, et un nœud `Recipe` pour les moteurs de recherche. La collection,
dans `content/site.toml` :

```toml
[collections.recipes]       # content/recipes/, {recipes}
type = "recipe"
serves = "for {}"
```

Le module, `theme/types/recipe.py` :

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

La page de la collection, `content/recipes/index.md`, et une recette,
`content/recipes/leek-soup.md` :

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

Sur un site dont le thème n'ajoute que ce type et dont le seul dossier de
collection est `content/recipes/`, la construction nomme le nouveau type
et sa collection, et `/recipes` se lit ainsi dans un terminal :

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

La page de la soupe clôt sa première section par la même carte, sans le
lien, et porte un nœud `Recipe` avec `"totalTime":"PT40M"` et
`"recipeYield":"4"`. Les mots sont ceux de la collection :
`serves = "for {}"` a remplacé le `"serves {}"` du type, et un
`site.fr.toml` les donnerait en français.

## Voir aussi

- [les collections](docs/content-types)
- [navigation](docs/content-types/navigation)
- [gabarits](docs/themes/layouts)
- [scripts](docs/themes/scripts)
