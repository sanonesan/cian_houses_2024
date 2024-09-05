from .cianhouseLocator import CianHouseLocator

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

from tqdm import tqdm
import time
from typing import Optional


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

    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        """Method for searching next page"""

        try:

            for _ in tqdm(range(self.count)):

                self.__parse_page()

                # Search for pagination buttons
                paginators = self.driver.find_element(*CianHouseLocator.PAGINATION_BTNS)

                # Search for element with LINK_TEXT "Дальше"
                # If no element with such atribute -> Exception
                next_page = paginators.find_element(
                    *CianHouseLocator.NEXT_BTN
                ).get_attribute("href")

                self.driver.get(url=next_page)
                time.sleep(0.25)
                # time.sleep(1)

        except Exception as error:
            print(error)

        pass

    def __parse_page(self):

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
            self.__set_up_Driver()
            self.__get_url()
            self.__paginator()
        except Exception as error:
            print(error)
