---
title: Thèmes
description: Ce qu'est un thème tilder, comment en utiliser un, et les pages qui décrivent ses fichiers, ses gabarits, ses classes, ses scripts et ses vérifications.
order: 30
---

## Nom

themes - l'apparence d'un site tilder

tilder écrit du HTML aux noms de classes stables, sans aucun style qui lui
soit propre ; c'est le dossier `theme/` du site qui décide de son
apparence. Un thème, c'est un gabarit à variables, une feuille de
style, et tout ce qu'il choisit d'y ajouter : polices, scripts, aperçu de
lien, types de contenu. tilder ne fournit aucun thème en dehors de celui du
site de départ, un thème minimal à copier puis à faire grandir.

## Ce qu'est un thème

Un thème est un dossier, `theme/`, à côté de `content/` et `assets/`. Un
seul fichier y est obligatoire, `layout.html` : le HTML qui entoure chaque
page, dans lequel la construction remplace `{{ title }}`, `{{ body }}` et
les autres variables. Tout le reste est facultatif :

- `style.css`, qui met en forme les classes écrites par la construction ;
- d'autres gabarits, pour un type de page ou demandés par une page ;
- des polices, des logos de profils, le modèle de l'aperçu de lien ;
- des scripts, qui améliorent une page sans être nécessaires à sa lecture ;
- des types de contenu, en Python, qui ajoutent des sortes de pages au site ;
- `theme.toml`, les réglages et les mots du thème, sous ceux du site.

La construction remplit le gabarit, copie ce qui doit être servi, et ne
sert jamais ce qu'elle se contente de lire. Le thème a la charge de
l'apparence et d'une part de l'accessibilité (contraste, focus, texte
masqué à l'écran) ; la construction, celle du balisage : titres, textes
alternatifs, libellés, attributs `aria-*`.

## Utiliser un thème

Un site utilise le thème de son dossier `theme/`, et aucun autre : aucun
réglage ne nomme un thème. Pour en utiliser un, copiez-le à cet endroit.

### celui du site de départ

  Le site de départ est livré avec son thème, `starter/theme/` dans le
  dépôt de tilder : un gabarit, une feuille de style et un aperçu de lien,
  sur les polices du système, sans aucun script. Il met en forme chaque
  classe écrite par la construction et respecte le contraste WCAG AA en
  clair comme en sombre. Partir du site de départ
  ([premiers pas](docs/guide/getting-started)) vous donne ce thème, à
  modifier comme bon vous semble.

### celui de ce site

  Le site que vous lisez a son propre thème, et montre ce que fait un thème
  plus fourni : deux gabarits de plus (`layouts/home.html` pour la page
  d'accueil, `layouts/doc.html` pour la documentation), deux types de
  contenu dans `types/` (`doc` et `showcase`), trois scripts (le bouton de
  copie, la barre latérale sur petit écran, la recherche), des polices
  hébergées sur le site, et ses mots en anglais et en français dans
  `theme.toml` et `theme.fr.toml`.

### un autre

  Copiez son dossier en tant que `theme/`, puis lisez son README : un thème
  qui ajoute des types de contenu indique les collections à déclarer dans
  `site.toml`, et un thème peut demander une version de tilder ou un
  réglage du serveur (une recherche lit son index, ce qui exige
  `connect-src 'self'` dans la Content-Security-Policy de la page).

```sh
rm -rf theme
cp -r ../other-theme theme
```

Un thème peut vivre dans son propre dépôt git, cloné en tant que `theme/` :
son dossier `.git`, ses fichiers git, ainsi qu'un `README.md` ou un
`LICENSE` à sa racine ne sont jamais servis.

## Modifier un thème que vous n'avez pas écrit

Deux façons de modifier un thème tout en reprenant sa prochaine version
telle quelle :

- **Ses mots et ses réglages** : définissez-les dans `content/site.toml`
  (ou `site.<lang>.toml`), qui a le dernier mot sur le `theme.toml` du
  thème ([configuration](docs/guide/project)).
- **Un fichier** : placez un fichier du même nom dans `assets/`. Il
  l'emporte sur celui du thème : `assets/style.css` remplace
  `theme/style.css`, `assets/layouts/doc.html` remplace le gabarit du
  thème qui porte ce nom.

## Confiance

Les `types/` d'un thème sont des modules Python, exécutés par la
construction avec les droits de la personne qui la lance. Un thème fait
partie du site, au même titre que tilder : lisez-le avant de l'utiliser,
comme tout code que vous exécutez. Un thème sans `types/` n'exécute rien
à la construction ; ses scripts s'exécutent dans le navigateur du lecteur,
selon les règles des [scripts](docs/themes/scripts).

## Les pages de cette section

[Fichiers](docs/themes/files) : chaque fichier qu'un thème peut fournir,
ce qu'en fait la construction, et ce qui est servi.

[Gabarits](docs/themes/layouts) : `layout.html` et `layouts/`, le choix du
gabarit d'une page, chaque variable et ce que le gabarit doit
conserver.

[Classes](docs/themes/classes) : chaque classe écrite par la construction,
l'élément qui la porte, et l'accessibilité dont le thème est responsable.

[Scripts](docs/themes/scripts) : `code.js`, `members.js`, le script d'un
type, où chacun est chargé et les règles qu'ils suivent.

[Vérifier un thème](docs/themes/checking) : `build.py --check`, qui
vérifie les classes et le contraste des couleurs d'un thème au regard du
tilder qui l'exécute.

## Voir aussi

- [le projet](docs/guide/project)
- [types personnalisés](docs/content-types/custom-types)
- [la référence de la configuration](docs/reference/configuration)
