import logging
import coloredlogs
from helpers.config import config

class Logger:
    """Provides access to file and stream logging"""
    def __init__(self):
        level = "INFO"
        if config.get("CB_LOGLEVEL"):
            level = config.get("CB_LOGLEVEL")

        logging.basicConfig(
            handlers=[
                logging.FileHandler("combahton.log"),
                logging.StreamHandler()
            ],
            level=level,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        coloredlogs.install(level=level)

    def get_logger(self):
        """Returns the created logger"""
        return logging
        