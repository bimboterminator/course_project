from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
RETRY_COUNT = 20


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=20) -> WebElement:
        return WebDriverWait(self.driver, timeout=timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=20):
        # попытки чтобы кликнуть
        for i in range(RETRY_COUNT):
            try:
                self.find(locator)
                element = WebDriverWait(self.driver, timeout=timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return

            except StaleElementReferenceException:
                if i < RETRY_COUNT - 1:
                    pass
        raise

    def enter_text(self, by_locator, text, timeout=None):

        self.wait(timeout).until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)
