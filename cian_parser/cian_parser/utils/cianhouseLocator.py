from selenium.webdriver.common.by import By

__all__ = ["CianHouseLocator"]


class CianHouseLocator:
    """Selectors for Cian"""

    PAGINATION_BTNS = (By.CSS_SELECTOR, '[data-name="Pagination"]')
    NEXT_BTN = (By.LINK_TEXT, "Дальше")

    DESCRIPTION_FRAME = (By.CSS_SELECTOR, '[data-name="LinkArea"]')
    # inner element of DESCRIPTION_FRAME
    URL = (By.CSS_SELECTOR, '[target="_blank"]')

    TITLES = (By.CSS_SELECTOR, '[data-name="CardComponent"]')
