---
title: Flux et images
description: Les fichiers qu'écrit tilder à côté des pages : flux RSS, iCalendar, icônes et share.png dessinés depuis le SVG à chaque construction, manifeste web.
order: 50
---

## Nom

feeds-and-images - RSS, iCalendar, icônes, aperçu de lien et manifeste

À côté des pages, la construction écrit les fichiers que lisent d'autres
programmes : un flux RSS par collection qui en demande un, dans chaque
langue ; un fichier iCalendar pour les événements ; les icônes et
l'aperçu de lien, dessinés à partir du SVG à chaque construction ; et le
manifeste web. Aucun n'est versionné ni modifié à la main : ils viennent
du contenu et de `site.toml`.

[TOC]

## RSS

Une collection écrit un flux RSS 2.0 quand son réglage `feed` désigne un
chemin et que son type fournit des entrées de flux : `post` et `event` le
font, `member` et `page` non ([types de contenu](docs/content-types)).
`defaults.toml` règle `blog/feed.xml` pour le blog et `events.xml` pour
les événements.

Le flux est écrit dans chaque langue, sous le préfixe de la langue :
`blog/feed.xml` et `fr/blog/feed.xml`, chacun avec les mots de sa langue
([langues](docs/guide/languages)).

| Élément | Valeur |
|---|---|
| `<title>` | le `feed_title` de la collection |
| `<link>` | la page de la collection, son réglage `nav`, en adresse absolue dans la langue |
| `<atom:link rel="self">` | l'adresse du flux lui-même |
| `<description>` | le `feed_description` de la collection |
| `<language>` | la langue de la passe, `site.lang` |
| `<lastBuildDate>` | `site.updated` |
| un `<item>` par élément | du plus récent au plus ancien : le titre, l'adresse en `<link>` et en `<guid>`, la date en `<pubDate>`, la description |

Chaque élément figure dans le flux, un événement passé comme un événement
à venir. Une page annonce un flux dans son `<head>` avec la clé d'en-tête
`feed:`, le nom de la collection ou `all`
([écrire des pages](docs/guide/writing)).

```toml
[collections.blog]
feed = "blog/feed.xml"
feed_title = "my site blog"
feed_description = "News of my site."
```

## iCalendar

Une collection `event` écrit un fichier iCalendar (RFC 5545) quand son
réglage `calendar` désigne un chemin ; `defaults.toml` règle
`calendar.ics` pour les événements. Les applications d'agenda s'y
abonnent. Il est écrit une seule fois, à la racine, dans la langue par
défaut : un calendrier n'a pas de langue d'interface.

Chaque événement est un `VEVENT` sur la journée entière : de sa date à
son `end`, ou le jour même ; un résumé fait du titre et de
`calendar.name` ; le `place` comme lieu, `lat` et `lon` comme `GEO` ; son
adresse et sa description. Le texte est ramené à l'ASCII, les lignes
coupées à 75 octets comme le demande la norme, et l'identifiant de
chaque événement est `<slug>@<uid_domain>`. Le nom du calendrier, sa
description, son identifiant de produit et son fuseau horaire viennent
de la table `[calendar]` ([event](docs/content-types/event),
[configuration](docs/reference/configuration)).

## Icônes

La construction dessine les icônes à partir d'un seul SVG,
`assets/logo.svg` (le fichier que nomme `share.logo_svg`, dans
`assets/`), à chaque construction :

| Fichier | Taille | Utilisé par |
|---|---|---|
| `favicon.ico` | 16, 32 et 48 pixels, dans un seul fichier | les onglets des navigateurs |
| `apple-touch-icon.png` | 180x180 | l'écran d'accueil d'un téléphone |
| `icon-192.png` | 192x192 | le manifeste web |
| `icon-512.png` | 512x512 | le manifeste web, le logo des données structurées (`share.logo`) |

`logo.svg` lui-même est servi tel quel, depuis `assets/`, pour les
navigateurs qui acceptent une icône SVG. Le gabarit pointe vers les
icônes ([gabarits et variables](docs/themes/layouts)) ; celui du site de
départ écrit :

```html
<link rel="icon" href="{{ root }}favicon.ico" sizes="48x48">
<link rel="icon" href="{{ root }}logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{{ root }}apple-touch-icon.png">
<link rel="manifest" href="{{ root }}site.webmanifest">
```

## L'aperçu de lien

`share.png` est l'image que montre un lien vers le site sur les réseaux
sociaux et dans les messageries, en 1200x630. La construction la dessine
à partir du `share.svg` du thème (ou de `assets/share.svg`, qui
l'emporte), un modèle qu'elle remplit d'abord :

| Variable | Valeur |
|---|---|
| `{{ logo }}` | `assets/logo.svg`, intégré en URI `data:` |
| `{{ wordmark }}` | `site.name`, en minuscules |
| `{{ manual_upper }}` | `site.manual`, en capitales |
| `{{ domain }}` | l'hôte de `site.url` |
| `{{ card_1 }}`, `{{ card_2 }}` | les lignes de `share.card` ; vide quand il n'y en a qu'une |
| `{{ section.key }}` | toute valeur de la configuration : `{{ share.text_color }}`, `{{ site.name }}` |

Une variable inconnue arrête la construction. Le texte est dessiné avec
les polices du thème, celles de son dossier `fonts/` : le moteur de rendu
lit le TrueType, pas le WOFF2, donc chaque `*.woff2` est d'abord
décompressé avec `woff2_decompress`, quand il est installé
([les fichiers d'un thème](docs/themes/files)).

L'`og:image` de chaque page est `share.png`, sauf si la page règle
`image:` ou si le thème dessine une carte par page (plus bas). Le fichier est nommé par `share.image`. Sans `share.svg`, aucun
aperçu n'est dessiné, et `og:image` est l'icône, `icon-512.png`, avec la
petite carte `summary` ([SEO](docs/reference/seo)).

## Une carte par page

Avec un `share-page.svg` dans le thème, chaque autre page a sa propre
carte : dessinée à chaque construction à partir des champs de la page,
écrite en `/previews/<key>.png`, et nommée par `og:image`,
`twitter:image` et l'`image` des données structurées d'un article ou
d'un événement. La clé est une empreinte du modèle rempli et des polices :
une page qui ne change pas garde son fichier et son adresse.
`share-<type>.svg`, `share-event.svg` par exemple, l'emporte pour les
pages de ce type. La page d'accueil garde `share.png` ; une page marquée
`noindex`, la 404, aussi. Une page qui règle `image:` montre cette image.

En plus des variables ci-dessus, le modèle lit celles de la page :

| Variable | Valeur |
|---|---|
| `{{ man }}` | le `man` de la page, sinon `footer.right` |
| `{{ path }}` | la place de la page, après `~/<site>` : `/events` pour un événement, `/mentorat` pour une page, `/blog` pour la page du blog |
| `{{ url }}` | l'adresse de cette place, sans le schéma : `example.org/events` |
| `{{ title_1 }}`, `{{ title_2 }}` | le `share_title` de la page, sinon son `title`, sur `share.title_lines` lignes de `share.title_columns` caractères |
| `{{ title_shift }}` | de combien de pixels remonte ce qui suit le titre quand celui-ci laisse une ligne vide : un `translate` |
| `{{ detail_1 }}` | le `tagline` de la page ; celui d'un article ou d'un événement est sa date en toutes lettres |
| `{{ detail_2 }}` | le `place` d'un événement, sinon l'`author` d'un article |
| `{{ tag }}`, `{{ tag_width }}`, `{{ tag_display }}` | le `tag` de la page ; la largeur d'un cadre autour ; `none` quand il n'y en a pas, pour `display=` |

Le texte est ajusté au nombre de caractères : le modèle convient à une
police à chasse fixe. Un titre se coupe aux espaces ; ce qui ne tient
pas sur sa dernière ligne est tronqué, terminé par `...`, trois points.
Une ligne de détail, et le tag, sont tronqués à `share.detail_columns`.
L'`og:image:alt` est le texte de la carte,
`~/my site/events - Meetup - samedi 21 novembre 2026 - Library`, sauf
si la page règle `image_alt`. Comme les diagrammes, les cartes sont en
cache : en mémoire tant que `--watch` tourne, dans `TILDER_CACHE`, et
dans la sortie précédente. Le thème de départ de tilder fournit un
`share-page.svg`.

## Outils et solutions de repli

Le dessin demande un moteur de rendu SVG. La construction prend le
premier qu'elle trouve :

1. `rsvg-convert` : il dessine le texte avec les polices du thème ;
2. `magick`, ImageMagick 7.

L'image Docker de tilder contient `rsvg-convert` et `woff2_decompress` :
une construction dans Docker dessine tout. Avec Python seul, installez
l'un d'eux depuis les paquets de votre système. Sans aucun des deux, la
construction fonctionne quand même et le dit une fois :

```text
warning: no rsvg-convert or magick: icons and share.png not made
```

Les liens du gabarit vers les icônes ne mènent alors nulle part, et les
aperçus pointent vers une image absente : installez un moteur de rendu
avant de déployer. Sans le logo, le fichier que nomme `share.logo_svg`,
la construction le dit aussi, et ne dessine rien :

```text
warning: no logo.svg in assets/: no icons, no share.png
```

Chaque avertissement est décrit dans [la ligne de commande](docs/reference/cli).

## Le manifeste web

`site.webmanifest`, écrit une seule fois à la racine, dit à un navigateur
comment installer le site comme une application. Avec les valeurs par
défaut, mis en page plus court :

```json
{
  "name": "my site",
  "short_name": "site",
  "lang": "en",
  "start_url": "./",
  "display": "browser",
  "background_color": "#FDF6E3",
  "theme_color": "#0F6E68",
  "icons": [
    {"src": "logo.svg", "type": "image/svg+xml", "sizes": "any"},
    {"src": "icon-192.png", "type": "image/png", "sizes": "192x192"},
    {"src": "icon-512.png", "type": "image/png", "sizes": "512x512"}
  ]
}
```

Les valeurs sont `site.name`, `share.short_name`, `site.lang`,
`share.background_color` et `share.theme_color`, dans la langue par
défaut.

## Voir aussi

- [types de contenu](docs/content-types)
- [SEO](docs/reference/seo)
- [les fichiers d'un thème](docs/themes/files)
