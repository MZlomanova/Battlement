from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from battlenet.ui.constants import BATTLE_NET_PRODUCT_URL


class ProductPage:
    def __init__(self, driver: WebDriver,
                 url: str = BATTLE_NET_PRODUCT_URL,
                 timeout: int = 60):
        self._driver = driver
        self._timeout = timeout
        self._url = url

    def open(self):
        self._driver.get(self._url)
        WebDriverWait(self._driver, self._timeout).until(
            EC.visibility_of_element_located(
                (By.ID, 'blz-nav-battlenet-logo')
            )
        )

    def get_options(self):
        return self._driver.find_elements(
            By.XPATH, "//storefront-product-option"
        )

    def set_option(self, option):
        self._driver.find_element(
            By.XPATH, 
            "//storefront-product-option/div/dl/dt[contains(text(), '"
            + option + "')]"
        ).click()

    def get_active_slide(self):
        return self._driver.find_element(
            By.CSS_SELECTOR,
            "#product-gallery__lead div.swiper-slide-active"
        )
