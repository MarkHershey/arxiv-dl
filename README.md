# arXiv-dl

Command-line Research Paper Downloader for [`arXiv.org`](https://arxiv.org/), [`ECVA`](https://www.ecva.net/papers.php) & [`CVF Open Access`](https://openaccess.thecvf.com/menu).

[![](https://img.shields.io/pypi/v/arxiv-dl)](https://pypi.org/project/arxiv-dl/)
[![](https://img.shields.io/pypi/dm/Arxiv-dl)](https://pypistats.org/packages/arxiv-dl)
[![](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![](https://img.shields.io/badge/license-MIT-black)](https://github.com/MarkHershey/arxiv-dl/blob/master/LICENSE)

_Disclaimer: This is a highly-opinionated command-line tool for downloading papers. It priorities ease of use for researchers. Obviously, this is not an ArXiv official project._

![](imgs/demo_v1.2.0.png)

## What does it do?

-   Support downloading papers from [arXiv](https://arxiv.org/), [ECCV](https://www.ecva.net/papers.php), [CVPR, ICCV, WACV](https://openaccess.thecvf.com/menu) via simple CLI.
-   Support downloading speedup by using [aria2](https://aria2.github.io/).
-   Retrieve the paper's metadata such as:
    -   Title, Abstract, Year
    -   Authors
    -   Comments (Conference acceptance info)
    -   Repository URLs
    -   `BibTeX` Citation
-   Automatically maintain a list of local papers and their metadata in a JSON file.
-   Configure the desired download destination via an environment variable or a command-line argument.
-   All downloaded papers will have standardized filename for easy browsing.

## Why?

-   Save time and effort to download and organize papers on your machine.
-   Speedup downloading process by using multiple parallel connections.
-   Local paper list would be handy for quick local lookup, making notes, and doing citations.

## How to install it?

This is a command-line tool, simply use `pip` to install the package globally, then you are good to go!

-   Pre-requisite: `Python 3.x`

```bash
python3 -m pip install -U arxiv-dl
```

> [!NOTE]
> After installation, you need to ensure the installation path is included in your PATH environment variable (tips: [here](https://github.com/MarkHershey/arxiv-dl/issues/16#issue-3266539938)). If you encounter any difficulty finding / setting the PATH, there is this recommended way of [installing stand alone command line tools](https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/), kindly follow its instruction when installing `arxiv-dl`.

Optionally, install [aria2c](https://aria2.github.io/) for multi-connection download speedup.

-   MacOS: `brew install aria2`
-   Linux: `sudo snap install aria2c`

## How to use it?

After installation, you may use the command `paper` in your shell to download papers. 
(Legacy commands `arxiv-dl` and `getpaper` are equivalent to the command `paper`.)

```bash
paper [OPTIONS] TARGET(s)
```

### Use in your shell:

```bash
# download a single TARGET
$ paper 1512.03385

# download multiple TARGETs separated by space
$ paper 2103.15538 2304.04415 https://arxiv.org/abs/1512.03385
```

### Supported types of download TARGETs:

<details>
<summary><strong>Click to expand</strong></summary>

✅ Supported, 🚧 Not Yet Supported, ❌ Not Supported

-   **[ArXiv](https://arxiv.org/)** 
    -   ✅ ArXiv ID: `1512.03385` or `arXiv:1512.03385`
    -   ✅ Legacy ArXiv ID: `alg-geom/9708001` or `cs/0002001`, etc.
    -   ✅ ArXiv Abstract Page URL: `https://arxiv.org/abs/1512.03385` 
    -   ✅ ArXiv PDF Page URL: `https://arxiv.org/pdf/1512.03385.pdf`
    -   ✅ ArXiv HTML Page URL: `https://arxiv.org/html/2506.15442`
-   **[CVF Open Access](https://openaccess.thecvf.com/menu) (CVPR, ICCV, WACV)**
    -   ✅ CVF Abstract Page URL: `https://openaccess.thecvf.com/content/**/html/**/*.html`
    -   ✅ CVF PDF Page URL: `https://openaccess.thecvf.com/content/**/papers/**/*.pdf`
-   **[ECVA](https://www.ecva.net/papers.php) (ECCV)** 
    -   ✅ ECVA Abstract Page URL: `https://www.ecva.net/html/**/*.php`
    -   ❌ ECVA PDF Page URL: `https://www.ecva.net/papers/**/*.pdf`
-   **[NeurIPS](https://papers.nips.cc/)**
    -   🚧 NeurIPS Abstract Page URL
    -   🚧 NeurIPS PDF Page URL
-   **[OpenReview](https://openreview.net/)**
    -   🚧 TODO
</details>

### Frequently used OPTIONS:

-   `-v`, `--verbose` (optional): set to verbose, print full details.
-   `-d`, `--download-dir` (optional): Specify one-time download directory. This option will override the default download directory or the one specified in the environment variable `ARXIV_DOWNLOAD_FOLDER`.
-   `-n`, `--n-threads` (optional): Specify the number of parallel connections to be used by `aria2`. 

> [!TIP]
> more options are available, run `paper -h` to see all options.

### Use it in your code:

```python
from arxiv_dl import download_paper

download_paper(target="1512.03385", download_dir=".", set_verbose_level="silent")
```


## Configurations

### Default Download Destination

-   Without any configurations, all paper will be downloaded to `$HOME/Downloads/ArXiv_Papers`, where `$HOME` is current user's home directory.

### Set Your Custom Download Destination _(Optional)_

You may configure your preferred download destination once and for all via an environment variable. This will override the default download destination. To do that, include the following line in your `.bashrc` or `.zshrc` file:

```bash
export ARXIV_DOWNLOAD_FOLDER="YOUR/PATH/TO/ANY/FOLDER"
```

-   Every time you use the `paper` command, the download destination will be set to the following order of priority:
    1.  Command-line option `-d` (highest priority)
    2.  Environment variable `ARXIV_DOWNLOAD_FOLDER`
    3.  Default download destination (lowest priority)

### Set Custom Command Alias _(Optional)_

-   You can always set your own preferred alias to rename the command or add more options.
-   Include the following line(s) in your `.bashrc` or `.zshrc` file to set your preferred alias:
    ```bash
    alias dp="paper"
    alias dpv="paper -v -d '~/Documents/Papers'"
    ```

## Development

### Set up development environment

```bash
# create a virtual environment
python3 -m venv venv && source venv/bin/activate

# install dependencies
pip install -U -r requirements.txt

# install the package in editable mode & dev dependencies
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

## License

This project is licensed under the [MIT License](https://github.com/MarkHershey/arxiv-dl/blob/master/LICENSE).  
&copy; Mark H. Huang. All rights reserved.
