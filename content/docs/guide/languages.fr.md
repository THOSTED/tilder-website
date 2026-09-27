---
title: Langues
description: Servir un site en plusieurs langues : les déclarer, traduire la configuration et les pages, et savoir ce que devient une page pas encore traduite.
order: 40
---

## Nom

languages - un site en plusieurs langues

Un site peut être servi en plusieurs langues : celle par défaut à la
racine, chacune des autres sous son propre préfixe, `/fr/`. Chaque langue
déclarée est un site complet : une page pas encore traduite est tout de
même servie, dans la langue où elle est écrite. Les traductions sont des
fichiers posés à côté des originaux, pour les pages comme pour la
configuration.

[TOC]

## Déclarer les langues

```toml
# content/site.toml
[site]
lang = "en"                 # la langue par défaut, à la racine
languages = ["en", "fr"]    # toutes, la langue par défaut d'abord

[languages]                 # les noms du sélecteur de langue
en = "English"
fr = "Français"
```

`site.languages` est vide par défaut : une seule langue, pas de préfixe,
et aucun nom de fichier n'est lu comme une traduction. La liste doit
contenir `site.lang`, sinon la construction s'arrête. Une langue absente
de `[languages]` affiche son code.

## Traduire la configuration

`content/site.fr.toml` ne contient que ce qui change en français,
par-dessus `site.toml` : `lang`, `locale` et `manual` dans `[site]`, les
`[labels]` que voit le lecteur, `[[nav]]` (une liste, donc remplacée d'un
bloc : reprenez toutes les entrées), les mots de chaque
`[collections.<name>]`, `[dates]`, les textes de `[share]`. Le nom du site
est une marque : gardez `title_suffix` tel quel.

```toml
# content/site.fr.toml
[site]
lang = "fr"
locale = "fr_FR"
manual = "Manuel de mon site"

[labels]
skip = "aller au contenu"
languages = "Langues"
```

Une langue déclarée sans son fichier reçoit les mots de la langue par
défaut : un site peut se traduire mot à mot. Un `site.<lang>.toml` pour
une langue que le site ne déclare pas arrête la construction, tout comme
un fichier dont `[site] lang` nomme une autre langue.

Un thème peut porter ses propres mots de la même façon, dans
`theme/theme.fr.toml`. Les couches, la dernière l'emportant :

```text
defaults.toml
  < theme/theme.toml < theme/theme.fr.toml
  < content/site.toml < content/site.fr.toml
```

Un `theme.<lang>.toml` pour une langue que le site ne déclare pas est
ignoré, ni lu ni servi : un thème se partage entre plusieurs sites et peut
connaître plus de langues que chacun d'eux.

## Traduire une page

Posez `about.fr.md` à côté de `about.md`. Il en va de même pour la page
d'un dossier, `blog/index.fr.md`, et pour les éléments d'une collection,
`blog/2026-01-01-hello.fr.md`. La traduction garde le nom de fichier
anglais : l'adresse est `/fr/about`, le même nom sous le préfixe.

Un suffixe qui ne nomme aucune langue déclarée arrête la construction,
pour qu'une faute de frappe ne devienne jamais une page que personne n'a
voulue : `about.fe.md` est une erreur. Pour la même raison, un nom dont la
dernière partie est un mot de deux ou trois lettres est lu comme un
suffixe, `readme.txt.md` compris ; `notes.v2.md` est un nom ordinaire.

Un site dans une seule langue ne lit aucun suffixe : là, `notes.old.md`
est la page `notes.old`.

## Repli

Pour construire une page en français, tilder prend le premier de ces
fichiers qui existe :

1. `about.fr.md` ;
2. `about.<default>.md`, avec le suffixe de la langue par défaut ;
3. `about.md` ;
4. `about.<other>.md`, les autres langues déclarées dans leur ordre.

Ainsi `/fr/about` existe même quand seul `about.md` existe : l'interface,
la navigation et les libellés en français, autour du texte anglais. La
langue du fichier retenu est la langue du contenu de la page : le gabarit
la reçoit par `{{ content_lang }}`, pour `<main lang="...">`, et un
lecteur d'écran lit le texte anglais avec une voix anglaise.

## Liens

Un lien écrit depuis la racine du site reste dans la langue de la page :
sur une page française, `about` mène à `/fr/about`. Une cible qui commence
par `/` en sort : `[in English](/about)`, `[en français](/fr/about)`. Un
fichier, une image ou une feuille de style, est écrit une seule fois à la
racine, et toutes les langues pointent vers le même. La page
[écrire des pages](docs/guide/writing#liens) donne chaque sorte de cible.

## Le sélecteur

La variable `{{ languages }}` du gabarit est un
`<nav class="languages">` avec un lien par langue déclarée, chacun vers la
même page dans cette langue ; la langue courante est marquée
`aria-current="page"`. Le sélecteur est vide sur un site dans une seule langue. La
région est nommée par `labels.languages`.

Les noms viennent de `[languages]` dans `content/site.toml` : chaque
langue est nommée de la même façon sur toutes les pages, chacune dans ses
propres mots. Une table `[languages]` dans `site.fr.toml` n'est pas lue.

Deux autres variables disent au gabarit où se trouvent les choses :
`{{ root }}` est la racine du site, même sous `/fr/`, pour la feuille de
style et les icônes, écrites une seule fois ; `{{ home }}` est la page
d'accueil de la langue de la page, pour les liens vers des pages.

## Ce que la construction écrit

| Sortie | Langue par défaut | Français |
|---|---|---|
| pages | `about.html` | `fr/about.html` |
| miroir en texte | `txt/about.txt` | `txt/fr/about.txt` |
| flux RSS | `blog/feed.xml` | `fr/blog/feed.xml` |
| page 404 | `404.html` | `fr/404.html` |
| calendrier, plan du site, `robots.txt`, manifeste, icônes | une fois, à la racine | - |

- Chaque page porte un `<link rel="alternate" hreflang="...">` pour chaque
  langue, plus `x-default` pour la langue par défaut, et les
  `og:locale:alternate` des autres langues.
- Un seul `sitemap.xml` liste toutes les adresses de toutes les langues,
  chacune avec ses variantes.
- Chaque langue a son propre flux RSS, avec son titre et sa description
  tirés de `[collections.<name>]`. Le `<link rel="alternate">` d'une page
  désigne le flux de sa langue.
- Le fichier iCalendar d'une collection d'événements est écrit une seule
  fois : un calendrier n'a pas de langue d'interface.
- Le miroir en texte nomme les langues sous sa règle d'en-tête :
  `LANGUAGES: en fr`.

Le serveur doit connaître chaque préfixe, pour sa page 404 : voir le
[déploiement](docs/guide/deployment).

## Limites

- Le miroir en texte ramène chaque caractère à l'ASCII et compte une
  colonne par caractère : il convient aux langues écrites en alphabet
  latin.
- tilder ne connaît aucune langue par son nom et ne contient aucun texte :
  chaque mot vient du fichier de la langue. Une langue que personne n'a
  traduite affiche les mots de la langue par défaut.
- Un élément gardé en fichier dans une langue et en dossier dans une autre
  n'est pas pris en charge : choisissez une seule forme par élément.

## Voir aussi

- [écrire des pages](docs/guide/writing)
- [la référence de la configuration](docs/reference/configuration)
- [le déploiement](docs/guide/deployment)
