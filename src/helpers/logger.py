import logging
from helpers.config import config

class Logger:
    def __init__(self):
        level = "INFO"
        if config.get("CB_LOGLEVEL"):
            level = config.get("CB_LOGLEVEL")

        logging.basicConfig(
            handlers=[
                logging.FileHandler("combahton.log"),
                logging.StreamHandler(),
            ],
            level=level,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )

    def getLogger(self):
        return logging