import json
import logging
import os
import re
import string
from pathlib import Path
from typing import Dict, List, Tuple, Union

import requests
from bs4 import BeautifulSoup

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
    src_website = "arxiv"
    if target[0].isdigit():
        paper_id = target
    else:
        paper_id = get_arxiv_id_from_url(target)

    assert valid_arxiv_id(paper_id)
    abs_url = f"https://arxiv.org/abs/{paper_id}"
    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

    return PaperData(
        paper_id=paper_id,
        abs_url=abs_url,
        pdf_url=pdf_url,
        src_website=src_website,
    )


if __name__ == "__main__":
    ...
