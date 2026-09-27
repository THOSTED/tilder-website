---
title: La ligne de commande
description: build.py et chacune de ses options, de --root à --check, ce qu'affiche la construction, chaque avertissement et erreur, et ses codes de sortie.
order: 60
---

## Nom

cli - build.py, ses options, ses messages et ses codes de sortie

tilder tient en une commande, `build.py`, lancée avec Python 3.11 ou plus
récent, ou dans son image Docker. Elle construit un projet dans un
dossier, une fois, ou le reconstruit à mesure que vous écrivez, ou
vérifie le thème sans rien construire. Ses messages ont tous la même
forme : ils nomment le fichier en cause et disent quoi faire.

[TOC]

## Synopsis

```text
python3 build.py [--root DIR] [--out DIR] [--watch] [--debug]
python3 build.py [--root DIR] --check [--markdown] [--debug]
python3 build.py --version
python3 build.py -h | --help
```

`build.py` se trouve à la racine d'une copie de tilder, et à
`/tilder/build.py` dans l'image Docker, dont la commande par défaut
surveille `/site` et construit dans `/out` :

```sh
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD:/site" -v "$PWD/public:/out" \
  ghcr.io/thosted/tilder:1.2.0 \
  python3 -B /tilder/build.py --root /site --out /out
```

Les options viennent dans n'importe quel ordre, sauf `-h` et `--help`,
qui ne comptent qu'en premier argument ; un argument que la construction
ne connaît pas est ignoré ([premiers pas](docs/guide/getting-started)).

## Options

### --root DIR

  Le projet à construire : le dossier qui contient `content/`, `theme/`
  et `assets/`. Sans elle, le projet est le dossier courant s'il a un
  dossier `content/`, sinon le dossier qui contient la copie de tilder.

### --out DIR

  Où va le site, dossier créé au besoin. Par défaut : `public/` dans le
  projet. La construction n'écrit que les fichiers qui ont changé, chacun
  remplacé d'un coup, pour qu'un serveur ne lise jamais un fichier à
  moitié écrit, et supprime chaque fichier qu'elle ne produit plus, puis
  les dossiers vides : le dossier de sortie appartient à la
  construction, n'y gardez rien d'autre.

### --watch

  Construire, puis surveiller le projet et reconstruire à chaque
  changement. Les sources, `content/`, `theme/`, `assets/`, un `LICENSE`
  à côté d'eux et les fichiers de tilder lui-même, sont examinées chaque
  seconde. Une construction qui échoue affiche ses erreurs, garde la
  dernière sortie valide et attend le changement suivant ; si la toute
  première construction échoue, elle recommence toutes les cinq secondes
  jusqu'à réussir. Un changement de tilder lui-même, ou des types d'un
  thème dans `theme/types/`, redémarre le processus pour charger le
  nouveau code.

  La surveillance reconstruit aussi à minuit, sans aucun changement : la
  date de la construction décide quels événements sont à venir et
  lesquels sont passés, si bien qu'un événement passe dans la liste des
  événements passés le lendemain. Minuit est celui de la machine : dans
  un conteneur, UTC sauf si la variable `TZ` dit autre chose.

### --check

  Depuis tilder 1.2 : vérifier le thème par rapport au tilder qui le
  lance, sans rien construire. Chaque classe qu'écrit la construction
  doit avoir une règle dans le `style.css` servi (`assets/style.css`
  l'emporte sur `theme/style.css`), sauf celles que nomme le
  `[check] unstyled` du thème ; chaque paire de couleurs de
  `[check] contrast` doit atteindre `contrast_min`, en thème clair, et en
  thème sombre quand la feuille de style en a un. Elle écrit une ligne
  `error:` par problème, puis une ligne de bilan par vérification, et sort
  avec 1 s'il y a un problème, 0 sinon
  ([vérifier un thème](docs/themes/checking)). Elle n'écrit rien, pas
  même le dossier de sortie : `--out` n'est pas lu.

### --markdown

  Depuis tilder 1.2, avec `--check` : écrire aussi le tableau des
  contrastes en Markdown, une ligne par paire et par thème, clair ou
  sombre, avec son rapport, pour le README d'un thème. Le tableau part
  sur la sortie standard et les lignes de bilan sur la sortie d'erreur :
  `--check --markdown > contrast.md` ne garde que le tableau.

### --debug

  Après chaque message d'erreur, afficher la trace Python qui l'a causé.
  Les messages sont censés suffire ; la trace sert pour un bogue de
  tilder ou d'un type de thème.

### --version

  Afficher la version de tilder et sortir : la version publiée de
  l'image, `1.2.0`, tirée de sa variable `TILDER_VERSION` ; `dev` depuis
  une copie du dépôt, où la variable n'est pas définie.

### -h, --help

  Afficher l'usage, les options et la carte des modules de tilder, puis
  sortir.

## Environnement

| Variable | Effet |
|---|---|
| `SITE_ROOT` | le projet à construire, comme `--root`, qui la définit |
| `BUILD_TODAY` | la date de la construction, `2026-05-16`, à la place de celle du jour : quels événements sont à venir, pour un test ou un aperçu |
| `BUILD_INTERVAL` | avec `--watch`, les secondes entre deux examens des sources ; par défaut `1` |
| `TILDER_VERSION` | ce qu'affiche `--version` ; définie par l'image Docker |
| `TZ` | le fuseau horaire de la date et de la reconstruction de minuit |

## Ce qu'affiche la construction

Sur la sortie standard, la première construction dit ce qu'elle a
compris, puis chaque construction énumère ce qu'elle a écrit, ou
`no change` ; un fichier supprimé apparaît précédé d'un `-` :

```console
$ python3 ../tilder/build.py
languages: en (default), fr
types: event, member, page, post
collections: blog (post, 1 item), events (event, no folder), ...
[10:42:07] built /home/me/my-site/public: 404.html, blog/feed.xml, ...
[10:43:12] built /home/me/my-site/public: about.html, txt/about.txt, ansi/about.txt
[10:44:30] built /home/me/my-site/public: -old.html
```

La ligne `languages:` n'apparaît que sur un site en plusieurs langues ;
la ligne `types:` ajoute les types qui viennent du thème,
`; from theme: talk`. Avec `--watch`, la construction dit aussi quand
elle attend après un échec ou redémarre sur du nouveau code. Les
avertissements et les erreurs vont sur la sortie d'erreur.

## Erreurs

Une erreur arrête la construction. Chaque message a la même forme :

```text
error: <file>[:<line>]: <what is wrong>. <what to do>
```

Le fichier est nommé depuis la racine du projet, ou depuis celle de
tilder pour l'un de ses propres fichiers ; la construction rassemble
chaque problème d'une étape avant de s'arrêter, si bien qu'un seul
lancement les montre tous.

```text
error: content/site.toml: collection "blog" has type "posts"; types are singular. Write type = "post"
error: content/blog/2026-02-30-hello.md: "2026-02-30" is not a date. Name the file YYYY-MM-DD-slug.md with the post's date
```

Les erreurs de la configuration et des langues :

| Message | Cause |
|---|---|
| `[members] is no longer read` | une table que lisait un tilder plus ancien ; ses clés vont sous `[collections.members]` |
| `[collection_defaults] is no longer read` | de même ; les mots d'un type vont sous chaque `[collections.<name>]` |
| `collection "..." has type "...s"; types are singular` | un type écrit au pluriel, `posts` |
| `collection "..." has type "...", which no type defines` | un type inconnu ; le message énumère ceux qui sont chargés |
| `collections "..." and "..." share the folder content/...` | deux collections avec un même `dir`, ou dont l'une a son `dir` dans celui de l'autre |
| `[site] languages does not contain the default language "..."` | `site.lang` absent de `site.languages` |
| `"..." is not a declared language` | un `site.<lang>.toml` ou une page `<name>.<lang>.md` pour une langue absente de `site.languages` |
| `[site] lang is "...", not "..."` | un `site.<lang>.toml` qui règle une autre langue |

Depuis tilder 1.2, une collection récursive en ajoute trois :

| Message | Cause |
|---|---|
| `collection "..." has recursive = ...` | une valeur autre que `true` ou `false` |
| `collection "..." is recursive, and its type "..." is dated` | une collection `post` ou `event` récursive |
| `is a second file for the item ..., with ...` | un même élément écrit à la fois `guide.md` et `guide/index.md` |

Les erreurs du contenu et du thème :

| Message | Cause |
|---|---|
| `cannot be built: <error>` | une page que la construction ne peut pas rendre, un `title:` manquant par exemple : le fichier est nommé, `--debug` montre la trace |
| `"..." is not a date` | un article ou un événement dont le nom de fichier commence par une date qui n'existe pas |
| `{...} names no ... collection` | un marqueur de liste qui nomme une collection d'un autre type, ou aucune |
| `no layout.html: a site needs a theme` | `theme/layout.html` manque |
| `layout "..." names no theme/layouts/....html` | le `layout:` d'une page nomme un fichier que le thème n'a pas |
| `unknown placeholder {{ ... }}` | un gabarit utilise un nom qui n'est ni une variable ni une clé de la configuration ([gabarits et variables](docs/themes/layouts)) |

Les types en Python d'un thème ont leurs propres erreurs, d'un `NAME`
manquant à un marqueur que deux types revendiquent, décrites dans
[vos propres types](docs/content-types/custom-types). Les erreurs de
`--check` sont décrites dans [vérifier un thème](docs/themes/checking).

Dans une construction unique, un fichier qui n'est pas du TOML valide,
ou un bogue, se termine par le message et la trace de Python lui-même,
pas par cette forme. Avec `--watch`, le même problème tient en une ligne,
`error: <erreur Python>: <quoi>`, et la trace ne suit qu'avec `--debug`.

## Avertissements

Un avertissement n'arrête pas la construction et ne change pas son code
de sortie : le site est construit, avec quelque chose qui manque ou qui
risque d'être tronqué. Chaque avertissement que la construction peut
écrire :

| Ligne | Sens |
|---|---|
| `warning: image not found: content/<path>` | une image dont le fichier n'existe pas |
| `warning: image without alt text: <path>` | une image au texte alternatif vide |
| `warning: unknown code language '<lang>', left plain` | le langage d'un bloc de code que tilder ne colore pas ([blocs](docs/reference/markdown/blocks)) |
| `warning: no <logo> in assets/: no icons, no share.png` | le logo que nomme `share.logo_svg`, `logo.svg` par défaut, manque |
| `warning: no rsvg-convert or magick: icons and share.png not made` | aucun moteur de rendu SVG n'est installé ([flux et images](docs/reference/feeds-and-images)) |
| `seo: <page>: title is N characters (max MAX)` | un `<title>` plus long que `seo.title_max`, `60` par défaut |
| `seo: <page>: description is N characters (MIN-MAX)` | une description hors de `seo.description_min` et `seo.description_max`, `50-160` par défaut |
| `seo: <page>: same title as <page>` | deux pages d'une même langue partagent un titre |
| `seo: <page>: same description as <page>` | deux pages d'une même langue partagent une description |

Sur un site en plusieurs langues, chaque ligne `seo:` nomme la langue de
la passe, celle par défaut comprise : `seo: [en] about.html: ...`,
`seo: [fr] about.html: ...` ([SEO](docs/reference/seo)). Un
site qui ne veut aucun avertissement fait échouer sa propre construction
dessus, comme la construction de ce site le fait sur toute ligne
`warning:` ou `seo:`. Dans un script shell :

```sh
python3 ../tilder/build.py 2> build.log; status=$?
cat build.log >&2
[ "$status" -eq 0 ] && ! grep -Eq '^(warning|seo):' build.log
```

## Codes de sortie

| Code | Quand |
|---|---|
| `0` | le site est construit, avec ou sans avertissements ; `--check` n'a trouvé aucun problème ; `--version` et `--help` |
| `1` | la construction s'est arrêtée sur une erreur ; `--check` a trouvé un problème ; une exception Python hors des messages de la construction |

Avec `--watch`, une construction qui échoue ne fait pas sortir : le
processus attend une correction, et tourne jusqu'à ce qu'on l'arrête.

## Voir aussi

- [premiers pas](docs/guide/getting-started)
- [vérifier un thème](docs/themes/checking)
- [la configuration](docs/reference/configuration)
