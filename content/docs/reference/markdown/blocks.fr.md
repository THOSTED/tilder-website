---
title: Blocs
description: Paragraphes et classes, état vide, listes, tâches, sommaire, filets, encadrés, alertes, blocs de code, tableaux et commentaires, chacun montré rendu.
order: 20
---

## Nom

blocks - paragraphes, listes, encadrés, code, tableaux et commentaires

Un bloc est une suite de lignes entre deux lignes vides : un paragraphe,
une liste, un encadré, un bloc de code, un tableau. Chaque construction
ci-dessous est donnée en source, puis rendue dans un cadre pointillé
marqué `Rendu`, exactement comme cette source s'affiche sur n'importe
quelle page du site.

[TOC]

## Paragraphe

Des lignes qui se suivent forment un paragraphe, jointes par des
espaces ; une ligne vide le termine. Des mots entre accolades à la fin
d'un paragraphe sont des classes, appliquées sur la page web seulement :
le miroir en texte imprime le paragraphe tel quel.

```text
La construction joint ces deux lignes
en un seul paragraphe.

Une ligne petite et atténuée. {small muted}

Une ligne pâle. {faint}

Une ligne en police à chasse fixe. {mono}

Une ligne dans la couleur d'avertissement. {warn}
```

### Rendu {example}

  La construction joint ces deux lignes
  en un seul paragraphe.

  Une ligne petite et atténuée. {small muted}

  Une ligne pâle. {faint}

  Une ligne en police à chasse fixe. {mono}

  Une ligne dans la couleur d'avertissement. {warn}

`small`, `muted`, `faint`, `mono` et `warn` sont les classes que tout
thème doit mettre en forme ([classes](docs/themes/classes)). Tout autre
mot entre les accolades devient aussi une classe, pour un thème qui la
met en forme. Un `{#id}` y est ignoré : un paragraphe n'a pas
d'identifiant.

## État vide

Un paragraphe entièrement entouré d'astérisques simples est un état
vide : la ligne atténuée, en chasse fixe, qui dit que quelque chose
n'existe pas encore. Une liste sans rien dedans affiche la même ligne.

```text
*Aucune conférence annoncée pour l'instant.*
```

### Rendu {example}

  *Aucune conférence annoncée pour l'instant.*

Les astérisques doivent ouvrir et fermer tout le paragraphe. Avec du
texte après l'astérisque fermant, `*Bientôt.* Revenez plus tard.` est un
paragraphe ordinaire qui commence en italique. Un paragraphe tout en gras
commence et finit lui aussi par des astérisques : il devient un état
vide, son texte en italique. Gardez le gras pour des mots dans une
phrase.

## Liste

Une ligne qui commence par `- ` ou `* ` est un élément à puce ; `1. ` ou
`1) ` commence un élément numéroté. Une liste numérotée part de son
premier numéro : `7.` puis `8.` compte à partir de 7. Mettez un élément
plus en retrait que celui du dessus pour imbriquer une liste dedans. Une
ligne en retrait qui n'est pas un élément prolonge l'élément du dessus.

```text
1. Copier le site de départ
2. Le construire, puis le laisser se reconstruire
   pendant que vous écrivez
   - `python3 builder/build.py`
   - `python3 builder/build.py --watch`
3. Écrire la première page
```

### Rendu {example}

  <!-- Le premier bloc de l'exemple : une liste ici serait la ligne meta de l'entrée. -->

  1. Copier le site de départ
  2. Le construire, puis le laisser se reconstruire
     pendant que vous écrivez
     - `python3 builder/build.py`
     - `python3 builder/build.py --watch`
  3. Écrire la première page

Dans le miroir en texte, chaque élément est en retrait de deux espaces,
sous la forme `- élément` ou `1. élément`, et ses lignes suivantes comme
ses listes imbriquées s'alignent sous son texte.

Une liste ne suit pas un paragraphe sans ligne vide : ses lignes
prolongeraient le paragraphe. Et juste après un titre `###`, une liste
est la [ligne meta](docs/reference/markdown/entries) de l'entrée, pas une
liste.

## Liste de tâches

`[ ]` ou `[x]` juste après la marque d'un élément en fait une tâche : une
case vide, ou cochée. Les lecteurs d'écran entendent `labels.task_todo`
ou `labels.task_done` pour la case (« à faire », « fait »).

```text
- [x] passer le blog en dossiers
- [ ] écrire le premier compte rendu
```

### Rendu {example}

  <!-- Le premier bloc de l'exemple : une liste ici serait la ligne meta de l'entrée. -->

  - [x] passer le blog en dossiers
  - [ ] écrire le premier compte rendu

Le miroir en texte imprime les cases en texte : `- [x] élément`,
`- [ ] élément`.

## Table des matières

`[TOC]` seul sur sa ligne liste les sections de la page, chacune liée à
sa section. Sur la page web, c'est un `<nav>` nommé par `labels.toc`,
replié par défaut dans un `<details>` qui s'ouvre sans aucun script. Dans
le miroir en texte, c'est une liste numérotée des noms de sections.
Chaque sortie ne liste que les sections qu'elle montre
([sections](docs/reference/markdown/sections)).

```text
[TOC]
```

### Rendu {example}

  [TOC]

`[toc]` fonctionne aussi, en majuscules comme en minuscules. Placez-la
là où le sommaire doit apparaître, en haut d'une longue page.
Cette page en a une sous son `## Nom` ; sur un écran large, le thème de
ce site déplace la première table des matières d'une page de
documentation dans la colonne de droite.

## Filet horizontal

`---`, `***` ou `___` seul sur sa ligne, entre deux lignes vides, trace
un filet : `<hr>` sur la page web, une ligne de tirets dans le miroir en
texte. Tout en haut d'un fichier, `---` ouvre plutôt l'en-tête.

```text
Au-dessus du filet.

---

Au-dessous du filet.
```

### Rendu {example}

  Au-dessus du filet.

  ---

  Au-dessous du filet.

## Encadré

Chaque ligne d'un encadré commence par `>`. Il est dessiné comme une
boîte sur la page web, et en retrait dans le miroir en texte. Une ligne
réduite à `>` sépare deux paragraphes. Un encadré contient des
paragraphes, avec leur balisage en ligne : une liste ou un bloc de code à
l'intérieur est lu comme du texte.

```text
> **Note :** les [archives ↗](https://archive.example.org/) gardent les anciens articles.
>
> Un second paragraphe.
```

### Rendu {example}

  > **Note :** les [archives ↗](https://archive.example.org/) gardent les anciens articles.
  >
  > Un second paragraphe.

Les pages de cette référence encadrent ainsi les exemples vivants du
[balisage en ligne](docs/reference/markdown/inline).

## Alerte

Un encadré dont la première ligne est `[!INFO]`, `[!WARNING]` ou
`[!ERROR]` est une alerte, dans la syntaxe de GitHub. Du texte peut
suivre le marqueur sur la même ligne. Les autres noms de GitHub sont
acceptés, en majuscules comme en minuscules.

```text
> [!INFO]
> La construction repasse à minuit.

> [!WARNING]
> Ne modifiez jamais `public/` à la main : la construction suivante le remplace.

> [!ERROR] Un `title:` manquant arrête la construction.
```

### Rendu {example}

  > [!INFO]
  > La construction repasse à minuit.

  > [!WARNING]
  > Ne modifiez jamais `public/` à la main : la construction suivante le remplace.

  > [!ERROR] Un `title:` manquant arrête la construction.

| Marqueur | Aussi accepté | Genre | Étiquette |
|---|---|---|---|
| `[!INFO]` | `[!NOTE]`, `[!TIP]` | info | `labels.info` |
| `[!WARNING]` | `[!IMPORTANT]`, `[!CAUTION]` | avertissement | `labels.warning` |
| `[!ERROR]` | `[!DANGER]` | erreur | `labels.error` |

Sur la page web, une alerte est une boîte avec un filet de couleur à
gauche et son étiquette, marquée `role="note"` pour les lecteurs
d'écran. Dans le miroir en texte, c'est une boîte dessinée en ASCII,
l'étiquette dans son filet du haut, colorée selon son genre dans le
miroir ANSI :

```text
+- ATTENTION ------------------------------------------------------+
| Ne modifiez jamais public/ a la main : la construction suivante  |
| le remplace.                                                     |
+------------------------------------------------------------------+
```

Les étiquettes viennent de `[labels]` dans `site.toml` : elles suivent la
langue de la page. Tout autre mot, `[!NOTICE]` par exemple, laisse un
encadré ordinaire qui commence par le marqueur tel qu'il est écrit.

## Bloc de code

Un bloc de code s'ouvre sur une clôture de trois accents graves et se
ferme sur une autre. Un nom de langage juste après la clôture ouvrante
active la coloration syntaxique, faite par la construction (sans script),
et affiche le langage dans le coin du bloc. Le bloc garde ses espaces
exactement, et une ligne longue défile de côté au lieu d'élargir la page.

````text
```python
def plier(texte, largeur=75):
    return textwrap.wrap(texte, largeur)
```
````

### Rendu {example}

  ```python
  def plier(texte, largeur=75):
      return textwrap.wrap(texte, largeur)
  ```

Pour montrer une clôture dans un bloc de code, comme le fait la source
ci-dessus, ouvrez le bloc extérieur avec plus d'accents graves : une
clôture de quatre ne se ferme que sur une ligne de quatre ou plus.

| Langage | Aussi accepté |
|---|---|
| `sh` | `bash`, `shell`, `zsh` |
| `console` | `terminal`, `shell-session` |
| `python` | `py` |
| `js` | `javascript`, `ts`, `typescript`, `node` |
| `c` | `h`, `cpp`, `c++` |
| `go` | `golang` |
| `rust` | `rs` |
| `sql` | `postgres`, `postgresql` |
| `json` | |
| `yaml` | `yml` |
| `ini` | `toml`, `cfg`, `systemd` |
| `conf` | `caddy`, `caddyfile`, `nginx` |
| `dockerfile` | `docker`, `containerfile` |
| `html` | `xml`, `svg` |
| `css` | |
| `make` | `makefile` |
| `diff` | `patch` |
| `text` | `plain`, `txt` |

Le nom peut s'écrire en majuscules ou en minuscules ; l'étiquette
l'affiche en minuscules, tel qu'il est écrit : `caddy`, pas `conf`. Trois
langages se lisent ligne par ligne plutôt que mot par mot :

- `console` : une ligne qui commence par une invite, `$ ` ou `# `,
  éventuellement précédée d'un utilisateur et d'un hôte, est une commande
  et se colore comme du shell ; toute autre ligne est une sortie,
  laissée brute.
- `diff` : les lignes ajoutées et retirées sont colorées différemment,
  les en-têtes de bloc atténués.
- `text` : aucune coloration, mais l'étiquette s'affiche. Chaque source
  Markdown de ce manuel est un bloc `text`.

````text
```console
$ python3 builder/build.py
built public/
```

```diff
-nav = "blog"
+nav = "blog/"
```
````

### Rendu {example}

  ```console
  $ python3 builder/build.py
  built public/
  ```

  ```diff
  -nav = "blog"
  +nav = "blog/"
  ```

Un bloc sans langage n'a ni étiquette ni coloration. Un langage que
tilder ne connaît pas affiche un avertissement à la construction et
laisse le bloc brut.

Si le thème fournit `code.js`, comme celui-ci, chaque bloc de code
reçoit un bouton qui copie son code en texte brut, libellé par
`labels.copy` et `labels.copied` ; le script n'est chargé que sur les
pages qui ont du code ([scripts](docs/themes/scripts)). Dans le miroir en
texte, le bloc est encadré de deux filets, le langage dans celui du
haut, et rien n'est ajouté à ses lignes, qui se copient proprement depuis
un terminal : elles sont seulement ramenées à l'ASCII, les tabulations
remplacées par quatre espaces. Une ligne plus longue que les 75 colonnes
du miroir est coupée et continuée sur la suivante, la coupure marquée par
`\`. Dans le miroir en couleur, `ansi/`, un bloc dans l'un des langages
ci-dessus (`text` et un langage inconnu exceptés) est aussi coloré,
chaque composant dans la couleur de son genre, selon les mêmes règles
que le HTML ; `txt/` reste brut dans tous les cas
([le miroir en texte](docs/reference/text-mirror)) :

```text
.-- python --------------------------------------------------------.
  def plier(texte, largeur=75):
      return textwrap.wrap(texte, largeur)
'------------------------------------------------------------------'
```

## Tableau

Des barres verticales séparent les cellules ; la deuxième ligne, de
tirets, sépare l'en-tête des rangées. Des deux-points dans cette ligne
règlent l'alignement de chaque colonne : `:---` à gauche, par défaut,
`:---:` centré, `---:` à droite. Le balisage en ligne fonctionne dans les
cellules, et `\|` y écrit une barre verticale. Chaque ligne du tableau
commence par `|` : une ligne sans elle fait du bloc un paragraphe.

```text
| Sortie | Format | Largeur |
|:-------|:------:|--------:|
| page   | HTML   | libre   |
| miroir | ASCII  | 75      |
| `a \| b` | texte | 5 |
```

### Rendu {example}

  | Sortie | Format | Largeur |
  |:-------|:------:|--------:|
  | page   | HTML   | libre   |
  | miroir | ASCII  | 75      |
  | `a \| b` | texte | 5 |

Les barres n'ont pas besoin d'être alignées, et chaque ligne de tirets en
compte au moins trois. Une rangée a autant de cellules que l'en-tête : une
cellule manquante est vide, une cellule en trop est ignorée. Sur la page
web, un tableau plus large que la colonne défile dans son propre cadre,
nommé par `labels.table` pour les lecteurs d'écran. Dans le miroir en
texte, il devient des colonnes alignées ; si elles ne tiennent pas en 75
colonnes, chaque rangée devient une fiche de lignes `En-tête: valeur`.

## Commentaire

Un bloc qui commence par `<!--` est recopié tel quel dans la page web,
où le navigateur ne l'affiche pas, et omis du miroir en texte.
Servez-vous-en pour des notes aux personnes qui modifient la page, comme
un fait encore à trouver :

```text
<!-- À COMPLÉTER : l'adresse du lieu. -->

*Lieu à annoncer.*
```

### Rendu {example}

  <!-- À COMPLÉTER : l'adresse du lieu. -->

  *Lieu à annoncer.*

Le commentaire dit ce qui manque, l'état vide le dit au lecteur. Tout le
bloc, jusqu'à la ligne vide suivante, est recopié tel quel : laissez une
ligne vide après le commentaire.

## Voir aussi

- [les sections](docs/reference/markdown/sections)
- [les entrées](docs/reference/markdown/entries)
- [le miroir en texte](docs/reference/text-mirror)
- [les classes](docs/themes/classes)
