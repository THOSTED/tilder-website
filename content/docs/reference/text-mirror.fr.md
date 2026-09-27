---
title: Le miroir en texte
description: Chaque page en texte : 75 colonnes, ramenée à l'ASCII, brute dans txt/ et en couleur dans ansi/, avec le code encadré et l'hôte en texte brut.
order: 30
---

## Nom

text-mirror - chaque page en texte, pour les terminaux

Chaque page que construit tilder sort deux fois : en HTML pour les
navigateurs, et en texte pour les terminaux, à partir de la même source,
si bien que les deux ne peuvent pas diverger. Le texte fait 75 colonnes
de large et se ramène à l'ASCII. Il est lui aussi écrit deux fois : brut
dans `txt/`, et coloré par des séquences d'échappement ANSI dans `ansi/`.
Un terminal qui demande une page au site reçoit la version en couleur.

[TOC]

## Où il se trouve

Le texte de chaque page est rangé sous `txt/` et `ansi/`, à l'adresse de
la page, avec `.txt`. La page d'un dossier porte le nom du dossier.

| Page | Brut | En couleur |
|---|---|---|
| `index.html` | `txt/index.txt` | `ansi/index.txt` |
| `about.html` | `txt/about.txt` | `ansi/about.txt` |
| `blog/index.html` | `txt/blog.txt` | `ansi/blog.txt` |
| `blog/2026-01-01-hello.html` | `txt/blog/2026-01-01-hello.txt` | `ansi/blog/2026-01-01-hello.txt` |
| `fr/about.html` | `txt/fr/about.txt` | `ansi/fr/about.txt` |

Servi par le Caddyfile d'exemple, `curl example.org/about` renvoie
`ansi/about.txt`, avec un 200 et sans redirection ; `?plain` renvoie
`txt/about.txt` à la place, pour l'enregistrer ou le passer à un autre
programme ; et l'hôte en texte brut sert `txt/` à tous les clients, aux
mêmes chemins ([déploiement](docs/guide/deployment)). Les fichiers se
lisent aussi depuis le disque :

```sh
less -R public/ansi/about.txt
curl example.org/about
curl "example.org/about?plain" > about.txt
```

`robots.txt` tient les moteurs de recherche à l'écart de `/txt/` et de
`/ansi/`, et `txt/robots.txt` de tout l'hôte en texte brut : le texte
double les pages ([SEO](docs/reference/seo)).

## La page en texte

Le texte suit les sections de la page, à la manière d'une page de
manuel (en raccourci ici : les vrais filets font 75 colonnes de large) :

```text
MYSITE(1)                 My Site Manual                 MYSITE(1)

LANGUAGES: en fr

NAME
     about - who we are

     A paragraph, wrapped at 75 columns, indented five spaces.

SEE ALSO
     ...

previous: Getting started                         next: Deployment

MYSITE                    2026-01-01                     MYSITE(1)
```

- Le filet d'en-tête : le `man:` de la page des deux côtés,
  `site.manual` au milieu.
- Sur un site en plusieurs langues, une ligne `LANGUAGES:` les énumère.
- Chaque section `##` : son titre en capitales à la première colonne, son
  corps en retrait de cinq espaces.
- Avant le pied de page, la ligne des voisins d'une collection
  séquentielle, avec `labels.prev` et `labels.next`
  ([navigation](docs/content-types/navigation)).
- Le filet de pied de page : `footer.left`, `site.updated`,
  `footer.right` ([configuration](docs/reference/configuration)).

Ce qui n'y figure pas : tout ce qui précède le premier `##`, une section
marquée `{html}`, et un bloc de commentaire. Une section marquée `{text}`
n'apparaît qu'ici, pas sur la page ([sections](docs/reference/markdown/sections)).
Les espaces en fin de ligne disparaissent, et jamais plus d'une ligne
vide n'en suit une autre.

## 75 colonnes

Chaque ligne tient en 75 colonnes : un terminal de 80 colonnes, le format
par défaut depuis le VT100, avec de la place pour une barre de
défilement, la marge de `less` ou d'un diff, ou le `>` d'un courriel
cité. Les paragraphes sont coupés sur les espaces, chaque ligne remplie autant
qu'elle le peut. Un mot
n'est jamais coupé, une URL ou une commande non plus : un mot plus long
que la ligne est donc la seule chose qui puisse dépasser le bord.

## ASCII

`txt/` est en ASCII : la source garde ses accents et sa typographie, le
miroir les ramène à l'ASCII. D'abord, ces caractères sont remplacés :

| Caractère | Devient |
|---|---|
| tiret cadratin, tiret demi-cadratin | `-` |
| apostrophes typographiques | `'` |
| guillemets anglais typographiques, guillemets français | `"` |
| point médian | `-` |
| points de suspension | `...` |
| flèche vers la droite | `->` |
| flèche nord-est, U+2197 | rien |
| les ligatures de o et e, de a et e, en capitale ou non | `oe`, `OE`, `ae`, `AE` |
| espace insécable, espace fine insécable | une espace |
| signe de multiplication | `x` |

Ensuite, chaque lettre perd ses accents et autres signes : un e accent
aigu devient e, un c cédille devient c. Dans la prose, les suites
d'espaces n'en font plus qu'une ; dans le code, l'espacement est gardé à
l'identique. Un caractère qui n'est ni dans le tableau ni une lettre
accentuée, un emoji ou une autre flèche, n'est pas converti : il passe
tel quel dans `txt/`, gardez donc ces caractères hors du texte destiné au
miroir.

## Les blocs en texte

| Bloc | Dans le miroir en texte |
|---|---|
| paragraphe | coupé en lignes ; ses classes, `{small muted}`, ne touchent que la page |
| liste | `- item`, `1. item`, `- [x] item`, `- [ ] item` ; les lignes suivantes et les listes imbriquées s'alignent sous le texte de l'élément |
| citation | en retrait de deux espaces de plus |
| encadré | une boîte, son libellé dans le filet du haut : `+- WARNING ---+`, tiré de `labels.info`, `labels.warning` ou `labels.error` |
| bloc de code | encadré de deux filets, voir plus bas |
| tableau | des colonnes alignées, comme `column -t` ; si elles ne tiennent pas en 75 colonnes, un enregistrement par ligne, une ligne `En-tête: valeur` par cellule |
| filet horizontal | une ligne de tirets |
| image | `[ image ] texte alternatif`, tiré de `labels.image`, puis la légende, puis le chemin du fichier depuis la racine du site |
| `[TOC]` | `labels.toc` en capitales, puis les titres des sections, numérotés |
| entrée | son titre, la première étiquette alignée à droite sur la même ligne, `[ tag ]` ; la ligne de métadonnées en dessous, une date en toutes lettres seulement ; son corps en retrait de quatre espaces de plus |

En ligne : un lien garde son libellé, et un lien externe y ajoute son
adresse entre parenthèses, `archive (https://example.org/)` ; une adresse
interne est omise, puisqu'un terminal la visite avec `curl` plutôt que de
la recopier. Le gras et l'italique deviennent du texte simple ; le texte
barré garde ses marques `~~`, puisque les retirer changerait le sens. Le
dialecte complet, bloc par bloc, est dans
[la référence Markdown](docs/reference/markdown).

## Le code encadré

Un bloc de code est encadré de deux filets qui disent quel bout est
lequel : celui du haut s'ouvre sur `.`, porte le langage et se ferme sur
`.` ; celui du bas s'ouvre et se ferme sur `'`. Le code est en retrait à
l'intérieur, sans rien d'ajouté sur ses propres lignes : il se copie
proprement depuis un terminal. En raccourci :

```text
.-- sh ------------------------------.
  curl example.org/about
'------------------------------------'
```

Le code garde son espacement à l'identique ; une tabulation avance
jusqu'au taquet suivant, toutes les quatre colonnes. Une ligne qui dépasse la 75e colonne est coupée et
continue sur la ligne suivante, en retrait de deux espaces, la coupure
marquée d'un `\` : un shell la lit comme une continuation.

## Les couleurs

`ansi/` est le même texte avec des séquences d'échappement ANSI : huit
couleurs, ou un accent en 256 couleurs choisi par le site (`text.accent`),
jamais de fond, pour se lire aussi bien sur un terminal clair que sombre.
La couleur suit le balisage, sans jamais être devinée d'après les mots :
la construction marque le code en ligne, les puces des listes, les
lignes des blocs de code et, dans un bloc de code coloré, chaque
composant, là où elle les rend, et colore exactement ceux-là, d'une
ligne à l'autre.

| Quoi | Couleur |
|---|---|
| les filets d'en-tête et de pied de page | atténués |
| le titre d'une section, quand il ne contient que des lettres, des chiffres, des espaces et `-()'` | gras |
| le nom de la page, sur la première ligne de la première section | gras |
| le `code` en ligne | la couleur d'accent, exactement jusqu'à ses accents graves |
| les puces des listes | la couleur d'accent |
| les URL | la couleur d'accent, soulignées |
| les `[ tags ]` | gras, dans la couleur d'accent |
| les filets d'un bloc de code | atténués |
| une ligne de commande dans un bloc de code sans langage, ou en `text` | la couleur d'accent |
| la boîte et le libellé d'un encadré d'information | la couleur d'accent, le libellé en gras |
| un encadré d'avertissement | jaune |
| un encadré d'erreur | rouge |

La couleur d'accent est `text.accent` : `"cyan"` par défaut, ou l'un des
huit noms de couleur, ou un index de 256 couleurs de 16 à 255, tel que
`208` pour l'orange, réglé dans `site.toml` (un `site.<lang>.toml` peut
régler le sien) ([configuration](docs/reference/configuration)). La
ponctuation qui referme une phrase autour d'une URL ou d'une ligne de
commande - un `.,;:!?` final, une apostrophe restée seule, une
parenthèse jamais ouverte - reste sans couleur : dans une phrase comme
(voir https://example.org/a_(b)), seule l'adresse est colorée, pas le
`).` qui la termine.

Une ligne de commande est une ligne de bloc de code qui commence par l'un
des mots de `text.commands`, seul ou après une invite, `$` ou `#` suivi
d'une espace ; par défaut, seulement `curl`. Un site ajoute les siens :

```toml
[text]
commands = ["curl", "docker", "python3"]
```

Les encadrés sont reconnus au libellé de leur filet du haut : les
couleurs suivent donc `labels.info`, `labels.warning` et `labels.error`
dans chaque langue. Retirez les séquences d'échappement d'un fichier de
`ansi/`, et il reste son jumeau de `txt/`, octet pour octet. `txt/` ne
contient aucune séquence d'échappement : il survit à `curl > fichier`.

## Les blocs de code colorés

Un bloc de code dans un langage que `highlight.py` connaît est aussi
coloré dans `ansi/`, chaque composant dans la couleur de son genre,
selon les mêmes règles que la page HTML : `ansi/` ne dit jamais le
contraire de ce que montre un navigateur. Seule la couleur change,
jamais un caractère ajouté : les espaces autour d'un composant restent
sans couleur, et une fois ses séquences d'échappement retirées, le bloc
est celui de `txt/`. Une ligne coupée à la 75e colonne garde ses
couleurs sur la ligne suivante.

| Composant | Couleur |
|---|---|
| mot-clé ; en `sh` et `console`, le mot de commande ; en `markdown`, `[!INFO]` et pareils, `[TOC]` | gras, dans la couleur d'accent |
| identifiant natif ou type ; en `sh` et `console`, une option (`-s`, `--out`) ; en `markdown`, une puce de liste, une case à cocher, l'emphase | la couleur d'accent |
| chaîne, une ligne `+` de `diff` ; en `markdown`, le `code` en ligne, le titre d'un lien | vert |
| commentaire, une invite `console` (`$ `, `# `) ; en `markdown`, une ligne de clôture, une règle, les barres d'un tableau, le `>` d'une citation, les `---` du front matter | atténué |
| nombre, variable ; en `markdown`, la cible d'un lien, les `{marqueurs}` qui terminent une ligne | magenta |
| étiquette, clé, section, l'en-tête d'un extrait `diff` (`@@`) ; en `markdown`, un titre, une clé du front matter | gras |
| une ligne `-` de `diff` | rouge |

Le mot de commande est le premier mot d'une commande : au début d'une
ligne (après une invite `$ ` en `console`), après `|`, `||`, `&&`, `;`,
`&`, `(`, `$(`, après un préfixe comme `sudo` ou `env`, et après
l'affectation d'une variable.

Les langages colorés sont `sh`, `python`, `js`, `c`, `go`, `rust`,
`sql`, `json`, `jsonc`, `yaml`, `kyaml`, `ini`, `conf`, `dockerfile`,
`html`, `css` et `make`, chacun selon ses propres règles, plus
`console`, `diff` et `markdown`, colorés ligne par ligne ; la liste
complète des noms et de leurs alias est dans [les blocs de
code](docs/reference/markdown/blocks). Un bloc sans langage, en
`text`, ou dans un langage que tilder ne connaît pas n'est pas coloré :
seules ses lignes de commande (`text.commands`) prennent la couleur
d'accent, et `txt/` reste brut dans tous les cas.

## Écarter une page

`text: no` dans l'en-tête d'une page n'écrit aucun texte pour elle, ni
dans `txt/` ni dans `ansi/`. La page 404 du site de départ le fait : un
terminal reçoit à la place un court message du serveur
([écrire des pages](docs/guide/writing), [déploiement](docs/guide/deployment)).

```markdown
---
title: 404
description: Page not found.
text: no
robots: noindex
---
```

## Voir aussi

- [déploiement](docs/guide/deployment)
- [la référence Markdown](docs/reference/markdown)
- [la configuration](docs/reference/configuration)
