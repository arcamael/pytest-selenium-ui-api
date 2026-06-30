from __future__ import annotations

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import settings

Locator = tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = settings.DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- waiting / finding --------------------------------------------------
    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Locator) -> list[WebElement]:
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def is_visible(self, locator: Locator) -> bool:
        try:
            return self.find_visible(locator).is_displayed()
        except (TimeoutException, WebDriverException):
            return False

    def is_enabled(self, locator: Locator) -> bool:
        try:
            return self.find(locator).is_enabled()
        except (TimeoutException, WebDriverException):
            return False

    def wait_until_invisible(self, locator: Locator) -> bool:
        return self.wait.until(EC.invisibility_of_element_located(locator))

    # --- actions ------------------------------------------------------------
    def click(self, locator: Locator) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        element.click()

    def type_text(self, locator: Locator, text: str, clear: bool = True) -> None:
        element = self.find_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.find_visible(locator).text.strip()
