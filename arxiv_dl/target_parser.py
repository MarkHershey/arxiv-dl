import re
from pathlib import Path
from typing import Union

from .logger import logger
from .models import PaperData

###############################################################################
### General


def parse_target(target: str) -> PaperData:
    """
    Parse the target URL and return the corresponding PaperData object.

    Args:
        target: URL of the paper or ArXiv ID.

    Returns:
        PaperData object containing the paper metadata.
    """
    if target[0].isdigit() or "arxiv.org" in target:
        return process_arxiv_target(target)
    elif "openaccess.thecvf.com" in target:
        return process_cvf_target(target)
    elif "ecva.net" in target:
        return process_ecva_target(target)
    elif "openreview.net" in target:
        return process_openreview_target(target)
    elif "nips.cc" in target:
        return process_nips_target(target)
    elif target.endswith(".pdf"):
        # TODO
        ...
        # return process_pdf_target(target)
    else:
        logger.error(f"[Abort] Unknown target: {target}")
        return False


###############################################################################
### ArXiv


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
### CVF (CVPR, ICCV, WACV)


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
### ECVA (ECCV)


def process_ecva_target(target: str) -> PaperData:
    # https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/6863_ECCV_2024_paper.php
    # https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06863.pdf
    assert "www.ecva.net" in target
    paper_data = PaperData(
        src_website="ECVA",
        paper_venue="ECCV",
    )

    tokens = target.split("/")
    _start = tokens.index("www.ecva.net")
    tokens = tokens[_start:]
    """
    0 www.ecva.net
    1 papers
    2 eccv_2024
    3 papers_ECCV
    4 html / papers
    5 xxxxxxxxxxxx.php
    """
    year = int(tokens[2].split("_")[1])
    paper_data.year = year

    if tokens[4] == "html" and year >= 2024:
        assert tokens[5].endswith(".php")
        paper_id: str = tokens[5].split("_")[0]
        # pad paper_id with zeros
        paper_id: str = paper_id.zfill(5)
        paper_data.paper_id = paper_id
        paper_data.abs_url = target
        paper_data.pdf_url = (
            f"https://www.ecva.net/papers/eccv_{year}/papers_ECCV/papers/{paper_id}.pdf"
        )
    elif tokens[4] == "html" and year == 2018:
        assert tokens[5].endswith(".php")
        paper_id: str = tokens[5][:-4]  # remove ".php"
        paper_data.paper_id = paper_id
        paper_data.abs_url = target
        paper_data.pdf_url = (
            f"https://www.ecva.net/papers/eccv_{year}/papers_ECCV/papers/{paper_id}.pdf"
        )
    elif tokens[4] == "html" and year <= 2022:
        assert tokens[5].endswith(".php")
        paper_id: str = tokens[5].split("_")[0]
        # pad paper_id with zeros
        paper_id: str = paper_id.zfill(5)
        paper_data.paper_id = paper_id
        paper_data.abs_url = target
        # unable to infer pdf_url from abs_url for ECCV 2022 and 2020
    elif tokens[4] == "papers" and year >= 2024:
        assert tokens[5].endswith(".pdf")
        paper_id: str = tokens[5].split(".")[0]
        paper_data.paper_id = paper_id
        # remove leading zeros
        paper_id: str = paper_id.lstrip("0")
        paper_data.abs_url = f"https://www.ecva.net/papers/eccv_{year}/papers_ECCV/html/{paper_id}_ECCV_2024_paper.php"
        paper_data.pdf_url = target
    elif tokens[4] == "papers" and year <= 2022:
        paper_data.pdf_url = target
        print(f"Currently unable to infer abs_url from pdf_url for ECCV {year}")
    else:
        raise Exception("Unexpected ECVA URL: {target}")

    return paper_data


###############################################################################
### NeurIPS


def process_nips_target(target: str) -> PaperData:
    # TODO
    ...


###############################################################################
### OpenReview


def process_openreview_target(target: str) -> PaperData:
    # TODO
    ...
