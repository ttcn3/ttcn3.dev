DESTDIR = "./public"
APIDIR  = "${DESTDIR}/api/v1"

.PHONY: all
all: build

.PHONY: build
build: ntt-update standards-update
	@mkdir -p "${DESTDIR}"
	@cp -rv --target="${DESTDIR}" assets content/*

# ntt-update updates all ntt related documents such as documentation or
# update-API.
.PHONY: ntt-update
ntt-update: ntt-pull-releases

# ntt-pull-releases updates the JSON files for ntt. These files are required by
# vscode-ttcn3 to find the latest ntt version without GitHub Rate Limiter.
.PHONY: ntt-pull-releases
ntt-pull-releases:
	@mkdir -p "${APIDIR}/ntt/releases/latest"
	curl 'https://api.github.com/repos/nokia/ntt/releases?per_page=100' > "${APIDIR}/ntt/releases/index.json"
	curl 'https://api.github.com/repos/nokia/ntt/releases/latest' > "${APIDIR}/ntt/releases/latest/index.json"

# standards-update retrieves the active TTCN-3 standard PDFs and metadata from
# the ETSI standards search.
.PHONY: standards-update
standards-update:
	python3 scripts/update-standards.py --output "${APIDIR}/standards/index.json"

.PHONY: clean
clean:
	@rm -rvf -- "${DESTDIR}"
