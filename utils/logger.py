import logging
from pathlib import Path

# Configure a single logger shared across the application.
LOG_FILE = Path("logs") / "app.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """Return an application logger configured with file and console handlers."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
