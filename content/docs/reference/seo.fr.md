---
title: SEO
description: Ce qu'écrit tilder pour les moteurs de recherche et les aperçus de lien : titre, description, canonique, Open Graph, JSON-LD, plans du site, robots.txt.
order: 40
---

## Nom

seo - titres, balises meta, données structurées, plans du site et vérifications

Tout ce qu'un moteur de recherche ou un aperçu de lien montre d'une page
vient de son en-tête et de `site.toml`. La construction écrit les balises
du `<head>`, les données structurées, les plans du site et `robots.txt`,
puis vérifie chaque titre et chaque description et avertit de ce que les
moteurs de recherche tronquent ou pénalisent. Rien à installer, rien à
remplir à la main.

[TOC]

## Ce que règle une page

| Clé | Devient |
|---|---|
| `title` | le `<title>`, avec `site.title_suffix` ; `og:title` et `twitter:title`, sans lui |
| `name` | le nom de la page dans le chemin du `<h1>`, et dans `og:title` à la place du titre |
| `description` | `<meta name="description">`, `og:description`, `twitter:description`, les données structurées, les flux |
| `image` | l'image de l'aperçu, `og:image` et `twitter:image`, relative au dossier de la page |
| `image_alt` | `og:image:alt` ; par défaut `share.image_alt` |
| `updated` | `<lastmod>` dans `sitemap.xml`, et le `dateModified` d'un article |
| `robots` | `<meta name="robots">` ; par défaut `seo.robots`. Avec `noindex`, la page sort des plans du site et des vérifications |

Chaque clé d'en-tête est décrite dans [écrire des pages](docs/guide/writing).
Écrivez d'abord pour les gens : un titre qui dit ce qu'est la page, une
description qui dit pourquoi l'ouvrir.

## Titre et description

Le `<title>`, la variable `{{ title }}` du gabarit, est le `title` de la
page suivi de `site.title_suffix`, sauf si le titre contient déjà
`site.name`, majuscules ou non. Avec les valeurs par défaut,
`title: about` donne `about - my site`.

La description est la `description` de la page, une phrase. Le gabarit du
site de départ l'écrit en `<meta name="description">` à partir de
`{{ page.description }}` ; la construction la reprend pour Open Graph et
la Twitter Card.

## L'URL canonique

Chaque page a une seule adresse, sur l'origine du site, sans `.html` :
`https://example.org/about`, `https://example.org/blog/`. Le gabarit
l'écrit en `<link rel="canonical">` à partir de `{{ canonical }}`, et la
construction s'en sert pour `og:url`, les données structurées et les
plans du site. Elle est tirée de `site.url`, qui doit être l'adresse à
laquelle le site est servi.

Sur un site en plusieurs langues, chaque page énumère aussi ses pages
sœurs, `<link rel="alternate" hreflang="...">`, une par langue déclarée,
et `hreflang="x-default"` pour celle par défaut
([langues](docs/guide/languages)).

## Le head

`{{ head }}` contient, dans cet ordre
([gabarits et variables](docs/themes/layouts)) :

- les variantes de langue, sur un site en plusieurs langues ;
- `<meta name="robots">` : le `robots` de la page, sinon `seo.robots`,
  `index, follow, max-image-preview:large` ;
- les balises `name` propres au type : un article qui a un `author`
  reçoit `<meta name="author">` ;
- Open Graph ;
- les balises `property` propres au type : l'`article:published_time`
  d'un article, et `article:tag` quand il a un `tag` ;
- la Twitter Card ;
- les données structurées.

## Open Graph

Ce que lit un aperçu de lien, sur les réseaux sociaux et dans les
messageries :

| Propriété | Valeur |
|---|---|
| `og:site_name` | `site.name` |
| `og:locale` | `site.locale` |
| `og:locale:alternate` | la `locale` de chaque autre langue déclarée, une fois |
| `og:type` | celui du type : `article` pour les articles, `website` pour tous les autres types intégrés |
| `og:title` | le `name` de la page, sinon son titre sans le suffixe |
| `og:description` | la description |
| `og:url` | l'URL canonique |
| `og:image` | l'`image` de la page ; sinon `share.png`, quand le thème a un `share.svg` ; sinon l'icône, `share.logo` |
| `og:image:alt` | l'`image_alt` de la page, sinon `share.image_alt` |
| `og:image:width`, `og:image:height` | la taille de l'image, lue dans le fichier, quand elle est connue |

Une `image` est au mieux un PNG ou un JPEG de 1200x630 : les réseaux
sociaux ignorent le plus souvent le SVG. La façon dont `share.png` et les
icônes sont dessinés est dans [flux et images](docs/reference/feeds-and-images).

## Twitter Card

| Nom | Valeur |
|---|---|
| `twitter:card` | `summary_large_image` quand l'image fait au moins 600 pixels de large et est plus large que haute ; sinon `summary` |
| `twitter:title` | comme `og:title` |
| `twitter:description` | la description |
| `twitter:image` | comme `og:image` |

## Données structurées

Chaque page porte un `<script type="application/ld+json">` : des données
inertes, jamais exécutées, que la politique de sécurité du site laisse
passer. C'est un graphe d'au plus quatre nœuds.

- `Organization` : `seo.organization`, l'adresse du site, et le logo,
  `share.logo`.
- `WebSite` : `site.name`, l'adresse du site, sa langue, et
  l'organisation comme éditeur.
- Le nœud propre à la page, donné par son type, avec l'adresse et la
  langue de la page.
- `BreadcrumbList` : la première entrée de `[[nav]]`, puis l'entrée que
  la page marque avec `nav:`, quand c'est une page du site et pas la page
  elle-même, puis la page. La page d'accueil n'en a pas.

Le nœud de la page, par type :

| Type | Nœud | Contenu |
|---|---|---|
| `page` | `WebPage` | le `<title>`, la description, le site dont elle fait partie |
| `post` | `BlogPosting` | titre, description, `datePublished` (la date du fichier), `dateModified` (`updated`, sinon la date), l'organisation comme éditeur, l'image, et `author` comme `Person` quand l'article en nomme un |
| `event` | `Event` | nom, description, `startDate`, `endDate` (`end`, sinon la date), prévu, en présentiel, le `place` comme `Place` avec `geo` quand `lat` et `lon` sont donnés, l'organisation comme organisateur, l'image |
| `member` | `ProfilePage` | le `<title>`, et une `Person` : le nom du membre, membre de l'organisation, les liens de profil comme `sameAs`, l'`affiliation` |

Un type ajouté par un thème donne son propre nœud, ou reçoit une
`WebPage` ([vos propres types](docs/content-types/custom-types)).
Vérifiez le résultat avec un validateur de données structurées après
avoir modifié un type.

## Plans du site

Deux plans du site à la racine, pour toutes les langues :

- `sitemap.xml` : chaque page, triée par adresse, avec son `<lastmod>` :
  l'`updated` de la page, sinon sa date pour un article ou un événement,
  sinon `site.updated`. Sur un site en plusieurs langues, chaque adresse
  énumère ses pages sœurs dans chaque langue, et `x-default`.
- `sitemap.txt` : les mêmes adresses, une par ligne.

Une page dont le `robots` contient `noindex` est écartée des deux, comme
la page 404 du site de départ. `robots.txt` indique `sitemap.xml` : donnez
aussi cette adresse aux consoles des moteurs de recherche.

## robots.txt

La construction en écrit deux, à partir de deux tables de la
configuration ([configuration](docs/reference/configuration)) :

- `robots.txt`, pour le site, à partir de `[robots]` : une ligne
  `Disallow:` par chemin de `robots.disallow`, par défaut `/txt/` et
  `/ansi/`, puis l'adresse du plan du site ;
- `txt/robots.txt`, le `robots.txt` de l'hôte en texte brut, qui sert
  `txt/` comme sa racine, à partir de `[robots_man]` : par défaut,
  `robots_man.disallow` vaut `/`, tout l'hôte.

Une liste vide écrit `Allow: /` à la place. Avec les valeurs par défaut :

```text
User-agent: *
Disallow: /txt/
Disallow: /ansi/

Sitemap: https://example.org/sitemap.xml
```

Les miroirs en texte doublent les pages : les moteurs de recherche sont
priés de n'indexer que les pages ([le miroir en texte](docs/reference/text-mirror)).

## Les vérifications de la construction

Après les pages de chaque langue, la construction vérifie chaque page,
sauf celles marquées `noindex`, et écrit une ligne sur sa sortie d'erreur
pour chaque problème :

```text
seo: about.html: title is 64 characters (max 60)
seo: about.html: description is 38 characters (50-160)
seo: blog/index.html: same title as about.html
seo: [fr] about.html: same description as index.html
```

| Avertissement | Quand |
|---|---|
| `title is N characters` | le `<title>`, suffixe compris, dépasse `seo.title_max`, `60` |
| `description is N characters` | la description est plus courte que `seo.description_min`, `50`, ou plus longue que `seo.description_max`, `160` |
| `same title as` | deux pages d'une même langue partagent un `<title>` |
| `same description as` | deux pages d'une même langue partagent une description |

Sur un site en plusieurs langues, chaque ligne nomme la langue de la
passe, `[fr]`. Un avertissement n'arrête pas la construction et ne
change pas son code de sortie : un site qui le veut, comme celui-ci, fait
échouer sa propre construction sur toute ligne `seo:`
([la ligne de commande](docs/reference/cli)). Les limites se changent
dans `[seo]` :

```toml
[seo]
title_max = 65
description_max = 155
```

## Voir aussi

- [écrire des pages](docs/guide/writing)
- [flux et images](docs/reference/feeds-and-images)
- [la configuration](docs/reference/configuration)
