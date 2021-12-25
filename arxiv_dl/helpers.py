import json
import logging
import os
import re
import string
from pathlib import Path
from typing import Dict, List, Tuple, Union

import requests
from logger import logger
from models import PaperData

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


def get_download_destination() -> Path:
    download_path: str = os.environ.get("ARXIV_DOWNLOAD_FOLDER")

    if download_path:
        download_path: Path = Path(download_path).resolve()

        if not download_path.is_dir():
            logger.error(
                f"Invalid ARXIV_DOWNLOAD_FOLDER: '{download_path}' is not a directory."
            )
            raise Exception(
                f"Invalid ARXIV_DOWNLOAD_FOLDER: '{download_path}' is not a directory."
            )
    else:
        download_path: Path = Path(DEFAULT_DOWNLOAD_PATH).resolve()

        if not download_path.is_dir():
            logger.debug(f"Creating Directory: '{DEFAULT_DOWNLOAD_PATH}'")
            os.makedirs(str(DEFAULT_DOWNLOAD_PATH))

    return download_path


def download_pdf(paper_data: PaperData, download_dir: Union[str, Path]) -> None:
    download_path: Path = Path(download_dir) / paper_data.download_name
    if download_path.is_file():
        logger.debug(f'Paper PDF already exists at: "{download_path}"')
    else:
        logger.debug(f"Downloading...")
        logger.setLevel(logging.WARNING)
        response = requests.get(paper_data.pdf_url)
        with download_path.open(mode="wb") as f:
            f.write(response.content)
        logger.setLevel(logging.DEBUG)
        logger.debug(f'Done! Paper saved to "{download_path}"')
    return None


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

[arXiv]({paper_data.abs_url}), [PDF]({paper_data.pdf_url})

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

    pattern = "^([0-2])([0-9])(0|1)([0-9])\.[0-9]{4,5}(v[0-9]{1,2})?$"

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
    pattern = "([0-2])([0-9])(0|1)([0-9])\.[0-9]{4,5}(v[0-9]{1,2})?"
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
    # TODO
    ...


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
    ...
