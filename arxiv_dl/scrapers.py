import json
import logging

import requests
from bs4 import BeautifulSoup

from .helpers import normalize_paper_title
from .logger import logger
from .models import PaperData


def scrape_metadata_arxiv(paper_data: PaperData) -> None:
    logger.setLevel(logging.DEBUG)
    logger.debug("[Processing] Retrieving paper metadata")
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


def scrape_metadata_cvf(paper_data: PaperData) -> None:
    logger.setLevel(logging.DEBUG)
    logger.debug("[Processing] Retrieving paper metadata from CVF")
    logger.setLevel(logging.WARNING)

    response = requests.get(paper_data.abs_url)
    if response.status_code != 200:
        logger.error(f"Cannot connect to {paper_data.abs_url}")
        raise Exception(f"Cannot connect to {paper_data.abs_url}")
    # make soup
    soup = BeautifulSoup(response.text, "html.parser")

    # get TITLE
    result = soup.find("div", id="papertitle")
    tmp = [i.string.strip() for i in result if i.string]
    paper_title = tmp[0].strip()  # NOTE: hardcoded
    paper_data.title = paper_title
    # print(paper_title)

    # get AUTHORS
    result = soup.find("div", id="authors")
    tmp = [i.string.strip() for i in result if i.string]
    authors_str = tmp[1].strip()  # NOTE: hardcoded
    authors_list = [x.strip() for x in authors_str.split(",") if x]
    paper_data.authors = authors_list
    # print(authors_list)

    # get ABSTRACT
    result = soup.find("div", id="abstract")
    tmp = [i.string.strip() for i in result if i.string]
    paper_abstract = "".join(tmp)
    paper_data.abstract = paper_abstract.strip()
    # print(paper_abstract)

    # get BIBTEX
    result = soup.find("div", class_="bibref")
    tmp = [i.string.strip() for i in result if i.string]
    bibtex = "".join(tmp)
    paper_data.bibtex = bibtex.strip()
    # print(bibtex)

    # NOTE: this doesn't work cuz it's a relative path and the path construction is different every year
    # get pdf link
    # result = soup.find_all("a", string="pdf")
    # if len(result) == 1:
    #     pdf_url = result[0].get("href")
    #     paper_data.pdf_url = f"https://openaccess.thecvf.com{pdf_url.strip()}"

    # get supplementary path
    result = soup.find_all("a", string="supp")
    if len(result) == 1:
        supp_url = result[0].get("href")
        paper_data.supp_url = f"{supp_url.strip()}"

    return None


def scrape_metadata_nips(paper_data: PaperData) -> None:
    # TODO
    ...


def scrape_metadata_openreview(paper_data: PaperData) -> None:
    # TODO
    ...


if __name__ == "__main__":
    ...
