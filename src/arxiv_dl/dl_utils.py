"""
Download utilities for arxiv-dl.

This module provides utilities for downloading files with progress tracking,
filename detection, and file management.
"""

import os
import shutil
import tempfile
import urllib.parse as urlparse
from typing import Dict, List, Optional, Union

import requests
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from .printer import console

# =============================================================================
# Utility Functions
# =============================================================================


def bytes_to_mb(bytes_int: int) -> float:
    """Convert bytes to megabytes.

    Args:
        bytes_int: Number of bytes

    Returns:
        Size in megabytes as float
    """
    return bytes_int / 1024 / 1024


def bytes_to_mb_str(bytes_int: int) -> str:
    """Convert bytes to megabytes as formatted string.

    Args:
        bytes_int: Number of bytes

    Returns:
        Size in megabytes as formatted string (e.g., "1.23")
    """
    mb = bytes_to_mb(bytes_int)
    return f"{mb:.2f}"


# Alias
_b2ms = bytes_to_mb_str


# =============================================================================
# Filename Detection and Management
# =============================================================================


def filename_from_url(url: str) -> Optional[str]:
    """Extract filename from URL.

    Args:
        url: URL to extract filename from

    Returns:
        Detected filename or None if not found
    """
    fname = os.path.basename(urlparse.urlparse(url).path)
    if len(fname.strip(" \n\t.")) == 0:
        return None
    return fname


def filename_from_headers(
    headers: Union[str, List[str], Dict[str, str]],
) -> Optional[str]:
    """Detect filename from Content-Disposition headers.

    Reference: http://greenbytes.de/tech/tc2231/

    Args:
        headers: HTTP headers as dict, list, or string

    Returns:
        Filename from content-disposition header or None
    """
    # Normalize headers to dict
    if isinstance(headers, str):
        headers = headers.splitlines()
    if isinstance(headers, list):
        headers = dict([x.split(":", 1) for x in headers])

    cdisp = headers.get("Content-Disposition")
    if not cdisp:
        return None

    cdtype = cdisp.split(";")
    if len(cdtype) == 1:
        return None

    if cdtype[0].strip().lower() not in ("inline", "attachment"):
        return None

    # Find filename parameter
    fnames = [x for x in cdtype[1:] if x.strip().startswith("filename=")]
    if len(fnames) > 1:
        return None

    name = fnames[0].split("=")[1].strip(' \t"')
    name = os.path.basename(name)
    if not name:
        return None

    return name


def filename_fix_existing(filename: str) -> str:
    """Add numeric suffix to filename if it already exists.

    Args:
        filename: Original filename

    Returns:
        Filename with numeric suffix if needed (e.g., "file (1).pdf")
    """
    dirname = "."
    name, ext = filename.rsplit(".", 1)

    # Find existing files with same base name
    names = [x for x in os.listdir(dirname) if x.startswith(name)]
    names = [x.rsplit(".", 1)[0] for x in names]
    suffixes = [x.replace(name, "") for x in names]

    # Filter suffixes that match ' (x)' pattern
    suffixes = [x[2:-1] for x in suffixes if x.startswith(" (") and x.endswith(")")]
    indexes = [int(x) for x in suffixes if set(x) <= set("0123456789")]

    idx = 1
    if indexes:
        idx += sorted(indexes)[-1]

    return f"{name} ({idx}).{ext}"


def detect_filename(
    url: Optional[str] = None,
    out: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    default: str = "download.wget",
) -> str:
    """Determine filename for saving file.

    Priority order: out > headers > url > default

    Args:
        url: URL to extract filename from
        out: Explicit output filename
        headers: HTTP headers to extract filename from
        default: Default filename if none detected

    Returns:
        Determined filename
    """
    names = {"out": "", "url": "", "headers": ""}

    if out:
        names["out"] = out or ""
    if url:
        names["url"] = filename_from_url(url) or ""
    if headers:
        names["headers"] = filename_from_headers(headers) or ""

    return names["out"] or names["headers"] or names["url"] or default


# =============================================================================
# Download Functionality
# =============================================================================


def _create_progress_bar(transient: bool = False) -> Progress:
    """Create a rich progress bar for downloads.

    Returns:
        Configured Progress instance
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        "[progress.percentage]{task.percentage:>3.0f}%",
        BarColumn(),
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeElapsedColumn(),
        console=console.console,
        transient=transient,
    )


def _download_file_with_progress(
    url: str, tmpfile: str, progress: Progress, task_id: int
) -> Dict[str, str]:
    """Download file with progress tracking.

    Args:
        url: URL to download
        tmpfile: Temporary file path
        progress: Progress bar instance
        task_id: Progress task ID

    Returns:
        Response headers

    Raises:
        requests.RequestException: If download fails
    """
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        headers = response.headers

        # Get total size if available
        total_size = int(response.headers.get("content-length", 0))
        if total_size > 0:
            progress.update(task_id, total=total_size)

        # Download the file
        downloaded_size = 0
        with open(tmpfile, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    if total_size > 0:
                        progress.update(task_id, completed=downloaded_size)
                    else:
                        # Update description with downloaded size for unknown total
                        progress.update(
                            task_id,
                            description=f"[cyan]Downloading ({_b2ms(downloaded_size)} MB)",
                        )

    return headers


def download_with_rich(
    url: str, out: Optional[str] = None, transient: bool = False
) -> str:
    """Download URL with rich progress bar and automatic filename detection.

    Downloads URL into a temporary file and then renames it to a filename
    autodetected from either URL or HTTP headers. Uses rich progress bar
    for better user experience.

    Args:
        url: URL to download
        out: Output filename or directory

    Returns:
        Filename where URL was downloaded to

    Raises:
        requests.RequestException: If download fails
        OSError: If file operations fail
    """
    # Handle output directory
    outdir = None
    if out and os.path.isdir(out):
        outdir = out
        out = None

    # Create temporary file
    prefix = detect_filename(url, out)
    fd, tmpfile = tempfile.mkstemp(".tmp", prefix=prefix, dir=".")
    os.close(fd)
    os.unlink(tmpfile)

    # Download with progress
    progress = _create_progress_bar(transient=transient)
    headers = None

    try:
        with progress:
            task = progress.add_task(f"[cyan]Downloading", total=None)
            headers = _download_file_with_progress(url, tmpfile, progress, task)

    except Exception as e:
        console.error(f"Download failed: {str(e)}")
        if os.path.exists(tmpfile):
            os.unlink(tmpfile)
        raise

    # Determine final filename and move file
    filename = detect_filename(url, out, headers)
    if outdir:
        filename = os.path.join(outdir, filename)

    # Add numeric suffix if filename already exists
    if os.path.exists(filename):
        filename = filename_fix_existing(filename)

    # Move temp file to final location
    shutil.move(tmpfile, filename)

    return filename


def download(url: str, out: Optional[str] = None) -> str:
    """Download URL without progress bar.

    Downloads URL into a temporary file and then renames it to a filename
    autodetected from either URL or HTTP headers. No visual progress tracking.

    Args:
        url: URL to download
        out: Output filename or directory

    Returns:
        Filename where URL was downloaded to

    Raises:
        requests.RequestException: If download fails
        OSError: If file operations fail
    """
    # Handle output directory
    outdir = None
    if out and os.path.isdir(out):
        outdir = out
        out = None

    # Create temporary file
    prefix = detect_filename(url, out)
    fd, tmpfile = tempfile.mkstemp(".tmp", prefix=prefix, dir=".")
    os.close(fd)
    os.unlink(tmpfile)

    try:
        # Download file without progress tracking
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            headers = response.headers

            # Download the file
            with open(tmpfile, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

    except Exception as e:
        if os.path.exists(tmpfile):
            os.unlink(tmpfile)
        raise

    # Determine final filename and move file
    filename = detect_filename(url, out, headers)
    if outdir:
        filename = os.path.join(outdir, filename)

    # Add numeric suffix if filename already exists
    if os.path.exists(filename):
        filename = filename_fix_existing(filename)

    # Move temp file to final location
    shutil.move(tmpfile, filename)

    return filename
