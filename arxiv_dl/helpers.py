import json
import logging
import os
import re
import shlex
import string
import subprocess
from pathlib import Path
from typing import Union

import requests

from .logger import logger
from .models import PaperData

DEFAULT_DOWNLOAD_PATH = Path.home() / "Downloads/ArXiv_Papers"


###########################################################################
### General Helper Functions


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
        os.makedirs(str(DEFAULT_DOWNLOAD_PATH), exist_ok=True)

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
    logger.setLevel(logging.WARNING)
    response = requests.get(url)
    with download_path.open(mode="wb") as f:
        f.write(response.content)
    logger.setLevel(logging.DEBUG)
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


###############################################################################
### ArXiv Helper Functions


def valid_arxiv_id(paper_id: str) -> bool:
    """
    Validate the arXiv ID according to official arXiv ID format.
    Current implementation validates paper accepted by arXiv during 2007 to 2029.

    Args: str
        paper_id: arXiv ID to be validated (e.g. '1901.01234')

    Returns: bool
        True if the arXiv ID is valid. False otherwise.

    Ref: https://arxiv.org/help/arxiv_identifier
    """
    if not isinstance(paper_id, str):
        return False

    pattern = r"^([0-2])([0-9])(0|1)([0-9])\.[0-9]{4,5}(v[0-9]{1,2})?$"

    if not re.fullmatch(pattern, paper_id):
        return False

    year = int(paper_id[0:2])
    month = int(paper_id[2:4])

    if not 7 <= year <= 29:
        return False
    if not 1 <= month <= 12:
        return False

    return True


def get_arxiv_id_from_url(url: str) -> str:
    """
    Extract the arXiv ID from the given URL.

    Args:
        url: URL of the arXiv paper.

    Returns:
        arXiv ID of the paper.

    Raises:
        Exception: If the URL is not a valid arXiv URL.
    """
    pattern = r"([0-2])([0-9])(0|1)([0-9])\.[0-9]{4,5}(v[0-9]{1,2})?"
    match = re.search(pattern, url)
    if match:
        return match[0]
    else:
        raise Exception("Could not find arXiv ID in URL.")


def process_arxiv_target(target: str) -> PaperData:
    if target[0].isdigit():
        paper_id = target
    else:
        paper_id = get_arxiv_id_from_url(target)
    assert valid_arxiv_id(paper_id)

    abs_url = f"https://arxiv.org/abs/{paper_id}"
    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    src_website = "ArXiv"

    return PaperData(
        paper_id=paper_id,
        abs_url=abs_url,
        pdf_url=pdf_url,
        src_website=src_website,
    )


###############################################################################
### CVF Helper Functions


def process_cvf_target(target: str) -> PaperData:
    # Get conference year
    pattern = r"20[0-9][0-9]"
    match = re.search(pattern, target)
    if match:
        idx_s, idx_e = match.span()
        year = int(target[idx_s:idx_e])
    else:
        year = 0

    idx = target.find("openaccess.thecvf.com")
    target = target[idx + 22 :]
    tokens = target.split("/")
    src_website = "CVF"

    target = tokens[-1]
    if target.endswith(".pdf"):
        target_name = target[:-4]
    elif target.endswith(".html"):
        target_name = target[:-5]
    else:
        raise Exception("Unexpected CVF URL.")

    workshop_name = None

    if 2013 <= year <= 2016 or (year == 2017 and "CVPR" in target):
        # main: content_venue/html/
        # main: content_venue/papers/
        # workshop: content_venue/workshop_name/html/
        # workshop: content_venue/workshop_name/papers/
        if len(tokens) == 4:
            venue = tokens[0]  # e.g. content_iccv_workshops_2013
            workshop_name = tokens[1]
            mid_path = f"{venue}/{workshop_name}"
        elif len(tokens) == 3:
            venue = tokens[0]  # e.g. content_cvpr_2013
            mid_path = f"{venue}"
        else:
            raise Exception("Unexpected CVF URL.")

        abs_url = f"https://openaccess.thecvf.com/{mid_path}/html/{target_name}.html"
        pdf_url = f"https://openaccess.thecvf.com/{mid_path}/papers/{target_name}.pdf"

    elif year == 2017 and "ICCV" in target:
        # super special case: content_venue is smaller case in main conference's abs_url only
        # main: content_venue/html/
        # main: content_venue/papers/
        # workshop: content_venue/workshop_name/html
        # workshop: content_venue/papers/workshop_name/
        if len(tokens) == 3:
            venue = tokens[0]
            abs_url = f"https://openaccess.thecvf.com/content_iccv_2017/html/{target_name}.html"
            pdf_url = f"https://openaccess.thecvf.com/content_ICCV_2017/papers/{target_name}.pdf"
        elif len(tokens) == 4:
            venue = tokens[0]
            if target.endswith(".html"):
                workshop_name = tokens[1]
            else:
                workshop_name = tokens[2]
            abs_url = f"https://openaccess.thecvf.com/{venue}/{workshop_name}/html/{target_name}.html"
            pdf_url = f"https://openaccess.thecvf.com/{venue}/papers/{workshop_name}/{target_name}.pdf"
        else:
            raise Exception("Unexpected CVF URL.")
    elif year == 2018:
        # main: content_venue/html/
        # main: content_venue/papers/
        # workshop: content_venue/workshop_name/html
        # workshop: content_venue/papers/workshop_name/
        if len(tokens) == 3:
            venue = tokens[0]
            abs_url = f"https://openaccess.thecvf.com/{venue}/html/{target_name}.html"
            pdf_url = f"https://openaccess.thecvf.com/{venue}/papers/{target_name}.pdf"
        elif len(tokens) == 4:
            venue = tokens[0]
            if target.endswith(".html"):
                workshop_name = tokens[1]
            else:
                workshop_name = tokens[2]
            abs_url = f"https://openaccess.thecvf.com/{venue}/{workshop_name}/html/{target_name}.html"
            pdf_url = f"https://openaccess.thecvf.com/{venue}/papers/{workshop_name}/{target_name}.pdf"
        else:
            raise Exception("Unexpected CVF URL.")
    elif 2019 <= year <= 2020:
        # main: content_venue/html/
        # main: content_venue/papers/
        # workshop: content_venue/html/workshop_name/
        # workshop: content_venue/papers/workshop_name/
        if len(tokens) == 3:
            venue = tokens[0]
            abs_url = f"https://openaccess.thecvf.com/{venue}/html/{target_name}.html"
            pdf_url = f"https://openaccess.thecvf.com/{venue}/papers/{target_name}.pdf"
        elif len(tokens) == 4:
            venue = tokens[0]
            workshop_name = tokens[2]
            abs_url = f"https://openaccess.thecvf.com/{venue}/html/{workshop_name}/{target_name}.html"
            pdf_url = f"https://openaccess.thecvf.com/{venue}/papers/{workshop_name}/{target_name}.pdf"
        else:
            raise Exception("Unexpected CVF URL.")

    elif year >= 2021:
        # main: content/venue/html/
        # main: content/venue/papers/
        # workshop: content/venue/workshop_name/html/
        # workshop: content/venue/workshop_name/papers/
        if len(tokens) == 4:
            venue = tokens[1]
            mid_path = f"content/{venue}"
        elif len(tokens) == 5:
            venue = tokens[1]
            workshop_name = tokens[2]
            mid_path = f"content/{venue}/{workshop_name}"
        else:
            raise Exception("Unexpected CVF URL.")

        abs_url = f"https://openaccess.thecvf.com/{mid_path}/html/{target_name}.html"
        pdf_url = f"https://openaccess.thecvf.com/{mid_path}/papers/{target_name}.pdf"

    else:
        raise Exception("Unexpected CVF URL.")

    # get conference venue
    _venue = venue.upper()
    if "ICCV" in _venue:
        paper_venue = "ICCV"
    elif "CVPR" in _venue:
        paper_venue = "CVPR"
    elif "WACV" in _venue:
        paper_venue = "WACV"

    if workshop_name:
        paper_venue += "_Workshops"

    paper_id = "_".join(target_name.split("_")[1:-3])

    download_name = f"{year}_{paper_venue}_{paper_id}.pdf"

    return PaperData(
        paper_id=paper_id,
        abs_url=abs_url,
        pdf_url=pdf_url,
        year=year,
        src_website=src_website,
        paper_venue=paper_venue,
        download_name=download_name,
    )


###############################################################################
### NeurIPS Helper Functions


def process_nips_target(target: str) -> PaperData:
    # TODO
    ...


###############################################################################
### OpenReview Helper Functions


def process_openreview_target(target: str) -> PaperData:
    # TODO
    ...


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
