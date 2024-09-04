import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import HouseParserItem


class AvitoHousesSpider(CrawlSpider):
    """
    Class for getting movie information from wikipedia.
    To run this code:
    1) go to dir: avito_houses/avito_houses/
    2) write in CLI: $scrapy crawl avito_houses -o avito_houses_data.csv
    """

    name = "avito_houses"
    # Set custom_settings
    custom_settings = {
        # Bigger value => More parsed links
        "CLOSESPIDER_ITEMCOUNT": 2500,
    }
    # Set allowed_domains
    allowed_domains = ["ru.wikipedia.org", "www.imdb.com"]
    # Set start_urls
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"]
    # Set some rules
    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=('//*[@class="plainlinks"]/tbody/tr/td//a'),
            ),
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths=('//*[@class="mw-category-group"]/ul//li//a'),
            ),
            callback="film_page_parse",
            follow=True,
        ),
    )

    def film_page_parse(self, response):
        # Create MovieItem variable
        movie = HouseParserItem()
        # Filling it's fields with initial empty lists
        movie["name"] = ""
        movie["director"] = ["unknown"]
        movie["genres"] = ["unknown"]
        movie["country"] = ["unknown"]
        movie["year"] = ["unknown"]
        movie["id_IMDb"] = ["unknown"]
        movie["rating_IMDb"] = ["unknown"]

        # Get Movie name (always the same as name of 1 Heading of wiki page)
        movie["name"] = response.css("#firstHeading > span::text").get()

        # Go through infobox of wikipedia (usually has all needed information).
        # Usually infobox has xpath as here, but sometimes it is in table[2], this
        # exception is handled later
        for u in response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr'):
            # Get name of row
            item_name = u.xpath(".//th//text()").extract_first()
            # Get it's content
            items = [s.strip("\n") for s in u.xpath(".//td//text()").extract()]

            # Get genres
            if "Жанр" in str(item_name):
                movie["genres"] = [item if item != "" else None for item in items]
                while None in movie["genres"]:
                    movie["genres"].remove(None)

            # Get directors
            elif "Режиссёр" in str(item_name):
                movie["director"] = [item if item != "" else None for item in items]
                while None in movie["director"]:
                    movie["director"].remove(None)

            # Get country
            elif "Стран" in str(item_name):
                movie["country"] = [
                    item if (item != "") and (item != "\xa0") else None
                    for item in items
                ]
                while None in movie["country"]:
                    movie["country"].remove(None)

            # Get year
            elif (
                ("Год" in str(item_name))
                or ("Дата" in str(item_name))
                or ("Дата выхода" in str(item_name))
                or ("Премьера" in str(item_name))
                or ("Первый показ" in str(item_name))
                or ("Трансляция" in str(item_name))
            ):
                movie["year"] = [item if item != "" else None for item in items]
                while None in movie["year"]:
                    movie["year"].remove(None)

            # Get id_IMDb
            elif "IMDb" in str(item_name):
                movie["id_IMDb"] = [item if item != "" else None for item in items]
                while None in movie["id_IMDb"]:
                    movie["id_IMDb"].remove(None)

        # check if infotable is in table[2]
        if ["unknown"] in movie.values() and movie["name"] != "Категория":
            # Go through infobox of wikipedia (usually has all needed information).
            for u in response.xpath(
                '//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr'
            ):
                # Get name of row
                item_name = u.xpath(".//th//text()").extract_first()
                # Get it's content
                items = [s.strip("\n") for s in u.xpath(".//td//text()").extract()]

                # Get genres
                if "Жанр" in str(item_name) and movie["genres"] == ["unknown"]:
                    movie["genres"] = [item if item != "" else None for item in items]
                    while None in movie["genres"]:
                        movie["genres"].remove(None)

                # Get directors
                elif "Режиссёр" in str(item_name) and movie["director"] == ["unknown"]:
                    movie["director"] = [item if item != "" else None for item in items]
                    while None in movie["director"]:
                        movie["director"].remove(None)

                # Get country
                elif "Стран" in str(item_name) and movie["country"] == ["unknown"]:
                    movie["country"] = [
                        item if (item != "") and (item != "\xa0") else None
                        for item in items
                    ]
                    while None in movie["country"]:
                        movie["country"].remove(None)

                # Get year
                elif (
                    ("Год" in str(item_name))
                    or ("Дата" in str(item_name))
                    or ("Дата выхода" in str(item_name))
                    or ("Премьера" in str(item_name))
                    or ("Первый показ" in str(item_name))
                    or ("Трансляция" in str(item_name))
                ) and movie["year"] == ["unknown"]:
                    movie["year"] = [item if item != "" else None for item in items]
                    while None in movie["year"]:
                        movie["year"].remove(None)

                # Get id_IMDb
                elif "IMDb" in str(item_name) and movie["id_IMDb"] == ["unknown"]:
                    movie["id_IMDb"] = [item if item != "" else None for item in items]
                    while None in movie["id_IMDb"]:
                        movie["id_IMDb"].remove(None)

        # Sometimes parses first page of wikipedia with h1 "Категория"
        # Handling that case
        if (
            movie["genres"] == ["unknown"]
            and movie["director"] == ["unknown"]
            and movie["country"] == ["unknown"]
            and movie["year"] == ["unknown"]
            and movie["id_IMDb"] == ["unknown"]
            and movie["name"] == "Категория"
        ):
            pass
        # Then some refactoring of collected data with usage of regex
        else:
            if movie["year"] != ["unknown"]:
                tmp = []
                for res_str in movie["year"]:
                    re_res = re.findall(r"\d{4}", res_str)
                    if re_res != []:
                        for x in re_res:
                            if x not in tmp:
                                tmp.append(x)

                movie["year"] = tmp

            if movie["country"] != ["unknown"]:
                tmp = []
                for res_str in movie["country"]:
                    re_res = []
                    for x in re.findall(r"(([A-Я]{1}[A-Яа-я]+(—|-|\s)*)+)", res_str):
                        if "Босния" not in x[0]:
                            if "Герцеговина" not in x[0]:
                                re_res.append(x[0])
                        else:
                            re_res.append("Босния и Герцеговина")

                    if re_res != []:
                        for x in re_res:
                            if x not in tmp:
                                tmp.append(x)
                movie["country"] = tmp

            if movie["genres"] != ["unknown"]:
                tmp = []
                for res_str in movie["genres"]:
                    re_res = [
                        x[0] for x in re.findall(r"(([А-Яа-яЁё]+(—|-|\s)*)+)", res_str)
                    ]
                    if re_res != []:
                        for x in re_res:
                            if x not in tmp and len(x) > 2:
                                tmp.append(x)
                movie["genres"] = tmp

            if movie["director"] != ["unknown"]:
                tmp = []
                for res_str in movie["director"]:
                    re_res = [
                        x[0] for x in re.findall(r"(([А-Яа-яЁё]+(—|-|\s)*)+)", res_str)
                    ]
                    if re_res != []:
                        for x in re_res:
                            if x not in tmp and (x != "и " or x != "и"):
                                tmp.append(x)
                movie["director"] = tmp

            # Try to get movie IMDb rating if we successfully parsed it's IMDb id
            if movie["id_IMDb"] != ["unknown"]:
                tmp = []
                for res_str in movie["id_IMDb"]:
                    re_res = re.findall(r"\d+", res_str)
                    if re_res != []:
                        for x in re_res:
                            tmp.append(x)
                movie["id_IMDb"] = tmp

                URL = f"https://www.imdb.com/title/tt{movie['id_IMDb'][0]}/ratings/"
                request = scrapy.Request(
                    url=URL,
                    callback=self.parse_IMDb_rating,
                    meta={"item": movie},
                )
                yield request
            else:
                yield movie

    # Parser for IMDb site for getting movie rating
    def parse_IMDb_rating(self, response):
        movie = response.meta["item"]
        # Get movie rating
        movie["rating_IMDb"] = str(
            response.xpath(
                '//div[@data-testid="rating-button__aggregate-rating__score"]/span/text()'
            ).extract_first()
        )
        yield movie
