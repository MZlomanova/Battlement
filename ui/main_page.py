from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from battlenet.ui.constants import BATTLE_NET_URL


class MainPage:
    def __init__(self, driver: WebDriver, timeout: int = 60):
        self._driver = driver
        self._timeout = timeout

    def open(self):
        self._driver.get(BATTLE_NET_URL)
        WebDriverWait(self._driver, self._timeout).until(
            EC.visibility_of_element_located(
                (By.ID, 'blz-nav-battlenet-logo')
            )
        )

    def get_recommended(self):
        return self.__find_cards("recommended")

    def get_featured(self):
        return self.__find_cards("featured")

    def get_trending_now(self):
        return self.__find_cards("trending-now")

    def get_most_gifted(self):
        return self.__find_cards("most-gifted")

    def set_language(self, language):
        WebDriverWait(self._driver, self._timeout).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid=footer]')
            )
        )

        language_selector = self._driver.find_element(
            By.CSS_SELECTOR, "blz-nav-footer").shadow_root.find_element(
                By.CSS_SELECTOR, ".top-section-desktop blz-locale-selector"
            ).shadow_root.find_element(
                By.CSS_SELECTOR, "[slot=locale-selector-primary-toggle]"
            ).shadow_root.find_element(
                By.CSS_SELECTOR, "button"
            )

        self.__perform_click(language_selector)

        language_link = self._driver.find_element(
            By.CSS_SELECTOR, "blz-nav-footer").shadow_root.find_element(
                By.CSS_SELECTOR, ".top-section-desktop blz-locale-selector"
            ).shadow_root.find_element(
                By.CSS_SELECTOR, "#dropdown blz-footer-link[data-id='"
                + language + "']"
            ).shadow_root.find_element(
                By.CSS_SELECTOR, "a"
            )

        self.__perform_click(language_link)

    def get_search_results(self, str):
        WebDriverWait(self._driver, self._timeout).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-id=search-form]')
            )
        ).click()

        self._driver.find_element(
            By.CSS_SELECTOR, "#search-desktop-input").send_keys(
                str
            )

        WebDriverWait(self._driver, self._timeout).until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR,
                 "#mat-autocomplete-0 div.search-result-group")
            )
        )

        return self._driver.find_elements(
            By.CSS_SELECTOR, "#mat-autocomplete-0 div.search-result-group")

    def select_search_item(self, item: WebElement):
        item.find_element(By.CSS_SELECTOR, ".result-container a").click()

        WebDriverWait(self._driver, self._timeout).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.product-page__grid')
            )
        )

    def __find_cards(self, block_id):
        WebDriverWait(self._driver, self._timeout).until(
            EC.visibility_of_element_located(
                (By.ID, block_id)
            )
        )
        return self._driver.find_elements(By.CSS_SELECTOR, "#" + block_id
                                          + " li")

    # https://stackoverflow.com/a/56512794
    def __perform_click(self, link):
        selector_click_action = ActionChains(self._driver)
        selector_click_action.move_to_element(link)
        selector_click_action.click(link)
        selector_click_action.perform()
