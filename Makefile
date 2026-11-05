DESTDIR = "./public"
APIDIR  = "${DESTDIR}/api/v1"

# Authenticate against the GitHub API if a token is available (avoids rate limits).
GH_AUTH = $(if ${GITHUB_TOKEN},-H "Authorization: Bearer ${GITHUB_TOKEN}")

.PHONY: all
all: build

.PHONY: build
build: ntt-update standards-update
	@mkdir -p "${DESTDIR}"
	@cp -rv --target="${DESTDIR}" assets content/*
	python3 scripts/update-standards.py --from-json "${APIDIR}/standards/index.json" --inject "${DESTDIR}/index.html"

# ntt-update updates all ntt related documents such as documentation or
# update-API.
.PHONY: ntt-update
ntt-update: ntt-pull-releases

# ntt-pull-releases updates the JSON files for ntt. These files are required by
# vscode-ttcn3 to find the latest ntt version without GitHub Rate Limiter.
.PHONY: ntt-pull-releases
ntt-pull-releases:
	@mkdir -p "${APIDIR}/ntt/releases/latest"
	@# -f: fail on HTTP errors, -L: follow redirects (GitHub answers 301 for
	@# moved repositories). Download to a temp file first so an error
	@# response never overwrites valid data.
	@curl -fsSL ${GH_AUTH} 'https://api.github.com/repos/nokia-steward/ntt/releases?per_page=100' > "${APIDIR}/ntt/releases/index.json.tmp"
	python3 -c 'import json,sys; assert isinstance(json.load(open(sys.argv[1])), list)' "${APIDIR}/ntt/releases/index.json.tmp"
	mv "${APIDIR}/ntt/releases/index.json.tmp" "${APIDIR}/ntt/releases/index.json"
	@curl -fsSL ${GH_AUTH} 'https://api.github.com/repos/nokia-steward/ntt/releases/latest' > "${APIDIR}/ntt/releases/latest/index.json.tmp"
	python3 -c 'import json,sys; assert "tag_name" in json.load(open(sys.argv[1]))' "${APIDIR}/ntt/releases/latest/index.json.tmp"
	mv "${APIDIR}/ntt/releases/latest/index.json.tmp" "${APIDIR}/ntt/releases/latest/index.json"

# standards-update retrieves the active TTCN-3 standard PDFs and metadata from
# the ETSI standards search.
.PHONY: standards-update
standards-update:
	python3 scripts/update-standards.py --output "${APIDIR}/standards/index.json"

.PHONY: clean
clean:
	@rm -rvf -- "${DESTDIR}"
