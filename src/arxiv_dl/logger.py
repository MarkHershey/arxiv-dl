import logging

import colorlog

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

_sh = colorlog.StreamHandler()
_sh.setLevel(logging.DEBUG)

_color_formatter = colorlog.ColoredFormatter(
    # fmt="%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s",
    fmt="%(log_color)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "green",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_yellow",
    },
    secondary_log_colors={},
    style="%",
)

_sh.setFormatter(_color_formatter)
logger.addHandler(_sh)
