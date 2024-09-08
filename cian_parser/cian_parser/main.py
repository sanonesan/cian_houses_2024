from utils.ciantools import CianHouseLinkExtractor, CianHousePageParser

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

        for room in range(1, 6 + 1):

            logger.info(f"Extracting {room}-room flats")

            terminal_handler["level"] = "WARNING"
            logger.configure(handlers=[terminal_handler, logfile_handler])

            CianHouseLinkExtractor(
                start_url=config["Cian"][f"URL_{room}"],
                count=int(config["Cian"]["PAGES_WITH_FLATS"]),
                csv_path=config["Cian"]["LINKS_TO_CHECK_PATH"]
                + f"links_to_check_{room}.csv",
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

        for room in range(1, 6 + 1):

            logger.info(f"Parsing {room}-room flats")

            terminal_handler["level"] = "WARNING"
            logger.configure(handlers=[terminal_handler, logfile_handler])

            CianHousePageParser(
                links_path=config["Cian"]["LINKS_TO_CHECK_PATH"]
                + f"links_to_check_{room}.csv",
                cian_houses_path=config["Cian"]["CIAN_HOUSES_PATH"],
                cian_houses_file_name=f"cian_houses_{room}_flats",
                user_agent=config["Cian"]["USER_AGENT"],
            ).parse()

            terminal_handler["level"] = "INFO"
            logger.configure(handlers=[terminal_handler, logfile_handler])
            logger.success("Links Parsed")
    except Exception as e:
        logger.error(e)
        raise
