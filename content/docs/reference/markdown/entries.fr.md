---
title: Entrées
description: Les titres ### d'une section : un événement, une personne, une carte. Leur ligne meta de dates et d'étiquettes, leur corps en retrait, leurs marqueurs.
order: 30
---

## Nom

entries - les titres `###`, leur ligne meta, leur corps et leurs marqueurs

Une entrée est un titre `###` dans une section : une conférence d'un
programme, une personne d'une liste, une carte d'une grille. Elle peut
porter une ligne meta de dates, de lieux et d'étiquettes, et un corps de
blocs en retrait sous elle. Les cartes qu'une collection écrit dans une
liste sont aussi des entrées, bâties de la même façon. Chaque exemple
ci-dessous est suivi de l'entrée qu'il produit.

[TOC]

## Une entrée

Un titre `###` ouvre une entrée dans la section en cours. Les blocs de
son corps sont en retrait de deux espaces ; le premier bloc qui n'est pas
en retrait termine l'entrée, et la page revient à la section.

```text
### Rencontre de printemps

  Trois conférences et un atelier, ouverts à tous.

De retour dans la section, après l'entrée.
```

Voici le rendu de cette source.

### Rencontre de printemps

  Trois conférences et un atelier, ouverts à tous.

De retour dans la section, après l'entrée.

Le titre peut contenir du balisage en ligne, un lien par exemple. Une
entrée n'a pas d'identifiant à elle : pour y mener, liez sa section. Les
entrées ne s'imbriquent pas : un titre `####` n'en est pas une.

Dans le miroir en texte, le titre est imprimé au retrait de la section et
le corps quatre espaces plus loin.

## La ligne meta

Une liste juste après le titre, en retrait comme le corps, est la ligne
meta de l'entrée et non une liste. Chaque élément est de l'un de trois
genres :

| Élément | Sur la page web | Dans le miroir en texte |
|---|---|---|
| un mot entre accents graves | une étiquette, dans un petit cadre | la première étiquette, à droite de la ligne du titre |
| `AAAA-MM-JJ \| date en toutes lettres` | `<time datetime="AAAA-MM-JJ">`, qui affiche la date en toutes lettres | la date en toutes lettres |
| tout autre texte | un élément simple | une ligne à lui |

```text
### Rencontre d'automne

  - 2026-10-17 | samedi 17 octobre 2026
  - Grande salle, 1 rue de l'Exemple, Exempleville
  - `conférences`

  Deux conférences, puis des questions.
```

Voici le rendu de cette source.

### Rencontre d'automne

  - 2026-10-17 | samedi 17 octobre 2026
  - Grande salle, 1 rue de l'Exemple, Exempleville
  - `conférences`

  Deux conférences, puis des questions.

Sur la page web, les éléments tiennent sur une ligne, séparés par des
points. La partie avant ` | ` va telle quelle dans l'attribut
`datetime` : écrivez la date sous la forme `AAAA-MM-JJ`. Les éléments de
la ligne meta sont du texte brut : un lien ou du gras s'y affiche tel
qu'il est écrit. Seule la première étiquette passe dans le miroir en
texte.

Pour un élément d'une collection, la construction écrit elle-même cette
ligne, à partir de l'en-tête ([types de contenu](docs/content-types)).

## Marqueurs

Comme une section, le titre d'une entrée peut se terminer par des
marqueurs entre accolades. Chacun devient une classe de l'entrée,
`entry--<marqueur>` ; trois d'entre eux ont un sens pour tilder et pour
tout thème.

| Marqueur | Classe | Effet |
|---|---|---|
| `{next}` | `.entry--next` | l'étiquette de l'entrée dans la couleur d'accent : le prochain événement |
| `{full}` | `.entry--full` | l'étiquette de l'entrée dans la couleur d'avertissement : un mentor qui n'a plus de place |
| `{link}` | `.entry--link` | une carte dont le lien du titre couvre toute la carte |
| tout autre mot | `.entry--<mot>` | une classe pour le thème |

```text
### Rencontre d'hiver {next}

  - `prochain`

### Permanence {full}

  - `complet`

### [Types de contenu](docs/content-types) {link}

  Les collections, et les types qui leur donnent forme.
```

Voici le rendu de cette source.

### Rencontre d'hiver {next}

  - `prochain`

### Permanence {full}

  - `complet`

### [Types de contenu](docs/content-types) {link}

  Les collections, et les types qui leur donnent forme.

`{next}` et `{full}` ne changent que l'étiquette ; la carte elle-même
ressemble à toutes les autres. La construction les pose sur les cartes
qu'elle écrit : `{next}` sur le premier événement d'une liste
`{upcoming}`, `{full}` sur un membre dont l'en-tête dit `full: yes`. Elle
pose `{link}` sur les cartes des articles et des événements d'une liste,
dont le titre mène à la page de l'élément ; la dernière entrée ci-dessus
est une telle carte, cliquable partout. Dans une section marquée
`{grid}`, les entrées sont disposées en cartes côte à côte
([sections](docs/reference/markdown/sections#cartes)).

Le thème de ce site met en forme un marqueur de plus, `{example}` : le
cadre pointillé marqué `Rendu` autour de chaque exemple vivant de la
page des [blocs](docs/reference/markdown/blocks).

```text
### Rendu {example}

  | un exemple | vivant |
  |---|---|
  | d'un | tableau |
```

## Le corps

Tout bloc peut entrer dans le corps d'une entrée : paragraphes, listes,
encadrés, code, tableaux, images. Chacun est en retrait de deux espaces,
ses lignes suivantes comprises, et des lignes vides les séparent comme
partout ailleurs.

```text
### Version 2.0

  - `version`

  Une nouvelle mise en page du programme.

  > [!INFO]
  > Lisez les notes avant de mettre à jour.

  - une liste après le premier bloc est une liste
  - et non une ligne meta
```

Voici le rendu de cette source.

### Version 2.0

  - `version`

  Une nouvelle mise en page du programme.

  > [!INFO]
  > Lisez les notes avant de mettre à jour.

  - une liste après le premier bloc est une liste
  - et non une ligne meta

Une liste n'est la ligne meta que si elle vient en premier, juste après
le titre. Un corps qui doit s'ouvrir sur une liste commence par un autre
bloc avant elle : une phrase, ou un
[commentaire](docs/reference/markdown/blocks#commentaire), que personne
ne voit.

## Voir aussi

- [les sections](docs/reference/markdown/sections)
- [les blocs](docs/reference/markdown/blocks)
- [les types de contenu](docs/content-types), pour les cartes d'une liste
- [les classes](docs/themes/classes)
