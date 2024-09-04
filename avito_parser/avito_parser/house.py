from typing import TypedDict, Optional


class House(TypedDict):
    price: Optional[str]
    adress: Optional[str]
    metro: Optional[str]
    floor: Optional[str]
    square: Optional[str]
    living_square: Optional[str]
    kitchen_square: Optional[str]
    year: Optional[str]
    renovation: Optional[str]
    ceiling_height: Optional[str]
    view: Optional[str]
    accomodation_type: Optional[str]
