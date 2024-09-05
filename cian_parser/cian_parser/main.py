from loguru import logger
from utils import CianHouseLinkExtractor, CianHousePageParser


if __name__ == "__main__":

    import configparser

    config = configparser.ConfigParser()
    config.read("settings.ini")

    # CianHouseLinkExtractor(
    #     start_url=config["Cian"]["URL"],
    #     count=int(config["Cian"]["PAGES_WITH_FLATS"]),
    #     csv_path=config["Cian"]["LINKS_TO_CHECK_PATH"],
    #     user_agent=config["Cian"]["USER_AGENT"],
    # ).parse()

    CianHousePageParser(
        links_path=config["Cian"]["LINKS_TO_CHECK_PATH"],
        cian_houses_path=config["Cian"]["CIAN_HOUSES_PATH"],
    ).parse()
