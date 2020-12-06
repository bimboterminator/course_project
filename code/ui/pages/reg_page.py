from selenium.common.exceptions import TimeoutException
from time import sleep
from ui.locators.basic_locators import RegPageLocators
from ui.pages.base_page import BasePage


class RegPage(BasePage):
    locators = RegPageLocators()

    def reg_with_text(self, login, email, passwd1, passwd2, accept=True):
        self.click(self.locators.GOTO)
        self.enter_text(self.locators.LOGINFIELD, login)
        self.enter_text(self.locators.PASSWDFIELD, passwd1)
        self.enter_text(self.locators.REPEAT, passwd2)
        self.enter_text(self.locators.EMAIL, email)
        self.click(self.locators.TERMS)
        self.click(self.locators.REGISTER)

    def invalid_login(self):
        sleep(2)
        try:
            namewrap = self.find(self.locators.LOGINLENGTH)

            if 'Incorrect username length' == namewrap.text:
                return True
            return False
        except TimeoutException:
            return False

    def invalid_email(self):
        sleep(2)
        try:
            namewrap = self.find(self.locators.WRONGEMAIL)

            if 'Invalid email address' == namewrap.text:
                return True
            return False
        except TimeoutException:
            return False

    def email_exists(self):
        sleep(2)
        try:
            namewrap = self.find(self.locators.INVEMAIL)
            if 'Such email already exists' == namewrap.text:
                return namewrap.text
            return namewrap.text
        except TimeoutException:
            return ''

    def user_exists(self):
        sleep(2)
        try:
            namewrap = self.find(self.locators.USREX)
            if 'User already exist' == namewrap.text:
                return True
            return False
        except TimeoutException:
            return False

    def pass_not_match(self):
        sleep(2)
        try:
            namewrap = self.find(self.locators.PASSNOTMATCH)

            if 'Passwords must match' == namewrap.text:
                return True
            return False
        except TimeoutException:
            return False

    def box_not_checked(self):

        try:
            self.click(self.locators.REGISTER)
            return
        except TimeoutException:
            return False

