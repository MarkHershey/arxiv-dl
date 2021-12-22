# https://arxiv.org/help/api/user-manual

import json
import logging
import os
import re
import string
from pathlib import Path
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

from helpers import (
    get_download_destination,
    normalize_paper_title,
    process_arxiv_target,
)
from logger import logger
from models import PaperData

download_dir: Path = None


def scrape_metadata_arxiv(paper_data: PaperData) -> None:
    logger.setLevel(logging.DEBUG)
    logger.debug("Processing...")
    logger.setLevel(logging.WARNING)

    response = requests.get(paper_data.abs_url)
    if response.status_code != 200:
        logger.error(f"Cannot connect to {paper_data.abs_url}")
        raise Exception(f"Cannot connect to {paper_data.abs_url}")
    # make soup
    soup = BeautifulSoup(response.text, "html.parser")

    # get TITLE
    result = soup.find("h1", class_="title mathjax")
    tmp = [i.string for i in result]
    paper_title = tmp.pop()
    paper_data.title = paper_title

    # get AUTHORS
    result = soup.find("div", class_="authors")
    author_list = [i.string.strip() for i in result]
    author_list.pop(0)
    while "," in author_list:
        author_list.remove(",")
    paper_data.authors = author_list

    # get ABSTRACT
    result = soup.find("blockquote", class_="abstract mathjax")
    tmp = [i.string for i in result]
    paper_abstract = tmp.pop()
    tmp = paper_abstract.split("\n")
    paper_abstract = " ".join(tmp)
    paper_data.abstract = paper_abstract.strip()

    # get COMMENTS
    result = soup.find("td", class_="tablecell comments mathjax")
    if result:
        comments = [i.string.strip() if i.string else "" for i in result]
        comments = " ".join(comments)
    else:
        comments = ""
    paper_data.comments = comments.strip()

    # get PWC (paper with code)
    # API: https://arxiv.paperswithcode.com/api/v0/papers/{paper_id}
    pwc_url = f"https://arxiv.paperswithcode.com/api/v0/papers/{paper_data.paper_id}"
    pwc_response = requests.get(pwc_url)
    if pwc_response.status_code == 200:
        pwc = pwc_response.text
        pwc = json.loads(pwc)
        official_code_urls: list = pwc.get("all_official", [])
        official_code_urls: list = [i.get("url") for i in official_code_urls]
        pwc_page_url: str = pwc.get("paper_url", "")
    else:
        official_code_urls = []
        pwc_page_url = ""
    paper_data.official_code_urls = official_code_urls
    paper_data.pwc_page_url = pwc_page_url.strip()

    # get BIBTEX
    bibtex_url = f"https://arxiv.org/bibtex/{paper_data.paper_id}"
    bibtex_response = requests.get(bibtex_url)
    if bibtex_response.status_code == 200:
        bibtex = bibtex_response.text
    else:
        bibtex = ""
    paper_data.bibtex = bibtex.strip()

    # construct filename
    paper_data.download_name = (
        f"{paper_data.paper_id}_{normalize_paper_title(paper_data.title)}.pdf"
    )

    return None


def download_pdf(paper_data: PaperData) -> None:
    download_path = download_dir / paper_data.download_name
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


def add_to_paper_list(paper_data: PaperData) -> None:
    paper_list_path: Path = download_dir / "000_Paper_List.json"
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


def create_paper_note(paper_data: PaperData) -> None:
    note_path = Path(download_dir) / f"{paper_data.paper_id}__Notes.md"
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


def add_paper(target: str, verbose: bool = False, *args, **kwargs) -> None:
    """
    Entry point

    Download paper and extract paper metadata
    """
    ### Get Target Download Directory
    try:
        global download_dir
        download_dir = get_download_destination()
    except Exception as e:
        logger.exception(e)
        logger.error("Abort: Environment Variable Error")
        return

    ### Filter Invalid Target String
    if not target or not isinstance(target, str):
        logger.error("Abort: Target is not specified correctly")
        return

    if (
        not target.startswith(("http://", "https://", "www."))
        and not target[0].isdigit()
    ):
        logger.error("Abort: Unknown target")
        return

    ### Identify Paper Source/Venues
    if target[0].isdigit() or "arxiv.org" in target:
        # assume target is an arXiv ID
        paper_data = process_arxiv_target(target)
    elif "openaccess.thecvf.com" in target:  # assume target is a CVF URL
        # CVPR, ICCV, WACV
        ...
    elif "papers.nips.cc/paper" in target:  # assume target is a NeurIPS URL
        ...
    elif "openreview.net" in target:  # assume target is an OpenReview URL
        ...
    elif target.endswith(".pdf"):  # assume target is a PDF file
        ...
    else:
        logger.error("Abort: Unknown target")
        return False

    # TODO: verify expected keys are present
    ...

    # start scraping from source website
    if paper_data.src_website == "arxiv":
        try:
            scrape_metadata_arxiv(paper_data)
        except Exception as err:
            logger.error(err)
            logger.error("Abort: Error while getting paper")
            return
    else:
        logger.error(f"Invalid source website: '{paper_data.src_website}'")
        return

    # adjust logging level
    logger.setLevel(logging.DEBUG)
    if verbose:
        logger.debug(json.dumps(paper_data.dict(), indent=4))

    # download paper
    try:
        download_pdf(paper_data)
    except Exception as err:
        logger.error("Error while downloading paper")
        return

    # update paper list
    try:
        add_to_paper_list(paper_data)
    except Exception as err:
        logger.warning("Error while updating paper list")
        return

    # Create paper notes
    try:
        create_paper_note(paper_data)
    except Exception as err:
        logger.warning("Error while creating note")
        return


if __name__ == "__main__":
    add_paper("1506.01497", verbose=True)
    add_paper("https://arxiv.org/abs/1506.01497", verbose=True)
