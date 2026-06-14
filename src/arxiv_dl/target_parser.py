import re
from datetime import datetime
from typing import List
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .models import PaperData
from .printer import console

###############################################################################
### General

HUGGINGFACE_PAPERS_URL = "https://huggingface.co/papers"
HUGGINGFACE_REQUEST_TIMEOUT = 10
HUGGINGFACE_RESERVED_PATHS = {
    "api",
    "blog",
    "chat",
    "collections",
    "datasets",
    "docs",
    "enterprise",
    "inference",
    "join",
    "languages",
    "learn",
    "login",
    "models",
    "new",
    "organizations",
    "papers",
    "posts",
    "pricing",
    "settings",
    "spaces",
    "support",
    "tasks",
}


def parse_target(target: str) -> PaperData:
    """
    Parse the target URL and return the corresponding PaperData object.

    Args:
        target: URL of the paper or ArXiv ID.

    Returns:
        PaperData object containing the paper metadata.
    """
    if "arxiv" in target.lower() or valid_arxiv_id(target):
        return process_arxiv_target(target)
    elif "openaccess.thecvf.com" in target:
        return process_cvf_target(target)
    elif "ecva.net" in target:
        return process_ecva_target(target)
    elif "openreview.net" in target:
        return process_openreview_target(target)
    elif "proceedings.neurips.cc" in target or "papers.nips.cc" in target:
        return process_nips_target(target)
    elif is_huggingface_paper_url(target):
        return process_huggingface_target(target)
    elif target.endswith(".pdf"):
        # TODO
        ...
        # return process_pdf_target(target)
    else:
        console.error(f"Unknown target: {target}")
        return False


def expand_target(target: str) -> List[str]:
    """
    Expand a target into one or more single-paper targets.

    Hugging Face paper listing pages expose links to individual
    `/papers/{arxiv_id}` pages, which can be downloaded one by one. Other
    targets are returned unchanged.
    """
    if is_huggingface_papers_listing_url(target) or is_huggingface_collection_url(
        target
    ):
        return get_huggingface_paper_urls_from_listing(target)
    return [target]


###############################################################################
### ArXiv


def valid_arxiv_id(paper_id: str) -> bool:
    """
    Validate the arXiv ID according to official arXiv ID format.
    Supports both legacy (pre-2007) and modern (post-2007) arXiv IDs.

    Args: str
        paper_id: arXiv ID to be validated (e.g. '1901.01234', 'math.GT/0309136', 'hep-th/9901001')

    Returns: bool
        True if the arXiv ID is valid. False otherwise.

    Ref: https://arxiv.org/help/arxiv_identifier
    """
    if not isinstance(paper_id, str):
        return False

    # Modern (post-2007) arXiv ID: YYMM.number or YYMM.numbervV
    modern_pattern = (
        r"^(?P<yy>[0-9]{2})(?P<mm>0[1-9]|1[0-2])\.(?P<num>[0-9]{4,5})(v[0-9]+)?$"
    )
    modern_match = re.fullmatch(modern_pattern, paper_id)
    if modern_match:
        yy = int(modern_match.group("yy"))
        mm = int(modern_match.group("mm"))
        num = modern_match.group("num")
        # Valid year/month for modern IDs: 0704 and later
        if yy < 7:
            return False
        if not (1 <= mm <= 12):
            return False
        # 4-digit sequence for 0704-1412, 5-digit for 1501+
        if yy < 15 or (yy == 14 and mm <= 12):
            if len(num) != 4:
                return False
        else:
            if len(num) != 5:
                return False
        return True

    # Legacy (pre-2007) arXiv ID: [archive][.subject_class]/YYMMNNN or NNNN
    # Example: math.GT/0309136, hep-th/9901001, math/0309136, cs/0701188
    legacy_pattern = r"^(?P<archive>[a-z\-]+)(\.[A-Z]{2})?/(?P<ym>[0-9]{4})(?P<seq>[0-9]{3,4})(v[0-9]+)?$"
    legacy_match = re.fullmatch(legacy_pattern, paper_id)
    if legacy_match:
        ym = legacy_match.group("ym")
        seq = legacy_match.group("seq")
        yy = int(ym[:2])
        mm = int(ym[2:])
        # Legacy IDs: 9107 (July 1991) through 0703 (March 2007)
        if not (91 <= yy <= 99 or 0 <= yy <= 7):
            return False
        if not (1 <= mm <= 12):
            return False
        if len(seq) not in (3, 4):
            return False
        return True

    return False


def get_arxiv_id_from_url(url: str) -> str:
    """
    Extract the arXiv ID from the given URL.

    Args:
        url: URL of the arXiv paper.

    Returns:
        arXiv ID of the paper (without version number to ensure latest version).

    Raises:
        Exception: If the URL is not a valid arXiv URL.
    """
    # Modern pattern: YYMM.number(vV)
    modern_pattern = r"[0-9]{2}(0[1-9]|1[0-2])\.[0-9]{4,5}(v[0-9]+)?"
    match = re.search(modern_pattern, url)
    if match:
        # Remove version number if present to get latest version
        arxiv_id = match[0]
        return re.sub(r"v[0-9]+$", "", arxiv_id)
    # Legacy pattern: [archive][.subject_class]/YYMMNNN or NNNN (optionally with vV)
    legacy_pattern = r"[a-z\-]+(\.[A-Z]{2})?/\d{6,7}(v[0-9]+)?"
    match = re.search(legacy_pattern, url)
    if match:
        # Remove version number if present to get latest version
        arxiv_id = match[0]
        return re.sub(r"v[0-9]+$", "", arxiv_id)
    raise Exception("Could not find arXiv ID in URL.")


def process_arxiv_target(target: str) -> PaperData:
    paper_id = get_arxiv_id_from_url(target)
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
### Hugging Face Papers


def normalize_url_for_parsing(target: str) -> str:
    target = target.strip()
    if target.startswith("//"):
        return f"https:{target}"
    if target.startswith(("www.", "huggingface.co/")):
        return f"https://{target}"
    return target


def is_huggingface_host(target: str) -> bool:
    parsed = urlparse(normalize_url_for_parsing(target))
    return parsed.netloc.lower() in {"huggingface.co", "www.huggingface.co"}


def get_huggingface_arxiv_id_from_url(url: str) -> str:
    """
    Extract the arXiv ID from a Hugging Face paper page URL.

    Hugging Face paper pages use `/papers/{arxiv_id}`, for example
    `https://huggingface.co/papers/2605.12357`.
    """
    if not is_huggingface_host(url):
        raise Exception("Unexpected Hugging Face URL.")

    parsed = urlparse(normalize_url_for_parsing(url))
    tokens = parsed.path.strip("/").split("/")
    if len(tokens) == 2 and tokens[0] == "papers" and valid_arxiv_id(tokens[1]):
        return re.sub(r"v[0-9]+$", "", tokens[1])

    raise Exception("Could not find arXiv ID in Hugging Face paper URL.")


def is_huggingface_paper_url(target: str) -> bool:
    try:
        get_huggingface_arxiv_id_from_url(target)
        return True
    except Exception:
        return False


def is_huggingface_papers_listing_url(target: str) -> bool:
    if not is_huggingface_host(target):
        return False

    parsed = urlparse(normalize_url_for_parsing(target))
    tokens = parsed.path.strip("/").split("/")

    if tokens == ["papers"]:
        return True

    if tokens == ["papers", "trending"]:
        return True

    if len(tokens) == 2 and tokens[1] == "papers":
        return tokens[0] not in HUGGINGFACE_RESERVED_PATHS

    if len(tokens) != 3 or tokens[0] != "papers":
        return False

    listing_kind, date_value = tokens[1], tokens[2]
    try:
        if listing_kind == "month":
            datetime.strptime(date_value, "%Y-%m")
            return True
        if listing_kind == "date":
            datetime.strptime(date_value, "%Y-%m-%d")
            return True
        if listing_kind == "week":
            datetime.strptime(f"{date_value}-1", "%G-W%V-%u")
            return re.fullmatch(r"[0-9]{4}-W[0-9]{2}", date_value) is not None
    except ValueError:
        return False

    return False


def is_huggingface_collection_url(target: str) -> bool:
    if not is_huggingface_host(target):
        return False

    parsed = urlparse(normalize_url_for_parsing(target))
    tokens = parsed.path.strip("/").split("/")
    return len(tokens) >= 3 and tokens[0] == "collections"


def process_huggingface_target(target: str) -> PaperData:
    paper_id = get_huggingface_arxiv_id_from_url(target)
    return process_arxiv_target(paper_id)


def get_huggingface_paper_urls_from_listing(target: str) -> List[str]:
    if not (
        is_huggingface_papers_listing_url(target)
        or is_huggingface_collection_url(target)
    ):
        raise Exception(f"Unexpected Hugging Face papers listing URL: {target}")

    target = normalize_url_for_parsing(target)
    response = requests.get(target, timeout=HUGGINGFACE_REQUEST_TIMEOUT)
    if response.status_code != 200:
        raise Exception(f"Cannot connect to {target}")

    soup = BeautifulSoup(response.text, "html.parser")
    paper_urls = []
    seen_paper_ids = set()
    for link in soup.find_all("a", href=True):
        url = urljoin(HUGGINGFACE_PAPERS_URL, link["href"])
        try:
            paper_id = get_huggingface_arxiv_id_from_url(url)
        except Exception:
            continue
        if paper_id not in seen_paper_ids:
            paper_urls.append(f"{HUGGINGFACE_PAPERS_URL}/{paper_id}")
            seen_paper_ids.add(paper_id)

    return paper_urls


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
    elif "ACCV" in _venue:
        paper_venue = "ACCV"
    else:
        raise Exception("Unexpected CVF URL.")

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
    pattern = (
        r"https?://[^/]*(?:proceedings\.neurips\.cc|papers\.nips\.cc)"
        r"/(?:paper_files/)?paper/(?P<year>[0-9]{4})/"
        r"(?P<kind>hash|file)/(?P<paper_id>[0-9a-fA-F]{32})-"
        r"(?P<doc_type>Abstract|Paper)(?P<suffix>[^/?#.]*)"
        r"\.(?P<ext>html|pdf)(?:[?#].*)?$"
    )
    match = re.match(pattern, target)
    if not match:
        raise Exception(f"Unexpected NeurIPS URL: {target}")

    year = int(match.group("year"))
    paper_id = match.group("paper_id").lower()
    doc_type = match.group("doc_type")
    suffix = match.group("suffix")
    ext = match.group("ext")

    if doc_type == "Abstract" and ext != "html":
        raise Exception(f"Unexpected NeurIPS URL: {target}")
    if doc_type == "Paper" and ext != "pdf":
        raise Exception(f"Unexpected NeurIPS URL: {target}")

    base_url = f"https://proceedings.neurips.cc/paper_files/paper/{year}"
    abs_url = f"{base_url}/hash/{paper_id}-Abstract{suffix}.html"
    pdf_url = f"{base_url}/file/{paper_id}-Paper{suffix}.pdf"
    paper_venue = "NeurIPS" if year >= 2018 else "NIPS"
    download_name = f"{year}_{paper_venue}_{paper_id}.pdf"

    return PaperData(
        paper_id=paper_id,
        abs_url=abs_url,
        pdf_url=pdf_url,
        year=year,
        src_website="NeurIPS",
        paper_venue=paper_venue,
        download_name=download_name,
    )


###############################################################################
### OpenReview


def process_openreview_target(target: str) -> PaperData:
    # TODO
    ...
