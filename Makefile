# The site's one entry point (GNU make). tilder runs from its Docker image
# at the tag in TILDER_VERSION, or from a checkout:
#
#   make                      check, then build content/ into public/
#   make check                tilder --check on the theme, and the docs' coverage
#   make site                 build only, failing on any warning
#   make watch                check once, then rebuild on every change
#   make serve                the compose stack: http://localhost:8080
#   make test                 the theme's tests
#   make clean                remove public/
#
#   make TILDER_BUILD=/path/to/tilder/build.py    a checkout instead of the image
#   make DOCKER=podman                            another container engine
#   make site ROOT=DIR OUT=DIR                    another project laid out the
#                                                 same way (DIR/content/, DIR/theme/)

TILDER_VERSION := $(patsubst v%,%,$(shell tr -d ' \n' < "$(CURDIR)/TILDER_VERSION"))
export TILDER_VERSION
DOCKER ?= docker
ROOT ?= $(CURDIR)
override ROOT := $(abspath $(ROOT))
OUT ?= $(ROOT)/public
override OUT := $(abspath $(OUT))
IMAGE = ghcr.io/thosted/tilder:$(TILDER_VERSION)

ifdef TILDER_BUILD
RUN = python3 -B "$(TILDER_BUILD)" --root "$(ROOT)"
OUTARG = --out "$(OUT)"
TREE = cp -R "$(dir $(abspath $(TILDER_BUILD)))." "$$tree"
else
RUN = $(DOCKER) run --rm -u "$$(id -u):$$(id -g)" -v "$(ROOT):/site:ro" -v "$(OUT):/out" \
	$(IMAGE) python3 -B /tilder/build.py --root /site
OUTARG = --out /out
TREE = $(DOCKER) run --rm $(IMAGE) tar -C /tilder -cf - . | tar -xf - -C "$$tree"
endif

.PHONY: all build check site watch serve test clean
all: build
build: check site

# The theme against the contract of this tilder (build.py --check, with
# theme/theme.toml's [check]), then content/docs/ against its facts
# (tools/check-coverage.py, on a copy of the tilder tree that runs).
check:
	@mkdir -p "$(OUT)"
	$(RUN) --check
	@tree=$$(mktemp -d) && trap 'rm -rf "$$tree"' EXIT && $(TREE) && \
		python3 tools/check-coverage.py --tilder "$$tree" --docs "$(ROOT)/content/docs"

# A warning (warning:, seo:) fails the build: the site prints none.
site:
	@mkdir -p "$(OUT)"
	@log=$$(mktemp) && trap 'rm -f "$$log"' EXIT; \
	status=0; $(RUN) $(OUTARG) 2>"$$log" || status=$$?; \
	cat "$$log" >&2; \
	[ "$$status" -eq 0 ] || exit "$$status"; \
	if grep -Eq '^(warning|seo):' "$$log"; then \
		echo "error: make: the build printed warnings (above). A build prints none" >&2; exit 1; fi

watch: check
	@mkdir -p "$(OUT)"
	$(RUN) $(OUTARG) --watch

serve:
	$(DOCKER) compose up -d
	@echo "the site: http://localhost:8080   its text mirror: http://localhost:8081"
	@echo "stop: TILDER_VERSION=$(TILDER_VERSION) $(DOCKER) compose down"

test:
	python3 -m unittest

clean:
	rm -rf "$(OUT)"
