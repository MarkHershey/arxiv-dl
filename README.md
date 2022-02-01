# arXiv-dl

Command-line [arXiv](https://arxiv.org/) Paper Downloader.
[[PyPI]](https://pypi.org/project/arxiv-dl/)
[[Source]](https://github.com/MarkHershey/arxiv-dl)

[![](https://img.shields.io/pypi/v/arxiv-dl)](https://pypi.org/project/arxiv-dl/)
[![](https://img.shields.io/pypi/dm/arxiv-dl)](https://pypi.org/project/arxiv-dl/)
[![](https://img.shields.io/badge/license-MIT-blue)](https://github.com/MarkHershey/arxiv-dl/blob/master/LICENSE)
[![](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

## Features

-   Download papers from `arXiv.org` via command line interface.
-   Support downloading speedup by using [aria2c](https://aria2.github.io/).
-   Name the downloaded Paper by its arXiv ID and title without whitespace.
-   Retrieve the Paper's metadata and save them in a corresponding MarkDown document:
    -   Paper Title
    -   Authors
    -   Abstract
    -   Comments (Conference acceptance info)
    -   Source Code Links
    -   Citation (`BibTeX`)
-   Configure the desired download destination via environment variables.

## Install

This is a command-line tool, you just need to use `pip` to install the package, then, you will be able to use the command `getpaper` in your terminal.

-   Pre-requisite: `Python 3`

```bash
pip install arxiv-dl
```

## Usage

```bash
$ getpaper [-v] [-d DOWNLOAD_DIR] [-n N_THREADS] urls [urls ...]
```

Example:

```bash
$ getpaper 1512.03385

# OR
$ getpaper https://arxiv.org/abs/1512.03385

# OR
$ getpaper https://arxiv.org/pdf/1512.03385.pdf
```

## Configuration (Optional)

Set Custom Download Destination Folder _(Optional)_

-   Let's say you want your papers get downloaded into `~/Documents/Papers`.
-   Make sure the folder `~/Documents/Papers` exists.
-   Set the environment variable `ARXIV_DOWNLOAD_FOLDER` to your desired location.
    ```bash
    export ARXIV_DOWNLOAD_FOLDER=~/Documents/Papers
    ```
-   If the environment variable is not set, paper will be downloaded into the default Download Destination `~/Downloads/ArXiv_Papers`.

## Development

```bash
python3 -m venv venv && \
source venv/bin/activate && \
pip install -e ".[dev]"
```

## License

[MIT License](LICENSE) - Copyright (c) 2021-2022 Mark Huang
