DESTDIR=./public

.PHONY: all
all: build

.PHONY: build
build:
	@mkdir -p "${DESTDIR}"
	@cp -rvt "${DESTDIR}" assets content/*

.PHONY: clean
clean:
	@rm -rvf -- "${DESTDIR}"
