---
title: Scripts
description: Les scripts qu'un thème tilder peut fournir, code.js, members.js et celui d'un type, où la construction charge chacun, et les règles qu'ils suivent.
order: 40
---

## Nom

scripts - ce que peuvent faire les scripts d'un thème, et où ils se chargent

Les scripts appartiennent au thème : tilder n'en écrit aucun et n'en a
besoin d'aucun. Il en connaît deux par leur nom, `code.js` pour le bouton
de copie et `members.js` pour la recherche parmi les membres, ainsi que
tout script que nomme un type de contenu. Il ne charge chacun que sur les
pages où il sert, et seulement si le thème fournit le fichier. Chaque
script améliore une page qui est complète sans lui.

[TOC]

## code.js

Un bouton de copie sur les blocs de code. La construction ajoute sa
balise à chaque page qui contient un bloc de code, où que ce soit dans ses
sections, quand le thème a un `code.js` :

```html
<script src="../code.js" defer
	data-copy="copy" data-copied="copied"></script>
```

Les mots du bouton viennent de `labels.copy` et `labels.copied`, par les
attributs `data-copy` et `data-copied` de la balise : le script ne
contient aucun texte à lui, il parle donc toutes les langues du site. Les
blocs sur lesquels il agit sont les éléments `pre.code`
([classes](docs/themes/classes)) ; l'étiquette de langue, `data-lang`,
ne fait pas partie du code, si bien qu'un script qui copie le `<code>`
intérieur copie le code seul.

## members.js et le script d'un type

Un type de contenu peut nommer un script dans son attribut `SCRIPT` : la
construction ajoute sa balise à chaque page dont une section liste ce
type, quand le thème fournit le fichier. Le type intégré `member` nomme
`members.js`, pour la recherche et le filtre d'une liste `{members}`
([les membres](docs/content-types/member)) :

```html
<script src="members.js" defer></script>
```

La liste fournit au script ce dont il a besoin, sous forme de données : le
corps de la section, un `<div class="b members grid">`, porte les mots de
la collection des membres (`data-search_label`, `data-search_placeholder`,
`data-all`, `data-one`, `data-many`, `data-none`), et chaque carte, un
`<div class="entry">`, son `data-category` et son `data-search`, les noms
du membre en ASCII et en minuscules.

Le type d'un thème fait de même : le type `doc` de ce site nomme
`search.js`, chargé sur les pages qui listent la documentation. Un type
écrit les `data-*` de la section qui le liste avec sa fonction
`list_data` ([types personnalisés](docs/content-types/custom-types)).

## Où vont les balises

`{{ script }}` contient toutes les balises dont la page a besoin :
d'abord les scripts que nomment les types listés, chacun une fois, puis
`code.js`. Chacune porte `defer`, pour s'exécuter une fois la page
analysée, et un `src` relatif à la page. Placez `{{ script }}` à la fin du
`<body>` de chaque gabarit ; un gabarit qui l'omet ne charge aucun de ces
scripts.

Un gabarit peut aussi charger un script à lui, sur toutes les pages qu'il
sert, avec sa propre balise :

```html
<script src="{{ root }}nav.js" defer></script>
```

C'est ainsi que le gabarit de documentation de ce site charge le script de
sa barre latérale. Comme tout fichier de thème, un script placé dans le
dossier `assets/` du site remplace celui du thème qui porte le même nom
([fichiers](docs/themes/files)).

## Les règles

Les scripts d'un thème suivent les règles du contrat de tilder (son
`AGENTS.md`, « Scripts »), que la Content-Security-Policy du serveur fait
respecter :

<!-- 1.2 -->

- **Un fichier, jamais en ligne.** De l'ES5, sans dépendance, dans un
  fichier que sert le site : jamais un `<script>` avec du code dans la
  page, jamais un CDN. La politique du Caddyfile d'exemple n'autorise les
  scripts que par `script-src 'self'`, si bien qu'un navigateur refuserait
  l'un comme l'autre. Le seul `<script>` en ligne est le JSON-LD qu'écrit
  la construction, qui est une donnée, pas du code.
- **Une amélioration, rien de plus.** La page est complète sans le script :
  tout texte lisible, tout lien praticable. Le script crée ses propres
  commandes, le bouton de copie, le champ de recherche, si bien qu'un
  lecteur sans JavaScript n'en voit aucune, plutôt qu'une commande qui ne
  fait rien.
- **Aucun texte à lui.** Ses mots viennent de la configuration, par des
  attributs `data-*` qu'écrit la construction ou le gabarit :
  `labels.copy` pour le bouton de copie, le `[search]` d'un thème pour sa
  recherche.
- **Ni stockage, ni cookie.**
- **Des requêtes vers la même origine seulement.** Un script peut
  récupérer les fichiers du site lui-même, un index de recherche par
  exemple, et rien d'autre : aucun autre hôte. La politique accorde
  `connect-src 'self'` ; sous une politique qui ne l'accorde pas, le
  navigateur bloque la requête, et le script doit alors retirer sa
  commande, comme le fait la recherche de ce site.

La même politique contient `style-src 'self'` : un script affiche et
masque avec des classes et l'attribut `hidden` plutôt qu'avec des styles
en ligne. La page [déploiement](docs/guide/deployment) donne la politique
complète.

## Voir aussi

- [types personnalisés](docs/content-types/custom-types)
- [déploiement](docs/guide/deployment)
- [classes](docs/themes/classes)
