from selenium.common.exceptions import TimeoutException
from time import sleep
from ui.locators.basic_locators import MainPageLocators
from ui.pages.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains


class MainPage(BasePage):
    locators = MainPageLocators()

    def find_api(self):
        try:
            self.click(self.locators.APIHREF)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def find_future(self):
        try:
            self.click(self.locators.FUTUREHREF)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def find_smtp(self):
        sleep(2)
        try:
            self.click(self.locators.SMPTHREF)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def home_random_fact(self):
        try:
            src_before = self.find(self.locators.FOOTER).text
            self.click(self.locators.HOME)
            self.wait(10)
            src_after = src_before = self.find(self.locators.FOOTER).text
            return src_before == src_after
        except TimeoutException:
            return False
        except IndexError:
            return "Link is not in a new TAB"

    def python_section(self):
        try:
            self.click(self.locators.PYTHONHREF)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def history_section(self):
        try:
            python = self.find(self.locators.PYTHONHREF)
            ActionChains(self.driver).move_to_element(python).perform()
            self.click(self.locators.HISTORY)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def flask_section(self):
        try:
            python = self.find(self.locators.PYTHONHREF)
            ActionChains(self.driver).move_to_element(python).perform()
            self.click(self.locators.FLASK)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def linux_section(self):
        try:
            python = self.find(self.locators.LINUX)
            ActionChains(self.driver).move_to_element(python).perform()
            self.click(self.locators.DWNLD)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def news_section(self):
        try:
            python = self.find(self.locators.NET)
            ActionChains(self.driver).move_to_element(python).perform()
            self.click(self.locators.NEWS)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def download_wireshark(self):
        try:
            python = self.find(self.locators.NET)
            ActionChains(self.driver).move_to_element(python).perform()
            self.click(self.locators.DWIRE)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def examples(self):
        sleep(2)
        try:
            python = self.find(self.locators.NET)
            ActionChains(self.driver).move_to_element(python).perform()
            self.click(self.locators.EXMP)
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return url
        except TimeoutException:
            return ''
        except IndexError:
            return "Link is not in a new TAB"

    def logout(self):
        self.click(self.locators.LOGOUT)

    def isOut(self):
        sleep(2)
        try:
            self.find(self.locators.SIGNBUTTON)
            return True
        except TimeoutException:
            return False

    def idIsPresent(self):
        sleep(2)
        try:
            self.find(self.locators.VK)
            return True
        except TimeoutException:
            return False





