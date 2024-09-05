import undetected_chromedriver as uc

from locator import LocatorCianMain
from house import CianHouse

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import bs4

from tqdm import tqdm
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
        print(self.links)

        pass

    def __parse_link(self, url):

        self.driver.get(url)
        # name = self.driver.find_element(
        #     By.CSS_SELECTOR, '[data-name="OfferTitleNew"]'
        # ).text

        house = CianHouse()
        # print(house)

        page_html = self.driver.page_source

        soup = bs4.BeautifulSoup(page_html, "html.parser")

        location = ""
        try:
            location_list = [x.text for x in soup.select("a[data-name=AddressItem]")]
            for i in range(len(location_list)):
                if i < len(location_list) - 1:
                    location = location + location_list[i] + ", "
                else:
                    location = location + location_list[i]
        except Exception as e:
            print(e)

        if location == "":
            location = "unknown"
        house["location"] = location

        metro = ""
        try:
            metro_list = [x.text for x in soup.select("li[data-name=UndergroundItem]")]
            metro = metro_list[0]
        except Exception as e:
            print(e)

        if metro == "":
            metro = "unknown"
        house["metro"] = house.re_metro(metro)

        #

        price = ""
        try:
            price_list = soup.select("div[data-testid=price-amount]")[0].text.split()[
                :-1
            ]
            for x in price_list:
                price = price + x
            price = int(price)
        except Exception as e:
            print(e)

        if price == "":
            price = "unknown"
        house["price"] = price

        try:
            soup_span = soup.select("span")
            for index, span in enumerate(soup_span):
                if house.selector(span.text):
                    house[house.selector(span.text)] = soup_span[index + 1].text
        except Exception as e:
            print(e)

        try:
            soup_p = soup.select("p")
            for index, p in enumerate(soup_p):
                if house.selector(p.text):
                    if house[house.selector(p.text)] == "unknown":
                        house[house.selector(p.text)] = soup_p[index + 1].text
        except Exception as e:
            print(e)

        if house["square"] != "unknown":
            house["square"] = house.re_square(house["square"])

        if house["living_square"] != "unknown":
            house["living_square"] = house.re_square(house["living_square"])

        if house["kitchen_square"] != "unknown":
            house["kitchen_square"] = house.re_square(house["kitchen_square"])

        if house["year"] != "unknown":
            house["year"] = house.re_year(house["year"])

        if house["floor"] != "unknown":
            house["floor"], house["floor_count"] = house.re_floor(house["floor"])

        if house["ceiling_height"] != "unknown":
            house["ceiling_height"] = house.re_ceiling(house["ceiling_height"])

        print(house)
        #
        # elems = self.driver.find_elements(By.CSS_SELECTOR, "span")
        # for index, span in enumerate(elems):
        #     print(index, span[index + 1].text)
        # elems = self.driver.find_elements(
        #     By.CSS_SELECTOR, '[data-name="ObjectFactoidsItem"]'
        # )
        # for i in range(len(elems)):
        #     element = str(elems[i].text).split(sep="\n")
        #     if self.__selector(element[0]):
        #         house[self.__selector(element[0])] = element[1]

        # elems = self.driver.find_elements(
        #     By.CSS_SELECTOR, '[data-name="OfferSummaryInfoItem"]'
        # )
        #
        # for i in range(len(elems)):
        #     element = str(elems[i].text).split(sep="\n")
        #     if self.__selector(element[0]):
        #         if house[self.__selector(element[0])] == "unknown":
        #             house[self.__selector(element[0])] = element[1]
        #
        # print(house)

        # print(name)

        pass

    def __set_up_Driver(self):
        self.driver = Driver(
            uc=True,
            agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            headless=True,
            page_load_strategy="eager",
            block_images=True,
        )
        pass

    def parse(self):
        # with SB(
        #     uc=True,
        #     agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        #     headed=False,
        #     headless=True,
        #     page_load_strategy="eager",
        #     block_images=True,
        #     skip_js_waits=True,
        # ) as self.driver:
        try:
            self.__set_up_Driver()
            for url in tqdm(self.links):
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
