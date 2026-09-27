---
title: Classes
description: Chaque classe que tilder écrit dans son HTML, regroupée comme dans son contrat, avec l'élément qui la porte, et l'accessibilité qui revient au thème.
order: 30
---

## Nom

classes - chaque classe écrite par la construction, à mettre en forme par le thème

La construction écrit du HTML sémantique avec un jeu fixe de noms de
classes, et jamais de style en ligne, de couleur ni de police : tout cela
revient au thème. Cette page donne ce jeu, regroupé comme dans le contrat
de tilder, avec l'élément qui porte chaque classe. Un thème qui les met
toutes en forme affiche correctement chaque page que tilder sait
construire ; `build.py --check` lui dit lesquelles il oublie.

[TOC]

## La page

| Classe | Sur | Rôle |
|---|---|---|
| `.sr-only` | `<span>` | obligatoire : du texte réservé aux lecteurs d'écran, à masquer visuellement. Les séparateurs du logotype, les mots qui remplacent la flèche d'un lien externe, le réseau d'un profil, « s'ouvre dans un nouvel onglet » |
| `.wordmark` | `<h1>` | le titre de la page, le logotype sous forme de chemin : `~/site/section/title` |
| `.tilde` | `<span>` | le `~/` du début, masqué aux lecteurs d'écran |
| `.slash` | `<span>` | chaque `/` entre deux segments, masqué aux lecteurs d'écran |
| `.here` | `<span>` | le segment propre à la page, le dernier |
| `.cursor` | `<span>` | un élément vide placé après, masqué aux lecteurs d'écran, pour un curseur |
| `.nav` | `<nav>` | la navigation du site, autour de `{{ nav }}` ; c'est le gabarit qui écrit cet élément (celui du site de départ : `<nav class="nav">`) |
| `.sep` | `<span>` | entre deux liens de `{{ nav }}`, un point médian masqué aux lecteurs d'écran |
| `.languages` | `<nav>` | le sélecteur de langue, `{{ languages }}` : un `<a>` par langue, l'actuelle marquée `aria-current="page"` |

Les segments du logotype situés entre le nom du site et celui de la page
mènent aux pages qu'ils nomment, quand elles existent ; sur la page
d'accueil, le logotype se réduit à `~/site` et au curseur.

## La navigation d'une collection

| Classe | Sur | Rôle |
|---|---|---|
| `.collection-nav` | `<nav>` | la barre latérale de la collection, `{{ collection_nav }}`, autour d'une `<ul>` de liens ; le lien de la page courante est `aria-current="page"` |
| `.collection-group` | `<li>` | un groupe d'éléments (leur `group:`), qui contient son libellé et une `<ul>` |
| `.collection-group-label` | `<span>` | le nom du groupe : un libellé, pas un titre |
| `.prev`, `.next` | `<a>` | `{{ prev }}` et `{{ next }}`, les liens vers les voisines, avec `rel="prev"` et `rel="next"` |
| `.prev-label`, `.next-label` | `<span>` | à l'intérieur, les mots `labels.prev` et `labels.next`, avant le titre de la voisine |

<!-- 1.2 -->

Une collection récursive imbrique ses dossiers dans la barre latérale,
sous forme de sections :

| Classe | Sur | Rôle |
|---|---|---|
| `.collection-section` | `<li>` | une section : son libellé, puis une `<ul>` de ses pages |
| `.collection-section--open` | `<li>` | ajoutée à la section qui contient la page courante, ce qui permet au thème de replier les autres |
| `.collection-section-label` | `<a>` ou `<span>` | le nom de la section : un lien vers sa propre page (son `index.md`), intitulé comme elle ; sans elle, un `<span>` avec le nom du dossier |

<!-- 1.2 -->

```html
<nav class="collection-nav" aria-label="In this section">
<ul>
	<li><a href="install">Install</a></li>
	<li class="collection-section collection-section--open"><a class="collection-section-label" href="guide">Guide</a>
	<ul>
		<li><a href="guide/writing" aria-current="page">Writing</a></li>
	</ul>
	</li>
</ul>
</nav>
```

## Sections et listes

| Classe | Sur | Rôle |
|---|---|---|
| `.s` | `<section>` | une section `##` de la page, qui contient son `<h2>` et son corps |
| `.b` | `<div>` | le corps de la section, après le `<h2>` |
| `.b.grid` | `<div>` | un corps marqué `{grid}`, ou une liste de membres : des entrées disposées en grille de cartes |
| `.members`, `.posts` | `<div class="b">` | un corps marqué `{members}` ou `{posts}`, qui liste cette collection |
| `.upcoming`, `.past`, `.next-event` | `<div class="b">` | un corps marqué `{upcoming}`, `{past}` ou `{next-event}`, qui liste des événements |
| `.entry` | `<div>` | une entrée : un `###` de la page, ou la carte d'un élément dans une liste, avec son titre en `<h3>` ; sur la page propre d'un élément, sa carte n'a pas de `<h3>`, le `<h1>` en tenant lieu |
| `.entry--next` | `<div class="entry">` | le prochain événement : la première carte de `{upcoming}`, la carte de `{next-event}` |
| `.entry--full` | `<div class="entry">` | un membre dont la capacité est atteinte, `full: yes` |
| `.entry--link` | `<div class="entry">` | une carte dont le titre est un lien vers la page de l'élément ; le thème peut étendre ce lien à toute la carte |
| `.meta` | `<p>` | la ligne de détails d'une entrée : une date, un auteur, un lieu, des pronoms..., chacun dans un `<span>` |
| `.tag` | `<span>` | une étiquette dans la ligne de détails : le `tag` d'un article, « à venir » ou « passé » pour un événement, la catégorie d'un membre |
| `.tag--next`, `.tag--full` | `<span class="tag">` | les étiquettes d'une carte `.entry--next` ou `.entry--full` |

Un marqueur qui nomme une collection, `{upcoming:meetups}`, donne la
classe sans ce nom : `upcoming`. Les mots des étiquettes et des états sont
toujours écrits : la carte d'un mentor complet le dit en toutes lettres
(le mot `full` de la collection), jamais par une couleur seule.

## Texte

| Classe | Sur | Rôle |
|---|---|---|
| `.small`, `.muted`, `.faint`, `.mono`, `.warn` | `<p>` | les classes qu'un auteur ajoute à la fin d'un paragraphe : `{small muted}` |
| `.empty` | `<p>` | l'état vide : une liste sans rien dedans, ou un paragraphe entièrement entre `*...*` |
| `.inset` | `<div>` | un encart `>`, qui contient des paragraphes |
| `.callout` | `<div role="note">` | un encadré, `> [!INFO]`, `[!WARNING]` ou `[!ERROR]` |
| `.callout--info`, `.callout--warning`, `.callout--error` | `<div class="callout">` | son genre |
| `.callout-label` | `<p>` | sa première ligne, le mot de son genre (`labels.info`...) |
| `u.u` | `<u>` | du texte `++souligné++` |

La [référence Markdown](docs/reference/markdown) montre chacune de ces
constructions, sa source et son rendu.

## Code

| Classe | Sur | Rôle |
|---|---|---|
| `pre.code` | `<pre tabindex="0">` | un bloc de code, autour d'un `<code>` ; il peut recevoir le focus, pour que le clavier le fasse défiler |
| `pre.code[data-lang]` | `<pre class="code">` | un bloc coloré : `data-lang` contient la langue telle qu'écrite, que le thème peut afficher (`content: attr(data-lang)`) ; le `<code>` intérieur est `language-<lang>` |
| `.hl-k` | `<span>` | un mot-clé |
| `.hl-b` | `<span>` | une fonction intégrée, un type, un littéral |
| `.hl-s` | `<span>` | une chaîne |
| `.hl-c` | `<span>` | un commentaire |
| `.hl-n` | `<span>` | un nombre |
| `.hl-v` | `<span>` | une variable |
| `.hl-p` | `<span>` | une invite, `$` ou `#` |
| `.hl-t` | `<span>` | une balise, une section, une clé |
| `.hl-gi`, `.hl-gd`, `.hl-gh` | `<span>` | dans un diff, une ligne ajoutée, une ligne supprimée, un en-tête de bloc |

Un bloc sans langue, ou dans une langue que tilder ne connaît pas, est un
simple `<pre class="code">`, sans `data-lang` ni jetons. Un diff garde ses
`+` et ses `-` : la couleur n'est jamais le seul signe.

## Tableaux, listes, figures

| Classe | Sur | Rôle |
|---|---|---|
| `.table` | `<div tabindex="0" role="region">` | l'enveloppe de chaque tableau, nommée par `labels.table`, pour qu'un tableau large défile seul au lieu de la page |
| `th.center`, `td.center` | `<th>`, `<td>` | une colonne alignée `:---:` |
| `th.right`, `td.right` | `<th>`, `<td>` | une colonne alignée `---:` ; l'alignement à gauche n'a pas de classe |
| `.tasks` | `<ul>` ou `<ol>` | une liste de tâches |
| `.task` | `<span role="img">` | la case d'une tâche, vide, nommée pour les lecteurs d'écran par `labels.task_done` ou `labels.task_todo` |
| `.task--done`, `.task--todo` | `<span class="task">` | son état, `[x]` ou `[ ]` |
| `.figure` | `<figure>` | une image seule sur sa ligne, avec sa `<figcaption>` quand elle a un titre |
| `.toc` | `<nav>` | un `[TOC]` : un `<details>` qui contient une `<ol>` des sections de la page, fermé par défaut |
| `.toc-label` | `<summary>` | le libellé du `[TOC]`, `labels.toc`, qui l'ouvre |
| `.profiles` | `<p>` | les liens de profil d'un membre |
| `.icon` | `<svg>` | le logo d'un réseau dans un lien de profil, tiré de `icons/<network>.svg`, masqué aux lecteurs d'écran |

## L'accessibilité qui revient au thème

La construction écrit le balisage : un seul `<h1>`, des `<h2>` pour les
sections et des `<h3>` pour les entrées, les textes alternatifs (elle
avertit quand une image n'en a pas), les libellés et les attributs
`aria-*`, des zones défilantes qui reçoivent le focus, un mot à côté de
chaque couleur. Le reste revient au thème :

- **Le contraste** : au moins 4,5:1 pour le texte, sur son fond, dans
  chaque jeu de couleurs que propose le thème.
  [Vérifier un thème](docs/themes/checking) mesure les paires qu'un thème
  déclare.
- **Le focus** : un contour visible sur tout ce qui reçoit le focus, les
  liens, le résumé du `[TOC]`, les `pre.code` et `.table` focalisables.
- **Le texte masqué** : `.sr-only` est masqué à l'écran, mais lu.
  `display: none` le cacherait aussi aux lecteurs d'écran ; la règle
  habituelle :

```css
.sr-only {
	position: absolute; width: 1px; height: 1px; overflow: hidden;
	clip-path: inset(50%); white-space: nowrap;
}
```

- **Les animations réduites** : aucune animation, ou aucune sous
  `@media (prefers-reduced-motion: reduce)`, pour le curseur du logotype
  comme pour le reste.

## Voir aussi

- [vérifier un thème](docs/themes/checking)
- [gabarits et variables](docs/themes/layouts)
- [la référence Markdown](docs/reference/markdown)
