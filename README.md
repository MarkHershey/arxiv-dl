# arXiv-dl

Command-line [arXiv](https://arxiv.org/) Paper Downloader.
[[PyPI]](https://pypi.org/project/arxiv-dl/)
[[Source]](https://github.com/MarkHershey/arxiv-dl)

[![](https://img.shields.io/pypi/v/arxiv-dl)](https://pypi.org/project/arxiv-dl/)
[![](https://img.shields.io/pypi/pyversions/arxiv-dl)](https://pypi.org/project/arxiv-dl/)
[![](https://img.shields.io/pypi/wheel/arxiv-dl)](https://pypi.org/project/arxiv-dl/)
[![](https://img.shields.io/pypi/dm/Arxiv-dl)](https://pypi.org/project/arxiv-dl/)
[![](https://img.shields.io/badge/license-MIT-blue)](https://github.com/MarkHershey/arxiv-dl/blob/master/LICENSE)
[![](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

_Disclaimer: This is a highly-opinionated CLI tool for downloading papers. It is designed to be easy to use. Obviously, not an official project._

## Features

-   Download papers from `arXiv.org` via simple command line interface.
-   Support downloading speedup by using [aria2c](https://aria2.github.io/).
-   Automatically maintain a local list of downloaded papers.
-   Retrieve the paper's metadata and citation:
    -   Paper Title
    -   Authors
    -   Abstract
    -   Comments (Conference acceptance info)
    -   Source Code Links
    -   Citation (`BibTeX`)
-   Configure the desired download destination via environment variables.
-   All downloaded papers will be named by its arXiv ID and paper title without whitespace.

### Why?

-   Save time and effort to download, rename, and organize papers.
-   Speedup downloading process by using parallel connections.
-   Local paper list would be handy for quick local lookup, locate, and cite papers.

## Install

This is a command-line tool, use `pip` to install the package globally.

-   Pre-requisite: `Python 3.x`

```bash
python3 -m pip install --upgrade arxiv-dl
```

(Optional) Install [aria2c](https://aria2.github.io/) for download speedup.

-   MacOS: `brew install aria2`
-   Linux: `sudo snap install aria2c`

## Usage

After installation, the command `getpaper` should be available in your terminal.

```bash
$ getpaper [-v] [-d DOWNLOAD_DIR] [-n N_THREADS] urls [urls ...]
```

Options:

-   `-v`, `--verbose` (optional): Print paper metadata.
-   `-d`, `--download-dir` (optional): Specify one-time download directory. This option will override the default download directory or the one specified in the environment variable `ARXIV_DOWNLOAD_FOLDER`.
-   `-n`, `--n-threads` (optional): Specify the number of parallel connections to be used by `aria2`.

Example:

![](imgs/demo.png)

```bash
# Use ArXiv Paper ID
$ getpaper 1512.03385 2103.15538

# Use ArXiv Abstract Page URL
$ getpaper https://arxiv.org/abs/2103.15538

# Use ArXiv PDF Page URL
$ getpaper https://arxiv.org/pdf/1512.03385.pdf
```

## Configurations

Set Custom Download Destination Folder _(Optional)_

-   Let's say you want your papers get downloaded into `~/Documents/Papers`.
-   Set the environment variable `ARXIV_DOWNLOAD_FOLDER` to your desired location.
    ```bash
    export ARXIV_DOWNLOAD_FOLDER=~/Documents/Papers
    ```
-   If the environment variable is not set, paper will be downloaded into the default Download Destination `~/Downloads/ArXiv_Papers`.

Set Custom Alias _(Optional)_

-   You can always set your own preferred alias for the `getpaper` command.
-   Include the alias in your `~/.bashrc` or other shell profile.
    ```bash
    alias dp="getpaper"
    alias dpv="getpaper -v -d '~/Documents/Papers'"
    ```

## Development

### Set up development environment

```bash
python3 -m venv venv && \
source venv/bin/activate && \
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Build the package

```bash
make
```

### Clean cache & build artifacts

```bash
make clean
```

## TODOs

-   [x] Add support for ara2c.
-   [ ] Add support for papers on CVF Open Access.
-   [ ] Add support for papers on OpenReview.

## License

[MIT License](LICENSE) - Copyright (c) 2021-2022 Mark Huang
