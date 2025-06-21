# https://arxiv.org/help/api/user-manual

import argparse
import json
from pathlib import Path
from typing import Union

from .helpers import (
    add_to_paper_list,
    create_paper_note,
    download_pdf,
    get_download_dest,
)
from .models import PaperData
from .printer import console
from .scrapers import scrape_metadata
from .target_parser import parse_target, valid_arxiv_id
from .updater import check_update


def download_paper(
    target: str,
    verbose: bool = False,
    download_dir: Union[Path, str, None] = None,
    n_threads: int = 5,
    pdf_only: bool = False,
    set_verbose_level: Union[str, int, None] = None,
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
    if set_verbose_level is not None:
        console.set_verbose_level(set_verbose_level)
    elif verbose:
        console.set_verbose_level("verbose")
    else:
        console.set_verbose_level("default")

    ### Get Target Download Directory
    try:
        if download_dir is None:
            download_dir: Path = get_download_dest()
        else:
            download_dir: Path = Path(download_dir).resolve()
            download_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.error(
            "Failed to set up download directory. Please check your environment configuration."
        )
        return False

    ### Filter Invalid Target String
    if not target or not isinstance(target, str):
        console.error("Invalid input: Please provide a valid paper URL or arXiv ID.")
        return False

    if (
        not target.startswith(("http://", "https://", "www."))
        and not valid_arxiv_id(target)
        and "arxiv" not in target.lower()
    ):
        console.error(
            f"Invalid input: '{target}' is not a recognized paper URL or arXiv ID.\n"
            "Please provide a valid URL from ArXiv, CVF, ECVA, or other supported sources, "
            "or a valid arXiv ID (e.g., '1512.03385')."
        )
        return False

    ### Identify Paper Source/Venues
    paper_data: PaperData = parse_target(target)

    # start scraping from source website
    scrape_metadata(paper_data)
    console.print_paper_info(paper_data)

    # download paper
    try:
        if paper_data.pdf_url:
            download_pdf(
                paper_data, download_dir=download_dir, parallel_connections=n_threads
            )
        else:
            console.warn("PDF download link not available for this paper.")
    except Exception as err:
        console.error("Failed to download the paper.")
        return False

    # update paper list
    try:
        add_to_paper_list(paper_data, download_dir=download_dir)
    except Exception as err:
        console.warn(
            "Could not update the paper tracking list, but the download completed successfully."
        )
        return False

    # Create paper notes
    try:
        if not pdf_only:
            create_paper_note(paper_data, download_dir=download_dir)
    except Exception as err:
        console.warn(
            "Could not create paper notes, but the PDF was downloaded successfully."
        )
        return False

    return True


def cli():
    parser = argparse.ArgumentParser(
        description="Download research papers from arxiv.org, CVF, ECVA, and other academic sources.",
        epilog="Examples:\n"
        "  paper 1512.03385                        # Download by arXiv ID\n"
        "  paper https://arxiv.org/abs/1512.03385  # Download by URL\n"
        "  paper 1512.03385 2103.15538             # Download multiple papers\n"
        "  paper 1512.03385 -d ~/Papers            # Specify download directory\n"
        "  paper 1512.03385 -p                     # Download PDF only (no notes)",
        formatter_class=argparse.RawTextHelpFormatter,
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
        console.process(i, len(urls), url)
        try:
            download_paper(
                target=url,
                verbose=args.verbose,
                download_dir=args.download_dir,
                n_threads=args.n_threads,
                pdf_only=args.pdf_only,
            )
        except Exception as e:
            console.error(f"Error processing '{url}': {e}")

        print()


if __name__ == "__main__":
    cli()
