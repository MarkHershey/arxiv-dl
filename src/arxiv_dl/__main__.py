# https://arxiv.org/help/api/user-manual

import argparse
import json
from pathlib import Path
from typing import Optional, Union

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


def set_verbosity(
    verbose: Optional[bool] = None,
    verbose_level: Optional[Union[str, int]] = None,
):
    """
    Note that console.set_verbose_level() will never throw an error by design, it will fallback to the default level if any error occurs.
    """
    if verbose_level is not None:
        console.set_verbose_level(verbose_level)
    elif verbose is True:
        console.set_verbose_level("verbose")
    else:
        console.set_verbose_level("default")


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
    set_verbosity(verbose=verbose, verbose_level=set_verbose_level)

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
        "targets",
        nargs="+",
        type=str,
        metavar="TARGET",
        help="Paper URL(s) or arXiv ID(s) to download",
    )

    # Create argument groups for better organization
    output_group = parser.add_argument_group(
        title="Output Options", description="Control where and how files are saved"
    )
    behavior_group = parser.add_argument_group(
        title="Behavior Options", description="Control download behavior and verbosity"
    )
    performance_group = parser.add_argument_group(
        title="Performance Options", description="Tune download performance settings"
    )

    # Output options
    output_group.add_argument(
        "-d",
        "--download_dir",
        metavar="DIR",
        type=str,
        help="Directory to save downloaded papers (default: ~/Downloads/ArXiv_Papers)",
    )
    output_group.add_argument(
        "-p",
        "--pdf_only",
        action="store_true",
        help="Download PDF only, skip creating Markdown notes and metadata files",
    )

    # Behavior options with mutually exclusive verbose arguments
    verbose_group = behavior_group.add_mutually_exclusive_group()
    verbose_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output with detailed information about papers and download process",
    )
    verbose_group.add_argument(
        "-vl",
        "--verbose_level",
        metavar="LEVEL",
        type=str,
        choices=["silent", "minimal", "default", "verbose"],
        help="Set verbosity level: silent (no output), minimal (errors only), default (standard info), verbose (all details)",
    )
    behavior_group.add_argument(
        "--no-update-check",
        action="store_true",
        help="Skip checking for package updates",
    )

    # Performance options
    performance_group.add_argument(
        "-n",
        "--n_threads",
        metavar="N",
        type=int,
        default=5,
        help="Number of parallel connections for faster downloads (default: 5, max: 16)",
    )

    args = parser.parse_args()

    # Set verbose level
    # NOTE: setting verbose level here is necessary because it controls the check_update() & console.process() below
    set_verbosity(verbose=args.verbose, verbose_level=args.verbose_level)

    # Check for updates (unless disabled)
    if not args.no_update_check and console.verbose_level >= 2:
        check_update()

    # Initialize variables
    targets = args.targets
    success_list = []
    exit_code = 0

    for i, target in enumerate(targets):
        # Log the current target
        console.process(i, len(targets), target)
        # Process current target
        try:
            success = download_paper(
                target=target,
                verbose=args.verbose,
                download_dir=args.download_dir,
                n_threads=args.n_threads,
                pdf_only=args.pdf_only,
                set_verbose_level=args.verbose_level,
            )
            print(success)
            success_list.append(success)
        except KeyboardInterrupt:
            # catch keyboard interrupt and exit with code 1
            console.error("arxiv-dl was interrupted by user")
            exit_code = 1
            break
        except Exception as e:
            # catch any unexpected errors and continue with the next target
            console.error(f"Error processing '{target}': {e}")
            exit_code = 1
        finally:
            # Add spacing between downloads
            if i < len(targets) - 1:
                print()

    # if any download failed, exit with code 1
    if False in success_list:
        exit_code = 1

    # exit with the appropriate code
    exit(exit_code)


if __name__ == "__main__":
    cli()
