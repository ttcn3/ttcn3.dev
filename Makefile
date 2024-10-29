DESTDIR=./public

.PHONY: all
all: build

.PHONY: build
build:
	@mkdir -p "${DESTDIR}/syntax"
	@cp -rvt "${DESTDIR}" assets content/*
	@cp -rvt "${DESTDIR}/syntax/" content/index.html

.PHONY: clean
clean:
	@rm -rvf -- "${DESTDIR}"
