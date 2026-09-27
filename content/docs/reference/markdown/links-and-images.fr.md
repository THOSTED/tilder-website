---
title: Liens et images
description: Cibles des liens écrites depuis la racine, ancres, liens entre langues, fichiers et autres sites ; images à côté de leur page, texte de remplacement, légendes.
order: 50
---

## Nom

links and images - des cibles depuis la racine, des figures à côté de la page

Un lien nomme sa cible depuis la racine du site, et la construction la
rend relative à la page : la même ligne fonctionne sur chaque page, si
profonde soit-elle. Une image fait l'inverse : son chemin part du dossier
de la page, pour qu'elle puisse se ranger à côté. Les liens et les images
ci-dessous sont vivants.

[TOC]

## Cibles des liens

`[libellé](cible)` est un lien. Écrivez une cible interne depuis la
racine du site, sans barre oblique au début et sans `.html` :

| Cible | Mène à |
|---|---|
| `docs/guide` | une page, `/docs/guide` |
| `blog/` | la page d'un dossier, `/blog/` : gardez la barre finale |
| vide, ou `./` | la page d'accueil de la langue |
| `docs/guide/writing#liens` | une section d'une autre page |
| `./#<id>` | une section de la page d'accueil |
| `#cibles-des-liens` | une section de cette page |
| `logo.svg`, `blog/feed.xml` | un fichier : tout dernier segment qui a une extension |
| `https://example.org/` | un autre site, laissé tel quel |

```text
Le [guide](docs/guide), le [blog](blog/), l'[accueil](./), la
[section des liens d'écrire des pages](docs/guide/writing#liens),
[cette section](#cibles-des-liens) et le [logo](logo.svg).
```

> Le [guide](docs/guide), le [blog](blog/), l'[accueil](./), la
> [section des liens d'écrire des pages](docs/guide/writing#liens),
> [cette section](#cibles-des-liens) et le [logo](logo.svg).

Cette page est `/fr/docs/reference/markdown/links-and-images` : la
construction écrit le premier lien `../../guide`, et la même source sur
la page d'accueil `docs/guide`. Une cible qui commence par `http` est
laissée intacte, tout comme une cible qui commence par `#`. La
construction ne vérifie pas les liens : une cible qui ne mène nulle part
est écrite quand même.

L'ancre d'une section est son identifiant, tiré de son titre ou fixé par
`{#id}` ([sections](docs/reference/markdown/sections#ids)). Il suit donc
la langue du titre : la section des liens d'écrire des pages est
`#links` en anglais et `#liens` en français.

## D'une langue à l'autre

Sur un site en plusieurs langues, une cible de page reste dans la langue
de la page où elle se trouve : `docs/guide` depuis une page française
mène à `/fr/docs/guide`. Une cible qui commence par `/` se lit telle
quelle depuis la racine du site, et quitte la langue :

```text
Lisez cette page [en anglais](/docs/reference/markdown/links-and-images)
ou [en français](/fr/docs/reference/markdown/links-and-images).
```

> Lisez cette page [en anglais](/docs/reference/markdown/links-and-images)
> ou [en français](/fr/docs/reference/markdown/links-and-images).

Un fichier est écrit une seule fois, à la racine du site, et toutes les
langues lient le même. Les flux RSS font exception : il y en a un par
langue, mais `blog/feed.xml` dans une page est une cible de fichier, donc
le flux de la langue par défaut ; écrivez `/fr/blog/feed.xml` pour le
flux français ([langues](docs/guide/languages)).

## Autres sites

Une cible qui commence par `http` est un lien vers un autre site.
Terminez son libellé par la flèche nord-est, U+2197, le signe que le lien
quitte le site : les lecteurs d'écran sautent la flèche et entendent
`labels.external` à la place.

```text
Le [site d'exemple ↗](https://example.org/) ne fait pas partie de celui-ci.
```

> Le [site d'exemple ↗](https://example.org/) ne fait pas partie de celui-ci.

Qu'un tel lien s'ouvre dans un nouvel onglet se règle une fois pour tout
le site, dans `site.toml` : `[links] new_tab = true` envoie chaque lien
externe vers un nouvel onglet, sauf ceux vers les hôtes listés dans
`same_tab` et leurs sous-domaines ; un lien qui ouvre un nouvel onglet le
dit d'abord aux lecteurs d'écran, avec `labels.new_tab`. Les valeurs par
défaut sont `new_tab = false` et `same_tab = []`
([écrire des pages](docs/guide/writing#liens)).

Dans le miroir en texte, un lien interne ne garde que son libellé,
puisqu'un lecteur dans un terminal le suit avec `curl` et non en le
recopiant. Un lien externe imprime son adresse entre parenthèses après
le libellé, sans la flèche : `site d'exemple (https://example.org/)`.

## Images

Une image est un bloc à elle seule : une seule ligne, entre deux lignes
vides. Le texte de remplacement va entre les crochets, le chemin entre
les parenthèses, et une légende facultative entre guillemets droits
après le chemin.

```text
![Un fichier Markdown, deux sorties : HTML et texte](flow.svg)

![Un fichier Markdown, deux sorties : HTML et texte](flow.svg "Une source, deux rendus.")
```

### Rendu {example}

  ![Un fichier Markdown, deux sorties : HTML et texte](flow.svg)

  ![Un fichier Markdown, deux sorties : HTML et texte](flow.svg "Une source, deux rendus.")

- Le chemin est **relatif au dossier de la page**, contrairement à un
  lien : rangez l'image à côté de la page. Cette page est
  `content/docs/reference/markdown/links-and-images.fr.md`, et son image
  `content/docs/reference/markdown/flow.svg`, que la version anglaise
  partage. Pour un article, faites de l'article un dossier,
  `blog/2026-01-01-hello/index.md`, avec l'image dedans.
- Le texte de remplacement est obligatoire : c'est ce que dit un lecteur
  d'écran et ce qu'affiche le miroir en texte.
- La légende peut contenir du balisage en ligne. Le chemin ne peut pas
  contenir d'espace.
- Une image d'un autre site, `https://example.org/carte.png`, est
  permise par la syntaxe, mais la politique de serveur recommandée ne
  laisse les pages charger que des images de leur propre site : elle ne
  s'affichera pas ([déploiement](docs/guide/deployment)).

Sur la page web, l'image est une `<figure>` : l'image à sa taille
naturelle, jamais plus large que la colonne, sa largeur et sa hauteur
(`width`, `height`) lues dans le fichier (PNG, JPEG, GIF, WebP ou SVG)
pour que la page ne saute pas pendant le chargement, un chargement
différé, et la légende dans un `<figcaption>`. Dans le miroir en texte,
le texte de remplacement suit le mot de `labels.image`, puis viennent la
légende et le chemin de l'image depuis la racine du site, pour `curl`.
La figure ci-dessus, dans le miroir de cette page :

```text
[ image ] Un fichier Markdown, deux sorties : HTML et texte
  Une source, deux rendus.
  /docs/reference/markdown/flow.svg
```

La construction avertit, et continue, quand le fichier manque ou que le
texte de remplacement est vide :

```text
warning: image not found: content/blog/2026-01-01-hello/flow.svg
warning: image without alt text: blog/2026-01-01-hello/flow.svg
```

Préférez le SVG pour les schémas : le dessin reste net à toute taille, et
un fichier SVG peut porter ses propres couleurs de mode sombre, dans un
bloc `@media (prefers-color-scheme: dark)`. La politique de serveur
recommandée laisse un fichier SVG se mettre en forme, jamais exécuter de
script. Les images d'aperçu des liens sont une autre affaire, réglée dans
l'en-tête ([flux et images](docs/reference/feeds-and-images)).

## Voir aussi

- [écrire des pages](docs/guide/writing)
- [les langues](docs/guide/languages)
- [le balisage en ligne](docs/reference/markdown/inline)
- [le miroir en texte](docs/reference/text-mirror)
