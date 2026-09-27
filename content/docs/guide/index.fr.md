---
title: Guide
description: Le parcours de tilder, page après page : l'installer, organiser un projet, écrire des pages, ajouter une langue, puis mettre le site en ligne.
order: 10
---

## Nom

guide - de la première construction au site en ligne

Le guide mène un site de rien jusqu'à la production en cinq pages, chacune
s'appuyant sur la précédente. Il explique ce que vous faites et pourquoi ;
la référence donne chaque valeur et chaque option en entier.

## Le parcours

[Premiers pas](docs/guide/getting-started) installe tilder, avec Docker ou
avec Python, copie le site de départ et le construit. La page montre le
mode surveillance, qui reconstruit à mesure que vous écrivez, et ce que la
construction laisse dans `public/`.

[Le projet](docs/guide/project) passe en revue les trois dossiers d'un
site, `content/`, `theme/` et `assets/`, les trois couches de la
configuration, et les fichiers qui finissent sur le serveur comme ceux qui
n'y vont jamais.

[Écrire des pages](docs/guide/writing) fait d'un fichier Markdown une
page : son adresse, chaque clé de l'en-tête, des sections à la manière
d'une page de manuel, les liens et les images.

[Langues](docs/guide/languages) ajoute une deuxième langue : la déclarer,
traduire la configuration et les pages, ce que devient une page pas encore
traduite, et ce que la construction écrit pour chaque langue.

[Déploiement](docs/guide/deployment) met le site en ligne : Docker et
compose, la configuration de Caddy qui sert le miroir en texte à `curl`,
et ce que les autres serveurs savent faire ou non.

## Voir aussi

- [la référence Markdown](docs/reference/markdown)
- [la référence de la configuration](docs/reference/configuration)
- [la ligne de commande](docs/reference/cli)
