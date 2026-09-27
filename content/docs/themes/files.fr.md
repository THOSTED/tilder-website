---
title: Les fichiers d'un thème
description: Chaque fichier qu'un thème tilder peut fournir, ce qu'en fait la construction, ce qu'elle sert, et comment assets/ prend le pas sur le thème.
order: 10
---

## Nom

files - ce que peut contenir le dossier d'un thème, et ce qui est servi

Un thème a besoin de `layout.html`, et de rien d'autre. Chacun des autres
fichiers a un rôle que la construction connaît, ou bien il est copié tel
quel sur le site. Les fichiers que la construction se contente de lire,
gabarits, types, configuration, ne sont jamais servis ; et un fichier de
même nom dans le dossier `assets/` du site l'emporte sur celui du thème.

[TOC]

## Les fichiers

| Fichier | | Rôle |
|---|---|---|
| `layout.html` | obligatoire | la page autour du contenu, remplie par des variables ([gabarits](docs/themes/layouts)) |
| `style.css` | attendu | copié à la racine du site ; le gabarit y fait référence. Il met en forme les classes écrites par la construction ([classes](docs/themes/classes)) |
| `code.js` | facultatif | un bouton de copie sur les blocs de code, chargé seulement sur les pages qui en contiennent ([scripts](docs/themes/scripts)) |
| `members.js` | facultatif | la recherche et le filtre d'une liste `{members}`, chargé seulement là |
| `fonts/` | facultatif | les polices web ; ses fichiers `*.woff2` servent aussi à dessiner le texte de `share.png` |
| `icons/<network>.svg` | facultatif | le logo d'un lien de profil d'un membre ; sans lui, le nom du réseau s'affiche |
| `share.svg` | facultatif | l'aperçu de lien, dessiné en `share.png` (1200x630) ; sans lui, `og:image` est l'icône |
| `layouts/<name>.html` | facultatif | un gabarit pour les pages d'un type, ou demandé par `layout:` dans l'en-tête d'une page ; les mêmes variables que `layout.html` |
| `types/<name>.py` | facultatif | un type de contenu que le thème ajoute, ou un type intégré qu'il remplace ([types personnalisés](docs/content-types/custom-types)) |
| `theme.toml` | facultatif | les valeurs de configuration du thème, sous le `site.toml` du site : les couleurs de `[share]`, les mots propres au thème, et `[check]` pour `build.py --check` |
| `theme.<lang>.toml` | facultatif | le jumeau de `theme.toml` pour une langue, entre lui et le `site.toml` du site |

Tout autre fichier, un second script, une image utilisée par la feuille de
style, un dossier `.well-known/`, est copié à la racine du site, au même
chemin.

## Ce qui est servi

Tout le contenu de `theme/` est copié tel quel à la racine du site, sauf :

- ce que lit la construction : `layout.html`, `layouts/`, `share.svg`,
  `icons/`, `types/`, `theme.toml` et chaque `theme.<lang>.toml` ;
- ce qui appartient au dépôt du thème plutôt qu'au site : `.git`, et tout
  fichier ou dossier dont le nom commence par `.git` (`.gitignore`,
  `.gitmodules`), à n'importe quelle profondeur ; un `README.md`, et tout
  fichier dont le nom commence par `LICENSE`, à la racine du dossier.

Ainsi, `theme/style.css` est servi en `/style.css`,
`theme/fonts/mono.woff2` en `/fonts/mono.woff2`, et le gabarit, que la
construction a déjà transformé en pages, n'est pas servi du tout. Le
gabarit fait référence à ces fichiers par `{{ root }}`, le chemin relatif
vers la racine du site ([variables](docs/themes/layouts)).

`assets/` suit les mêmes règles. La page [le projet](docs/guide/project)
les présente pour les trois dossiers d'un site.

## assets/ l'emporte sur theme/

Pour chaque fichier de thème qu'elle lit ou sert, la construction cherche
d'abord dans `assets/`, puis dans `theme/`. Un site peut ainsi remplacer
un fichier d'un thème qu'il n'a pas écrit, sans toucher au thème :

| Le site ajoute | Il remplace |
|---|---|
| `assets/style.css` | `theme/style.css` |
| `assets/layout.html` | `theme/layout.html` |
| `assets/layouts/doc.html` | le `layouts/doc.html` du thème |
| `assets/share.svg` | l'aperçu de lien du thème |
| `assets/icons/github.svg` | le logo du thème pour ce réseau |
| `assets/code.js` | le bouton de copie du thème |

Trois exceptions : les types de contenu ne sont lus que dans
`theme/types/`, les polices qui dessinent `share.png` que dans
`theme/fonts/`, et la configuration que dans `theme/theme.toml` ; pour la
configuration, un site modifie plutôt son propre `site.toml`.

## theme.toml

La couche du thème dans la configuration, fusionnée par-dessus le
`defaults.toml` de tilder et sous le `site.toml` du site : table par
table, clé par clé, si bien qu'un site redéfinit une valeur et garde les
autres. Elle contient ce pour quoi le thème a besoin d'une valeur :

- `[share]` : les couleurs de l'aperçu de lien et de l'interface du
  navigateur (`theme_color`, `background_color`...), décrites dans la
  [référence de la configuration](docs/reference/configuration) ;
- les mots propres au thème, dans des tables à lui, que ses gabarits
  lisent par des variables (`{{ search.label }}`) ;
- `[check]` : ce que vérifie `build.py --check`
  ([vérifier un thème](docs/themes/checking)).

```toml
# theme/theme.toml
[search]
label = "Search the documentation"
none = "No page matches."

[share]
theme_color = "#2e6b34"
background_color = "#f7f8f3"
```

Un gabarit qui lit `{{ search.label }}` a besoin que la clé existe : une
variable qui nomme une clé qu'aucune couche ne définit arrête la
construction. Le `theme.toml` du thème est l'endroit où donner une valeur
à chaque clé qu'il utilise.

### theme.<lang>.toml

  Un fichier par langue que parle le thème : `theme.fr.toml` contient le
  français des mots du thème. Il est ignoré quand le site ne déclare pas
  cette langue : un thème peut donc fournir des langues qu'un site n'a pas
  ([langues](docs/guide/languages)). Il se place entre `theme.toml` et les
  fichiers du site, dans cet ordre, le dernier l'emportant :

```text
defaults.toml
  < theme/theme.toml < theme/theme.fr.toml
  < content/site.toml < content/site.fr.toml
```

## share.svg et les polices

`share.svg` est le modèle de l'aperçu de lien : la construction le remplit
puis le dessine en `share.png`, de 1200 pixels sur 630, l'image que les
réseaux sociaux affichent à côté d'un lien. Ses variables sont
`{{ logo }}` (le `assets/logo.svg` du site, sous forme d'URL `data:`),
`{{ manual_upper }}`, `{{ wordmark }}`, `{{ domain }}`, `{{ card_1 }}`,
`{{ card_2 }}` et toute valeur de `site.toml` (`{{ site.name }}`),
échappées pour le XML. La
[référence des flux et des images](docs/reference/feeds-and-images) les
décrit, ainsi que les outils qui dessinent l'image.

Le texte de `share.png` est dessiné avec les polices du thème : chaque
`fonts/*.woff2`, converti pour le moteur de rendu quand `woff2_decompress`
est installé (l'image Docker l'inclut). Sans lui, le moteur de rendu se
rabat sur les polices du système.

## icons/

`icons/<network>.svg` est le logo d'un lien de profil d'un membre, pour
les réseaux qu'une page de membre peut citer : `linkedin`, `github`,
`gitlab`, `mastodon`, `bluesky`, `website`. La construction l'insère dans
la page sous forme d'un `<svg class="icon">`, masqué aux lecteurs d'écran
(le lien garde pour eux le nom du réseau, en texte). Elle conserve le
`viewBox` du fichier et le `d` de ses éléments `<path>`, rien d'autre :
une icône est faite de tracés, elle doit avoir un `viewBox`, et c'est le
thème qui la colore (`.icon { fill: currentColor; }` la dessine dans la
couleur du texte). Sans le fichier, le lien affiche le nom du réseau.

## Voir aussi

- [gabarits et variables](docs/themes/layouts)
- [le projet](docs/guide/project)
- [les membres](docs/content-types/member)
