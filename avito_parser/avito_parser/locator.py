from selenium.webdriver.common.by import By


class LocatorCianMain:
    """Selectors for Cian Main pages"""

    PAGINATION_BTNS = (By.CSS_SELECTOR, '[data-name="Pagination"]')
    NEXT_BTN = (By.LINK_TEXT, "Дальше")

    DESCRIPTION_FRAME = (By.CSS_SELECTOR, '[data-name="LinkArea"]')
    # inner element of DESCRIPTION_FRAME
    URL = (By.CSS_SELECTOR, '[target="_blank"]')

    TITLES = (By.CSS_SELECTOR, '[data-name="CardComponent"]')


class LocatorCianFull:
    """Selectors for Cian detailed analysis"""
