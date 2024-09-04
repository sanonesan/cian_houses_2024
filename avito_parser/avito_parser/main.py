import undetected_chromedriver as uc

from seleniumbase import SB
from locator import LocatorCianMain
from house import House

# import time

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd


class CianHousesLinkExtractor:

    def __init__(
        self,
        start_url: str,
        count: int = 100,
        csv_path="links_to_check.csv",
    ) -> None:

        self.url = start_url
        self.count = count
        self.csv_path = csv_path

        file = open(self.csv_path, "w")
        file.write("links,\n")
        file.close()

        pass

    def __set_up(self):
        options = Options()
        custom_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        # add the custom User Agent to Chrome Options
        options.add_argument(f"--user-agent={custom_user_agent}")
        options.add_argument("--headless")
        self.driver = uc.Chrome(options=options)

    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        """Method for searching next page"""

        try:

            while self.count > 0:

                self.__parse_page()

                # Search for pagination buttons
                paginators = self.driver.find_element(*LocatorCianMain.PAGINATION_BTNS)

                # Search for element with LINK_TEXT "Дальше"
                # If no element with such atribute -> Exception
                next_page = paginators.find_element(
                    *LocatorCianMain.NEXT_BTN
                ).get_attribute("href")

                self.driver.get(url=next_page)
                print(next_page)
                # self.driver.sleep(0.5)

                self.count -= 1
                # time.sleep(1)

        except Exception as error:
            print(error)

        finally:
            print("STOP")

        pass

    def __parse_page(self):

        print("PARSING PAGE")
        titles = self.driver.find_elements(*LocatorCianMain.TITLES)

        file = open(self.csv_path, "a")

        for title in titles:
            url = (
                title.find_element(
                    By.CSS_SELECTOR,
                    '[data-name="LinkArea"]',
                )
                .find_element(By.CSS_SELECTOR, '[target="_blank"]')
                .get_attribute("href")
            )
            file.write(url + ",\n")
        file.close()

        pass

    def parse(self):

        self.__set_up()
        self.__get_url()
        self.__paginator()


class CianHousesParser:

    def __init__(self, links_path) -> None:

        self.links = pd.read_csv(links_path)["links"].tolist()
        # print(self.links)

        pass

    def __selector(self, element: str):
        if element == "Тип жилья":
            return "accomodation_type"
        elif element == "Общая площадь":
            return "square"
        elif element == "Жилая площадь":
            return "living_square"
        elif element == "Площадь кухни":
            return "kitchen_square"
        elif element == "Высота потолков":
            return "ceiling_height"
        elif element == "Ремонт" or element == "Отделка":
            return "renovation"
        elif element == "Этаж":
            return "floor"
        elif element == "Год постройки" or element == "Год сдачи":
            return "year"
        elif element == "Вид из окон":
            return "view"
        else:
            return False

    def __parse_link(self, url):

        self.driver.get(url)
        # name = self.driver.find_element(
        #     By.CSS_SELECTOR, '[data-name="OfferTitleNew"]'
        # ).text

        house = {
            "price": "unknown",
            "adress": "unknown",
            "metro": "unknown",
            "floor": "unknown",
            "square": "unknown",
            "living_square": "unknown",
            "kitchen_square": "unknown",
            "year": "unknown",
            "renovation": "unknown",
            "ceiling_height": "unknown",
            "view": "unknown",
            "accomodation_type": "unknown",
        }

        elems = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-name="ObjectFactoidsItem"]'
        )
        for i in range(len(elems)):
            element = str(elems[i].text).split(sep="\n")
            if self.__selector(element[0]):
                house[self.__selector(element[0])] = element[1]

        elems = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-name="OfferSummaryInfoItem"]'
        )

        for i in range(len(elems)):
            element = str(elems[i].text).split(sep="\n")
            if self.__selector(element[0]):
                if house[self.__selector(element[0])] == "unknown":
                    house[self.__selector(element[0])] = element[1]

        print(house)

        # print(name)

        pass

    def parse(self):
        with SB(
            uc=True,
            agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            headed=False,
            headless=True,
            page_load_strategy="eager",
            block_images=True,
            skip_js_waits=True,
        ) as self.driver:
            try:
                for url in self.links:
                    self.__parse_link(url)

            except Exception as error:
                print(error)
        pass


if __name__ == "__main__":

    # CianHousesLinkExtractor(
    #     start_url="https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=-1",
    #     count=1,
    #     csv_path="links_to_check.csv",
    # ).parse()

    CianHousesParser(links_path="links_to_check.csv").parse()

    # import configparser
    # config = configparser.ConfigParser()
    # config.read("settings.ini")
    #
    # print(config["Avito"]["URL"])
    #
    # while True:
    #     AvitoParser(
    #         url=config["Avito"]["URL"],
    #         count=1,
    #     ).parse()
