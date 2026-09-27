---
title: Navigation
description: L'ordre des pages d'une collection, leurs groupes et leurs sections, la barre latérale, les liens vers la page précédente et suivante, leur ligne en texte.
order: 60
---

## Nom

navigation - l'ordre d'une collection, sa barre latérale et ses voisins

Les pages d'une collection ont un ordre, fixé par leur type. Un thème le
montre de trois façons : une barre latérale de toutes les pages, groupées
et imbriquées, des liens vers la page précédente et la suivante, et, dans
le miroir en texte, une ligne qui nomme les deux. Ce manuel est construit
ainsi : la barre latérale à gauche, les liens au pied de chaque page.

[TOC]

## L'ordre

L'ordre d'une collection est la `sort_key` de son type, appliquée à
chaque élément ; sans elle, l'ordre des identifiants. Les articles et les
événements sont nommés par leur date, si bien que leurs identifiants se
trient par date ; leurs listes lisent ensuite cet ordre à rebours, du plus
récent au plus ancien. Les membres se trient par catégorie, puis par nom.
La barre latérale, les voisins, la ligne en texte et les listes partent
tous de cet ordre.

La documentation de ce site utilise le type `doc` de son thème, dont
l'ordre est la clé d'en-tête `order`, un nombre entier, puis
l'identifiant :

```text
---
title: Getting started
description: Install tilder, build the starter site, look around.
order: 10
---
```

Une page sans `order` compte pour `1000`, après les pages numérotées.
`order` est une clé du type `doc`, pas de tilder : un autre type trie
selon ce que lit sa `sort_key`
([vos propres types](docs/content-types/custom-types)). Une traduction
garde l'`order` de son original, pour que les deux langues listent les
pages de la même façon.

## Les groupes

Un élément peut fixer `group` dans son en-tête. La barre latérale
rassemble alors les éléments de chaque groupe sous le libellé du groupe :
d'abord les éléments sans groupe, puis chaque groupe dans l'ordre de son
premier élément, les éléments d'un groupe dans l'ordre de la collection.

```text
---
title: Deployment
description: Put a site online: Docker, compose, Caddy, others.
group: Serving
---
```

Le libellé d'un groupe est comparé tel qu'il est écrit, langue par
langue : tous les fichiers français d'un groupe doivent écrire leur
`group` de la même façon, sinon la barre latérale montre deux groupes.
Les voisins ignorent les groupes.

## Les sections

Dans une collection récursive (tilder 1.2), les dossiers sont des
sections, comme le sont les sections de ce manuel. L'ordre va en
profondeur d'abord : dans un dossier, ses éléments et ses sections sont
triés par `sort_key`, une section d'après sa propre page, son `index.md`
ou un `<name>.md` à côté du dossier (une section qui n'en a pas vient
après, par nom de dossier) ; la page d'une section vient d'abord, puis les
pages qu'elle contient. Ainsi `order: 20` dans
`content/docs/content-types/index.md` place la section entière, et
`order: 10` dans `content/docs/content-types/page.md` place la page à
l'intérieur.

La barre latérale imbrique les sections, chacune avec pour libellé le
titre de sa propre page, en lien, ou le nom de son dossier quand elle n'en
a pas. `group` fonctionne à tous les niveaux. Les voisins et la ligne en
texte suivent le même ordre en profondeur d'abord : la dernière page
d'une section mène à ce qui la suit, la page suivante du dossier parent ou
la page de la section suivante.

## La barre latérale

La variable `{{ collection_nav }}` du gabarit est la barre latérale de la
collection : chaque élément, dans l'ordre, groupé, la page courante
marquée par `aria-current="page"`. Elle apparaît sur les éléments de la
collection et, sans rien de marqué, sur la page de la collection
elle-même ; elle est vide ailleurs.

```html
<nav class="collection-nav" aria-label="In this section">
<ul>
	<li><a href="start">Getting started</a></li>
	<li class="collection-group"><span class="collection-group-label">Serving</span>
	<ul>
		<li><a href="deployment" aria-current="page">Deployment</a></li>
	</ul>
	</li>
</ul>
</nav>
```

Avec des sections (tilder 1.2), une section est un élément de liste de
classe `.collection-section` qui contient son libellé et une liste
imbriquée ; la section de la page courante ajoute
`.collection-section--open`, pour qu'un thème puisse replier les autres.
Le libellé, `.collection-section-label`, est un lien vers la page de la
section, ou un `<span>` pour une section qui n'en a pas.

Le `<nav>` est nommé pour les lecteurs d'écran par le `nav_label` de la
collection, sinon par `labels.collection_nav`, `"In this section"` par
défaut :

```toml
[collections.docs]
type = "doc"
nav_label = "In the manual"
```

Ses classes sont `.collection-nav`, `.collection-group` et
`.collection-group-label`, et les voisins ci-dessous ajoutent `.prev`,
`.prev-label`, `.next` et `.next-label` : la page
[classes](docs/themes/classes) les liste toutes, et
[gabarits](docs/themes/layouts) dit où placer les variables.

## Précédent et suivant

`{{ prev }}` et `{{ next }}` relient une page à ses voisines dans l'ordre,
sans tenir compte des groupes :

```html
<a class="prev" rel="prev" href="writing"><span class="prev-label">previous</span> Writing pages</a>
<a class="next" rel="next" href="deployment"><span class="next-label">next</span> Deployment</a>
```

Chacune est vide à son bout de la collection, sur la page de la
collection elle-même et sur toute page hors d'une collection. Les
libellés sont `labels.prev`, `"previous"`, et `labels.next`, `"next"`,
traduits dans le `site.<lang>.toml` de chaque langue
([configuration](docs/reference/configuration)).

## La ligne en texte

Un type qui fixe `SEQUENTIAL = True` donne au miroir en texte de chaque
élément une ligne de plus, juste avant le pied de page : la page
précédente à gauche, la suivante à droite, chacune avec son libellé.

```text
previous: Writing pages                                     next: Languages
```

La ligne fait 75 colonnes au plus, en ASCII. Quand les deux côtés ne
tiennent pas, chacun garde la moitié de la largeur et un titre qui dépasse
sa moitié est coupé par `...` ; un côté court laisse sa place à l'autre.
La première page n'a que `next:`, la dernière que `previous:`. Le type
`doc` de ce site fixe `SEQUENTIAL`, pour que `curl` puisse parcourir le
manuel de page en page.

## Voir aussi

- [les collections](docs/content-types)
- [vos propres types](docs/content-types/custom-types)
- [gabarits](docs/themes/layouts)
- [le miroir en texte](docs/reference/text-mirror)
