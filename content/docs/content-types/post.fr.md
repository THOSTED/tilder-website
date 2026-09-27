---
title: post
description: Le type post : des articles datés, nommés par leur date, listés du plus récent au plus ancien par {posts}, avec un flux RSS et des données BlogPosting.
order: 20
---

## Nom

post - des articles datés, du plus récent au plus ancien, avec un flux RSS

Un article est un fichier Markdown nommé par sa date, dans une collection
de type `post` : un blog, des actualités, des notes de version. La
collection liste ses articles du plus récent au plus ancien partout où une
section porte `{posts}`, en écrit un flux RSS, et dit aux moteurs de
recherche comme aux aperçus de liens que chacun est un article, avec sa
date et son auteur.

[TOC]

## Réglages

Une collection `post` peut fixer ces clés sous `[collections.<name>]` ;
chacune a sa valeur par défaut dans le module du type, `types/post.py`.

| Clé | Défaut | Rôle |
|---|---|---|
| `man` | `"SITE-BLOG(7)"` | le nom de page de manuel de ses éléments, sauf s'ils fixent le leur |
| `nav` | `"blog/"` | l'entrée de `[[nav]]` que ses éléments marquent comme courante, et le lien du flux |
| `empty` | `"No post yet."` | le texte d'une liste `{posts}` vide |
| `feed` | `""` | le chemin du flux RSS depuis la racine du site, `"blog/feed.xml"` ; vide pour aucun |
| `feed_title` | `"posts"` | le titre du flux |
| `feed_description` | `"Posts."` | la description du flux |

Le blog de ce site, par exemple :

```toml
[collections.blog]
type = "post"
man = "TILDER-BLOG(7)"
feed = "blog/feed.xml"
feed_title = "tilder blog"
feed_description = "Release notes of tilder."
```

`defaults.toml` déclare déjà `[collections.blog]`, avec `dir = "blog"` et
`feed = "blog/feed.xml"` : créer `content/blog/` suffit pour en commencer
un ([les collections](docs/content-types)).

## Un fichier par article

Le fichier d'un article se nomme `YYYY-MM-DD-slug.md` : sa date, un tiret,
puis un identifiant fait de minuscules, de chiffres et de tirets. Ce nom
est l'adresse de l'article, et sa date est celle de l'article ; il n'y a
pas de clé `date:`.

| Source, dans `content/blog/` | Adresse |
|---|---|
| `2026-01-01-hello.md` | `/blog/2026-01-01-hello` |
| `2026-01-01-hello.fr.md` | `/fr/blog/2026-01-01-hello` |
| `2026-03-01-release/index.md` | `/blog/2026-03-01-release` |
| `2026-03-01-release/flow.svg` | `/blog/2026-03-01-release/flow.svg` |

- Un article qui montre des images est un dossier, avec `index.md` et les
  images à côté.
- Un fichier du dossier dont le nom ne commence pas par une date n'est pas
  un article : il est construit comme une page ordinaire, qui fixe
  elle-même son `man`, son `tagline` et son `nav`.
- Un nom dont la date n'existe pas arrête la construction :
  `"2026-02-30" is not a date`.
- `index.md` est la page du blog lui-même, et `_template.md` n'est jamais
  construit.

## En-tête

```text
---
title: Hello
description: The first post, in a file named by its date: all a post needs.
author: Me
tag: news
---
```

| Clé | Rôle |
|---|---|
| `title` | le titre de l'article |
| `description` | une phrase : le texte de la carte dans une liste, le résumé dans le flux, l'aperçu du lien |
| `author` | un auteur nommé, sur la carte, dans `<meta name="author">` et dans les données structurées |
| `tag` | un mot, l'étiquette de la carte et l'`article:tag` |
| `man` | par défaut, le `man` de la collection |
| `nav` | par défaut, le `nav` de la collection |
| `tagline` | par défaut, la date en toutes lettres, écrite selon les `[dates]` de la langue : `Thursday 1 January 2026` en anglais |
| `updated` | une date, `2026-03-01` : la dernière modification, dans le plan du site et les données structurées ; par défaut, la date de l'article |

Toutes les autres clés d'[écrire des pages](docs/guide/writing)
s'appliquent aussi : `image`, `robots`, `group`...

## La carte

La carte d'un article montre sa date, son auteur et son étiquette, la
date dans un élément `<time>`. Dans une liste, la carte montre aussi la
description, et son titre mène à l'article ; sur la page de l'article, la
même carte, sans le lien, clôt la première section. Dans le miroir en
texte :

```text
     Hello                                                         [ news ]
     Thursday 1 January 2026
     Me

         The first post, in a file named by its date: all a post needs.
```

## La liste

Une section marquée `{posts}` liste tous les articles de la collection, du
plus récent au plus ancien. La page du blog se résume souvent à cela :

```text
---
man: MYSITE-BLOG(7)
title: blog
description: Posts, newest first, one Markdown file each, named by date.
tagline: posts
nav: blog/
feed: blog
---

## Posts {posts}
```

`{posts:news}` liste la collection `news` depuis n'importe quelle page ;
une liste vide affiche le texte `empty` de la collection. `feed: blog`
annonce le flux du blog dans le `<head>` de la page.

## RSS

Quand `feed` est fixé, la construction écrit à ce chemin le flux RSS 2.0
de la collection : tous les articles, du plus récent au plus ancien,
chacun avec son titre, son adresse (qui sert aussi de `guid`), sa date et
sa description. Le titre du canal est `feed_title`, sa description
`feed_description`, et son lien la page que désigne `nav`.

Chaque langue a son propre flux, sous son préfixe : `blog/feed.xml` en
anglais, `fr/blog/feed.xml` en français, avec les mots que `site.fr.toml`
donne à la collection ([langues](docs/guide/languages)). Un `feed` vide,
la valeur par défaut du type, n'en écrit aucun.

## Moteurs de recherche

Un article est un article, de toutes les manières dont la page peut le
dire :

- son corps est enveloppé dans un `<article>`, que cherchent les modes
  lecture ;
- `og:type` vaut `article`, avec `article:published_time` (la date) et
  `article:tag` (le `tag`), plus `<meta name="author">` quand un auteur
  est nommé ;
- son nœud JSON-LD est un `BlogPosting` : `headline`, `description`,
  `datePublished`, `dateModified` (`updated`, sinon la date),
  l'organisation du site comme `publisher`, l'`image` d'aperçu, et
  l'`author` comme `Person` quand il est nommé.

La [référence du référencement](docs/reference/seo) montre le `<head>` en
entier.

## Voir aussi

- [les collections](docs/content-types)
- [event](docs/content-types/event)
- [flux et images](docs/reference/feeds-and-images)
