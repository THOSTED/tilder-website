---
man: TILDER-SHOWCASE(7)
title: Vitrine
description: Des sites construits avec tilder, et comment y faire figurer le vôtre : une issue ou une pull request avec son adresse et une ligne.
tagline: des sites construits avec tilder
nav: showcase/
---

## Nom

vitrine - des sites construits avec tilder

Des sites que tilder construit, chacun avec son adresse, une ligne qui le
présente et, s'il en a une, une capture d'écran. Vous avez construit le
vôtre avec tilder ? Il peut figurer ici.

## Sites {showcase}

## Figurer dans la vitrine

Ouvrez une issue ou une pull request sur
[THOSTED/tilder ↗](https://github.com/THOSTED/tilder) avec :

- l'adresse du site ;
- une ligne qui dit ce qu'il est ;
- si vous le souhaitez, une capture d'écran.

Chaque site tient dans un fichier, `showcase/<slug>/index.md`, avec sa
capture d'écran à côté. Le slug est un nom court du site, en minuscules.
Une pull request ajoute ce dossier ; une issue donne ce qu'il contient :

```markdown
---
title: Example site
url: https://example.org/
description: Les notes d'une petite équipe, en français et en anglais, avec un miroir texte pour les terminaux.
image: shot.png
order: 10
---

## Nom

example - les notes d'une petite équipe
```

| Front matter | |
|---|---|
| `title` | le nom du site |
| `url` | **obligatoire**, l'adresse du site, `https://example.org` |
| `description` | une phrase, le texte de la carte |
| `image` | facultative, une capture d'écran à côté du fichier (`showcase/<slug>/shot.png`) |
| `order` | facultatif, un nombre entier : la place dans la liste (1000 par défaut, puis le slug) |

## Voir aussi

- [pourquoi tilder](why)
- [la documentation](docs/)
