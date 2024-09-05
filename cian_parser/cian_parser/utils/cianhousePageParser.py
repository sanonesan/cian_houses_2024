from .cianhouse import CianHouse, BASE_HOUSE


import bs4
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

import csv
import time
from tqdm import tqdm
from typing import Optional
import pandas as pd

__all__ = ["CianHousePageParser"]


class CianHousePageParser:

    def __init__(
        self,
        links_path: str,
        cian_houses_path: str,
        user_agent: Optional[str] = None,
    ) -> None:

        self.links = pd.read_csv(links_path)["links"].unique().tolist()
        self.cian_houses_path = cian_houses_path
        self.user_agent = user_agent
        with open(self.cian_houses_path, "w") as csvFile:
            wr = csv.DictWriter(csvFile, BASE_HOUSE.keys())
            wr.writeheader()
        pass

    def __parse_link(self, url):

        flag = True

        while True:

            self.driver.get(url)
            # self.driver.implicitly_wait(0.5)
            page_html = self.driver.page_source
            soup = bs4.BeautifulSoup(page_html, "html.parser")

            house = CianHouse()
            house["url"] = url

            location = ""
            try:
                location_list = [
                    x.text for x in soup.select("a[data-name=AddressItem]")
                ]
                for i in range(len(location_list)):
                    if i < len(location_list) - 1:
                        location = location + location_list[i] + ", "
                    else:
                        location = location + location_list[i]
            except Exception as e:
                pass

            if location == "":
                location = "unknown"
            house["location"] = location

            metro = ""
            try:
                metro_list = [
                    x.text for x in soup.select("li[data-name=UndergroundItem]")
                ]
                metro = metro_list[0]
            except Exception as e:
                # print(e)
                pass

            if metro == "":
                metro = "unknown"
            house["metro"] = house.re_metro(metro)

            price = ""
            try:
                price_list = soup.select("div[data-testid=price-amount]")[
                    0
                ].text.split()[:-1]
                for x in price_list:
                    price = price + x
                price = int(price)
            except Exception as e:
                pass

            if price == "":
                price = "unknown"
            house["price"] = price

            try:
                soup_span = soup.select("span")
                for index, span in enumerate(soup_span):
                    if house.selector(span.text):
                        house[house.selector(span.text)] = soup_span[index + 1].text
            except Exception as e:
                pass

            try:
                soup_p = soup.select("p")
                for index, p in enumerate(soup_p):
                    if house.selector(p.text):
                        if house[house.selector(p.text)] == "unknown":
                            house[house.selector(p.text)] = soup_p[index + 1].text
            except Exception as e:
                pass

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

            # print(house)
            if house["price"] != "unknown" or house["metro"] != "unknown":
                with open(self.cian_houses_path, "a") as file:
                    wr = csv.DictWriter(file, house.keys())
                    wr.writerow(house)
                break
            print("SLEEP")
            time.sleep(10)

        pass

    def __set_up_Driver(self):
        options = Options()
        options.page_load_strategy = "eager"

        if self.user_agent is not None:
            # add the custom User Agent to Chrome Options
            options.add_argument(f"--user-agent={self.user_agent}")
        # options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-extensions")
        # options.add_argument("--enable-automation")
        # options.add_argument("--disable-browser-side-navigation")
        # options.add_argument("--disable-web-security")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-infobars")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-setuid-sandbox")
        # options.add_argument("--disable-software-rasterizer")

        self.driver = uc.Chrome(options=options)

        pass

    def parse(self):
        try:
            self.__set_up_Driver()
            for url in tqdm(self.links):
                self.__parse_link(url)

        except Exception as error:
            pass
            # logger.exception(error)
            # print(error)
        pass
