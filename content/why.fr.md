---
man: TILDER-WHY(7)
title: Pourquoi tilder
description: Les principes de tilder, ce qu'il laisse de côté à dessein face à Hugo, Jekyll et Eleventy, et quand c'est le bon outil.
tagline: les principes, et ce que tilder ne fait pas
nav: why
---

## Nom

why - les principes de tilder

tilder génère des sites qui se lisent comme une page de manuel, dans un
navigateur comme dans un terminal. Il en fait peu, et c'est voulu : chaque
page est écrite une fois, rendue deux fois, et servie sans rien aller
chercher ailleurs. Cette page explique pourquoi, ce que cela coûte, et
quand un autre outil vous conviendra mieux.

[TOC]

## Principes

### 75 colonnes

  Une page de manuel est une colonne de texte qu'un terminal affiche sans
  retour à la ligne. tilder garde cette largeur : le miroir en texte de
  chaque page tient sur 75 colonnes, code compris, ce qui laisse de la
  place, dans un terminal de 80 colonnes, pour une barre de défilement, la
  marge d'un pager ou une citation dans un courriel. Le thème de ce site
  garde la même mesure dans le navigateur : une page se lit de la même
  façon des deux côtés.

### Deux rendus pour tout

  Chaque page s'écrit une fois, en Markdown, et se génère deux fois : en
  HTML pour le navigateur, en texte ASCII pour le terminal, avec un double
  en couleurs. Les deux viennent de la même source et ne peuvent donc pas
  diverger. Une construction n'est prise en charge que lorsqu'elle se rend
  des deux façons ; le texte est la moitié du produit, pas un à-côté.
  `curl` reçoit le texte à la place du HTML.

### Rien d'un tiers

  Une page générée ne charge rien depuis un autre site : ni CDN, ni service
  de polices, ni script distant, ni iframe, ni image distante. Polices,
  styles et scripts sont les fichiers du thème, servis par votre serveur.
  Les liens vers d'autres sites sont permis ; y charger quoi que ce soit ne
  l'est pas.

### Aucun JavaScript nécessaire

  Chaque page se lit en entier sans JavaScript. Les scripts appartiennent
  au thème et ne font qu'ajouter : sur ce site, un bouton pour copier le
  code et la recherche dans la documentation. Chacun crée lui-même ses
  commandes ; sans lui, rien ne manque et rien n'est cassé.

### Aucun pistage

  Ni mesure d'audience, ni cookies, ni formulaires, ni code côté serveur :
  le résultat n'est que des fichiers statiques. Le Caddyfile d'exemple va
  plus loin et jette les journaux d'accès : une visite ne laisse pas non
  plus de trace sur le serveur.

### La bibliothèque standard, rien d'autre

  tilder est écrit en Python avec sa seule bibliothèque standard : rien à
  installer, ni gestionnaire de paquets, ni framework, ni préprocesseur.
  Les outils extérieurs ne servent qu'à dessiner les icônes et l'image de
  partage, et sont facultatifs : `rsvg-convert`, avec `woff2_decompress`
  pour que l'image de partage prenne les polices du thème, sinon
  ImageMagick ; sans l'un ni l'autre, ces images sont omises avec un
  avertissement. L'image Docker contient `rsvg-convert` et
  `woff2_decompress`.

### Accessibilité

  Un seul `<h1>` par page, des titres dans l'ordre, des repères, des
  libellés, un texte alternatif obligatoire, des blocs de code et des
  tableaux atteignables au clavier. Un lecteur d'écran signale les liens
  qui quittent le site ou ouvrent un onglet, et aucun sens ne repose sur la
  seule couleur. Le contraste et le focus relèvent du thème : le thème de
  départ et celui de ce site respectent le niveau AA des WCAG.

## Ce que tilder ne fait pas

Hugo, Jekyll et Eleventy sont des générateurs de sites statiques mûrs et
polyvalents, chacun avec une large communauté. Ils savent construire
presque n'importe quel site, et grandissent avec lui. tilder construit un
seul genre de site et laisse de côté une bonne part de ce qu'ils
proposent :

- **Pas de langage de gabarits.** Le `layout.html` d'un thème est du HTML
  simple, avec des emplacements comme `{{ title }}` remplis à la
  génération : ni boucles, ni conditions, ni inclusions. Les autres offrent aux thèmes un vrai langage
  de gabarits.
- **Pas d'écosystème d'extensions.** Il n'y a rien à installer. La seule
  façon d'étendre tilder est un type de contenu : un module Python dans le
  thème, qui ajoute ses propres éléments, listes et marqueurs.
- **Pas de chaîne de traitement des ressources.** Ni Sass, ni
  regroupement, ni minification, ni redimensionnement d'images. Les
  fichiers du thème et les images posées à côté d'une page sont servis
  tels quels ; la génération lit la taille d'une image et ne dessine que
  les icônes et l'image de partage.
- **Pas de shortcodes.** Les seuls ajouts à Markdown sont des marqueurs
  entre accolades, comme `{grid}` sur une section ou `{small}` sur un
  paragraphe ; les marqueurs d'une collection, comme `{posts}`, placent sa
  liste dans une page.
- **Pas de HTML brut dans le Markdown.** Tout ce qui ne fait pas partie du
  dialecte est échappé et affiché comme du texte ; seul un commentaire
  HTML passe, et seulement dans le HTML.
- **Un dialecte restreint.** Les titres sont `##` et `###`, rien d'autre ;
  pas de notes de bas de page, de listes de définitions, de liens par
  référence, d'URL nues, d'images dans une phrase ni d'échappements.
  Chaque construction coûte deux rendus : la liste reste courte.
- **Ni pagination, ni pages d'étiquettes.** Une collection est listée en
  entier, dans l'ordre que donne son type : les plus récents d'abord, à
  venir puis passés, ou un ordre que vous fixez.
- **Un schéma simple pour les langues.** Une traduction est le même
  fichier avec un suffixe de langue, `why.fr.md` à côté de `why.md`, et
  les mots de l'interface d'une langue tiennent dans son propre fichier
  TOML. Pas de clés de traduction dans les pages, pas de dossier par
  langue dans `content/`.

Si un site a besoin de l'un de ces points, mieux vaut choisir l'un des
autres.

## Quand l'utiliser

tilder convient à un site fait surtout de texte : une documentation, les
pages d'un projet, des notes de version, une petite association avec ses
événements et ses membres, une page personnelle. Il convient quand vous
voulez que le site se lise dans un terminal comme dans un navigateur, ne
charge rien d'ailleurs, et se génère avec Python pour seul outil.

Il ne convient pas à un site qui demande une mise en page riche d'une page
à l'autre, des médias intégrés depuis d'autres services, des applications
côté client, ou un vaste catalogue avec pagination et étiquettes. Là, les
contraintes qui rendent tilder simple deviennent un obstacle.

## Voir aussi

- [bien démarrer](docs/guide/getting-started)
- [la documentation](docs/)
- [tilder sur GitHub ↗](https://github.com/THOSTED/tilder)
