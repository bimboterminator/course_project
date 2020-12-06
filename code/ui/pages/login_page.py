from selenium.common.exceptions import TimeoutException
from time import sleep
from ui.locators.basic_locators import LoginPageLocators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    locators = LoginPageLocators()

    def auth_with_text(self, login, passwd):

        self.enter_text(self.locators.LOGINFIELD, login)
        self.enter_text(self.locators.PASSWDFIELD, passwd)
        self.click(self.locators.SIGNBUTTON)

    def login_isDisplayed(self, login):
        try:
            namewrap = self.find(self.locators.LOGINSHOW)
            if login == namewrap.text.split()[2]:
                return True
            return False
        except TimeoutException:
            return False

    def error_isDisplayed(self):
        sleep(1)
        try:
            namewrap = self.find(self.locators.ERRORMSG)
            if 'Invalid username or password' == namewrap.text:
                return True
        except TimeoutException:
            return False

    def access_denied(self):
        sleep(2)
        try:
            namewrap = self.find(self.locators.DENIED)
            if 'Ваша учетная запись заблокирована' == namewrap.text:
                return True
        except TimeoutException:
            return False
