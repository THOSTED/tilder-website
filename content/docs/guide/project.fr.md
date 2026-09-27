---
title: Le projet
description: Les trois dossiers d'un site tilder, content/, theme/ et assets/, les trois couches de sa configuration, et ce qui est servi.
order: 20
---

## Nom

project - les dossiers d'un site et sa configuration

Un projet tilder tient en trois dossiers : `content/` pour ce que vous
écrivez, `theme/` pour l'apparence, `assets/` pour les fichiers servis
tels quels. La configuration se construit en trois couches, des valeurs
par défaut de tilder jusqu'à votre propre `site.toml`. La construction lit
le tout et ne sert que ce qui a sa place sur un site web.

[TOC]

## Les trois dossiers

```text
my-site/
  content/          les pages, et la configuration du site
    site.toml         les réglages et les mots du site
    site.fr.toml      ce qui change en français (facultatif)
    index.md          la page d'accueil
    404.md            la page d'une adresse introuvable
    blog/             une collection : un fichier par article
  theme/            l'apparence
    layout.html       la page autour du contenu (obligatoire)
    style.css
    theme.toml        la configuration propre au thème (facultatif)
  assets/           servis tels quels
    logo.svg          la source de chaque icône et de share.png
  public/           le site construit, jamais versionné
```

### content/

  Chaque fichier Markdown est une page, à l'adresse que donne son chemin
  ([écrire des pages](docs/guide/writing)). Un dossier déclaré comme
  collection dans `site.toml` contient les éléments d'un même type :
  articles, événements, membres, ou un type ajouté par le thème
  ([types de contenu](docs/content-types)). Tout autre fichier, une image
  ou un PDF, est copié sur le site au même chemin : une image vit à côté
  de la page qui la montre.

### theme/

  `layout.html` est le seul fichier obligatoire d'un thème : le HTML
  autour de chaque page, rempli par des variables. Le reste est
  facultatif : `style.css`, des scripts, des polices, d'autres gabarits,
  des types de contenu en Python, et `theme.toml`. Le thème du site de
  départ est un thème complet et minimal pour commencer
  ([thèmes](docs/themes)).

### assets/

  Les fichiers propres au projet, servis tels quels à la racine du site :
  `assets/logo.svg` devient `/logo.svg`. C'est aussi la source à partir de
  laquelle la construction dessine les icônes et l'aperçu de lien. Un
  fichier de `assets/` l'emporte sur le fichier du thème de même nom : un
  site peut remplacer un fichier d'un thème qu'il n'a pas écrit,
  `style.css` ou `layout.html`, sans toucher au thème.

## La configuration

Les réglages d'un site, et chaque mot qu'un lecteur voit en dehors des
pages, viennent de fichiers TOML. tilder ne contient aucun texte à lui.
Trois couches, chacune fusionnée par-dessus la précédente, si bien que
chacune ne dit que ce qui change :

1. `defaults.toml`, dans tilder : chaque clé qu'il lit, avec sa valeur par
   défaut et un commentaire. La
   [référence de la configuration](docs/reference/configuration) les
   documente une à une.
2. `theme/theme.toml` : les valeurs propres au thème, comme les couleurs
   de l'aperçu de lien.
3. `content/site.toml` : votre site. Il a le dernier mot.

```toml
# content/site.toml : ce qui diffère des valeurs par défaut
[site]
name = "mon site"
url = "https://example.org"
title_suffix = " - mon site"

[footer]
right = "MONSITE(1)"
```

Chaque langue supplémentaire ajoute un fichier à la couche du thème et à
celle du site, lus dans cet ordre, le dernier l'emportant :

```text
defaults.toml
  < theme/theme.toml < theme/theme.fr.toml
  < content/site.toml < content/site.fr.toml
```

Les tables sont fusionnées clé par clé : un `site.fr.toml` qui définit
`[site] manual` garde toutes les autres clés de `[site]`. Une liste de
tables, comme les entrées `[[nav]]` de la navigation, est remplacée d'un
bloc : un fichier qui la définit reprend toutes les entrées. Les réglages
d'une collection partent des valeurs par défaut de son type, dans le
module du type, et `[collections.<name>]` s'applique par-dessus.

Les fichiers de configuration sont relus à chaque construction : une
modification s'applique à la suivante. Aucun n'est jamais servi.

## Ce qui est servi

La construction fait des pages avec `content/` et copie le reste ;
quelques fichiers sont lus, jamais servis.

| Dossier | Servi | Jamais servi |
|---|---|---|
| `content/` | les pages, construites depuis le Markdown ; tout autre fichier, à son propre chemin | les sources Markdown ; `site.toml` et `site.<lang>.toml` ; tout fichier ou dossier dont le nom commence par `_` |
| `theme/` | tout le reste, à la racine du site : `style.css`, les scripts, `fonts/`... | `layout.html`, `layouts/`, `share.svg`, `icons/`, `types/`, `theme.toml` et `theme.<lang>.toml` ; `.git` et tout fichier dont le nom commence par `.git` ; un `README.md` ou un `LICENSE` à sa racine |
| `assets/` | tout le reste, à la racine du site | la même liste que pour `theme/` |

Un fichier `LICENSE` à la racine du projet, à côté de `content/`, est
servi à la racine du site.

Le préfixe `_` garde brouillons et modèles dans `content/` : `_draft.md`
ou `blog/_template.md` n'est jamais construit. La liste du thème permet à
un thème de vivre dans son propre dépôt git, avec son README et sa
licence, sans les publier.

## Rien de généré n'est versionné

`public/` est reconstruit à partir des sources à chaque fois : ajoutez-le
à `.gitignore`. Les icônes et `share.png` sont redessinés à chaque
construction, depuis `assets/logo.svg` et le `share.svg` du thème : eux
non plus ne sont pas versionnés. Ce qui va dans le dépôt, c'est
`content/`, `theme/`, `assets/`, et ce qui les construit et les sert : un
fichier compose, un Caddyfile.

```text
# .gitignore
public/
```

## Voir aussi

- [écrire des pages](docs/guide/writing)
- [la référence de la configuration](docs/reference/configuration)
- [les fichiers d'un thème](docs/themes/files)
