# https://arxiv.org/help/api/user-manual

import json
import logging
from pathlib import Path

from .helpers import (
    add_to_paper_list,
    create_paper_note,
    download_pdf,
    get_download_dest,
)
from .logger import logger
from .models import PaperData
from .scrapers import scrape_metadata
from .target_parser import parse_target


def main(
    target: str,
    verbose: bool = False,
    download_dir: Path = None,
    n_threads: int = 5,
    pdf_only: bool = False,
    *args,
    **kwargs,
) -> bool:
    """
    Entry point of the package's main functionality.
    This pipeline has three main steps:
        1. Process Target: Identify the source of the paper (ArXiv, CVF, NeurIPS, OpenReview, etc.)
        2. Scrape Metadata: Extract metadata from the source website
        3. Download Paper: Download the paper PDF file and save it to the target directory
    """

    ### Get Target Download Directory
    try:
        if download_dir is None:
            download_dir: Path = get_download_dest()
        else:
            download_dir: Path = Path(download_dir).resolve()
            download_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.exception(e)
        logger.error("[Abort] Environment Variable Error")
        return False

    ### Filter Invalid Target String
    if not target or not isinstance(target, str):
        logger.error("[Abort] Target is not specified correctly")
        return False

    if (
        not target.startswith(("http://", "https://", "www."))
        and not target[0].isdigit()
    ):
        logger.error(
            f"[Abort] Target should be a URL or an ArXiv ID. Unknown target: '{target}'"
        )
        return False

    ### Identify Paper Source/Venues
    paper_data: PaperData = parse_target(target)

    # start scraping from source website
    scrape_metadata(paper_data)

    # adjust logging level
    logger.setLevel(logging.DEBUG)
    if verbose:
        logger.debug(json.dumps(paper_data.dict(), indent=4))

    # download paper
    try:
        if paper_data.pdf_url:
            download_pdf(
                paper_data, download_dir=download_dir, parallel_connections=n_threads
            )
        else:
            # TODO: think how to handle this; maybe improve error message
            logger.warning("[Warn] No PDF URL found")
    except Exception as err:
        logger.exception(err)
        logger.error("[Abort] Error while downloading paper")
        return False

    # update paper list
    try:
        add_to_paper_list(paper_data, download_dir=download_dir)
    except Exception as err:
        logger.exception(err)
        logger.warning("[Warn] Error while updating paper list")
        return False

    # Create paper notes
    try:
        if not pdf_only:
            create_paper_note(paper_data, download_dir=download_dir)
    except Exception as err:
        logger.exception(err)
        logger.warning("[Warn] Error while creating note")
        return False

    return True


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    tmp_dir = root_dir / "tmp"
    tmp_dir.mkdir(exist_ok=True)

    from puts import timeitprint

    @timeitprint
    def test_performances():
        main("1506.01497", verbose=True, download_dir=tmp_dir)
        # main("https://arxiv.org/abs/1506.01497", verbose=True, download_dir=tmp_dir)

    test_performances()
