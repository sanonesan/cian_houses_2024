from utils import CianHouseLinkExtractor, CianHousePageParser

import sys
import datetime

from loguru import logger

import configparser

if __name__ == "__main__":

    terminal_handler = {
        "sink": sys.stderr,
        "level": "INFO",
    }

    logfile_handler = {
        "sink": f"./logs/cianhouse_{datetime.datetime.now()}.log",
        "level": "INFO",
        "rotation": "250KB",
    }
    logger.configure(handlers=[terminal_handler, logfile_handler])

    try:
        logger.info("Reading CONFIG")
        config = configparser.ConfigParser()
        config.read("settings.ini")
        logger.success("CONFIG read")
    except Exception as e:
        logger.error(e)
        raise

    try:
        logger.info("Running LinkExtractor...")
        terminal_handler["level"] = "WARNING"
        logger.configure(handlers=[terminal_handler, logfile_handler])

        CianHouseLinkExtractor(
            start_url=config["Cian"]["URL"],
            count=int(config["Cian"]["PAGES_WITH_FLATS"]),
            csv_path=config["Cian"]["LINKS_TO_CHECK_PATH"],
            user_agent=config["Cian"]["USER_AGENT"],
        ).parse()

        terminal_handler["level"] = "INFO"
        logger.configure(handlers=[terminal_handler, logfile_handler])
        logger.success("Links Extracted")

    except Exception as e:
        logger.error(e)
        raise

    try:
        logger.info("Running PageParser...")
        terminal_handler["level"] = "WARNING"
        logger.configure(handlers=[terminal_handler, logfile_handler])

        CianHousePageParser(
            links_path=config["Cian"]["LINKS_TO_CHECK_PATH"],
            cian_houses_path=config["Cian"]["CIAN_HOUSES_PATH"],
        ).parse()

        terminal_handler["level"] = "INFO"
        logger.configure(handlers=[terminal_handler, logfile_handler])
        logger.success("Links Parsed")
    except Exception as e:
        logger.error(e)
        raise
