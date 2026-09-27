---
title: Gabarits et variables
description: layout.html et layouts/, comment tilder choisit le gabarit d'une page, chaque variable avec sa valeur et son échappement, et ce qu'un gabarit doit garder.
order: 20
---

## Nom

layouts - la page autour du contenu, et ses variables

Un gabarit est un fichier HTML dans lequel la construction remplace
chaque `{{ name }}` par une valeur : le titre de la page, ses sections, la
navigation, une valeur de `site.toml`. `layout.html` sert pour toutes les
pages ; `layouts/<name>.html` sert pour les pages d'un type, ou pour une
page qui le demande. Une variable inconnue arrête la construction : un
gabarit n'est jamais publié avec un trou.

[TOC]

## layout.html et layouts/

`theme/layout.html` est le seul fichier qu'un thème doit avoir : sans lui,
la construction s'arrête sur `no layout.html: a site needs a theme`. Les
autres gabarits se rangent dans `theme/layouts/`, un fichier chacun,
nommé d'après ce qu'il sert : `layouts/home.html` pour une page d'accueil,
`layouts/post.html` pour les articles. Tous les gabarits acceptent les
mêmes variables.

Le `layout.html` du site de départ est un exemple complet et court.
Réduit à l'essentiel :

```html
<!DOCTYPE html>
<html lang="{{ site.lang }}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ page.description }}">
<link rel="stylesheet" href="{{ root }}style.css">
<link rel="canonical" href="{{ canonical }}">{{ feeds }}
{{ head }}
</head>
<body>
<a class="skip" href="#contenu">{{ labels.skip }}</a>
<nav class="nav" aria-label="{{ labels.nav }}">
{{ nav }}
</nav>
{{ languages }}
{{ brand }}
<main id="contenu" lang="{{ content_lang }}">
{{ body }}
{{ prev }}
{{ next }}
</main>
<footer>{{ footer.right }}</footer>
{{ script }}</body>
</html>
```

## Le gabarit d'une page

La construction retient le premier de ces cas qui s'applique :

1. `layout:` dans l'en-tête de la page : `layout: home` utilise
   `layouts/home.html`. Le fichier doit exister ; sinon, la construction
   s'arrête en nommant la page.
2. Le gabarit du type de la page, son `LAYOUT`, qui vaut par défaut le
   nom du type : un article utilise `layouts/post.html`, un événement
   `layouts/event.html`, si le thème a le fichier. Le type d'un thème peut
   en nommer un autre ([types personnalisés](docs/content-types/custom-types)).
3. `layout.html`.

Un thème donne donc aux articles leur propre page en ajoutant
`layouts/post.html`, sans aucun réglage. Comme pour tout fichier de thème,
un gabarit placé dans le dossier `assets/` du site l'emporte sur celui du
thème ([fichiers](docs/themes/files)).

## Les variables

Une variable est un nom entre doubles accolades ; les espaces à
l'intérieur sont facultatifs (`{{title}}` fonctionne). Chacune est
remplacée par sa valeur :

| Variable | Valeur |
|---|---|
| `{{ title }}` | le texte du `<title>` : le titre de la page suivi de `site.title_suffix`, sauf si le titre contient déjà le nom du site |
| `{{ type }}` | le type de la page : `page`, `post`, `event`, `member`, ou celui d'un thème |
| `{{ page.<key> }}` | une valeur de l'en-tête de la page : `{{ page.description }}`, `{{ page.man }}`, `{{ page.tagline }}` ; vide quand la page ne la définit pas |
| `{{ <section>.<key> }}` | une valeur de la configuration : `{{ site.lang }}`, `{{ site.manual }}`, `{{ footer.left }}`, `{{ labels.skip }}`, le `{{ search.label }}` d'un thème |
| `{{ root }}` | le chemin relatif de la page à la racine du site (`./`, `../`), pour `style.css`, les icônes, le manifeste, les polices : la racine du site, même sur une page sous `/fr/` |
| `{{ home }}` | le chemin relatif vers la page d'accueil de la langue de la page, pour les liens vers des pages : `{{ home }}{{ footer.left_link }}` ; identique à `root` sur un site en une seule langue |
| `{{ canonical }}` | l'URL absolue de la page, pour `<link rel="canonical">` |
| `{{ feeds }}` | un `<link rel="alternate">` pour chaque flux RSS que nomme la page |
| `{{ head }}` | le reste du `<head>` : robots, auteur, Open Graph, Twitter Card, JSON-LD ([SEO](docs/reference/seo)) |
| `{{ brand }}` | le `<h1>` de la page : le logotype sous forme de chemin, `~/<site>/<section>/<title>` |
| `{{ nav }}` | les liens de `[[nav]]`, l'actuel marqué `aria-current="page"` |
| `{{ languages }}` | le sélecteur de langue, un `<nav>` avec un lien par langue déclarée, l'actuelle marquée `aria-current="page"` ; vide sur un site en une seule langue |
| `{{ collection_nav }}` | la barre latérale de la collection de la page : ses éléments dans l'ordre de la collection, regroupés selon leur `group:`, l'actuel marqué `aria-current="page"` ; sur la page propre de la collection, la même liste, rien de marqué ; vide ailleurs |
| `{{ prev }}`, `{{ next }}` | les liens vers les voisines de la page dans sa collection, étiquetés par `labels.prev` et `labels.next` ; vides à chaque extrémité, sur la page propre de la collection et hors d'une collection |
| `{{ content_lang }}` | la langue du contenu de la page : identique à `site.lang`, sauf si la page est servie en repli, auquel cas c'est la langue du fichier qui tient lieu de traduction |
| `{{ body }}` | les sections de la page, enveloppées dans un `<article>` pour un type qui est un article (articles, événements) |
| `{{ script }}` | les balises `<script>` dont la page a besoin, si le thème a les fichiers ([scripts](docs/themes/scripts)) |

<!-- 1.2 -->

Dans une collection récursive, comme cette documentation,
`{{ collection_nav }}` est un arbre : chaque dossier est une section, un
`<li class="collection-section">` avec son libellé et sa propre liste, et
la section qui contient la page porte aussi `collection-section--open`, ce
qui permet au thème de replier les autres ([classes](docs/themes/classes)).

### page.<key>

  N'importe quelle clé de l'en-tête, telle que la page l'écrit, une fois
  que le type a rempli ses valeurs par défaut : le `{{ page.man }}` d'un
  événement est le `man` de la collection quand l'événement ne définit pas
  le sien. Une clé que la page ne définit pas donne une valeur vide, jamais
  une erreur : un gabarit peut donc lire des clés que seules certaines
  pages possèdent (`{{ page.tagline }}`).

### <section>.<key>

  N'importe quelle valeur de la configuration fusionnée, `defaults.toml`
  puis le `theme.toml` du thème puis le `site.toml` du site, dans la
  langue de la page : les pages françaises lisent aussi `theme.fr.toml` et
  `site.fr.toml`. Un nom qu'aucune couche ne définit arrête la
  construction sur `unknown placeholder`, en nommant le gabarit : un thème
  donne une valeur, dans son propre `theme.toml`, à chaque clé que lisent
  ses gabarits ([fichiers](docs/themes/files)).

## Échappement

Les valeurs de l'en-tête et de la configuration, `{{ page.<key> }}` et
`{{ <section>.<key> }}`, sont échappées pour le HTML : `<`, `>`, `&` et
les guillemets deviennent des entités, si bien qu'une valeur est sûre dans
un attribut comme dans le texte. `{{ title }}` est échappé lui aussi.

Les valeurs que calcule la construction sont insérées telles quelles,
puisque ce sont déjà du HTML ou un chemin : `type`, `root`, `home`,
`canonical`, `brand`, `nav`, `languages`, `collection_nav`, `prev`,
`next`, `content_lang`, `feeds`, `head`, `body`, `script`.

## Ce que le gabarit doit garder

La construction écrit un balisage accessible et indexable ; quatre de ses
éléments vivent dans le gabarit, et un thème les conserve :

- `lang="{{ site.lang }}"` sur `<html>` : la langue de la page, que lisent
  les lecteurs d'écran et les moteurs de recherche.
- Un seul `{{ brand }}` : c'est l'unique `<h1>` de la page. Les titres du
  corps commencent à `<h2>`.
- Un `<main id="contenu">`, ou une autre cible portant l'identifiant visé
  par le lien d'évitement : le premier lien de la page permet au clavier
  de sauter la navigation.
- `<link rel="canonical" href="{{ canonical }}">` : l'unique adresse de la
  page pour les moteurs de recherche.

Sur un site en plusieurs langues, `<main lang="{{ content_lang }}">` est
recommandé : une page servie en repli, pas encore traduite, garde alors la
langue de son texte au sein d'une page d'une autre langue.

Tout le reste relève du thème : l'emplacement de la navigation, le fait
que `{{ collection_nav }}` soit une barre latérale, l'affichage même de
`{{ prev }}` et `{{ next }}`. Un gabarit qui omet `{{ script }}` ne charge
aucun des scripts que nomme la construction ; un gabarit qui omet
`{{ head }}` perd les métadonnées de la page.

## Voir aussi

- [les fichiers d'un thème](docs/themes/files)
- [classes](docs/themes/classes)
- [la navigation dans une collection](docs/content-types/navigation)
- [écrire des pages](docs/guide/writing)
