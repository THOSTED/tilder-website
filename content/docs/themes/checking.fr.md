---
title: Vérifier un thème
description: build.py --check vérifie un thème au regard du tilder qui l'exécute : une règle pour chaque classe écrite, et le contraste des paires de couleurs.
order: 50
---

## Nom

checking - build.py --check, les classes et le contraste d'un thème

`build.py --check` vérifie le thème du site au regard du tilder qui
l'exécute, et ne construit rien. Deux vérifications : chaque classe
qu'écrit la construction a une règle dans `style.css`, et chaque paire de
couleurs que déclare le thème atteint son contraste minimal, en mode
clair comme en mode sombre. La commande affiche une ligne par problème et
sort avec le code 1 s'il y en a un : elle trouve donc sa place avant une
construction, dans un Makefile ou en intégration continue.

[TOC]

## La commande

Depuis le projet, avec Python :

```sh
python3 ../tilder/build.py --check
python3 ../tilder/build.py --check --markdown   # et le tableau
```

Avec Docker, le projet monté en lecture seule, puisque rien n'est écrit :

```sh
docker run --rm -v "$PWD:/site:ro" ghcr.io/thosted/tilder:1.3.0 \
  python3 -B /tilder/build.py --root /site --check
```

Elle affiche une ligne `error:` par problème, sous la même forme que les
erreurs de la construction, le fichier, ce qui ne va pas, puis ce qu'il
faut faire, et une ligne de bilan pour chaque vérification menée : avec
des paires de contraste déclarées mais sans `style.css`, la vérification
du contraste donne une erreur au lieu d'un bilan. Le code de sortie vaut
0 quand chaque vérification réussit ou est ignorée, 1 quand un problème a
été trouvé. La construction normale ne lance jamais ces vérifications :
lancez-les quand le thème change, ou avant chaque construction.

Par exemple, tilder 1.2.0 qui vérifie le thème de ce site tel qu'il était
écrit pour tilder 1.1, avant qu'il ne mette en forme les trois classes de
section de la 1.2 et que son `theme.toml` ne déclare des paires de
contraste :

```console
$ python3 ../tilder/build.py --check
error: theme/style.css: no rule for .collection-section. Style it, or name it in [check] unstyled (theme/theme.toml)
error: theme/style.css: no rule for .collection-section--open. Style it, or name it in [check] unstyled (theme/theme.toml)
error: theme/style.css: no rule for .collection-section-label. Style it, or name it in [check] unstyled (theme/theme.toml)
classes: 3 of 72 not styled
contrast: skipped, no [check] contrast in theme/theme.toml
$ echo $?
1
```

## Les classes

tilder tient la liste de chaque classe qu'il écrit, `CLASSES` dans son
`src/contract.py` : les classes de la page [classes](docs/themes/classes).
La vérification cherche chacune d'elles dans `style.css`, le
`assets/style.css` du site s'il en a un, sinon celui du thème : une classe
compte quand `.name` apparaît sans caractère de nom à sa suite, hors
commentaires et hors contenu des chaînes. Ainsi `.toc` ne compte pas pour
`.toc-label`, et une classe citée seulement dans un commentaire manque.

Un thème qui laisse volontairement une classe sans style la nomme dans
`[check] unstyled`, et la vérification l'ignore : un thème sans logos de
profils, par exemple, n'a rien à mettre en forme dans `.icon`. Sans
`style.css`, la vérification est ignorée, avec une note.

```text
classes: 72 of the contract, all styled
classes: 3 of 72 not styled
classes: skipped, no theme/style.css
```

Comme la liste vient du tilder qui lance la vérification, une nouvelle
version de tilder qui écrit une nouvelle classe la fait signaler : le
thème apprend ce qu'il doit mettre en forme avant qu'une page ne l'affiche
sans style.

## Le contraste

Le thème déclare les paires de couleurs qui portent du texte, le
premier plan puis le fond, sous forme de propriétés personnalisées de son
`style.css`, dans `[check] contrast`. La vérification calcule le rapport
de contraste WCAG 2 de chaque paire et signale, avec son rapport, chacune
de celles qui passent sous `contrast_min` : 4,5 par défaut, le minimum
WCAG AA pour le texte.

Elle lit les couleurs là où un navigateur les lirait :

- **clair** : les propriétés personnalisées de la règle `:root` de
  `style.css` ;
- **sombre** : celles de la règle `:root` à l'intérieur de `@media
  (prefers-color-scheme: dark)`, par-dessus celles du mode clair, si bien
  que le mode sombre ne définit que ce qui change. Sans une telle règle,
  seul le mode clair est vérifié.

Seule compte une règle dont le sélecteur est exactement `:root` : pas
`:root, .dark`, pas une règle placée dans `@supports` ou `@layer`. Une
couleur utilisée par une paire doit s'écrire en hexadécimal, `#rgb` ou
`#rrggbb` ; une propriété absente, ou qui n'est pas une couleur
hexadécimale (`rgb()`, un `var()`, un nom), est une erreur qui la nomme.
Sans paires, la vérification est ignorée ; avec des paires et sans
`style.css`, c'est une erreur.

```text
error: theme/style.css: dark: --muted on --bg is 3.87:1, below 4.5:1. Darken or lighten one of them
error: theme/style.css: light: --accent is rgb(0 112 126), not a hex colour. Write it #rrggbb, or leave its pairs out of [check] contrast
```

Sa ligne de bilan indique combien de paires elle a mesurées, et dans
quels modes :

```text
contrast: 20 pairs (light, dark), all at or above 4.5:1
contrast: 1 of 18 pairs below 4.5:1, 1 unreadable
contrast: skipped, no [check] contrast in theme/theme.toml
```

## La table [check]

Les trois clés se placent dans le `theme.toml` du thème, sous `[check]`.
Elles sont lues dans `defaults.toml`, puis dans le `theme.toml` du thème,
puis dans le `site.toml` du site, le dernier l'emportant : un site peut
les modifier dans son propre `site.toml` sans toucher au thème.

| Clé | Par défaut | |
|---|---|---|
| `unstyled` | `[]` | les classes du contrat que le thème laisse volontairement sans style (le point est facultatif) |
| `contrast` | `[]` | des paires de propriétés personnalisées de `style.css`, le premier plan puis le fond ; vide : rien n'est vérifié |
| `contrast_min` | `4.5` | le plus petit rapport de contraste admis pour chaque paire |

```toml
# theme/theme.toml
[check]
unstyled = ["icon"]              # pas de logos de profils
contrast = [
	["--fg", "--bg"], ["--fg", "--bg-inset"],
	["--fg-muted", "--bg"], ["--fg-muted", "--bg-inset"],
	["--accent", "--bg"],
]
contrast_min = 4.5
```

Une table mal formée est une erreur à part entière : `unstyled` doit être
une liste de noms, `contrast` une liste de paires de noms commençant par
`--`, `contrast_min` un nombre.

## Un tableau pour le README

Avec `--markdown`, la vérification affiche aussi le tableau des
contrastes en Markdown, sur la sortie standard, et ses lignes de bilan
sur la sortie d'erreur : redirigez la sortie vers un fichier et collez le
tableau dans le README du thème, pour que ses utilisateurs voient les
rapports sans rien lancer.

```sh
python3 ../tilder/build.py --check --markdown > contrast.md
```

Le tableau donne d'abord le mode clair, puis le sombre, chaque paire
dans l'ordre de `[check] contrast`. Ses premières lignes pour le thème du
site de départ :

```markdown
| scheme | foreground | background | ratio | minimum |
|---|---|---|---:|---:|
| light | `--fg` | `--bg` | 17.40 | 4.5 |
| light | `--fg` | `--bg-inset` | 15.68 | 4.5 |
| light | `--fg-muted` | `--bg` | 7.46 | 4.5 |
| light | `--fg-muted` | `--bg-inset` | 6.72 | 4.5 |
```

Le thème du site de départ passe les deux vérifications et déclare ses
paires dans `starter/theme/theme.toml` : un modèle pour votre propre
thème.

## Voir aussi

- [classes](docs/themes/classes)
- [la ligne de commande](docs/reference/cli)
- [les fichiers d'un thème](docs/themes/files)
