REMOVE = rm -rvf
UV ?= uv

.PHONY: all build test publish testpublish publish-dry-run clean

all: build

build:
	$(UV) build --no-sources

test:
	$(UV) run --extra dev pytest

clean:
	$(REMOVE) build
	$(REMOVE) logs
	$(REMOVE) dist
	$(REMOVE) arxiv_dl.egg-info
	$(REMOVE) ./**/__pycache__
	$(REMOVE) ./*/**/__pycache__
	$(REMOVE) tmp/*
	$(REMOVE) .pytest_cache
	$(REMOVE) .DS_Store

publish-dry-run: build
	$(UV) publish --dry-run --trusted-publishing never

publish:
	$(UV) publish

testpublish:
	$(UV) publish --index testpypi
