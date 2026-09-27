---
title: event
description: Le type event : des éléments datés avec un lieu, à venir ou passés selon la date de construction, les listes {upcoming}, {past}, {next-event}, les flux.
order: 30
---

## Nom

event - des éléments datés avec un lieu, à venir ou passés

Un événement est un fichier Markdown nommé par sa date, dans une
collection de type `event` : des rencontres, des conférences, des sorties.
Sa carte dit quand et où ; il est à venir jusqu'à ce que sa date soit
passée, puis passé, sans que personne ne touche au fichier. La collection
liste ses événements de trois façons, écrit un flux RSS et un fichier
iCalendar auquel les applications d'agenda s'abonnent.

[TOC]

## Réglages

Une collection `event` peut fixer ces clés sous `[collections.<name>]` ;
chacune a sa valeur par défaut dans le module du type, `types/event.py`.

| Clé | Défaut | Rôle |
|---|---|---|
| `event.man` | `"SITE-EVENTS(7)"` | le nom de page de manuel de ses éléments, sauf s'ils fixent le leur |
| `event.nav` | `"events"` | l'entrée de `[[nav]]` que ses éléments marquent comme courante, et le lien du flux |
| `event.upcoming_tag` | `"upcoming"` | l'étiquette de la carte d'un événement à venir |
| `event.past_tag` | `"past"` | l'étiquette de la carte d'un événement passé |
| `event.none_upcoming` | `"No upcoming event."` | le texte d'une liste `{upcoming}` ou `{next-event}` vide |
| `event.none_past` | `"No past event."` | le texte d'une liste `{past}` vide |
| `event.link_label` | `"event website ↗"` | le lien vers le site de l'événement, sur sa page |
| `event.map_label` | `"see on OpenStreetMap ↗"` | le lien vers le lieu sur la carte, sur sa page |
| `event.feed` | `""` | le chemin du flux RSS depuis la racine du site, `"events.xml"` ; vide pour aucun |
| `event.feed_title` | `"events"` | le titre du flux |
| `event.feed_description` | `"Upcoming and past events."` | la description du flux |
| `event.calendar` | `""` | le chemin du fichier iCalendar depuis la racine du site, `"events.ics"` ; vide pour aucun |

Une étiquette vide, `upcoming_tag = ""`, laisse la carte sans étiquette.
`defaults.toml` déclare déjà `[collections.events]`, avec
`feed = "events.xml"` et `calendar = "calendar.ics"` : créer
`content/events/` suffit pour commencer. Une deuxième collection nomme les
siens :

```toml
[collections.talks]
type = "event"
nav = "talks"
feed = "talks.xml"
calendar = "talks.ics"
upcoming_tag = "soon"
none_upcoming = "No talk planned yet."
```

## Un fichier par événement

Le fichier d'un événement se nomme `YYYY-MM-DD-slug.md`, la date à
laquelle il commence, comme celui d'un article
([post](docs/content-types/post)) : la même forme en dossier pour les
images, les mêmes traductions `.fr.md`, les mêmes erreurs pour une date
qui n'existe pas.

Un événement dure des journées entières. Aucune clé ne donne l'heure :
écrivez-la dans la description ou dans la page, et donnez le dernier jour
dans `end` quand il dure plus d'une journée.

## En-tête

```text
---
title: Spring meetup
description: Talks and a workshop on documentation, then dinner.
place: 1 Example Street, Exampleton
link: https://meetup.example/spring
end: 2099-03-02
lat: 48.8566
lon: 2.3522
---
```

| Clé | Rôle |
|---|---|
| `title` | le nom de l'événement |
| `description` | une phrase : le texte de la carte dans une liste, le résumé dans le flux, la `DESCRIPTION` du calendrier |
| `place` | le lieu : une adresse ou une salle, sur la carte, dans le `LOCATION` du calendrier et dans les données structurées |
| `link` | le site de l'événement, lié depuis sa page avec `link_label` |
| `end` | `YYYY-MM-DD`, le dernier jour d'un événement de plusieurs jours |
| `lat`, `lon` | les coordonnées du lieu : un repère exact sur la carte, le `GEO` du calendrier, le `geo` des données structurées |
| `man`, `nav` | par défaut, le `man` et le `nav` de la collection |
| `tagline` | par défaut, la date en toutes lettres, écrite selon les `[dates]` de la langue |

Toutes les autres clés d'[écrire des pages](docs/guide/writing)
s'appliquent aussi. Ne donnez des coordonnées que si vous les
connaissez : sans elles, le lien vers la carte cherche plutôt l'adresse
donnée par `place`.

## La carte

La carte montre la date dans un `<time>`, prolongée jusqu'à `end` en
toutes lettres quand l'événement dure plusieurs jours
(`Sunday 1 March 2099 - Monday 2 March 2099`), le lieu, et l'étiquette :
`upcoming_tag` quand l'événement commence aujourd'hui ou plus tard,
`past_tag` une fois ce jour passé. Dans une liste, elle montre la
description et mène à l'événement.

Sur la page de l'événement, la carte mène aussi à son site (`link`,
avec le libellé `link_label`) et au lieu sur OpenStreetMap
(`map_label`) : un repère à `lat` et `lon` quand les deux sont donnés,
sinon une recherche de `place`. C'est un lien, pas une carte intégrée :
le navigateur d'un lecteur n'appelle aucun autre site tant qu'il ne
clique pas. Le miroir en texte garde le site de l'événement et laisse le
lien vers la carte de côté : l'adresse est déjà sur la carte, et l'URL de
la carte ne tiendrait pas en 75 colonnes.

## À venir et passés

Trois marqueurs listent une collection d'événements, tous selon la date
de construction :

| Marqueur | Liste |
|---|---|
| `{upcoming}` | les événements qui commencent aujourd'hui ou plus tard, du plus proche au plus lointain ; le premier est marqué comme le prochain (`.entry--next`, `.tag--next`) |
| `{past}` | les événements qui ont commencé avant aujourd'hui, du plus récent au plus ancien |
| `{next-event}` | le prochain événement seulement, marqué de la même façon |

```text
## Upcoming {upcoming}

## Past {past}
```

Chacun accepte un nom de collection, `{upcoming:talks}`, comme tout
marqueur ([les collections](docs/content-types)). Une liste vide affiche
`none_upcoming` ou `none_past`.

« Aujourd'hui », c'est le jour où le site est construit. Un événement ne
passe d'une liste à l'autre que lorsque le site est reconstruit : un site
qui a des événements doit donc être reconstruit chaque jour. En mode
surveillance, tilder reconstruit à minuit pour cette seule raison, même
si aucun fichier n'a changé ; le fichier compose du
[déploiement](docs/guide/deployment) le lance ainsi. Un site construit à
la main, ou en intégration continue, a besoin de sa propre construction
quotidienne. La construction lit le jour dans la variable d'environnement
`BUILD_TODAY` quand elle est définie, `BUILD_TODAY=2099-03-01` : c'est
ainsi qu'on prévisualise les listes telles qu'elles seront un autre jour.

## RSS

Quand `feed` est fixé, le flux RSS de la collection liste tous les
événements, à venir et passés, de la date la plus tardive à la plus
ancienne, chacun avec son titre, son adresse, sa date et sa description ;
`feed_title` et `feed_description` nomment le canal. Chaque langue a le
sien, sous son préfixe, comme pour les articles
([post](docs/content-types/post)).

## iCalendar

Quand `calendar` est fixé, la construction écrit un fichier iCalendar
(RFC 5545) auquel les applications d'agenda peuvent s'abonner. Il est
écrit une seule fois, dans la langue par défaut, et contient tous les
événements de la collection :

- chaque événement comme un `VEVENT` sur des journées entières, de sa
  date à son `end` ou à sa date (`DTEND` est le lendemain, comme le veut
  le format), avec son `UID`, son titre suivi du nom du calendrier comme
  `SUMMARY`, le `place` comme `LOCATION`, `lat` et `lon` comme `GEO`, son
  adresse comme `URL` et sa description ;
- le nom, la description, l'identifiant de produit et le fuseau horaire
  du calendrier lui-même, pris dans la table `[calendar]` :
  `calendar.name`, `calendar.description`, `calendar.prodid`,
  `calendar.timezone`, et `calendar.uid_domain` pour les identifiants.
  Leurs valeurs par défaut sont sur la page
  [les collections](docs/content-types).

Le texte est ramené à l'ASCII et coupé en lignes de 75 octets, comme
l'exige le format.

## Moteurs de recherche

Le corps d'un événement est enveloppé dans un `<article>`. Son nœud
JSON-LD est un `Event` : `name`, `description`, `startDate` (la date),
`endDate` (`end`, sinon la date), un événement programmé et en présentiel,
son `location` comme `Place` nommé par `place` (avec `geo` d'après `lat`
et `lon`), l'organisation du site comme `organizer`, et l'`image`
d'aperçu. Son `og:type` vaut `website`.

## Voir aussi

- [les collections](docs/content-types)
- [post](docs/content-types/post)
- [flux et images](docs/reference/feeds-and-images)
- [la ligne de commande](docs/reference/cli)
