---
title: Types de contenu
description: Les collections de pages d'un même type : les déclarer, leurs éléments, les marqueurs de liste, leurs flux RSS et iCalendar, et les quatre types fournis.
order: 20
---

## Nom

content types - les collections, et les types qui leur donnent forme

Une collection est un dossier de `content/` dont les fichiers sont les
éléments d'un même type : les articles d'un blog, les événements d'un
agenda, les membres d'un groupe. Le type dit ce qu'est un élément : les
clés d'en-tête qu'il lit, sa carte dans une liste, ses données
structurées, son flux. tilder fournit quatre types, et un thème ajoute les
siens en Python. Cette page déclare les collections et les liste ; les
pages suivantes décrivent chaque type.

[TOC]

## Les types

| Type | Éléments | Listes | Flux | Page |
|---|---|---|---|---|
| `page` | toute page hors d'une collection | - | - | [page](docs/content-types/page) |
| `post` | articles, notes, notes de version | du plus récent au plus ancien | RSS | [post](docs/content-types/post) |
| `event` | rencontres, conférences, sorties | à venir et passés, selon la date de construction | RSS et iCalendar | [event](docs/content-types/event) |
| `member` | personnes | par catégorie, puis par nom | - | [member](docs/content-types/member) |

Un thème ajoute des types dans `theme/types/`, écrits exactement comme
ceux de tilder ([vos propres types](docs/content-types/custom-types)). Ce
manuel est lui-même une collection du type `doc` du thème, et sa vitrine
une collection d'un type `showcase`.

## Déclarer une collection

Une collection est une table de `site.toml`, `[collections.<name>]`. Son
nom est celui par lequel les marqueurs et la clé d'en-tête `feed:` la
désignent.

```toml
[collections.talks]         # {upcoming:talks}, {past:talks}
type = "event"
dir = "talks"               # content/talks/, served at /talks/...
feed = "talks.xml"
calendar = "talks.ics"
upcoming_tag = "soon"
```

| Clé | Rôle |
|---|---|
| `type` | le type de ses éléments : `post`, `event`, `member`, ou un type du thème ; `post` par défaut. Les types sont au singulier : `type = "posts"` arrête la construction |
| `dir` | son dossier sous `content/` ; par défaut, le nom de la collection. Deux collections ne peuvent ni partager un dossier ni s'imbriquer l'une dans l'autre |
| `nav_label` | le nom accessible de sa barre latérale, `{{ collection_nav }}` ; par défaut `labels.collection_nav` ([navigation](docs/content-types/navigation)) |
| `recursive` | `true` pour lire aussi les sous-dossiers (tilder 1.2) ; `false` par défaut, sauf si les réglages du type en décident autrement |
| chaque réglage de son type | les mots et les options du type, chacun avec une valeur par défaut dans le module du type : une collection ne règle que ce qui diffère |

Les réglages de chaque type sont listés sur sa page. Un `site.fr.toml`
peut reprendre `[collections.<name>]` avec les seuls mots qui changent :
les tables sont fusionnées clé par clé, si bien que le flux français
reçoit un titre en français tandis que `type` et `dir` restent tels que
`site.toml` les fixe ([langues](docs/guide/languages)).

Un type qu'aucun module ne définit arrête la construction, qui nomme les
types chargés :

```text
error: content/site.toml: collection "talks" has type "tlak", which no type defines. Types loaded: event, member, page, post (types/)
```

## Trois collections par défaut

Le `defaults.toml` de tilder déclare les trois collections que la plupart
des sites ont :

```toml
[collections.blog]
type = "post"
dir = "blog"
feed = "blog/feed.xml"

[collections.events]
type = "event"
dir = "events"
nav = "events"
feed = "events.xml"
calendar = "calendar.ics"

[collections.members]
type = "member"
dir = "members"
```

Une collection dont le dossier n'existe pas est inactive : pas d'élément,
pas de flux, pas de calendrier, et un marqueur qui la nomme affiche son
texte de liste vide. Un site commence donc un blog en créant
`content/blog/`, sans rien configurer. Un `[collections.blog]` dans
`site.toml` est fusionné avec celui par défaut : ce site y règle son nom
de page de manuel et les mots de son flux. Le résumé de la
construction dit quelles collections sont actives :

```text
collections: blog (post, 3 items), events (event, no folder), members (member, no folder)
```

## Les éléments

Un élément est un fichier du dossier de la collection, ou un dossier à lui
seul :

| Source | Élément | Page |
|---|---|---|
| `content/talks/2099-03-01-first-talk.md` | `2099-03-01-first-talk` | `/talks/2099-03-01-first-talk` |
| `content/talks/2099-03-01-first-talk/index.md` | le même, avec ses images à côté | la même |
| `content/talks/2099-03-01-first-talk.fr.md` | sa traduction française | `/fr/talks/2099-03-01-first-talk` |
| `content/talks/_template.md` | aucun : un nom qui commence par `_` n'est jamais construit | - |
| `content/talks/index.md` | aucun : la page de la collection elle-même | `/talks/` |

- Un type daté, `post` ou `event`, lit sa date dans le nom du fichier,
  `YYYY-MM-DD-slug.md` ([post](docs/content-types/post)).
- La page de la collection est `<dir>/index.md`, ou une page nommée comme
  le dossier, à côté de lui (`talks.md` pour `talks/`). C'est une page
  ordinaire : elle fixe elle-même son `man`, son `tagline` et son `nav`,
  et porte la liste.
- Avec les types fournis, l'en-tête d'un élément peut omettre `man`,
  `nav` et, pour les types datés, `tagline` : le type les remplit à partir
  des réglages de la collection.

## Collections récursives

<!-- 1.2 -->

Avec `recursive = true` (tilder 1.2), une collection lit aussi ses
sous-dossiers, à toute profondeur. `content/docs/guide/writing.md` est
l'élément `guide/writing`, servi à `/docs/guide/writing`, dans la section
`guide`. Le `index.md` d'un sous-dossier est l'élément nommé comme le
dossier, servi à côté de lui : `content/docs/guide/index.md` est
`/docs/guide`, la page de la section. Un `guide.md` à côté du dossier peut
tenir ce rôle à sa place ; une section qui n'a ni l'un ni l'autre n'a pas
de page, et le nom de son dossier la représente. La documentation que
vous lisez est une telle collection.

<!-- 1.2 -->

`recursive` vaut `false` sauf si la collection ou les réglages de son type
le fixent, et ne prend que `true` ou `false`. Un type daté ne peut pas
être récursif, et deux fichiers pour un même élément (`guide.md` et
`guide/index.md`) arrêtent la construction. L'ordre des pages, en
profondeur d'abord, est décrit sur la page
[navigation](docs/content-types/navigation).

## Les listes

Un titre de section qui se termine par le marqueur d'un type est rempli
des cartes de la collection, une par élément, chacune cliquable en
entier :

```text
## Posts {posts}

## Coming up {upcoming:talks}
```

| Marqueur | Type | Remplit la section avec |
|---|---|---|
| `{posts}` | `post` | tous les articles, du plus récent au plus ancien |
| `{upcoming}` | `event` | les événements datés d'aujourd'hui ou plus tard, du plus proche au plus lointain, le premier mis en avant |
| `{past}` | `event` | les événements antérieurs à aujourd'hui, du plus récent au plus ancien |
| `{next-event}` | `event` | le prochain événement seulement |
| `{members}` | `member` | tous les membres, en grille, par catégorie puis par nom |

- `{marker:name}` nomme la collection à lister : `{posts:news}`,
  `{upcoming:talks}`. Un nom qui n'est pas une collection du type du
  marqueur arrête la construction.
- Un `{marker}` seul liste la collection de ce type propre à la page :
  celle dont le dossier contient la page, ou dont la page porte le nom ; à
  défaut, la première collection de ce type.
- Une liste vide affiche le texte prévu par la collection : `empty` pour
  les articles et les membres, `none_upcoming` et `none_past` pour les
  événements.
- Les blocs écrits sous le titre restent, après les cartes.
- Le mot du marqueur devient aussi une classe du corps de la section
  (`.posts`, `.upcoming`), et une grille de membres ajoute `.grid`
  ([classes](docs/themes/classes)).

Le type d'un thème apporte ses propres marqueurs, comme les `{docs}` et
`{showcase}` de ce site.

## Flux et calendriers

Chaque collection peut écrire deux fichiers, chacun désigné dans ses
réglages par un chemin depuis la racine du site ; un chemin vide n'écrit
rien.

- `feed` : un flux RSS de tous les éléments, dans l'ordre inverse de la
  collection (du plus récent au plus ancien pour les articles et les
  événements), pour les types qui fournissent des entrées de flux (`post`
  et `event`, pas `member`). Le flux est écrit dans chaque langue, sous
  son préfixe : `blog/feed.xml` et `fr/blog/feed.xml`, avec les mots de
  `feed_title` et `feed_description` dans cette langue. La clé d'en-tête
  `feed:` d'une page, un nom de collection ou `all`, annonce le flux dans
  son `<head>` ([écrire des pages](docs/guide/writing)).
- `calendar` : un fichier iCalendar de tous les événements, pour le type
  `event`. Il est écrit une seule fois, dans la langue par défaut : un
  calendrier n'a pas de langue d'interface
  ([event](docs/content-types/event)).

Tous les calendriers du site partagent la table `[calendar]` :

| Clé | Défaut | Rôle |
|---|---|---|
| `calendar.name` | `"events"` | le nom du calendrier dans les applications (`X-WR-CALNAME`), et le suffixe du résumé de chaque événement, `First talk - events` |
| `calendar.description` | `"Events."` | la description du calendrier (`X-WR-CALDESC`) |
| `calendar.prodid` | `"-//site//events//EN"` | l'identifiant du produit (`PRODID`) |
| `calendar.timezone` | `"UTC"` | le fuseau horaire du calendrier (`X-WR-TIMEZONE`) |
| `calendar.uid_domain` | `"example.org"` | le domaine de l'identifiant de chaque événement, `<slug>@<uid_domain>` : mettez le vôtre |

```toml
[calendar]
name = "talks"
description = "Talks of the group."
prodid = "-//example.org//talks//EN"
uid_domain = "example.org"
```

Comme le calendrier est écrit dans la langue par défaut, il prend ces
valeurs dans `site.toml` ; un `[calendar]` dans `site.fr.toml` n'est pas
utilisé.

## Voir aussi

- [page](docs/content-types/page), [post](docs/content-types/post),
  [event](docs/content-types/event), [member](docs/content-types/member)
- [vos propres types](docs/content-types/custom-types)
- [navigation](docs/content-types/navigation)
- [flux et images](docs/reference/feeds-and-images)
