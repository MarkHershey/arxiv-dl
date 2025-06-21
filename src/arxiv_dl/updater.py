import importlib.metadata
import json

import requests

from .printer import console


def check_latest_version():
    """Check the latest version of arxiv-dl on PyPI."""
    pypi_url = "https://pypi.org/pypi/arxiv-dl/json"
    try:
        response = requests.get(pypi_url)
    except requests.exceptions.ConnectionError:
        return ""
    except Exception as e:
        return ""

    if response.status_code == 200:
        pypi_data = response.text
        pypi_data = json.loads(pypi_data)
        latest_version = pypi_data.get("info", {}).get("version", "")
    else:
        latest_version = ""
    return latest_version


def check_current_version():
    """Check the current version of arxiv-dl."""
    current_version = importlib.metadata.version("arxiv-dl")
    return current_version


def check_update():
    """Remind user to update arxiv-dl if there is a new version."""
    latest_version = check_latest_version()
    current_version = check_current_version()
    console.print(f"[dim]\[arxiv-dl] (version: {current_version})")

    if latest_version and latest_version != current_version:
        console.print(
            f"[yellow]\[arxiv-dl] latest version available: {latest_version}. You may update by running: pip3 install -U arxiv-dl"
        )

    print()


if __name__ == "__main__":
    check_update()
