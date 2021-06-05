# arXiv-dl

Command-line [arXiv.org](https://arxiv.org/) Papers Downloader

[[Source Code]](https://github.com/MarkHershey/arxiv-dl)
[[PyPI]](https://pypi.org/project/arxiv-dl/)

## Features

-   Download paper named `[id]_[title].pdf` into destination folder.
-   Maintain a papers list named `000_Paper_List.json` in the destination folder.
-   Extract paper metadata, like `title`, `authors`, `abstract`, `bibtex`, `code`, and write them into a new MarkDown document named `[id]__Notes.md` in the destination folder.

## Install

This is a command-line tool, you just need to use `pip` to install the package, then, you will be able to use the command `getpaper` in your terminal.

-   Pre-requisite: `Python 3`

```bash
pip install arxiv-dl
```

## Usage

```bash
$ getpaper "URL or ID"
```

Example:

```bash
$ getpaper 1512.03385

# OR
$ getpaper https://arxiv.org/abs/1512.03385

# OR
$ getpaper https://arxiv.org/pdf/1512.03385.pdf
```

Deprecating Commands:

-   `add-paper`
-   `dl-paper`

## Configuration (Optional)

Set Custom Download Destination Folder _(Optional)_

-   Let's say you want your papers get downloaded into `~/Documents/Papers`.
-   Make sure the folder `~/Documents/Papers` exists.
-   Set the environment variable `ARXIV_DOWNLOAD_FOLDER` to your desired location.
    ```bash
    $ export ARXIV_DOWNLOAD_FOLDER=~/Documents/Papers
    ```
-   If the environment variable is not set, paper will be downloaded into the default Download Destination `~/Downloads/ArXiv_Papers`.

## License

[MIT License](LICENSE) - Copyright (c) 2021 Mark Huang
