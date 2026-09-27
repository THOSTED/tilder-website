---
title: member
description: Le type member : une page par personne, une grille qu'on peut filtrer avec {members}, des catégories, les pronoms, les profils publics et members.js.
order: 40
---

## Nom

member - des personnes, une page chacune, dans une grille où l'on peut chercher

Un membre est une personne décrite une seule fois, dans l'en-tête d'un
fichier, au sein d'une collection de type `member` : les personnes d'une
association, d'une équipe, une liste de mentors. Chacune a sa page et une
carte avec ses noms, ses pronoms, son affiliation et ses profils publics ;
une section marquée `{members}` les montre toutes en une grille que le
`members.js` du thème peut parcourir et filtrer.

[TOC]

## Réglages

Une collection `member` peut fixer ces clés sous `[collections.<name>]` ;
chacune a sa valeur par défaut dans le module du type, `types/member.py`.

| Clé | Défaut | Rôle |
|---|---|---|
| `man` | `"SITE-MEMBERS(7)"` | le nom de page de manuel de ses éléments, sauf s'ils fixent le leur |
| `nav` | `"members"` | l'entrée de `[[nav]]` que ses éléments marquent comme courante |
| `categories` | `["admin", "member"]` | les catégories, dans l'ordre de la grille et des boutons du filtre |
| `default_category` | `"member"` | la catégorie d'un membre dont l'en-tête n'en fixe pas |
| `empty` | `"No member listed yet."` | le texte d'une liste `{members}` vide |
| `search_label` | `"search"` | le libellé du champ de recherche |
| `search_placeholder` | `"first or last name"` | le texte indicatif du champ de recherche |
| `all` | `"all"` | le bouton du filtre qui montre toutes les catégories |
| `one` | `"entry"` | le mot qui suit le décompte, au singulier |
| `many` | `"entries"` | le mot qui suit le décompte, au pluriel |
| `none` | `"No entry matches."` | ce que dit une recherche qui ne trouve rien |
| `full` | `"full"` | dit sur la carte d'un membre dont la capacité est atteinte |

Les six mots de `search_label` à `none` sont destinés à `members.js`, qui
ne contient aucun texte. `defaults.toml` déclare déjà
`[collections.members]`, sur `content/members/` ; un site qui a des
mentors ajoute leur catégorie et ses propres mots :

```toml
[collections.members]
type = "member"
categories = ["admin", "mentor", "member"]
search_placeholder = "name"
```

## Un fichier par membre

Un membre est `content/members/<slug>.md`, ou un dossier avec son
`index.md`. Le type n'est pas daté : n'importe quel identifiant convient,
`jane-doe.md`. Partez d'un `_template.md` placé dans le dossier, qui liste
chaque champ ; son nom l'empêche d'être construit.

## En-tête

```text
---
title: Jane Doe
description: Jane Doe, who runs the project and answers its mail.
tagline: admin
first_name: Jane
last_name: Doe
pronouns: she/her
category: admin
affiliation: Example Corp
website: https://jane.example
mastodon: https://social.example/@jane
---
```

| Clé | Rôle |
|---|---|
| `first_name`, `last_name` | le prénom et le nom ; `last_name` trie la grille |
| `display_name` | le nom à afficher quand ce n'est ni le prénom ni le nom : un nom choisi, un pseudonyme, un nom unique. S'il est donné, c'est le seul nom affiché ; les autres restent cherchables |
| `pronouns` | tels que la personne les écrit (`elle`, `il/lui`, `iel`) ; demandez, ne devinez jamais, et laissez vide si elle préfère |
| `category` | l'une des `categories` de la collection ; par défaut `default_category`. L'étiquette de la carte, et celle du filtre |
| `affiliation` | une entreprise, une école ou un projet, si la personne veut en afficher un |
| `capacity` | une note sur ce qu'elle peut encore prendre, `2 per term`, pour une catégorie qui en tient le compte, comme les mentors |
| `full` | `yes` quand cette capacité est atteinte : l'étiquette passe à la couleur d'avertissement et `full` est dit en toutes lettres |
| `linkedin`, `github`, `gitlab`, `mastodon`, `bluesky`, `website` | les adresses de profils publics (plus bas) |
| `man`, `nav` | par défaut, le `man` et le `nav` de la collection |

Laissez vide ce qui ne s'applique pas : un champ vide n'affiche rien. Il
n'y a volontairement aucun champ pour le genre, l'âge ou une photo.
`title` et `description` sont ceux de la page, comme sur toute page ; la
carte montre le nom du membre, pas le titre.

## La grille

Une section marquée `{members}` liste tous les membres de la collection
en grille (`.grid`), dans cet ordre : par catégorie, dans l'ordre de
`categories` (une catégorie absente de cette liste vient après) ; puis par
nom, sans tenir compte des accents ni de la casse ; puis par nom de
fichier.

```text
## Members {members}
```

Chaque carte montre le nom (`display_name`, sinon le prénom et le nom),
une ligne avec les pronoms, l'affiliation, la capacité et, quand `full`
est donné, le mot `full`, la catégorie en étiquette, et les liens vers
les profils. Dans la grille, le nom mène à la page du membre ; sur cette
page, la même carte, sans le lien, clôt la première section.

## Profils

Six clés portent des profils publics, affichés dans cet ordre :
`linkedin`, `github`, `gitlab`, `mastodon`, `bluesky`, `website`. Chacune
contient une adresse, ou plusieurs séparées par des espaces, un compte
personnel et un compte professionnel ; chacune est alors nommée par la
dernière partie de son adresse, `GitHub (jane)`.

- **Logos.** Un lien montre le `theme/icons/<network>.svg` du thème,
  `icons/github.svg` pour `github`, inséré dans la page (ses tracés
  seulement, avec la classe `.icon`, pour que le thème le colore) et
  masqué aux lecteurs d'écran, qui entendent le nom du réseau à la place.
  Sans icône, le lien montre le nom suivi de `↗`. `website` est nommé par
  `labels.website`, `"website"` par défaut
  ([configuration](docs/reference/configuration)).
- **Vérification.** Chaque lien porte `rel="me"`, qui permet à un profil
  renvoyant vers la page de la vérifier, et les adresses forment le
  `sameAs` des données structurées du membre.
- **Miroir en texte.** Chaque profil tient sur une ligne,
  `GitHub: <address>`.

## Recherche et filtre

Une page qui a une section `{members}` charge le `members.js` du thème,
si le thème en fournit un : le type le nomme dans son `SCRIPT`. Le script
appartient au thème ; celui que tilder décrit ajoute un champ de
recherche (prénom, nom et nom affiché, sans tenir compte des accents ni
de la casse, chaque mot devant correspondre) et un bouton par catégorie.
Sans JavaScript, la grille entière s'affiche, tout simplement
([scripts](docs/themes/scripts)).

Il trouve dans la page ce dont il a besoin. Chaque carte porte
`data-category` et `data-search` (les noms du membre, en ASCII
minuscule), et la section porte les six mots de la collection en
`data-search_label`, `data-search_placeholder`, `data-all`, `data-one`,
`data-many` et `data-none`, si bien que le script parle la langue de la
page.

## Moteurs de recherche

La page d'un membre est une `ProfilePage` dont la `mainEntity` est une
`Person` : son `name` est le titre affiché de la page (son `name:`, sinon
son titre sans le suffixe du site), pas `display_name` ; l'organisation
du site est son `memberOf`, les profils son `sameAs`, et l'`affiliation` comme `Organization`. Une
collection de membres n'a pas de flux RSS : le type ne fournit pas
d'entrées de flux.

## Voir aussi

- [les collections](docs/content-types)
- [scripts](docs/themes/scripts)
- [les fichiers d'un thème](docs/themes/files)
