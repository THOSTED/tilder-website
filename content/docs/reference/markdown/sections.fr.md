---
title: Sections
description: Les titres ## d'une page : les rangées de manuel qu'ils dessinent, l'identifiant de chacun, et chaque marqueur entre accolades qui change une section.
order: 10
---

## Nom

sections - les titres `##`, leurs identifiants et leurs marqueurs

Une page est une suite de sections, comme une page de manuel. Chacune
commence à un titre `##` et court jusqu'au suivant ; des marqueurs entre
accolades, à la fin du titre, lui donnent un identifiant, la réservent à
une seule sortie, la disposent en grille de cartes ou la remplissent
depuis une collection. Les sections de cette page servent elles-mêmes
d'exemples : chaque marqueur ci-dessous est employé par une section que
vous voyez, ou, pour l'un d'eux, que vous ne voyez pas.

[TOC]

## Une section

Un titre `##` ouvre une section, et tout ce qui suit, jusqu'au `##`
suivant, lui appartient. Sur la page web, la section est une rangée de
la page de manuel : son nom dans la marge de gauche, son contenu à côté.
Dans le miroir en texte, le nom est imprimé en capitales contre la marge
et le contenu en retrait de cinq espaces en dessous.

```markdown
## Nom

sections - les titres `##`, leurs identifiants et leurs marqueurs

Une page est une suite de sections, comme une page de manuel.
```

Cette source est le début de cette page. Les pages s'ouvrent sur
`## Nom`, une ligne `nom - résumé`, puis un paragraphe qui résume la page
([écrire des pages](docs/guide/writing)) ; tilder ne l'exige pas, mais
c'est ainsi qu'une page de manuel se lit.

Un titre `##` tient seul, avec ou sans ligne vide autour. Seuls `##` et
`###`, suivis d'une espace, sont des titres : une ligne qui commence par
`#`, `####` ou `##Titre` est un paragraphe, imprimé tel quel. Le titre
d'une section est lui aussi imprimé tel quel, sans balisage en ligne :
`**gras**` y garde ses astérisques, sur la page, dans la table des
matières et dans le miroir en texte.

Ce qui précède le premier `##` d'un fichier est rendu en haut de la page
web, hors de toute section, et omis du miroir en texte.

## Identifiants {#ids}

Chaque section reçoit un identifiant, pour qu'un lien puisse y mener.
Par défaut, il vient du titre : les accents ramenés à l'ASCII, en
minuscules, chaque suite d'autres caractères remplacée par un tiret.
`## Les identifiants` donne `les-identifiants` ; une deuxième section du
même titre donne `les-identifiants-2`.

`{#id}` à la fin du titre fixe l'identifiant :

```markdown
## Identifiants {#ids}
```

Cette section s'écrit ainsi : son identifiant est `ids`, et
[ce lien](#ids) y mène depuis cette page, comme
`docs/reference/markdown/sections#ids` depuis n'importe quelle autre. Un
identifiant fixe garde les liens valables quand le titre est reformulé
ou traduit : la page anglaise emploie le même.

## Marqueurs

Un titre peut se terminer par des marqueurs entre accolades : un par
paire d'accolades, ou plusieurs séparés par des espaces, dans n'importe
quel ordre.

```markdown
## Contact {#write}
## Membres {members} {#team}
## À venir {upcoming:talks grid}
```

| Marqueur | Effet |
|---|---|
| `{#id}` | l'identifiant de la section, au lieu de celui tiré du titre |
| `{html}` | sur la page web seulement : le miroir en texte omet la section |
| `{text}` | dans le miroir en texte seulement : la page web omet la section |
| `{grid}` | dispose les entrées de la section en grille de cartes |
| `{posts}`, `{upcoming}`, `{past}`, `{next-event}`, `{members}` | remplit la section depuis une collection (plus bas) |
| un marqueur d'un type du thème | remplit la section depuis une collection de ce type, comme le `{docs}` de ce site |
| tout autre mot | une classe sur le corps de la section |

La section suivante de cette page s'écrit `## Cartes {grid}` : ses trois
entrées sont disposées en cartes, côte à côte si la page est assez
large, l'une sous l'autre sur un téléphone. Chaque bloc d'une section en
grille est une case de la grille : une telle section ne contient en
général que des entrées. Dans le miroir en texte, une grille est une
liste d'entrées comme une autre.

## Cartes {grid}

### Première carte

  Chaque entrée `###` d'une section `{grid}` est une carte.

### Deuxième carte

  Les cartes se partagent la largeur de la colonne.

### Troisième carte

  Une [entrée](docs/reference/markdown/entries) garde sa ligne meta et
  son corps dans une carte.

## Une seule sortie

`{text}` réserve une section au miroir en texte, et `{html}` à la page
web. Servez-vous-en pour ce qui n'a de sens que dans une sortie : une
remarque sur `curl` pour les lecteurs du terminal, une section bâtie
autour d'une image pour le navigateur.

```markdown
## Dans le terminal {text}

Vous lisez le miroir en texte.

## Dans le navigateur {html}

Cette section n'est pas dans le miroir en texte.
```

Ces deux sections suivent, écrites comme ci-dessus. Sur cette page web,
vous ne voyez que la seconde ; dans un terminal,
`curl tilder.thosted.fr/fr/docs/reference/markdown/sections` n'imprime
que la première. La table des matières de chaque sortie ne donne que ses
propres sections.

## Dans le terminal {text}

Vous lisez le miroir en texte : la page web n'a pas cette section.

## Dans le navigateur {html}

Cette section n'est que sur la page web : le miroir en texte l'omet.

## Marqueurs de liste

Une section dont le titre se termine par le marqueur d'un type est
remplie par la construction avec les cartes d'une collection, une par
élément : le titre et son marqueur sont tout ce que vous écrivez.

```markdown
## Articles {posts}

## À venir {upcoming:talks}

## Pages {docs}
```

| Marqueur | Remplit la section avec |
|---|---|
| `{posts}` | les articles, du plus récent au plus ancien |
| `{upcoming}` | les événements datés d'aujourd'hui ou plus tard, du plus proche au plus lointain |
| `{past}` | les événements antérieurs à aujourd'hui, du plus récent au plus ancien |
| `{next-event}` | le prochain événement seulement |
| `{members}` | les membres, en grille |

Un marqueur peut nommer sa collection, `{upcoming:talks}` ; un marqueur
seul liste la collection de ce type à laquelle appartient la page, sinon
la première déclarée. Les blocs écrits sous le titre restent, après les
cartes. La dernière ligne de la source ci-dessus est celle par laquelle
l'[accueil de la documentation](docs/) liste ces pages : `{docs}` est le
marqueur du type de thème de ce site. Chaque marqueur, et ce qu'affiche
une liste vide, se trouvent sur la page des
[types de contenu](docs/content-types).

## Classes

Un marqueur qui ne dit rien à tilder devient une classe sur le corps de
la section, le `<div class="b">` à côté du titre, que le thème met en
forme. `{grid}` est lui aussi une telle classe, et un marqueur de liste
ajoute son propre mot, sans le nom de la collection : `{upcoming:talks}`
donne `.upcoming`.

```markdown
## Partenaires {wide}
```

Le corps de cette section est `<div class="b wide">`. Les classes qu'un
thème met en forme sont listées sur la page des
[classes](docs/themes/classes).

## Voir aussi

- [les entrées](docs/reference/markdown/entries), les titres `###` d'une
  section
- [écrire des pages](docs/guide/writing)
- [les types de contenu](docs/content-types), pour les marqueurs de liste
