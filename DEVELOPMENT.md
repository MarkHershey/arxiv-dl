# Development

This document covers contributor and maintainer workflows for `arxiv-dl`.

## Set Up Development Environment

Install `uv` if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create or sync the project environment, including development tools:

```bash
uv sync --extra dev
```

## Run Tests

```bash
uv run --extra dev pytest
```

For a focused test run:

```bash
uv run --extra dev pytest tests/test_process_nips_target.py -q
```

## Build

Build the source distribution and wheel:

```bash
uv build --no-sources
```

The Makefile wraps the same command:

```bash
make
```

## Publish

For normal releases, prefer GitHub Actions Trusted Publishing. Make the release commit first, then tag that commit:

```bash
git tag -a v1.2.3 -m v1.2.3
git push origin master
git push origin v1.2.3
```

The tag push triggers `.github/workflows/publish.yml`, builds the package, and publishes through PyPI Trusted Publishing.

For a local manual upload, set a project-scoped PyPI token and publish the already-built files:

```bash
export UV_PUBLISH_TOKEN="pypi-..."
uv publish
```

To test against TestPyPI:

```bash
export UV_PUBLISH_TOKEN="pypi-..."
uv publish --index testpypi
```

## Clean Build Artifacts

```bash
make clean
```
