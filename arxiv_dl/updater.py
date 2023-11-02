import json

import pkg_resources
import requests


def check_latest_version():
    """Check the latest version of arxiv-dl on PyPI."""
    pypi_url = "https://pypi.org/pypi/arxiv-dl/json"
    try:
        response = requests.get(pypi_url)
    except requests.exceptions.ConnectionError:
        return ""
    except Exception as e:
        # print(e)
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
    current_version = pkg_resources.get_distribution("arxiv-dl").version
    return current_version


def check_update():
    """Remind user to update arxiv-dl if there is a new version."""
    latest_version = check_latest_version()
    current_version = check_current_version()
    print(f"[arxiv-dl] (version: {current_version})")

    if latest_version and latest_version != current_version:
        print(
            f"[arxiv-dl] latest version available: {latest_version}. You may update by running: pip install --upgrade arxiv-dl\n"
        )


if __name__ == "__main__":
    check_update()
