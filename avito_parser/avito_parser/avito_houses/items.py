# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# Class for Parsing Houses
class HouseParserItem(scrapy.Item):
    name = scrapy.Field()
    director = scrapy.Field()
    genres = scrapy.Field()
    country = scrapy.Field()
    id_IMDb = scrapy.Field()
    rating_IMDb = scrapy.Field()
    year = scrapy.Field()

    pass
