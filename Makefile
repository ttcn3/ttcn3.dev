DESTDIR = "./public"
APIDIR  = "${DESTDIR}/api/v1"

.PHONY: all
all: build

.PHONY: build
build: ntt-update
	@mkdir -p "${DESTDIR}"
	@cp -rv --target="${DESTDIR}" assets content/*

.PHONY: ntt-update
ntt-update: ntt-pull-releases

.PHONY: ntt-pull-releases
ntt-pull-releases:
	@mkdir -p "${APIDIR}/ntt/releases/"
	curl 'https://api.github.com/repos/nokia/ntt/releases' > "${APIDIR}/ntt/releases/index.json"
	curl 'https://api.github.com/repos/nokia/ntt/releases/latest' > "${APIDIR}/ntt/releases/latest.json"

.PHONY: clean
clean:
	@rm -rvf -- "${DESTDIR}"
