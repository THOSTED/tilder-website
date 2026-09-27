---
title: Balisage en ligne
description: Gras, italique, texte barré et souligné, code et liens au fil d'une phrase : les six constructions en ligne, ce qui reste littéral, et le miroir en texte.
order: 40
---

## Nom

inline - gras, italique, barré, souligné, code et liens

Dans un paragraphe, un élément de liste, une cellule de tableau, une
légende ou le titre `###` d'une entrée, tilder lit six constructions et
rien d'autre. Chacune est montrée ci-dessous en source, puis rendue dans
un cadre, comme elle s'affiche dans n'importe quelle phrase du site.

[TOC]

## Gras et italique

Deux astérisques de chaque côté mettent le texte en gras. Un astérisque
ou un tiret bas de chaque côté le mettent en italique.

```markdown
Un mot en **gras**, un en *italique*, et _un autre_ encore.
```

> Un mot en **gras**, un en *italique*, et _un autre_ encore.

Les deux s'écrivent de façon à laisser le texte ordinaire tranquille :

- `*italique*` ne doit pas toucher d'espace à l'intérieur, si bien que
  `2 * 3 * 4` reste tel quel ;
- `_italique_` ne fonctionne qu'autour de mots entiers, si bien que
  `snake_case` reste tel quel.

```markdown
2 * 3 * 4 font 24, et snake_case n'est pas en italique.
```

> 2 * 3 * 4 font 24, et snake_case n'est pas en italique.

Sur la page web, le gras est `<b>` et l'italique `<em>`. Le miroir en
texte imprime les mots seuls, sans les marques.

Un paragraphe entièrement entouré d'astérisques simples n'est pas en
italique : c'est un [état vide](docs/reference/markdown/blocks#etat-vide).

## Barré et souligné

Deux tildes de chaque côté barrent le texte ; deux signes plus de chaque
côté le soulignent, d'un trait pointillé, car un soulignement plein se
lit comme un lien sur le web.

```markdown
La rencontre a lieu ~~vendredi~~ samedi, ++à midi++.
```

> La rencontre a lieu ~~vendredi~~ samedi, ++à midi++.

`++souligné++` suit la même règle que l'italique : pas juste après une
lettre, et sans toucher d'espace à l'intérieur, si bien que `C++` et
`1 ++ 2` restent tels quels. Sur la page web, ce sont `<del>` et
`<u class="u">`. Le miroir en texte imprime le texte barré avec ses
tildes, `~~vendredi~~` : les ôter changerait le sens. Le texte souligné
est imprimé tel quel.

## Code

Un mot ou une expression entre accents graves est du code : en police à
chasse fixe, et jamais lu pour un autre balisage.

```markdown
Lancez `python3 builder/build.py`, et gardez **`--watch` actif** pendant que vous écrivez.
```

> Lancez `python3 builder/build.py`, et gardez **`--watch` actif** pendant que vous écrivez.

La fin de cet exemple montre aussi la règle suivante : pas
d'imbrication. Le gras garde les accents graves tels quels, pas du code.
Le code ne peut pas non plus contenir d'accent grave. Dans le miroir en
texte, le code est imprimé tel quel, et coloré dans le miroir ANSI.

## Liens

`[libellé](cible)` est un lien. La cible s'écrit depuis la racine du
site, sans barre oblique au début et sans `.html` ; la construction la
rend relative à la page.

```markdown
Lisez [le guide](docs/guide), ou l'[exemple ↗](https://example.org/).
```

> Lisez [le guide](docs/guide), ou l'[exemple ↗](https://example.org/).

La page [liens et images](docs/reference/markdown/links-and-images)
donne chaque genre de cible : les ancres, les liens d'une langue à
l'autre, les fichiers et les autres sites.

## Ce qui reste littéral

Les six constructions ne s'imbriquent pas : la première trouvée
l'emporte, et garde son contenu en texte brut. Il n'y a pas de caractère
d'échappement : une barre oblique inverse est imprimée, et n'arrête pas
le balisage qui la suit. Tout le reste, HTML compris, est imprimé tel
qu'il est écrit.

```markdown
**[un lien](docs/)** est en gras, et <b>ceci</b> ne l'est pas.
Un \*antislash\* n'échappe rien.
```

> **[un lien](docs/)** est en gras, et <b>ceci</b> ne l'est pas.
> Un \*antislash\* n'échappe rien.

Les deux lignes font un seul paragraphe : du gras qui contient la source
d'un lien, du HTML affiché en texte, puis une barre oblique inverse
imprimée devant de l'italique. Reformulez plutôt que d'échapper. Dans une
cellule de tableau, `\|` est une barre verticale
([tableaux](docs/reference/markdown/blocks#tableau)).

## Dans le miroir en texte

Le miroir en texte imprime les mots de chaque construction et ôte leurs
marques, sauf les tildes du texte barré. Un lien interne ne garde que son
libellé, puisqu'un lecteur dans un terminal le suit avec `curl` et non en
le recopiant ; un lien vers un autre site imprime son adresse entre
parenthèses après le libellé. Les accents et les caractères
typographiques sont ramenés à l'ASCII : les lettres accentuées perdent
leur accent, les guillemets et les tirets typographiques deviennent
simples, et la flèche nord-est des liens externes disparaît. Les lignes
sont coupées à 75 colonnes
([le miroir en texte](docs/reference/text-mirror)).

## Voir aussi

- [liens et images](docs/reference/markdown/links-and-images)
- [les blocs](docs/reference/markdown/blocks)
- [le miroir en texte](docs/reference/text-mirror)
