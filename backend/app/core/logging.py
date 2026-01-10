import logging
import sys

from app.core.settings import settings


def setup_logging():
    log_level = settings.LOG_LEVEL.upper()
    logger = logging.getLogger()
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    logger.debug("Logging is set up.")
