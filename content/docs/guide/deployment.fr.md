---
title: Déploiement
description: Mettre un site tilder en ligne avec Docker, compose et Caddy : URL propres, miroir en texte pour curl, hôte en texte brut, en-têtes, autres serveurs.
order: 50
---

## Nom

deployment - servir le site, aux navigateurs comme aux terminaux

`public/` est un site statique : n'importe quel serveur web peut le servir.
tilder fournit un fichier compose et une configuration Caddy qui le
servent comme il est pensé : des adresses sans `.html`, le miroir en texte
pour `curl` à la même adresse que la page, un hôte qui ne sert que du
texte, des en-têtes stricts. Cette page explique ce contrat, puis ce que
les autres serveurs peuvent en garder.

[TOC]

## Docker et compose

Le dépôt de tilder contient les deux fichiers dans `examples/` :
`compose.yaml` et `Caddyfile`. Copiez-les à côté de `content/`, `theme/`
et `assets/`, puis :

```sh
docker compose up -d
```

La pile compte deux services. `build` lance l'image de tilder : il
construit le site dans un volume, puis surveille les sources et
reconstruit à chaque modification et à minuit. `web`, c'est Caddy, qui
sert ce volume ; il démarre dès que la première construction a écrit
`index.html`.

```yaml
services:
  build:
    image: ghcr.io/thosted/tilder:1
    volumes:
      - ./content:/site/content:ro
      - ./theme:/site/theme:ro
      - ./assets:/site/assets:ro
      - site:/out
    healthcheck:
      test: ["CMD", "test", "-f", "/out/index.html"]
  web:
    image: caddy:2-alpine
    depends_on:
      build:
        condition: service_healthy
    ports:
      - "8080:80"
      - "8081:81"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - site:/srv:ro
volumes:
  site:
```

Cet extrait laisse de côté les délais du contrôle de santé et
l'environnement. Le tag d'image `1` suit la dernière version 1.x ; fixez
une version complète, `1.2.0`, pour choisir le moment où le site change de
générateur.

Les hôtes viennent de l'environnement de `web`. En local, les valeurs par
défaut servent le site sur `site.localhost:8080` et son texte sur
`man.site.localhost:8080` ; les ports 8080 et 8081 répondent aussi à
n'importe quel hôte, si bien que `localhost:8080` sert le site et
`localhost:8081` son texte, tout comme l'adresse de la machine sur le
réseau. En production :

| Variable | Valeur en production | Ce que c'est |
|---|---|---|
| `SITE_HOST` | `example.org` | le site, le même hôte que `site.url` |
| `WWW_HOST` | `www.example.org` | redirigé vers le site, jamais servi |
| `MAN_HOST` | `man.example.org` | l'hôte en texte brut |
| `SITE_ORIGIN` | `https://example.org` | la destination de la redirection du `www` |
| `AUTO_HTTPS` | `on` | Caddy obtient et renouvelle les certificats |

Avec `AUTO_HTTPS` activé, publiez les ports 80 et 443 de Caddy plutôt que
8080 et 8081, et faites pointer les trois noms vers la machine.

## URL propres

Les pages sont des fichiers en `.html` sur le disque, et des adresses
sans : `/about` sert `about.html`, `/blog/` sert `blog/index.html`. Chaque
page a une seule adresse ; les autres y redirigent, de façon permanente :

- `/about.html` mène à `/about` ;
- `/index` et `/index.html` mènent à `/`, et de même pour la page de
  chaque dossier listée dans le filtre `@index`, `/blog/index` et
  `/fr/index` dans l'exemple : ajoutez-y vos propres dossiers ;
- `/blog` mène à `/blog/` quand `blog/index.html` existe.

Les règles, tirées du bloc `handle` de l'exemple pour les navigateurs (ses
en-têtes sont laissés de côté ici) :

```caddyfile
@index path /index /index.html /blog/index /blog/index.html /fr/index /fr/index.html
redir @index {http.request.uri.path.dir} permanent
@noslash {
  file {path}/index.html
  not path */
}
redir @noslash {path}/ permanent
@html path_regexp html ^/(.*)\.html$
redir @html /{re.html.1} permanent
try_files {path} {path}.html {path}/index.html
file_server
```

Les liens qu'écrit tilder ont déjà cette forme : un lecteur qui les suit
ne rencontre jamais de redirection.

## Les terminaux reçoivent le texte

Une requête de `curl`, `wget` ou `httpie`, reconnue à son `User-Agent`,
pour une page (une adresse sans point) reçoit le miroir en texte, en
couleurs, depuis `ansi/`, en `text/plain`, avec un code 200 : pas de
redirection à suivre, pas besoin de `-L`. La seule redirection retire une
barre oblique finale, de `/blog/` vers `/blog`, l'adresse du texte du
dossier. Ajoutez `?plain` pour l'ASCII nu de `txt/`, à enregistrer ou à
passer à un autre programme : un bloc jumeau fait de même depuis `txt/`,
non reproduit ici.

```caddyfile
@terminal {
  header_regexp User-Agent (?i)^(curl|wget|httpie)/
  path_regexp ^/[^.]*$
  not path /LICENSE
  not query plain= plain=1 plain=true
}
handle @terminal {
  root * /srv/ansi
  header Content-Type "text/plain; charset=utf-8"
  header Cache-Control "public, max-age=300"
  @slash path_regexp slash ^(/.+)/$
  redir @slash {re.slash.1} permanent
  rewrite / /index.txt
  try_files {path}.txt {path} {path}/index.txt
  file_server
}
```

Une adresse avec un point, `style.css` ou `blog/feed.xml`, est servie
telle quelle : `curl -O` télécharge les fichiers comme d'habitude. La même
adresse répond du HTML à un navigateur et du texte à un terminal, alors
chaque réponse du site porte `Vary: User-Agent` : sans cet en-tête, un
cache partagé pourrait donner l'un à la place de l'autre.

```console
$ curl example.org/about
$ curl "example.org/about?plain" > about.txt
```

## L'hôte en texte brut

`MAN_HOST` ne sert que `txt/` : l'ASCII nu de chaque page, aux mêmes
chemins, quel que soit le client. Il ne devine rien, ce qui en fait
l'interface des scripts. Ses pages portent `X-Robots-Tag: noindex`, et
son `robots.txt`, écrit depuis `[robots_man]`, demande aux moteurs de
recherche de rester dehors : c'est le site qu'ils indexent. Le
`robots.txt` du site, écrit depuis `[robots]`, les tient à l'écart de
`/txt/` et `/ansi/`.

## En-têtes

**Politique de sécurité du contenu.** Les pages peuvent charger styles,
polices, images, manifeste et scripts depuis le site lui-même, et rien
d'ailleurs ; un script en ligne ne s'exécute jamais. `connect-src 'self'`
permet au script d'un thème de récupérer un fichier du même site, comme
l'index de recherche de ce manuel, et aucun autre hôte. Le Caddyfile écrit
la politique sur une seule ligne :

```text
default-src 'none'; style-src 'self'; font-src 'self';
img-src 'self'; manifest-src 'self'; script-src 'self';
connect-src 'self'; form-action 'none'; base-uri 'none';
frame-ancestors 'none'
```

Un fichier SVG reçoit sa propre politique, qui le laisse se styler avec un
élément `<style>`, sans jamais exécuter de script.

**Cache.** Les polices se gardent un an (`immutable` : une police ne
change jamais sous le même nom) ; styles, scripts et images une journée ;
les pages et le texte en couleurs servi aux terminaux cinq minutes, pour
qu'une reconstruction se voie vite.

**Compression.** Les réponses sont compressées en zstd ou en gzip.

**Le reste.** `X-Content-Type-Options: nosniff`,
`X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, une
`Permissions-Policy` qui coupe la géolocalisation, le micro et la caméra ;
pas d'en-tête `Server`. Les calendriers, les flux et le manifeste
reçoivent leur type de contenu.

**Journaux.** Les journaux d'accès sont jetés, `log { output discard }` :
un site construit avec tilder ne piste pas ses lecteurs. Gardez-le ainsi.

## Pages d'erreur

Une page introuvable reçoit le `404.html` du site, ou celui de sa langue
(`/fr/404.html`) sous le préfixe d'une langue. Chaque langue à préfixe
prend une ligne dans `handle_errors` ; un préfixe que le site ne déclare
pas reçoit la page 404 par défaut. Un terminal reçoit un court texte à la
place : modifiez le `SITE(1)` et le `curl example.org` de l'exemple pour
nommer votre site.

```caddyfile
handle_errors {
  @terminalerror header_regexp User-Agent (?i)^(curl|wget|httpie)/
  respond @terminalerror "SITE(1)

Page not found.

See: curl example.org
" 404
  @fr path /fr/*
  rewrite @fr /fr/404.html
  rewrite * /404.html
  file_server
}
```

## Autres serveurs

nginx, Apache ou un hébergeur statique servent `public/` tel quel. Ce
qu'ils en gardent dépend de ce qu'on peut leur dire :

- **URL propres.** Les liens qu'écrit tilder n'ont pas de `.html`, pas
  plus que les adresses canoniques de ses pages, de son plan du site et de
  ses flux. Sans règle qui associe `/about` à `about.html`, ils ne mènent
  nulle part. La plupart des serveurs et beaucoup d'hébergeurs statiques
  savent le faire ; commencez par là.
- **Le texte pour curl.** Il faut une règle sur le `User-Agent`. Sans
  elle, `curl` reçoit le HTML ; le texte reste disponible sous
  `/txt/about.txt` et `/ansi/about.txt`. Si vous ajoutez la règle,
  ajoutez `Vary: User-Agent` avec elle.
- **En-têtes.** La politique, les durées de cache, la compression et les
  journaux jetés relèvent du serveur. Un hébergeur qui ne pose aucun
  en-tête sert le site sans eux : il fonctionne, avec moins de
  protection.
- **Pages d'erreur.** Une seule page `404.html` est courante ; une page
  404 par langue demande une règle par préfixe.

Chaque lien entre pages est relatif, et chaque page est complète sans ses
scripts. Les adresses absolues viennent de `site.url` : le lien canonique,
`og:url`, les plans du site et les flux. Donnez-lui l'adresse à laquelle
le site est servi.

## Voir aussi

- [premiers pas](docs/guide/getting-started)
- [le miroir en texte](docs/reference/text-mirror)
- [le référencement](docs/reference/seo)
