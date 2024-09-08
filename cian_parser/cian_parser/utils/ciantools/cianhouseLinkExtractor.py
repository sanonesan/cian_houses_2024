from .cianhouseLocator import CianHouseLocator

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from tqdm import tqdm
import time
from typing import Optional

from loguru import logger


__all__ = ["CianHouseLinkExtractor"]


class CianHouseLinkExtractor:

    def __init__(
        self,
        start_url: str,
        count: int,
        csv_path: str,
        user_agent: Optional[str] = None,
    ) -> None:

        self.url = start_url
        self.count = count
        self.csv_path = csv_path
        self.user_agent = user_agent

        file = open(self.csv_path, "w")
        file.write("links\n")
        file.close()

        pass

    def __paginator(self):
        """Method for searching next page"""

        self.driver.get(self.url)

        next_page = "NO URL"

        pbar = tqdm(range(1, self.count + 1))
        for _ in range(self.count):

            try:
                self.__parse_page()
                logger.success(f"Page {self.driver.current_url} parsed")
                pbar.update(1)

                except_counter = 0
                while True:

                    try:
                        # Search for pagination buttons
                        paginators = self.driver.find_element(
                            *CianHouseLocator.PAGINATION_BTNS
                        )
                        # Search for element with LINK_TEXT "Дальше"
                        # If no element with such atribute -> Exception
                        next_page = paginators.find_element(
                            *CianHouseLocator.NEXT_BTN
                        ).get_attribute("href")
                        break
                    except Exception as e:
                        if type(e) is NoSuchElementException:
                            except_counter += 1
                        else:
                            logger.critical(type(e))
                        self.driver.refresh()
                        logger.info("NoSuchElementException trying to refresh page")
                        time.sleep(0.25)

                        if except_counter == 2:
                            raise e
                        pass

                self.driver.get(url=next_page)
                time.sleep(0.25)
                # time.sleep(1)

            except Exception as e:
                if type(e) is NoSuchElementException:
                    msg = f"""
                    \bIt was the last page OR cannot find NETX_BUTTON element!
                    \bLast visited URL: {self.driver.current_url}!
                    """
                    logger.warning(msg)
                    break
                else:
                    logger.error(e)
                    raise

        pass

    def __parse_page(self):

        try:
            titles = self.driver.find_elements(*CianHouseLocator.TITLES)

            file = open(self.csv_path, "a")

            for title in titles:
                url = (
                    title.find_element(*CianHouseLocator.DESCRIPTION_FRAME)
                    .find_element(*CianHouseLocator.URL)
                    .get_attribute("href")
                )
                file.write(url + "\n")
            file.close()
        except Exception as e:
            logger.error(e)
            raise

        pass

    def __set_up_Driver(self):
        options = Options()

        if self.user_agent is not None:
            # add the custom User Agent to Chrome Options
            options.add_argument(f"--user-agent={self.user_agent}")
        options.add_argument("--headless")

        self.driver = uc.Chrome(options=options)

        pass

    def parse(self):
        try:
            logger.trace("Start extracting links")
            self.__set_up_Driver()
            self.__paginator()
            logger.success("Links EXTRACTED")
        except Exception as e:
            logger.error(e)
            raise
