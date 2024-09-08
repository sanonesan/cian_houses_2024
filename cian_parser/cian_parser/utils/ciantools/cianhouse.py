import re

__all__ = ["BASE_HOUSE", "CianHouse"]

BASE_HOUSE = {
    "price": "unknown",
    "location": "unknown",
    "geo_lat": "unknown",
    "geo_lng": "unknown",
    "metro": "unknown",
    "floor": "unknown",
    "floor_count": "unknown",
    "square": "unknown",
    "living_square": "unknown",
    "kitchen_square": "unknown",
    "year": "unknown",
    "finish_type": "unknown",
    "ceiling_height": "unknown",
    "view": "unknown",
    "house_type": "unknown",
    "heating": "unknown",
    "breakdown": "unknown",
    "parking": "unknown",
    "accomodation_type": "unknown",
    "author": "unknown",
    "url": "url",
}


class CianHouse(dict):

    def __init__(self):
        super().__init__()
        self.update(BASE_HOUSE)

    @classmethod
    def selector(cls, element: str):
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
            return "finish_type"
        elif element == "Этаж":
            return "floor"
        elif element == "Год постройки" or element == "Год сдачи":
            return "year"
        elif element == "Вид из окон":
            return "view"
        elif element == "Тип дома":
            return "house_type"
        elif element == "Отопление":
            return "heating"
        elif element == "Аварийность":
            return "breakdown"
        elif element == "Паковка":
            return "parking"
        elif element == "Застройщик":
            return "author"
        else:
            return False

    def re_square(self, square: str):
        head, _, tail = re.findall(r"(\d+,{0,}\d{0,})", square)[0].partition(",")
        return float(head + "." + tail)

    def re_ceiling(self, ceiling: str):
        head, _, tail = re.findall(r"(\d+,{0,}\d{0,})", ceiling)[0].partition(",")
        return float(head + "." + tail)

    def re_year(self, year):
        return int(re.findall(r"\d+", year)[0])

    def re_floor(self, floor):
        res = re.findall(r"\d+", floor)
        return int(res[0]), int(res[1])

    def re_metro(self, metro):
        res = re.findall(
            r"([a-zA-Zа-яА-ЯёЁ]+\s\d+\s[a-zA-Zа-яА-ЯёЁ]+|[a-zA-Zа-яА-ЯёЁ]+\s[a-zA-Zа-яА-ЯёЁ]+|[a-zA-Zа-яА-ЯёЁ]+)",
            metro,
        )[0]
        return res
