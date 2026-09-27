# tilder-website

The site of [tilder](https://github.com/THOSTED/tilder), served at
<https://tilder.thosted.fr>: its manual, in English and in French, a
showcase of sites built with it, and its release notes. The site is built
with tilder itself, from the version pinned in `TILDER_VERSION`.

## The repository

```text
content/                  the site: pages, docs/, showcase/, blog/, site.toml, site.fr.toml
theme/                    the documentation theme (its own README.md, MIT)
assets/logo.svg           the logo, drawn to the icons and the link preview
Makefile                  build, check, watch, serve, test, clean
compose.yaml              the build and Caddy, locally and in production
Caddyfile                 from tilder's examples/Caddyfile, hosts from the environment
.env.example              the hosts and ports, local defaults
TILDER_VERSION            the pinned tilder, 1.2.0
tools/check-coverage.py   the docs name every fact of the pinned tilder
tests/                    the theme's tests, its fixture site (tests/site/), the content's tests
.gitignore                public/, .env, __pycache__/
docs/superpowers/         specs and plans
```

`public/` is the build's output and is never committed.

## Make

GNU make, run from the repository (or `make -C DIR`), and Docker (or
another engine) with the pinned image, or a tilder checkout. Paths may
hold spaces.

| Target | Does |
|---|---|
| `make`, `make build` | `check`, then `site` |
| `make check` | tilder's `--check` on the theme (every class styled, the contrast of the colour pairs `theme/theme.toml` declares), then `tools/check-coverage.py` on the docs |
| `make site` | builds `content/` into `public/`; fails on any `warning:` or `seo:` line |
| `make watch` | checks once, then rebuilds on every change |
| `make serve` | `docker compose up -d`: the site at http://localhost:8080, its text mirror at http://localhost:8081 |
| `make stop` | `docker compose down`: stops the stack |
| `make test` | the tests (`python3 -m unittest`) |
| `make clean` | removes `public/` |

tilder runs from `ghcr.io/thosted/tilder:<TILDER_VERSION>`, as the
calling user, the project mounted read-only. Two variables change that:

```sh
make TILDER_BUILD=/path/to/tilder/build.py   # a checkout instead of the image
make DOCKER=podman                           # another container engine
```

`ROOT` and `OUT` build another project laid out the same way
(`make site ROOT=DIR OUT=DIR`); the tests use them.

## Serving

`compose.yaml` holds one stack: `build` renders the site into a volume
with the pinned image, then exits; `web` (Caddy) serves it, with clean
URLs, the text mirror for `curl`, and the plain-text host. `make serve`
starts it, `make stop` stops it. compose reads `TILDER_VERSION` from the
environment: the Makefile exports it, and a compose command run by hand
needs it too:

```sh
export TILDER_VERSION=$(cat TILDER_VERSION)
docker compose run build     # rebuild into the running stack
```

The hosts and ports come from `.env`: copy `.env.example`, whose defaults
serve locally without TLS. In production, set the real hosts, the
standard ports and `AUTO_HTTPS=on`: Caddy fetches the certificates.

## Keeping the docs true

The site pins one tilder version, and its docs describe that version.
To bump the pin:

1. Write the new version in `TILDER_VERSION`.
2. Read what changed: tilder's git log between the two tags, and the
   diffs of its `docs/` and `defaults.toml`. Update the pages, in both
   languages.
3. `make check`: tilder's `--check` holds the theme to the new contract,
   and `tools/check-coverage.py` fails on any key, setting, front-matter
   key, class, placeholder or command-line option of the new tilder that
   no page names, in English or in French.
4. `make test` and `make`: the site builds with no warning.

## Licence

The theme (`theme/`) is under the MIT licence, `theme/LICENSE`; its fonts
under the SIL Open Font License, `theme/fonts/OFL-*.txt`.
