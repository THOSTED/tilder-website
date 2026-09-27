---
title: Écrire des pages
description: D'un fichier Markdown à une page : son adresse, chaque clé de l'en-tête, les sections de page de manuel, les liens entre langues, les images.
order: 30
---

## Nom

writing - pages, en-tête, sections, liens et images

Une page est un fichier Markdown dans `content/` : un en-tête qui dit ce
qu'est la page, puis des sections à la manière d'une page de manuel. Son
chemin lui donne son adresse. Les liens s'écrivent depuis la racine du
site et la construction les rend relatifs ; les images se rangent à côté
de la page qui les montre.

[TOC]

## Pages et adresses

Le chemin d'un fichier dans `content/` est son adresse, sans le `.md`. Le
`index.md` d'un dossier est la page du dossier lui-même, avec une barre
oblique finale.

| Source | Adresse | Miroir en texte |
|---|---|---|
| `content/index.md` | `/` | `txt/index.txt` |
| `content/about.md` | `/about` | `txt/about.txt` |
| `content/blog/index.md` | `/blog/` | `txt/blog.txt` |
| `content/blog/2026-01-01-hello.md` | `/blog/2026-01-01-hello` | `txt/blog/2026-01-01-hello.txt` |
| `content/blog/2026-01-01-hello/index.md` | la même | le même |

- La construction écrit `about.html` ; le serveur répond à `/about` avec
  ce fichier ([déploiement](docs/guide/deployment)).
- Nommez les fichiers en anglais, en minuscules, avec des tirets :
  `code-of-conduct.md`. La page elle-même peut être dans n'importe quelle
  langue, et ses traductions gardent le même nom
  ([langues](docs/guide/languages)).
- Un fichier ou un dossier dont le nom commence par `_` n'est jamais
  construit : `_draft.md`, `blog/_template.md`.
- Un élément de collection peut être un dossier, `<slug>/index.md`, pour
  garder ses images à côté de lui ; sa page reste `/blog/<slug>`.
- Chaque page figure dans `sitemap.xml` et `sitemap.txt`, sauf si son
  `robots` contient `noindex`.

Dans une collection récursive, comme la documentation que vous lisez, les
dossiers s'imbriquent : `content/docs/guide/writing.md` est la page
`/docs/guide/writing`, et le `index.md` d'un dossier est la page propre de
cette section, placée à côté de lui : `content/docs/guide/index.md` est
`/docs/guide`. La page des [collections](docs/content-types) explique
l'interrupteur, `recursive`.

## L'en-tête

L'en-tête ouvre le fichier, entre deux lignes `---` : une ligne
`clé: valeur` par clé. Les valeurs sont du texte brut, jamais entre
guillemets : `nav: ""` donnerait deux guillemets, alors la page d'accueil
écrit `nav:` sans rien derrière.

```markdown
---
man: MYSITE-ABOUT(7)
title: À propos
description: Qui écrit ce site et pourquoi, et comment nous joindre.
tagline: qui, pourquoi, et comment écrire
nav: about
---

## Nom

about - qui écrit ce site
```

Ces clés valent pour toutes les pages. Celles marquées obligatoires
arrêtent la construction quand elles manquent ; `man`, `tagline` et `nav`
viennent de la collection pour ses éléments, qui peuvent s'en passer.

| Clé | Rôle |
|---|---|
| `man` | obligatoire : le nom de page de manuel, `MYSITE-ABOUT(7)`, dans la règle d'en-tête de la page et de son miroir en texte |
| `title` | obligatoire : le titre de la page. Le `<title>` y ajoute `site.title_suffix`, sauf si le titre nomme déjà le site. La construction avertit au-delà de `seo.title_max` caractères, suffixe compris (60) |
| `description` | obligatoire : une phrase, pour les moteurs de recherche, les aperçus de lien et les flux. La construction avertit hors de `seo.description_min` à `seo.description_max` caractères (50 à 160) |
| `name` | le dernier segment de la page dans le chemin du `<h1>`, `~/mon site/<name>` ; par défaut, le titre sans le suffixe. Sur la page d'un dossier, il nomme aussi le segment de ce dossier sur chaque page qu'il contient. `heading` en est l'ancienne orthographe |
| `tagline` | la ligne sous le logotype, pour le `{{ page.tagline }}` du gabarit ; celle d'un article ou d'un événement est par défaut sa date |
| `nav` | l'entrée de `[[nav]]` marquée comme courante, par son `href` : `about`, `blog/`, rien pour la page d'accueil, `-` pour aucune |
| `feed` | le nom d'une collection, ou `all` : ajoute le `<link rel="alternate">` du flux RSS de cette collection |
| `text` | `text: no` ne construit pas de miroir en texte pour la page (c'est le cas de la page 404) |
| `image` | l'aperçu de lien, relatif au dossier de la page ; par défaut `share.image`. Un PNG ou un JPEG, idéalement en 1200x630 : les réseaux sociaux ignorent le plus souvent le SVG |
| `image_alt` | le texte alternatif de l'aperçu ; par défaut `share.image_alt` |
| `updated` | une date, `2026-03-01` : la dernière modification de la page dans le plan du site ; par défaut, la date d'un élément, sinon `site.updated` |
| `robots` | le `<meta name="robots">` de la page ; par défaut `seo.robots`. Avec `noindex`, la page sort des plans du site et des vérifications de référencement de la construction |
| `layout` | `layout: home` rend la page avec le gabarit `layouts/home.html` du thème, qui doit exister |
| `group` | dans une collection, le groupe de l'élément dans la barre latérale du thème |
| `order` | lu par le thème de ce site, pas par tilder : un nombre entier, la place de la page parmi celles de la documentation (1000 par défaut) |

Chaque type lit aussi ses propres clés : `author` et `tag` pour un
article, `place` et `end` pour un événement, les noms et les profils d'un
membre. Elles sont listées avec leur type, dans
[types de contenu](docs/content-types). Toute autre clé est conservée, et
un gabarit l'affiche avec `{{ page.<key> }}`
([gabarits](docs/themes/layouts)).

## Les sections

Une section est un titre `##` et ce qui le suit. Elle se présente comme
une rangée de page de manuel : le nom dans la marge de gauche, le texte à
côté. Dans le miroir en texte, le nom est imprimé en capitales contre la
marge et le texte en retrait en dessous.

Les pages s'ouvrent sur `## Nom` (`## Name` en anglais), comme une page de
manuel : le nom de la page, un tiret et une ligne qui dit ce qu'elle est,
puis un paragraphe qui la résume. Les autres sections suivent dans l'ordre
où le lecteur en a besoin.

```markdown
## Nom

about - qui écrit ce site

Un paragraphe qui résume la page.

## Contact {#write}

Écrivez à l'adresse ci-dessous.
```

Un titre peut se terminer par des marqueurs entre accolades. `{#write}`
donne à la section l'identifiant `write`, si bien que `about#write` y
mène ; sans marqueur, l'identifiant vient du titre. `{text}` retire une
section de la page HTML, et `{html}` du miroir en texte. `{grid}` dispose
ses entrées en cartes, un marqueur de liste comme `{posts}` la remplit
depuis une collection, et tout autre mot devient une classe. Les titres
`###` d'une section sont des entrées, dont le texte est en retrait de deux
espaces. La [référence des sections](docs/reference/markdown/sections)
donne chaque marqueur.

## Liens

Écrivez la cible d'un lien depuis la racine du site : sans barre oblique
au début, sans `.html`. La construction la réécrit relativement à la
page, si bien que la même source fonctionne sur n'importe quelle page, à
n'importe quelle profondeur.

| Cible | Mène à |
|---|---|
| `blog/2026-01-01-hello` | une page |
| `blog/` | la page d'un dossier : gardez la barre oblique |
| vide, ou `./` | la page d'accueil |
| `about#write` | une section d'une page |
| `#write` | une section de cette page |
| `blog/feed.xml`, `logo.svg` | un fichier, servi sous son propre nom |
| `https://example.org/` | un autre site, laissé tel quel |

Cette page mène à la suivante par `[langues](docs/guide/languages)` ; la
construction écrit `languages`, puisque les deux sont dans
`/fr/docs/guide/`.

**D'une langue à l'autre.** Sur un site en plusieurs langues, une cible
reste dans la langue de la page : `docs/guide/languages` sur une page
française est la page française, `/fr/docs/guide/languages`. Une cible qui
commence par `/` sort de la langue : `[in English](/about)` depuis une page
française, `[en français](/fr/about)` depuis une page anglaise. Un fichier
est écrit une seule fois, à la racine, et toutes les langues pointent vers
le même. Les flux RSS sont écrits par langue, mais un lien vers
`blog/feed.xml` dans une page reste le flux de la langue par défaut :
écrivez `/fr/blog/feed.xml` pour le flux français
([langues](docs/guide/languages)).

**Liens externes.** Terminez le libellé d'un lien vers un autre site par
la flèche nord-est, U+2197 : `[archive ↗](https://example.org/)`. Les
lecteurs d'écran sautent la flèche et entendent `labels.external` à la
place ; le miroir en texte la supprime. Que les liens externes s'ouvrent
ou non dans un nouvel onglet se décide une fois pour tout le site, dans
`site.toml` :

```toml
[links]
new_tab = true                # liens externes : nouvel onglet
same_tab = ["example.com"]    # sauf ces hôtes et sous-domaines
```

Les valeurs par défaut sont `new_tab = false` et `same_tab = []`. Un lien
qui ouvre un nouvel onglet le dit d'avance aux lecteurs d'écran, avec
`labels.new_tab`. Dans le miroir en texte, un lien interne ne garde que
son libellé, tandis qu'un lien externe affiche son adresse entre
parenthèses après lui.

## Images

Une image est seule sur sa ligne, comme en Markdown ; le texte entre
guillemets après le chemin, facultatif, devient sa légende :

```markdown
![Les deux sorties d'une page](flow.svg "Une source, deux rendus.")
```

- Le chemin est relatif au dossier de la page, contrairement aux liens :
  rangez l'image à côté de la page. Pour un article, prenez un dossier,
  `blog/2026-01-01-hello/`, avec `index.md` et l'image dedans.
- Le texte alternatif est obligatoire : c'est ce que dit un lecteur
  d'écran et ce qu'affiche le miroir en texte,
  `[ image ] Les deux sorties d'une page`.
- La construction lit la largeur et la hauteur dans le fichier (PNG, JPEG,
  GIF, WebP, SVG), pour que la page ne saute pas pendant le chargement.
- Une image venue d'un autre site est permise par la syntaxe, mais la
  politique de serveur recommandée ne laisse les pages charger que les
  images de leur propre site : elle ne s'affichera pas.

La construction avertit, et continue, quand le fichier manque ou que le
texte alternatif est vide :

```text
warning: image not found: content/blog/2026-01-01-hello/flow.svg
warning: image without alt text: blog/2026-01-01-hello/flow.svg
```

Préférez le SVG pour les schémas : un fichier SVG peut porter ses propres
couleurs pour le mode sombre, et le serveur le laisse se styler lui-même,
jamais exécuter de script. La
[référence des liens et des images](docs/reference/markdown/links-and-images)
entre dans le détail.

## Voir aussi

- [la référence Markdown](docs/reference/markdown)
- [les langues](docs/guide/languages)
- [le référencement](docs/reference/seo)
