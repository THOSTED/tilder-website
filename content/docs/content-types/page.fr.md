---
title: page
description: Le type page : tout fichier Markdown hors d'une collection, sans réglage, sans carte ni liste, décrit aux moteurs de recherche comme une WebPage.
order: 10
---

## Nom

page - le type de toute page hors d'une collection

Tout fichier Markdown qui n'est pas l'élément d'une collection est une
`page` : la page d'accueil, une page « à propos », la page d'une
collection qui porte sa liste, la page 404. Le type n'ajoute rien à ce
que la page écrit. Il n'a aucun réglage, ne donne de carte à aucune liste
et n'écrit aucun flux.

[TOC]

## En-tête

Une page dit tout elle-même : `man`, `title`, `description`, `tagline` et
`nav` s'écrivent dans son en-tête, puisqu'aucune collection ne les lui
fournit. Toutes les clés d'[écrire des pages](docs/guide/writing)
s'appliquent.

```text
---
man: MYSITE-ABOUT(7)
title: About
description: Who writes this site and why, and how to reach them.
tagline: who, why and how to write
nav: about
---
```

## Ce que fait le type

- **Gabarit.** `layouts/page.html` du thème s'il existe, sinon
  `layout.html` ; la clé `layout:` d'une page en choisit un autre
  ([gabarits](docs/themes/layouts)).
- **Carte.** Aucune : une page n'apparaît jamais dans une liste.
- **Données structurées.** Un nœud `WebPage`, avec le titre et la
  description de la page, rattaché au `WebSite` du site
  ([référencement](docs/reference/seo)).
- **Open Graph.** `og:type` vaut `website`.

Un thème peut remplacer ce type, comme tout type fourni, en livrant un
module nommé `page` dans `theme/types/`
([vos propres types](docs/content-types/custom-types)).

## Voir aussi

- [écrire des pages](docs/guide/writing)
- [les collections](docs/content-types)
- [post](docs/content-types/post)
