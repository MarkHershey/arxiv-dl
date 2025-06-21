# https://arxiv.org/help/api/user-manual

import argparse
import json
import logging
from pathlib import Path
from typing import Union

from .helpers import (
    add_to_paper_list,
    create_paper_note,
    download_pdf,
    get_download_dest,
)
from .logger import logger
from .models import PaperData
from .scrapers import scrape_metadata
from .target_parser import parse_target, valid_arxiv_id
from .updater import check_update


def download_paper(
    target: str,
    verbose: bool = False,
    download_dir: Union[Path, str, None] = None,
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
        logger.error(
            "❌ Failed to set up download directory. Please check your environment configuration."
        )
        return False

    ### Filter Invalid Target String
    if not target or not isinstance(target, str):
        logger.error("❌ Invalid input: Please provide a valid paper URL or arXiv ID.")
        return False

    if not target.startswith(("http://", "https://", "www.")) and not valid_arxiv_id(
        target
    ):
        logger.error(
            f"❌ Invalid input: '{target}' is not a recognized paper URL or arXiv ID.\n"
            "Please provide a valid URL from ArXiv, CVF, ECVA, or other supported sources, "
            "or a valid arXiv ID (e.g., '1512.03385')."
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
            logger.warning("⚠️  PDF download link not available for this paper.")
    except Exception as err:
        logger.exception(err)
        logger.error("❌ Failed to download the paper.")
        return False

    # update paper list
    try:
        add_to_paper_list(paper_data, download_dir=download_dir)
    except Exception as err:
        logger.exception(err)
        logger.warning(
            "⚠️  Could not update the paper tracking list, but the download completed successfully."
        )
        return False

    # Create paper notes
    try:
        if not pdf_only:
            create_paper_note(paper_data, download_dir=download_dir)
    except Exception as err:
        logger.exception(err)
        logger.warning(
            "⚠️  Could not create paper notes, but the PDF was downloaded successfully."
        )
        return False

    return True


def cli():
    parser = argparse.ArgumentParser(
        description="Download research papers from ArXiv, CVF, ECVA, and other academic sources.",
        epilog="Examples:\n"
        "  paper 1512.03385                    # Download by arXiv ID\n"
        "  paper https://arxiv.org/abs/1512.03385  # Download by URL\n"
        "  paper 1512.03385 2103.15538         # Download multiple papers\n"
        "  paper 1512.03385 -d ~/Papers        # Specify download directory\n"
        "  paper 1512.03385 -p                 # Download PDF only (no notes)",
    )
    parser.add_argument(
        "urls",
        nargs="+",
        type=str,
        help="Paper URL(s) or arXiv ID(s) to download",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed information about the paper and download process",
    )
    parser.add_argument(
        "-p",
        "--pdf_only",
        action="store_true",
        help="Download PDF only, skip creating Markdown notes",
    )
    parser.add_argument(
        "-d",
        "--download_dir",
        type=str,
        help="Directory to save downloaded papers (default: ~/Downloads/ArXiv_Papers)",
        required=False,
    )
    parser.add_argument(
        "-n",
        "--n_threads",
        type=int,
        help="Number of parallel connections for faster downloads (default: 5, max: 16)",
        required=False,
        default=5,
    )
    args = parser.parse_args()

    urls = args.urls

    check_update()

    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] >>> {url}")
        try:
            download_paper(
                target=url,
                verbose=args.verbose,
                download_dir=args.download_dir,
                n_threads=args.n_threads,
                pdf_only=args.pdf_only,
            )
        except Exception as e:
            print(f"❌ Error processing '{url}': {e}")

        print()


if __name__ == "__main__":
    cli()
