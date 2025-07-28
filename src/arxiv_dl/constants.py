from dataclasses import dataclass


@dataclass
class Constants:

    REPO_URL: str = "https://github.com/MarkHershey/arxiv-dl"
    BUG_REPORT_URL: str = "https://github.com/MarkHershey/arxiv-dl/issues"
    BUG_REPORT_MSG: str = (
        f"To report a bug or share feedback, please visit {BUG_REPORT_URL}"
    )


CONSTANTS = Constants()
