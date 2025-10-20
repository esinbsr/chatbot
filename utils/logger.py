"""Simple logging helper shared across the project."""

from __future__ import annotations

import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def _build_handler(handler: logging.Handler) -> logging.Handler:
    handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))
    handler.setLevel(logging.INFO)
    return handler


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger writing both to stdout and logs/app.log."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.addHandler(_build_handler(logging.FileHandler(LOG_FILE, encoding="utf-8")))
    logger.addHandler(_build_handler(logging.StreamHandler()))
    logger.propagate = False
    return logger


__all__ = ["get_logger"]

