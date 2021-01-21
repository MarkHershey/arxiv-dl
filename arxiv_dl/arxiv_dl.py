# built-in modules
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple

# external modules
import requests
import colorlog
from bs4 import BeautifulSoup

DEFAULT_DOWNLOAD_PATH = Path.home() / "Downloads/ArXiv_Papers"

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

sh = colorlog.StreamHandler()
sh.setLevel(logging.DEBUG)

color_formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s %(black)s(%(filename)s:%(lineno)s)",
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

    if "arxiv.org/abs" in url:
        ## abstract page
        paper_id = get_paper_id_from_url(url)
        paper_url = url
        pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
        return paper_id, paper_url, pdf_url
    elif "arxiv.org/pdf" in url:
        ## pdf page
        paper_id = get_paper_id_from_url(url)
        paper_url = f"https://arxiv.org/abs/{paper_id}"
        pdf_url = url
        return paper_id, paper_url, pdf_url
    else:
        logger.error("Unexpected URL Error by arxiv URL Handler.")
        raise Exception("Unexpected URL Error by arxiv URL Handler.")


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


def get_paper_from_arxiv(tmp_paper_dict: Dict[str, str]) -> Dict[str, str]:
    paper_url = tmp_paper_dict.get("paper_url")
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
    logger.debug(f"Paper Title: {paper_title}")

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
    tmp_paper_dict["abstract"] = paper_abstract

    # get COMMENTS
    result = soup.find("td", class_="tablecell comments mathjax")
    if result:
        comments = [i.string.strip() if i.string else "" for i in result]
        comments = " ".join(comments)
    else:
        comments = ""
    tmp_paper_dict["comments"] = comments

    return tmp_paper_dict


def download_pdf(paper_dict: dict) -> None:
    filepath = Path(paper_dict.get("filepath"))
    if filepath.is_file():
        logger.debug(f"Paper PDF already exist at: {filepath}")
    else:
        response = requests.get(paper_dict.get("pdf_url"))
        with filepath.open(mode="wb") as f:
            f.write(response.content)
        logger.debug(f"Successfully downloaded at: {filepath}")
    return


def add_to_paper_list(download_dir: Path, paper_dict: dict) -> None:
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


def create_paper_note(download_dir: Path, paper_dict: dict) -> None:
    paper_id = paper_dict.get("paper_id", "").strip()
    note_path = Path(download_dir) / f"{paper_id}_Notes.md"
    paper_url = paper_dict.get("paper_url", "")
    pdf_url = paper_dict.get("pdf_url", "")
    title = paper_dict.get("title", "")
    authors: list = paper_dict.get("authors", [])
    authors: list = [f"- {name}" for name in authors]
    authors: str = "\n".join(authors)
    abstract = paper_dict.get("abstract", "")
    comments = paper_dict.get("comments", "")
    contnet = f"""
# {title}

[arXiv]({paper_url}), [PDF]({pdf_url})

## Authors

{authors}

## Abstract

{abstract}

## Comments

{comments}

## Code

- [None]()

## Notes

Type your reading notes here...

"""
    if not note_path.is_file():
        with note_path.open(mode="w") as f:
            f.write(contnet)
    return


def dl_paper(url: str) -> None:
    """
    Get a Paper dictionary from a supported URL
    """
    try:
        download_dir: Path = get_local_paper_folder_path()
    except Exception as e:
        logger.exception(e)
        logger.error("Abort: Environment Variable Error")
        return

    try:
        tmp_paper_dict = process_url(url)
    except Exception as err:
        logger.error(f"Abort: Error while processing URL: {url}")
        return

    # verify expected keys are present
    for key in ("paper_id", "paper_url", "pdf_url", "src_website"):
        if not key in tmp_paper_dict:
            logger.error(f"Abort: Error while processing URL: {url}")
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


def add_paper(url: str) -> None:
    """
    Get a Paper dictionary from a supported URL
    """
    try:
        download_dir: Path = get_local_paper_folder_path()
    except Exception as e:
        logger.exception(e)
        logger.error("Abort: Environment Variable Error")
        return

    try:
        tmp_paper_dict = process_url(url)
    except Exception as err:
        logger.error(f"Abort: Error while processing URL: {url}")
        return

    # verify expected keys are present
    for key in ("paper_id", "paper_url", "pdf_url", "src_website"):
        if not key in tmp_paper_dict:
            logger.error(f"Abort: Error while processing URL: {url}")
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
    add_paper("https://arxiv.org/pdf/2009.12547.pdf")
