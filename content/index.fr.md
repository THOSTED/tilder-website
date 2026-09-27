---
man: TILDER(1)
title: tilder - un générateur de sites en page de manuel
description: tilder fait d'un fichier Markdown une page HTML pour le navigateur et son miroir en texte pour le terminal, avec la seule bibliothèque standard de Python.
tagline: un générateur de sites en page de manuel
nav:
layout: home
---

## Nom

tilder - un générateur de sites en page de manuel

Un fichier Markdown en entrée, deux rendus en sortie : une page HTML pour
le navigateur et son miroir en texte pour le terminal. tilder s'appuie sur
la seule bibliothèque standard de Python ; ses pages se lisent sans
JavaScript et ne chargent rien depuis un site tiers.

## Un fichier, deux rendus {grid}

```markdown
---
title: hello
man: HELLO(7)
---

## Name

hello - a page

## Description

One **Markdown** file, two outputs.
```

```html
<section class="s" id="description">
	<h2>Description</h2>
	<div class="b">
		<p>One <b>Markdown</b> file, two outputs.</p>
	</div>
</section>
```

```console
$ curl example.org/hello
NAME
     hello - a page

DESCRIPTION
     One Markdown file, two outputs.
```

## Fonctionnalités {grid}

### Miroir en texte

  Chaque page a son double en texte brut, sur 75 colonnes, en noir et
  blanc ou en couleurs pour le terminal. `curl` le reçoit à la place du
  HTML.

### Types de contenu

  Pages, articles, événements et membres, chacun avec ses listes, et des
  flux RSS et iCalendar. Un thème peut ajouter son propre type en
  quelques lignes de Python.

### Langues

  La langue par défaut à la racine, les autres sous leur préfixe, par
  exemple `/fr/`. Une page non traduite s'affiche dans une autre langue,
  et `hreflang`, le plan du site et les flux suivent.

### Référencement

  URL canoniques, Open Graph, Twitter Card, JSON-LD, plan du site et
  `robots.txt`. À chaque génération, tilder vérifie les titres et les
  descriptions, et prévient quand l'un d'eux est trop long ou trop court.

### Thèmes

  tilder écrit un HTML sémantique aux noms de classes stables ; le dossier
  `theme/` du site décide de son apparence. Le site de départ fournit un
  thème minimal à copier ; le site que vous lisez en utilise un autre.

### Accessibilité

  Un seul `<h1>` par page, des repères, des libellés, des textes
  alternatifs et des régions nommées. Un lecteur d'écran signale les liens
  qui quittent le site ou ouvrent un onglet, et chaque page se lit en
  entier sans JavaScript.

### Aucune dépendance

  La bibliothèque standard de Python, rien à installer. Les outils
  extérieurs ne servent qu'à dessiner les icônes et l'aperçu des liens,
  et sont facultatifs : `rsvg-convert`, avec `woff2_decompress`, sinon
  ImageMagick ; sans l'un ni l'autre, ces images sont omises avec un
  avertissement. L'image Docker contient `rsvg-convert` et
  `woff2_decompress`. Aucune page ne charge quoi que ce soit depuis un
  autre site.

## Démarrage rapide

Copiez le site de départ du dépôt, le dossier `starter/`, un petit site
avec son thème, puis générez-le avec l'image Docker,
`ghcr.io/thosted/tilder:1.4.1` :

```sh
git clone --branch v1.4.1 https://github.com/THOSTED/tilder
cp -r tilder/starter my-site && cd my-site
mkdir -p public
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD:/site" -v "$PWD/public:/out" \
  ghcr.io/thosted/tilder:1.4.1 \
  python3 -B /tilder/build.py --root /site --out /out
```

Le site est dans `public/`. Avec Python, sans Docker, lancez plutôt
`python3 ../tilder/build.py` dans `my-site/`. Le guide
[bien démarrer](docs/guide/getting-started) prend le relais.

## Voir aussi

- [la documentation](docs/)
- [pourquoi tilder](why)
- [tilder sur GitHub ↗](https://github.com/THOSTED/tilder)
