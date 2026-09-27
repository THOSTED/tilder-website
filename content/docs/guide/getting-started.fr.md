---
title: Premiers pas
description: Installer tilder avec Docker ou Python 3.11, copier le site de départ, le construire, le reconstruire en écrivant, et s'y retrouver dans public/.
order: 10
---

## Nom

getting started - installer tilder et construire un premier site

tilder tourne depuis son image Docker ou depuis une copie du dépôt avec
Python 3.11 ou plus récent ; rien d'autre n'est nécessaire. Cette page
copie le site de départ, un petit site bilingue avec son propre thème, le
construit, le fait se reconstruire pendant que vous écrivez, et fait le
tour de ce que la construction laisse dans `public/`.

[TOC]

## Installer

### Avec Docker

  L'image `ghcr.io/thosted/tilder` contient le générateur, Python et les
  outils qui dessinent les icônes. Elle porte un tag par version : `1.2.0`,
  `1.2` et `1` suivent les versions publiées, `latest` la branche
  principale. Fixez une version, pour que le site se construise demain
  comme aujourd'hui :

  ```sh
  docker pull ghcr.io/thosted/tilder:1.2.0
  ```

  Le générateur est dans `/tilder` à l'intérieur de l'image, avec la
  documentation de référence de sa version dans `/tilder/docs/`.

### Avec Python

  Une copie du dépôt suffit : tilder n'utilise que la bibliothèque
  standard de Python, il n'y a donc rien à installer avec `pip`. Il faut
  Python 3.11 ou plus récent.

  ```sh
  git clone --branch v1.2.0 https://github.com/THOSTED/tilder
  python3 tilder/build.py --help
  ```

### Les icônes et l'image de partage

  Chaque construction dessine `favicon.ico` et les icônes PNG à partir du
  fichier `assets/logo.svg` du site. Quand le thème a un `share.svg`, elle
  dessine aussi `share.png`, l'aperçu de lien en 1200x630, à partir de ce
  modèle, logo compris ; sans lui, l'aperçu est la plus grande des icônes.
  Il lui faut un moteur de rendu SVG : `rsvg-convert` d'abord, sinon
  `magick`, d'ImageMagick. L'image Docker contient `rsvg-convert`, ainsi
  que `woff2_decompress`, pour que l'aperçu soit dessiné avec les polices
  du thème.

  Sans aucun des deux, la construction continue et le signale, une fois :

  ```text
  warning: no rsvg-convert or magick: icons and share.png not made
  ```

  Les pages sont complètes, mais les icônes et l'aperçu qu'elles
  désignent manquent. Sans `assets/logo.svg`, rien de tout cela n'est
  produit non plus, et la construction prévient :

  ```text
  warning: no logo.svg in assets/: no icons, no share.png
  ```

## Copier le site de départ

Le dossier `starter/` du dépôt est un site complet : une page d'accueil,
un blog avec un article, une page 404, en anglais et en français, et un
thème minimal sur les polices du système. Copiez-le et faites-en le
vôtre :

```sh
git clone --branch v1.2.0 https://github.com/THOSTED/tilder
cp -r tilder/starter my-site
cd my-site
```

Sautez le clonage si vous l'avez déjà fait pour lancer tilder avec
Python.

On y trouve les trois dossiers de tout projet : `content/` (les pages et
`site.toml`), `theme/` (l'apparence) et `assets/` (le logo). La page
[le projet](docs/guide/project) les décrit un par un.

Le site de départ déclare deux langues. Pour un site dans une seule
langue, supprimez `content/site.fr.toml`, tous les fichiers `.fr.md` et
la ligne `languages` de `content/site.toml`.

## La première construction

Avec Docker, depuis `my-site/` :

```sh
mkdir -p public
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD:/site" -v "$PWD/public:/out" \
  ghcr.io/thosted/tilder:1.2.0 \
  python3 -B /tilder/build.py --root /site --out /out
```

`-u` vous rend propriétaire de ce que la construction écrit ; créer
`public/` d'abord évite que Docker le crée au nom de root.

Avec Python, depuis `my-site/`, à côté de la copie `tilder/` :

```sh
python3 ../tilder/build.py
```

tilder construit le dossier courant quand il contient un dossier
`content/`, et écrit dans son `public/`. Depuis un autre endroit, nommez
les deux : `--root` est le projet à construire, `--out` l'endroit où
écrire le site.

```sh
python3 tilder/build.py --root my-site --out my-site/public
```

La construction affiche ce qu'elle a trouvé, puis chaque fichier écrit :

```console
$ python3 ../tilder/build.py
languages: en (default), fr
types: event, member, page, post
collections: blog (post, 1 item), events (event, no folder), ...
[10:42:07] built /home/me/my-site/public: 404.html, ...
```

Une construction suivante n'écrit que ce qui a changé, et supprime du
dossier de sortie tout fichier qu'elle ne produit plus : ce dossier
appartient à tilder, n'y gardez rien d'autre.

Un problème dans le contenu arrête la construction, avec un message qui
nomme le fichier et dit quoi faire ; le code de sortie est alors 1. Un
avertissement, comme une image sans texte alternatif ou une description
trop longue pour les moteurs de recherche, ne l'arrête pas. Tous les
messages sont listés dans la
[référence de la ligne de commande](docs/reference/cli).

## Reconstruire en écrivant

`--watch` construit une fois, puis surveille le projet et reconstruit à
chaque modification :

```sh
python3 ../tilder/build.py --watch
```

La commande par défaut de l'image est cette même surveillance, de `/site`
vers `/out` :

```sh
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD:/site" -v "$PWD/public:/out" ghcr.io/thosted/tilder:1.2.0
```

Elle regarde `content/`, `theme/` et `assets/` chaque seconde. Une
construction qui échoue garde la dernière sortie valable et attend la
modification suivante. Une modification du générateur lui-même, ou des
types Python d'un thème dans `theme/types/`, relance le processus pour
charger le nouveau code.

Elle reconstruit aussi à minuit, sans aucune modification : la date de la
construction décide quels événements sont à venir et lesquels sont passés,
si bien qu'un événement rejoint la liste des événements passés le
lendemain de sa date. Minuit est celui de la machine : dans un conteneur,
UTC, sauf si la variable `TZ` en décide autrement.

## Ce que contient public/

Pour le parcourir, servez le dossier : les liens n'ont pas de `.html`,
donc ouvrir les fichiers depuis le disque les casse, et la pile compose de
la page [déploiement](docs/guide/deployment) les sert comme prévu. La
construction a écrit :

| Chemin | Ce que c'est |
|---|---|
| `index.html`, `blog/index.html`, `404.html`... | les pages, pour les navigateurs |
| `fr/...` | les mêmes pages en français, sous le préfixe de la langue |
| `txt/` | le miroir en texte, en ASCII pur, sur 75 colonnes : `txt/index.txt` |
| `ansi/` | le même texte, en couleurs pour les terminaux |
| `blog/feed.xml`, `fr/blog/feed.xml` | le flux RSS du blog, un par langue |
| `sitemap.xml`, `sitemap.txt`, `robots.txt` | pour les moteurs de recherche |
| `favicon.ico`, `icon-192.png`, `icon-512.png`, `apple-touch-icon.png` | les icônes, dessinées depuis `assets/logo.svg` |
| `share.png`, `site.webmanifest` | l'aperçu de lien, et le manifeste web |
| `style.css`, `logo.svg` | les fichiers du thème et les ressources, copiés |

Un site avec des événements reçoit aussi leur flux RSS et un fichier
iCalendar. Rien de tout cela ne se modifie à la main, et rien n'est
versionné : `public/` est reconstruit à partir des sources à chaque fois.

## Voir aussi

- [le projet](docs/guide/project)
- [la ligne de commande](docs/reference/cli)
- [le déploiement](docs/guide/deployment)
