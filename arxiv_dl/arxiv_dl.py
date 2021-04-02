# https://arxiv.org/help/api/user-manual

import json
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

import colorlog
import requests
from bs4 import BeautifulSoup

DEFAULT_DOWNLOAD_PATH = Path.home() / "Downloads/ArXiv_Papers"

###########################################################################
# Set up colored logger

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

sh = colorlog.StreamHandler()
sh.setLevel(logging.DEBUG)

color_formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "green",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_yellow",
    },
    secondary_log_colors={},
    style="%",
)

sh.setFormatter(color_formatter)
logger.addHandler(sh)

###########################################################################


def get_local_paper_folder_path() -> Path:
    download_path = os.environ.get("ARXIV_DOWNLOAD_FOLDER")
    if download_path:
        download_path = Path(download_path).resolve()
        if not download_path.is_dir():
            logger.error(
                f"Invalid ARXIV_DOWNLOAD_FOLDER: '{download_path}' is not a directory."
            )
            raise Exception(
                f"Invalid ARXIV_DOWNLOAD_FOLDER: '{download_path}' is not a directory."
            )
    else:
        download_path = Path(DEFAULT_DOWNLOAD_PATH).resolve()
        if not download_path.is_dir():
            logger.debug(f"Creating Directory: '{DEFAULT_DOWNLOAD_PATH}'")
            os.makedirs(str(DEFAULT_DOWNLOAD_PATH))

    return download_path


def process_arxiv_url(url: str) -> Tuple[str]:
    def get_paper_id_from_url(url) -> str:
        while "/" in url:
            slash_idx = url.find("/")
            url = url[slash_idx + 1 :]
        if url.endswith(".pdf"):
            return url[:-4]
        else:
            return url

    paper_id = get_paper_id_from_url(url)

    if "arxiv.org/abs" in url:
        # url is abstract page
        paper_url = url
        pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    elif "arxiv.org/pdf" in url:
        # url is pdf page
        paper_url = f"https://arxiv.org/abs/{paper_id}"
        pdf_url = url
    else:
        logger.error("Unexpected URL Error by arxiv URL Handler.")
        raise Exception("Unexpected URL Error by arxiv URL Handler.")

    return paper_id, paper_url, pdf_url


def process_url(url: str) -> Dict[str, str]:
    if "arxiv.org" in url:
        src_website = "arxiv"
        paper_id, paper_url, pdf_url = process_arxiv_url(url)
    else:
        logger.error("URL not supported")
        raise Exception("URL not supported")

    tmp_paper_dict = {
        "paper_id": paper_id,
        "paper_url": paper_url,
        "pdf_url": pdf_url,
        "src_website": src_website,
    }

    return tmp_paper_dict


def validate_arxiv_paper_id(paper_id: str) -> None:
    """
    Raise exception if the given paper_id is not a valid arXiv identifier.

    Current implementation validates paper accepted by arXiv during 2007 to 2029

    Ref: https://arxiv.org/help/arxiv_identifier
    """
    error = "Invalid arXiv paper identifier."
    if not isinstance(paper_id, str):
        raise TypeError(error)

    pattern = "^([0-2])([0-9])(0|1)([0-9])\.[0-9]{4,5}(v[0-9]{1,2})?$"

    if not re.fullmatch(pattern, paper_id):
        raise ValueError(error)

    year = int(paper_id[0:2])
    month = int(paper_id[2:4])

    if not 7 <= year <= 29:
        raise ValueError(error)
    if not 1 <= month <= 12:
        raise ValueError(error)


def process_paper_id(paper_id: str) -> Dict[str, str]:
    # validate first
    validate_arxiv_paper_id(paper_id)
    src_website = "arxiv"
    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    paper_url = f"https://arxiv.org/abs/{paper_id}"

    tmp_paper_dict = {
        "paper_id": paper_id,
        "paper_url": paper_url,
        "pdf_url": pdf_url,
        "src_website": src_website,
    }

    return tmp_paper_dict


def get_paper_from_arxiv(tmp_paper_dict: Dict[str, str]) -> Dict[str, str]:
    logger.setLevel(logging.DEBUG)
    logger.debug("Processing...")
    logger.setLevel(logging.WARNING)
    paper_url = tmp_paper_dict.get("paper_url")
    paper_id = tmp_paper_dict.get("paper_id")
    response = requests.get(paper_url)

    if response.status_code != 200:
        logger.error(f"Cannot connect to {paper_url}")
        raise Exception(f"Cannot connect to {paper_url}")

    # make soup
    soup = BeautifulSoup(response.text, "html.parser")

    # get TITLE
    result = soup.find("h1", class_="title mathjax")
    tmp = [i.string for i in result]
    paper_title = tmp.pop()
    tmp_paper_dict["title"] = paper_title
    logger.setLevel(logging.DEBUG)
    logger.debug(f"Paper Title: {paper_title}")
    logger.setLevel(logging.WARNING)

    # get AUTHORS
    result = soup.find("div", class_="authors")
    author_list = [i.string.strip() for i in result]
    author_list.pop(0)
    while "," in author_list:
        author_list.remove(",")
    tmp_paper_dict["authors"] = author_list

    # get ABSTRACT
    result = soup.find("blockquote", class_="abstract mathjax")
    tmp = [i.string for i in result]
    paper_abstract = tmp.pop()
    tmp = paper_abstract.split("\n")
    paper_abstract = " ".join(tmp)
    tmp_paper_dict["abstract"] = paper_abstract.strip()

    # get COMMENTS
    result = soup.find("td", class_="tablecell comments mathjax")
    if result:
        comments = [i.string.strip() if i.string else "" for i in result]
        comments = " ".join(comments)
    else:
        comments = ""
    tmp_paper_dict["comments"] = comments.strip()

    # get PWC (paper with code)
    # API: https://arxiv.paperswithcode.com/api/v0/papers/{paper_id}
    pwc_url = f"https://arxiv.paperswithcode.com/api/v0/papers/{paper_id}"
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
    tmp_paper_dict["official_code_urls"] = official_code_urls
    tmp_paper_dict["pwc_page_url"] = pwc_page_url.strip()

    # get BIBTEX
    bibtex_url = f"https://arxiv.org/bibtex/{paper_id}"
    bibtex_response = requests.get(bibtex_url)
    if bibtex_response.status_code == 200:
        bibtex = bibtex_response.text
    else:
        bibtex = ""
    tmp_paper_dict["bibtex"] = bibtex.strip()

    return tmp_paper_dict


def download_pdf(paper_dict: Dict[str, str]) -> None:
    filepath = Path(paper_dict.get("filepath"))
    if filepath.is_file():
        logger.debug(f"Paper PDF already exists at: {filepath}")
    else:
        logger.debug(f"Downloading...")
        logger.setLevel(logging.WARNING)
        response = requests.get(paper_dict.get("pdf_url"))
        with filepath.open(mode="wb") as f:
            f.write(response.content)
        logger.setLevel(logging.DEBUG)
        logger.debug(f"Done! Paper saved to {filepath}")
    return


def add_to_paper_list(download_dir: Path, paper_dict: Dict[str, str]) -> None:
    paper_list_path = Path(download_dir) / "000_Paper_List.json"
    paper_id = paper_dict.get("paper_id")
    if not paper_list_path.is_file():
        paper_list = dict()
        paper_list[paper_id] = paper_dict
        with paper_list_path.open(mode="w") as f:
            json.dump(paper_list, f, indent=4)
    else:
        with paper_list_path.open() as f:
            paper_list = json.load(f)
        if paper_id not in paper_list:
            paper_list[paper_id] = paper_dict
            with paper_list_path.open(mode="w") as f:
                json.dump(paper_list, f, indent=4)
    return


def create_paper_note(download_dir: Path, paper_dict: Dict[str, str]) -> None:
    paper_id = paper_dict.get("paper_id", "").strip()
    note_path = Path(download_dir) / f"{paper_id}__Notes.md"
    paper_url = paper_dict.get("paper_url", "")
    pdf_url = paper_dict.get("pdf_url", "")
    title = paper_dict.get("title", "")
    authors: list = paper_dict.get("authors", [])
    authors: list = [f"- {name}" for name in authors]
    authors: str = "\n".join(authors)
    abstract = paper_dict.get("abstract", "")
    comments = paper_dict.get("comments", "")
    bibtex = paper_dict.get("bibtex", "")
    official_code_urls: list = paper_dict.get("official_code_urls", [])
    official_code_urls: list = [f"- [{url}]({url})" for url in official_code_urls]
    official_code_urls: str = "\n".join(official_code_urls)
    pwc_page_url = paper_dict.get("pwc_page_url", "")
    if pwc_page_url:
        pwc_page_url = f"- [{pwc_page_url}]({pwc_page_url})"

    # markdown content text
    md_content = f"""
# {title}

[arXiv]({paper_url}), [PDF]({pdf_url})

## Authors

{authors}

## Abstract

{abstract}

## Comments

{comments}

## Source Code

Official Code

{official_code_urls}

Community Code

{pwc_page_url}

## Bibtex

```tex
{bibtex}
```

## Notes

Type your reading notes here...

"""
    if not note_path.is_file():
        with note_path.open(mode="w") as f:
            f.write(md_content)
    return


def dl_paper(identifier: str) -> None:
    """
    Entry point for dl-paper command

    Download paper only
    """
    try:
        download_dir: Path = get_local_paper_folder_path()
    except Exception as e:
        logger.exception(e)
        logger.error("Abort: Environment Variable Error")
        return

    try:
        if identifier and identifier[0].isdigit():
            tmp_paper_dict = process_paper_id(identifier)
        else:
            tmp_paper_dict = process_url(identifier)
    except Exception as err:
        logger.error(f"Abort: Error while processing paper identifier: {identifier}")
        return

    # verify expected keys are present
    for key in ("paper_id", "paper_url", "pdf_url", "src_website"):
        if not key in tmp_paper_dict:
            logger.error(
                f"Abort: Error while processing paper identifier: {identifier}"
            )
            return

    # start scraping from source website
    src_website = tmp_paper_dict.get("src_website")
    if src_website == "arxiv":
        try:
            paper_dict = get_paper_from_arxiv(tmp_paper_dict)
        except Exception as err:
            logger.error(err)
            logger.error("Abort: Error while getting paper")
            return
    else:
        logger.error(f"Invalid source website: '{src_website}'")
        return

    # adjust logging level
    logger.setLevel(logging.DEBUG)

    # construct filename
    paper_title = paper_dict.get("title", "")
    paper_id = paper_dict.get("paper_id", "").strip()
    paper_title = paper_title.strip().replace(" ", "_")
    filepath = download_dir / f"{paper_id}_{paper_title}.pdf"
    paper_dict["filepath"] = str(filepath)

    # download paper
    try:
        download_pdf(paper_dict)
    except Exception as err:
        logger.error("Error while downloading paper")
        return


def add_paper(identifier: str) -> None:
    """
    Entry point for add-paper command

    Download paper and extract paper metadata
    """
    try:
        download_dir: Path = get_local_paper_folder_path()
    except Exception as e:
        logger.exception(e)
        logger.error("Abort: Environment Variable Error")
        return

    try:
        if identifier and identifier[0].isdigit():
            tmp_paper_dict = process_paper_id(identifier)
        else:
            tmp_paper_dict = process_url(identifier)
    except Exception as err:
        logger.error(f"Abort: Error while processing paper identifier: {identifier}")
        return

    # verify expected keys are present
    for key in ("paper_id", "paper_url", "pdf_url", "src_website"):
        if not key in tmp_paper_dict:
            logger.error(
                f"Abort: Error while processing paper identifier: {identifier}"
            )
            return

    # start scraping from source website
    src_website = tmp_paper_dict.get("src_website")
    if src_website == "arxiv":
        try:
            paper_dict = get_paper_from_arxiv(tmp_paper_dict)
        except Exception as err:
            logger.error(err)
            logger.error("Abort: Error while getting paper")
            return
    else:
        logger.error(f"Invalid source website: '{src_website}'")
        return

    # adjust logging level
    logger.setLevel(logging.DEBUG)

    # construct filename
    paper_title = paper_dict.get("title", "")
    paper_id = paper_dict.get("paper_id", "").strip()
    paper_title = paper_title.strip().replace(" ", "_")
    filepath = download_dir / f"{paper_id}_{paper_title}.pdf"
    paper_dict["filepath"] = str(filepath)

    # download paper
    try:
        download_pdf(paper_dict)
    except Exception as err:
        logger.error("Error while downloading paper")
        return

    # update paper list
    try:
        add_to_paper_list(download_dir, paper_dict)
    except Exception as err:
        logger.warning("Error while updating paper list")
        return

    # Create paper notes
    try:
        create_paper_note(download_dir, paper_dict)
    except Exception as err:
        logger.warning("Error while creating note")
        return


if __name__ == "__main__":
    add_paper("1506.01497")
    add_paper("https://arxiv.org/abs/1506.01497")
