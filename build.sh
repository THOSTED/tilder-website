#!/bin/sh
# Build the site with tilder, after the theme's checks. Fails on any
# build warning.
#
#   ./build.sh                          content/ -> public/
#   ./build.sh --out DIR                somewhere else
#   ./build.sh --root DIR --out DIR     another project laid out the same way
#                                       (the theme's tests build tests/site)
#   ./build.sh --watch                  rebuild on every change (checks once)
#
# tilder comes from its Docker image, ghcr.io/thosted/tilder, at the tag in
# TILDER_VERSION. A local checkout instead (before the image exists, or to
# work on tilder itself):
#
#   TILDER_BUILD=/path/to/tilder/build.py ./build.sh
#
# DOCKER=podman picks another container engine.
set -eu

here=$(cd "$(dirname "$0")" && pwd)
root=$here
out=$here/public
watch=""
while [ $# -gt 0 ]; do
	case $1 in
		--root) root=$(cd "$2" && pwd); shift 2 ;;
		--out) mkdir -p "$2"; out=$(cd "$2" && pwd); shift 2 ;;
		--watch) watch=--watch; shift ;;
		*) echo "usage: build.sh [--root DIR] [--out DIR] [--watch]" >&2; exit 2 ;;
	esac
done

# The theme contract: with TILDER_BUILD, the checkout's own docs/theme.md;
# otherwise the vendored copy of the pinned version's docs/theme.md (the
# image has it too, at /tilder/docs/theme.md, but the checks and tests
# must not need Docker).
if [ -n "${TILDER_BUILD:-}" ]; then
	contract=$(dirname "$TILDER_BUILD")/docs/theme.md
else
	contract=$here/tools/tilder-theme.md
fi
python3 "$here/tools/check-theme.py" "$root/theme/style.css" "$contract"
python3 "$here/tools/check-contrast.py" "$root/theme/style.css"

if [ -n "${TILDER_BUILD:-}" ]; then
	set -- python3 -B "$TILDER_BUILD" --root "$root" --out "$out"
else
	version=$(tr -d ' \n' < "$here/TILDER_VERSION")
	set -- "${DOCKER:-docker}" run --rm -u "$(id -u):$(id -g)" \
		-v "$root:/site:ro" -v "$out:/out" \
		"ghcr.io/thosted/tilder:${version#v}" \
		python3 -B /tilder/build.py --root /site --out /out
fi

if [ -n "$watch" ]; then
	exec "$@" --watch
fi

log=$(mktemp)
trap 'rm -f "$log"' EXIT
status=0
"$@" 2>"$log" || status=$?
cat "$log" >&2
if [ "$status" -ne 0 ]; then
	exit "$status"
fi
if grep -Eq '^(warning|seo):' "$log"; then
	echo "error: build.sh: the build printed warnings (above). A build prints none" >&2
	exit 1
fi
