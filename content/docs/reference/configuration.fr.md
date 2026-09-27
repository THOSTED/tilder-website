---
title: Configuration
description: Chaque clé du defaults.toml de tilder, table par table : sa valeur par défaut, son rôle, et un exemple de réglage dans site.toml.
order: 20
---

## Nom

configuration - chaque clé de defaults.toml

tilder lit chaque réglage d'un site, et chaque mot qu'un lecteur voit en
dehors des pages, dans des fichiers TOML. Son propre `defaults.toml`
contient chaque clé avec une valeur par défaut neutre, en anglais ; le
`theme.toml` du thème et le `content/site.toml` du site se fusionnent
par-dessus, et ne disent que ce qui change. Cette page reprend chaque clé
de `defaults.toml`, table par table, avec sa valeur par défaut telle que
le fichier l'écrit.

[TOC]

## La fusion des fichiers

Chaque fichier se fusionne par-dessus le précédent, le dernier l'emporte :
`defaults.toml`, puis `theme/theme.toml`, puis `content/site.toml`. Sur un
site en plusieurs langues, `theme/theme.<lang>.toml` vient après
`theme.toml`, et `content/site.<lang>.toml` après `site.toml`, pour la
passe de cette langue ([le projet](docs/guide/project),
[langues](docs/guide/languages)).

- Les tables se fusionnent clé par clé : un fichier qui règle
  `[site] manual` garde toutes les autres clés de `[site]`.
- Une valeur qui n'est pas une table, liste comprise, remplace la
  précédente en entier. Une liste de tables, `[[nav]]`, aussi : un
  fichier qui la règle en répète chaque entrée.
- Les réglages d'une collection partent des valeurs par défaut de son
  type, dans le module du type, avec `[collections.<name>]` par-dessus
  ([types de contenu](docs/content-types)).

Les fichiers sont relus à chaque construction, et aucun n'est jamais
servi. Une clé que tilder ne lit pas est ignorée, sauf les quelques
tables retirées, qui arrêtent la construction avec un message disant où
sont passées leurs clés ([la ligne de commande](docs/reference/cli)).

## Site

La table `[site]` : qui est le site, où il vit, sa langue.

| Clé | Défaut | Rôle |
|---|---|---|
| `site.name` | `"my site"` | le logotype, `~/my site` ; `og:site_name` ; le `WebSite` des données structurées ; le `name` du manifeste web |
| `site.url` | `"https://example.org"` | l'origine canonique, sans barre oblique finale : chaque adresse absolue qu'écrit la construction commence par elle |
| `site.lang` | `"en"` | la langue par défaut, servie à la racine : le `lang` de la page, des flux, du manifeste |
| `site.locale` | `"en_GB"` | `og:locale`, pour Open Graph |
| `site.manual` | `"My Site Manual"` | le centre du filet d'en-tête de page de manuel, sur la page et dans le miroir en texte |
| `site.updated` | `2026-01-01` | une date TOML, pas une chaîne : la date du filet de pied de page, le `lastBuildDate` des flux, le dernier recours de `<lastmod>` dans le plan du site |
| `site.title_suffix` | `" - my site"` | ajouté à chaque `<title>` qui ne contient pas déjà `site.name` |
| `site.languages` | `[]` | chaque langue servie, celle par défaut (`lang`) en premier ; vide : une seule langue, sans préfixe |

`site.url` doit être l'adresse à laquelle le site est servi : les liens
canoniques, `og:url`, les plans du site, les flux et le calendrier en
sont tirés. `site.title_suffix` n'est ajouté que si le titre ne nomme pas
déjà le site, majuscules ou non : une page intitulée `About my site`
garde son titre tel quel.

```toml
[site]
name = "my site"
url = "https://example.org"
lang = "en"
locale = "en_GB"
manual = "My Site Manual"
updated = 2026-05-16
title_suffix = " - my site"
languages = ["en", "fr"]
```

## Pied de page

La table `[footer]` : le filet de pied de page de manuel, en bas de
chaque page, avec `site.updated` en son milieu.

| Clé | Défaut | Rôle |
|---|---|---|
| `footer.left` | `"SITE"` | la gauche du filet ; dans le gabarit du site de départ, un lien |
| `footer.left_link` | `""` | la cible de `footer.left`, depuis la page d'accueil de la langue : `""` est la page d'accueil elle-même |
| `footer.right` | `"SITE(1)"` | la droite du filet |

Le miroir en texte écrit lui-même le filet à partir de ces clés. Sur la
page, le gabarit les place où il veut : celui du site de départ écrit
`<a href="{{ home }}{{ footer.left_link }}">{{ footer.left }}</a>`
([gabarits et variables](docs/themes/layouts)).

```toml
[footer]
left = "MYSITE"
left_link = "about"
right = "MYSITE(1)"
```

## Libellés

La table `[labels]` : les mots de l'interface, dont beaucoup ne
s'entendent qu'à travers un lecteur d'écran. Traduisez-les dans
`site.<lang>.toml`.

| Clé | Défaut | Rôle |
|---|---|---|
| `labels.skip` | `"skip to content"` | le lien d'évitement, le premier de la page (une variable du gabarit) |
| `labels.nav` | `"Main navigation"` | le nom du repère de navigation (une variable du gabarit) |
| `labels.info` | `"INFO"` | le libellé d'un encadré d'information, sur la page et dans la boîte du miroir en texte |
| `labels.warning` | `"WARNING"` | le libellé d'un encadré d'avertissement |
| `labels.error` | `"ERROR"` | le libellé d'un encadré d'erreur |
| `labels.image` | `"image"` | la ligne d'une image dans le miroir en texte : `[ image ] texte alternatif` |
| `labels.task_done` | `"done"` | un élément fait d'une liste de tâches, lu par les lecteurs d'écran |
| `labels.task_todo` | `"to do"` | un élément à faire d'une liste de tâches, lu par les lecteurs d'écran |
| `labels.to_top` | `"↑ back to top"` | le lien qui remonte en haut de la page (une variable du gabarit) |
| `labels.copy` | `"copy"` | le bouton de copie des blocs de code, transmis au `code.js` du thème |
| `labels.copied` | `"copied"` | le même bouton, une fois la copie faite |
| `labels.external` | `"external site"` | dit par les lecteurs d'écran après un lien externe marqué de la flèche, à la place de la flèche |
| `labels.new_tab` | `"opens in a new tab"` | dit par les lecteurs d'écran sur un lien qui ouvre un nouvel onglet |
| `labels.table` | `"table"` | le nom de la zone défilante d'un tableau |
| `labels.toc` | `"contents"` | le titre du bloc `[TOC]` ; en capitales dans le miroir en texte |
| `labels.website` | `"website"` | le site personnel d'un membre, parmi ses liens de profil |
| `labels.languages` | `"Languages"` | le nom du sélecteur de langue, `{{ languages }}` |
| `labels.collection_nav` | `"In this section"` | le nom de la barre latérale `{{ collection_nav }}` ; une collection peut régler son propre `nav_label` |
| `labels.prev` | `"previous"` | le libellé de `{{ prev }}`, et de la ligne d'un type séquentiel dans le miroir en texte |
| `labels.next` | `"next"` | le libellé de `{{ next }}`, et de cette même ligne |

Les trois libellés d'encadré choisissent aussi la couleur de la boîte
dans le miroir en couleur : la boîte dont le filet du haut porte
`labels.info` est cyan, `labels.warning` jaune, `labels.error` rouge
([le miroir en texte](docs/reference/text-mirror)). Les variables du
gabarit ne servent que là où le `layout.html` du thème les écrit, comme
le fait celui du site de départ.

```toml
# content/site.fr.toml
[labels]
skip = "aller au contenu"
toc = "sommaire"
prev = "précédent"
next = "suivant"
```

## Liens

La table `[links]` : les liens externes s'ouvrent-ils dans un nouvel
onglet ?

| Clé | Défaut | Rôle |
|---|---|---|
| `links.new_tab` | `false` | `true` : chaque lien externe, `http://` ou `https://`, s'ouvre dans un nouvel onglet |
| `links.same_tab` | `[]` | avec `new_tab` activé, les hôtes dont les liens restent dans le même onglet, sous-domaines compris |

Un lien qui ouvre un nouvel onglet reçoit `target="_blank"` et
`rel="noopener"`, et l'annonce aux lecteurs d'écran avec
`labels.new_tab`. La règle vaut pour les liens des pages, la navigation
et les liens de profil d'un membre ([écrire des pages](docs/guide/writing)).

```toml
[links]
new_tab = true
same_tab = ["example.com"]    # et ses sous-domaines
```

## Langues

La table `[languages]` est vide par défaut : elle associe au code d'une
langue le nom qu'affiche le sélecteur de langue. Une langue sans nom
affiche son code.

```toml
[languages]
en = "English"
fr = "Français"
```

Les noms ne sont lus que dans la configuration de la langue par défaut :
ils s'écrivent une fois, dans `site.toml`, chacun dans sa propre langue
([langues](docs/guide/languages)).

## Navigation

La liste de tables `[[nav]]` : la navigation, dans l'ordre, une table par
lien. Par défaut, elle a une entrée.

| Clé | Défaut | Rôle |
|---|---|---|
| `nav.label` | `"home"` | le texte du lien |
| `nav.href` | `""` | la cible, écrite depuis la racine du site : `""` est la page d'accueil, `docs/` la page d'un dossier, `about` une page ; `https://` fait un lien externe |

Une page marque son entrée comme courante avec sa clé d'en-tête `nav:`,
égale au `href` de l'entrée ([écrire des pages](docs/guide/writing)). La
première entrée est aussi la première étape du fil d'Ariane de chaque
page dans les données structurées, et l'entrée que marque la page, sauf
la page d'accueil ou un lien externe, la deuxième ([SEO](docs/reference/seo)).
Les liens restent dans la langue courante : `about`, depuis une page
française, mène à `/fr/about`.

Une liste de tables se remplace en entier : un site qui ajoute un lien
les écrit tous, le premier compris.

```toml
[[nav]]
label = "home"
href = ""

[[nav]]
label = "blog"
href = "blog/"

[[nav]]
label = "source ↗"
href = "https://example.com/my-site"
```

## SEO

La table `[seo]` : les données structurées, la valeur par défaut pour
les robots, et les limites des vérifications de la construction
([SEO](docs/reference/seo)).

| Clé | Défaut | Rôle |
|---|---|---|
| `seo.organization` | `"My Site"` | l'éditeur : le nœud `Organization` des données structurées de chaque page |
| `seo.robots` | `"index, follow, max-image-preview:large"` | le `<meta name="robots">` d'une page qui ne règle pas `robots:` |
| `seo.title_max` | `60` | un `<title>` plus long, suffixe compris, donne un avertissement |
| `seo.description_min` | `50` | une description plus courte donne un avertissement |
| `seo.description_max` | `160` | une description plus longue donne un avertissement |

```toml
[seo]
organization = "Example Group"
title_max = 65
```

## Partage

La table `[share]` : les icônes, l'aperçu de lien et le manifeste web.
Les icônes sont dessinées à chaque construction à partir de
`assets/logo.svg`, et `share.png` à partir du `share.svg` du thème,
rempli avec les valeurs d'ici ([flux et images](docs/reference/feeds-and-images)).

| Clé | Défaut | Rôle |
|---|---|---|
| `share.logo_svg` | `"logo.svg"` | la source de chaque icône, un fichier de `assets/` |
| `share.image` | `"share.png"` | le fichier de l'aperçu par défaut, 1200x630, dessiné à partir du `share.svg` du thème : l'`og:image` de chaque page qui ne règle pas `image:`, quand le thème en a un |
| `share.logo` | `"icon-512.png"` | le logo des données structurées, et l'aperçu d'un thème sans `share.svg` ; le nom d'une icône que dessine la construction |
| `share.image_alt` | `"my site"` | l'`og:image:alt` d'une page qui ne règle pas `image_alt:` |
| `share.card` | `["a man-page website"]` | les lignes de l'aperçu sous le nom, une ou deux : `{{ card_1 }}` et `{{ card_2 }}` dans `share.svg` |
| `share.theme_color` | `"#0F6E68"` | la couleur de l'interface du navigateur : le `theme_color` du manifeste, le `<meta name="theme-color">` du site de départ, et l'aperçu |
| `share.background_color` | `"#FDF6E3"` | le `background_color` du manifeste, et le fond de l'aperçu |
| `share.text_color` | `"#073642"` | le texte de l'aperçu |
| `share.muted_color` | `"#506C75"` | le texte secondaire de l'aperçu |
| `share.rule_color` | `"#DED7C3"` | les filets de l'aperçu |
| `share.short_name` | `"site"` | le `short_name` du manifeste, le nom sous une icône sur l'écran d'accueil d'un téléphone |

Les cinq couleurs servent au `share.svg` du thème, qui les lit sous la
forme `{{ share.text_color }}` et ainsi de suite ; un thème les règle
d'habitude dans son `theme.toml`, en accord avec sa palette. Seules
`theme_color` et `background_color` sont aussi écrites par la
construction elle-même, dans le manifeste.

```toml
[share]
image_alt = "~/my site"
card = ["meetups and talks", "in Exampleville"]
short_name = "mysite"
```

## Collections

`[collections.<name>]` déclare un dossier de `content/` dont les fichiers
sont les éléments d'un même type ([types de contenu](docs/content-types)).
Ses clés sont les réglages du type, chacun décrit sur la page du type,
plus celles-ci :

| Clé | Défaut | Rôle |
|---|---|---|
| `type` | `"post"` | le type : `page`, `post`, `event`, `member`, ou un type ajouté par le thème |
| `dir` | le nom de la collection | le dossier, sous `content/` |

<!-- 1.2 -->

Depuis tilder 1.2, `recursive = true` fait des sous-dossiers de `dir`
des sections de la collection, et de leurs fichiers ses éléments, dans
l'arbre de la barre latérale ([navigation](docs/content-types/navigation)).
La valeur est `false` sauf si la collection ou les `DEFAULTS` de son
type la règlent ; un type daté, comme `post` ou `event`, ne peut pas
être récursif, et la construction s'arrête s'il l'est.

`defaults.toml` déclare les trois collections que la plupart des sites
ont. Chacune reste inactive tant que son dossier n'existe pas : ni page,
ni flux, ni calendrier.

| Clé | Défaut |
|---|---|
| `collections.blog.type` | `"post"` |
| `collections.blog.dir` | `"blog"` |
| `collections.blog.feed` | `"blog/feed.xml"` |
| `collections.events.type` | `"event"` |
| `collections.events.dir` | `"events"` |
| `collections.events.nav` | `"events"` |
| `collections.events.feed` | `"events.xml"` |
| `collections.events.calendar` | `"calendar.ics"` |
| `collections.members.type` | `"member"` |
| `collections.members.dir` | `"members"` |

Un site ne règle que ce qui en diffère, ou déclare les siennes :

```toml
[collections.blog]
man = "MYSITE-BLOG(7)"
feed_title = "my site blog"

[collections.talks]
type = "event"
feed = "talks.xml"
calendar = "talks.ics"
```

Les réglages de chaque type intégré sont sur sa page :
[post](docs/content-types/post), [event](docs/content-types/event),
[member](docs/content-types/member), [page](docs/content-types/page).

## Dates

La table `[dates]` : comment une date s'écrit en toutes lettres, sur la
carte d'un article ou d'un événement et comme accroche d'un article ou
d'un événement.

| Clé | Défaut | Rôle |
|---|---|---|
| `dates.weekdays` | `["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]` | les jours, lundi en premier |
| `dates.months` | `["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]` | les mois, janvier en premier |
| `dates.first` | `"1"` | comment s'écrit le premier jour du mois |
| `dates.format` | `"{weekday} {day} {month} {year}"` | le modèle |

`dates.format` prend quatre noms entre accolades : `{weekday}`, `{day}`
(le numéro du jour, sans zéro devant, ou `dates.first` le premier du
mois), `{month}` et `{year}`. Avec les valeurs par défaut, `2026-11-21`
s'écrit Saturday 21 November 2026. En français, « samedi 1er novembre » :

```toml
# content/site.fr.toml
[dates]
weekdays = ["lundi", "mardi", "mercredi", "jeudi", "vendredi",
            "samedi", "dimanche"]
months = ["janvier", "février", "mars", "avril", "mai", "juin",
          "juillet", "août", "septembre", "octobre", "novembre",
          "décembre"]
first = "1er"
format = "{weekday} {day} {month} {year}"
```

## Calendrier

La table `[calendar]` : ce que partagent tous les fichiers iCalendar du
site, pour les collections qui règlent `calendar`
([event](docs/content-types/event)).

| Clé | Défaut | Rôle |
|---|---|---|
| `calendar.name` | `"events"` | le nom du calendrier dans les applications, et la fin du résumé de chaque événement |
| `calendar.description` | `"Events."` | la description du calendrier |
| `calendar.prodid` | `"-//site//events//EN"` | l'identifiant du produit, `PRODID` |
| `calendar.timezone` | `"UTC"` | le fuseau horaire du calendrier |
| `calendar.uid_domain` | `"example.org"` | le domaine de l'identifiant de chaque événement, `<slug>@<uid_domain>` : mettez le vôtre |

```toml
[calendar]
name = "my site events"
prodid = "-//example.org//events//EN"
uid_domain = "example.org"
```

## Texte

La table `[text]` : les couleurs du miroir en texte.

| Clé | Défaut | Rôle |
|---|---|---|
| `text.commands` | `["curl"]` | les mots qui commencent une ligne de commande à mettre en valeur, dans un bloc de code du miroir en couleur |

Une ligne de bloc de code qui commence par l'un de ces mots, seul ou
après une invite, `$` ou `#` suivi d'une espace, prend la couleur
d'accent dans `ansi/` ; `txt/` n'a aucune couleur
([le miroir en texte](docs/reference/text-mirror)).

```toml
[text]
commands = ["curl", "docker", "python3"]
```

## Robots

Deux tables, une par `robots.txt` qu'écrit la construction
([SEO](docs/reference/seo)).

| Clé | Défaut | Rôle |
|---|---|---|
| `robots.disallow` | `["/txt/", "/ansi/"]` | le `robots.txt` du site : les chemins que les moteurs de recherche sont priés d'ignorer, les miroirs en texte |
| `robots_man.disallow` | `["/"]` | `txt/robots.txt`, le `robots.txt` de l'hôte en texte brut : tout |

Chaque chemin devient une ligne `Disallow:` ; une liste vide écrit
`Allow: /` à la place. Le `robots.txt` du site indique aussi
`sitemap.xml`.

```toml
[robots]
disallow = ["/txt/", "/ansi/", "/drafts/"]
```

## Vérification du thème

<!-- 1.2 -->

La table `[check]` appartient au thème : lue par `build.py --check`
(tilder 1.2), elle se règle dans `theme/theme.toml` ; `content/site.toml`
peut aussi la régler, fusionnée par-dessus celle du thème comme toute
autre table. `unstyled`, les
classes que le thème laisse sans style à dessein (défaut `[]`) ;
`contrast`, les paires de couleurs à vérifier (défaut `[]`, rien de
vérifié) ; `contrast_min`, le contraste minimal de chaque paire (défaut
`4.5`). Chaque clé est décrite dans
[vérifier un thème](docs/themes/checking).

## Voir aussi

- [le projet](docs/guide/project)
- [types de contenu](docs/content-types)
- [gabarits et variables](docs/themes/layouts)
- [la ligne de commande](docs/reference/cli)
