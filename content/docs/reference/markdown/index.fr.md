---
title: La référence Markdown
description: Le dialecte Markdown de tilder sur une page : ses principes, un aide-mémoire de chaque construction, et ce qu'il laisse de côté exprès.
order: 10
---

## Nom

markdown - le dialecte que lit tilder, construction par construction

Chaque page d'un site tilder est un fichier Markdown, écrit dans un
dialecte court et strict, avec quelques ajouts pour la mise en page de
manuel. Cette page le résume ; les cinq pages suivantes reprennent
chaque famille de constructions, et montrent chacune deux fois : sa
source, puis la construction elle-même, rendue sur la page par la
construction qui rend tout le reste du site.

[TOC]

## Principes

- **Une liste courte, pas CommonMark.** tilder lit les constructions de
  cette référence, et rien d'autre. Tout le reste est imprimé en texte
  brut, tel qu'il est écrit, jamais deviné.
- **Deux rendus.** Chaque construction est rendue deux fois à partir de
  la même source : en HTML pour le site, et en texte ASCII de 75
  colonnes pour le [miroir en texte](docs/reference/text-mirror) que
  reçoit un terminal. Chaque page de cette référence dit à quoi
  ressemblent les deux.
- **Une ligne vide sépare les blocs.** Un titre `##` ou `###` tient
  seul, ligne vide ou non ; tout autre bloc s'arrête à la ligne vide
  suivante.
- **Une page est une page de manuel.** Les titres `##` en sont les
  sections, les titres `###` les entrées qu'elles contiennent, et elle
  s'ouvre sur `## Nom` ([écrire des pages](docs/guide/writing)).

## Aide-mémoire

| Source | HTML | Miroir en texte |
|---|---|---|
| `## Titre {#id} {html} {text} {grid}` | `<section class="s">`, `<h2>` | `TITRE` contre la marge |
| `## Titre {posts}`, `{upcoming:nom}`... | la section, remplie des cartes d'une collection | les cartes, en entrées |
| `### Titre {next} {full}` | `.entry`, `.entry--next`, `.entry--full` | le titre, en retrait, sa première étiquette à droite |
| une liste juste après `###` | la ligne `.meta` de l'entrée | une ligne par élément |
| `- AAAA-MM-JJ \| date` dans la ligne meta | `<time>` | la date en toutes lettres |
| `- élément`, `1. élément`, imbriqués par le retrait | `<ul>`, `<ol>` | `  - élément`, `  1. élément` |
| `- [ ] à faire`, `- [x] fait` | `.tasks`, une case | `  - [ ] à faire` |
| `[TOC]` seul sur sa ligne | `.toc`, replié | une liste numérotée des sections |
| `---` seul sur sa ligne | `<hr>` | une ligne de tirets |
| `> texte` | `.inset` | en retrait |
| `> [!INFO]`, `[!WARNING]`, `[!ERROR]` | `.callout` | un cadre ASCII, l'étiquette dans son filet du haut |
| une clôture d'accents graves, avec un langage | `<pre class="code">`, coloré | encadré, tel quel |
| `\| a \| b \|` puis `\|---\|---\|` | `<table>` dans un conteneur qui défile | des colonnes alignées, ou des fiches |
| `![alt](fichier "légende")` seul sur sa ligne | `<figure>`, `<img>` | `[ image ] alt`, la légende, le chemin |
| `*texte*`, le paragraphe entier | `.empty` | brut |
| `texte {small muted}` | `<p class="small muted">` | brut |
| `<!-- ... -->` | recopié tel quel | omis |
| `[libellé](cible)` | `<a>` | le libellé, et une URL externe |
| `**g**`, `*i*`, `_i_` | `<b>`, `<em>` | le texte |
| `~~b~~`, `++s++` | `<del>`, `<u class="u">` | `~~b~~`, le texte |
| un mot entre accents graves | `<code>` | le mot |

## Les pages

[Sections](docs/reference/markdown/sections) : les titres `##`,
l'identifiant de chacun, et les marqueurs entre accolades qui changent
une section : `{#id}`, `{html}`, `{text}`, `{grid}` et les marqueurs de
liste.

[Blocs](docs/reference/markdown/blocks) : les paragraphes et leurs
classes, l'état vide, les listes et les listes de tâches, la table des
matières, les filets, les encadrés et les alertes, les blocs de code, les
tableaux et les commentaires.

[Entrées](docs/reference/markdown/entries) : les titres `###`, leur
ligne meta de dates et d'étiquettes, leur corps en retrait et leurs
marqueurs.

[Balisage en ligne](docs/reference/markdown/inline) : le gras,
l'italique, le texte barré et souligné, le code, et ce qui reste
littéral.

[Liens et images](docs/reference/markdown/links-and-images) : les cibles
écrites depuis la racine du site, les ancres, les liens d'une langue à
l'autre et vers d'autres sites ; les images, leur texte de remplacement
et leurs légendes.

## Ce qui n'est pas pris en charge

Exprès : chaque construction coûte deux rendus, et chacune de celles que
lit tilder doit être juste dans un navigateur comme dans un terminal.

- Les titres autres que `##` et `###` : une ligne qui commence par `#`
  ou `####` est un paragraphe ordinaire, imprimé tel quel.
- Les notes de bas de page, les listes de définitions, les liens par
  référence et les URL nues : une adresse n'est un lien que si elle
  s'écrit `[libellé](cible)`.
- Les images au milieu d'une phrase, et le HTML brut : une image est un
  bloc à elle seule, et le HTML dans le texte s'affiche en texte,
  échappé. Seul un bloc qui commence par `<!--` passe tel quel dans la
  page.
- L'échappement par barre oblique inverse : `\*` imprime aussi la barre.
  Reformulez plutôt. La seule exception est `\|`, une barre verticale
  dans une cellule de tableau.
- Le balisage en ligne dans le balisage en ligne : `**[un lien](docs/)**`
  est du texte en gras, pas un lien en gras.
- Les listes, le code ou les tableaux dans un encadré : un encadré
  contient des paragraphes.
- Les scripts dans le contenu. Les scripts du thème sont joints par la
  construction, sur les pages qui en ont besoin
  ([scripts](docs/themes/scripts)).

## Voir aussi

- [écrire des pages](docs/guide/writing)
- [le miroir en texte](docs/reference/text-mirror)
- [les classes](docs/themes/classes)
