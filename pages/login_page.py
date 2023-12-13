from locators.locator import *
from pages.base_page import BasePage


class LoginPage(BasePage):
    def set_credentials(self, username, password):
        self._type(LoginPageLocators.USERNAME, username)
        self._type(LoginPageLocators.PASSOWRD, password)

    def click_login_button(self):
        self._click(LoginPageLocators.LOGIN_BUTTON)

    def login(self, username, password):
        self.set_credentials(username, password)
        self.click_login_button()

    def seek_error(self):
        try:
            element = self.driver.find_element(*LoginPageLocators.ERROR)
            print("ERRORRRR ELEMENT:::::: ", element)
            return element.text
        except:
            return 0
