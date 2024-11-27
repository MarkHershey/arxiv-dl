import json
import logging
import os
import re
import shlex
import string
import sys
import subprocess
from pathlib import Path
from typing import Union

import pymupdf

from .dl_utils import download
from .logger import logger
from .models import PaperData

DEFAULT_DOWNLOAD_PATH = Path.home() / "Downloads/ArXiv_Papers"


###########################################################################
### General Helper Functions


def _initial_configs() -> dict:
    return dict(
        download_dir=str(DEFAULT_DOWNLOAD_PATH),  # download destination folder
        verbose=False,  # show verbose prints
        debug=False,  # show debug prints
        quite=False,  # no stdout, return code only
        pdf_only=False,  # download only PDF
        n_threads=5,  # number of parallel connections
    )


def get_config_path() -> Path:
    """Get platform-specific config file path."""
    current_platform = sys.platform
    if current_platform in ("linux", "darwin"):
        config_dir = Path.home() / ".config/arxiv-dl"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "config.json"
    elif current_platform == "win32":
        local_app_data = os.getenv("LOCALAPPDATA", Path.home() / "AppData/Local")
        config_dir = Path(local_app_data) / "arxiv-dl"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "config.json"
    else:
        raise Exception("Unknown platform.")

    # create config file if it does not exist
    if not config_path.is_file():
        with config_path.open(mode="w") as f:
            json.dump(_initial_configs(), f, indent=4, sort_keys=True)

    return config_path


def normalize_paper_title(title: str) -> str:
    normalized_title = ""
    for char in title:
        if char in string.printable:
            if char in string.ascii_letters or char in string.digits:
                # accept only ascii letters and digits
                normalized_title += char
            elif char in string.whitespace:
                # convert whitespaces to underscores
                normalized_title += "_"
            elif char in "?+-":
                # accept only plus, minus, and question mark
                normalized_title += char
            else:
                pass
    return normalized_title


def get_download_dest() -> Path:
    """Get the download destination folder path."""
    dl_path: str = os.environ.get("ARXIV_DOWNLOAD_FOLDER")

    if dl_path:
        dl_path: Path = Path(dl_path).resolve()
    else:
        dl_path: Path = Path(DEFAULT_DOWNLOAD_PATH).resolve()

    if not dl_path.is_dir():
        logger.debug(f"Creating Directory: '{DEFAULT_DOWNLOAD_PATH}'")
        dl_path.mkdir(parents=True, exist_ok=True)

    return dl_path


def download_pdf(
    paper_data: PaperData,
    download_dir: Union[str, Path],
    parallel_connections: int = 5,
) -> None:
    download_path: Path = Path(download_dir) / paper_data.download_name
    N = int(parallel_connections)
    assert N > 0, "Number of parallel connections must be greater than 0."
    assert N <= 16, "Number of parallel connections must be less than 16."

    if download_path.is_file():
        logger.debug(f'[Done] Paper PDF already exists at: "{download_path}"')
        return None

    if paper_data.src_website == "CVF":
        # NOTE: download from CVF is sufficiently fast using 1 connection
        N = 1

    if command_exists("aria2c") and N > 1:
        out = aria2_download(
            url=paper_data.pdf_url,
            download_dir=download_dir,
            download_name=paper_data.download_name,
            parallel_connections=parallel_connections,
        )
    else:
        out = http_download(
            url=paper_data.pdf_url,
            download_dir=download_dir,
            download_name=paper_data.download_name,
        )

    if isinstance(out, Path):
        if out.is_file():
            logger.debug(f'[Done] Paper saved to "{download_path}"')

    add_pdf_metadata(paper_data, download_path)

    return None


def http_download(
    url: str,
    download_dir: Union[str, Path],
    download_name: str,
) -> Path:
    """
    Assume:
        1. download_dir exists.
        2. target file does not exist.
    """
    download_dir = Path(download_dir)
    assert download_dir.is_dir(), "Download directory does not exist."
    download_path: Path = download_dir / download_name
    assert download_path.is_file() is False, "File already exists"

    logger.debug("[Downloading] Using HTTP")
    download(url=url, out=str(download_path))
    return download_path


def aria2_download(
    url: str,
    download_dir: Union[str, Path],
    download_name: str,
    parallel_connections: int = 5,
) -> Path:
    """
    Download the paper using aria2. Assume the aria2 executable is in the system path.

    Args:
        url: URL of the paper.
        download_dir: Directory to download the paper to.
    """
    download_dir = Path(download_dir)
    assert download_dir.is_dir(), "Download directory does not exist."
    download_path: Path = download_dir / download_name
    assert download_path.is_file() is False, "File already exists"

    N = int(parallel_connections)
    assert N > 0, "Number of parallel connections must be greater than 0."
    assert N <= 16, "Number of parallel connections must be less than 16."

    aria2_command = (
        f"aria2c -x {N} -s {N} -d '{download_dir}' -o '{download_name}' {url}"
    )
    # NOTE: aria2c flags:
    # -x, --max-connection-per-server=<NUM>
    #     The maximum number of connections to one server for each download.
    # -s, --split=<N>
    #     Download a file using N connections.
    # -d, --dir=<DIR>
    #     The directory to store the downloaded file.
    # -o, --out=<FILE>
    #     The file name of the downloaded file relative to the directory given in -d option.

    # logger.debug(f"Executing: '{aria2_command}'")
    logger.debug(f"[Downloading] Using aria2 with {N} connections")
    completed_proc = subprocess.run(
        shlex.split(aria2_command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed_proc.returncode != 0:
        logger.error(
            f"[Error] aria2c failed with return code {completed_proc.returncode}"
        )
        logger.error(f"[Error] Output: {completed_proc.stdout.decode('utf-8')}")
        return None

    return download_path


def command_exists(command: str) -> bool:
    """
    Check if the command exists in the system.

    Args: str
        command: command to be checked.

    Returns: bool
        True if the command exists. False otherwise.
    """
    # >= Python 3.3 and is cross-platform
    from shutil import which

    return which(command) is not None


def add_pdf_metadata(paper_data: PaperData, download_path: Path):
    doc = pymupdf.open(download_path)
    doc.set_metadata(
        {
            "author": ", ".join(paper_data.authors),
            "title": paper_data.title,
            "subject": paper_data.abstract,
        }
    )
    doc.saveIncr()
    doc.close()


def add_to_paper_list(paper_data: PaperData, download_dir: Union[str, Path]) -> None:
    paper_list_path: Path = Path(download_dir) / "000_Paper_List.json"
    paper_dict = paper_data.dict()

    paper_list = dict()
    if paper_list_path.is_file():
        with paper_list_path.open() as f:
            paper_list = json.load(f)

    if paper_data.paper_id not in paper_list:
        paper_list[paper_data.paper_id] = paper_dict
        with paper_list_path.open(mode="w") as f:
            json.dump(paper_list, f, indent=4)

    return None


def create_paper_note(paper_data: PaperData, download_dir: Union[str, Path]) -> None:
    note_path: Path = Path(download_dir) / f"{paper_data.paper_id}__Notes.md"
    authors: list = paper_data.authors
    authors: list = [f"- {name}" for name in authors]
    authors: str = "\n".join(authors)

    official_code_urls: list = paper_data.official_code_urls
    official_code_urls: list = [
        f"- [{url}]({url})" for url in paper_data.official_code_urls
    ]
    official_code_urls: str = "\n".join(official_code_urls)

    pwc_page_url = paper_data.pwc_page_url
    if pwc_page_url:
        pwc_page_url = f"- [{pwc_page_url}]({pwc_page_url})"

    # markdown content text
    md_content = f"""
# {paper_data.title}

[Abstract]({paper_data.abs_url}), [PDF]({paper_data.pdf_url})

## Authors

{authors}

## Abstract

{paper_data.abstract}

## Comments

{paper_data.comments}

## Source Code

Official Code

{official_code_urls}

Community Code

{pwc_page_url}

## Bibtex

```tex
{paper_data.bibtex}
```

## Notes

Type your reading notes here...

"""
    if not note_path.is_file():
        with note_path.open(mode="w") as f:
            f.write(md_content)
    return


if __name__ == "__main__":
    abs_url = "https://openaccess.thecvf.com/content/CVPR2021/html/Wu_Greedy_Hierarchical_Variational_Autoencoders_for_Large-Scale_Video_Prediction_CVPR_2021_paper.html"
    pdf_url = "https://openaccess.thecvf.com/content/CVPR2021/papers/Wu_Greedy_Hierarchical_Variational_Autoencoders_for_Large-Scale_Video_Prediction_CVPR_2021_paper.pdf"
    paper_data = process_cvf_target(abs_url)
    print(paper_data)

    abs_url2 = "https://openaccess.thecvf.com/content_cvpr_2013/html/Kim_Deformable_Spatial_Pyramid_2013_CVPR_paper.html"
    pdf_url2 = "https://openaccess.thecvf.com/content_cvpr_2013/papers/Kim_Deformable_Spatial_Pyramid_2013_CVPR_paper.pdf"
    paper_data2 = process_cvf_target(abs_url2)
    print(paper_data2)

    assert paper_data.abs_url == abs_url
    assert paper_data.pdf_url == pdf_url

    assert paper_data2.abs_url == abs_url2
    assert paper_data2.pdf_url == pdf_url2
