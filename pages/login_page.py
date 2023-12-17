from locators.locator import *
from pages.base_page import BasePage
from variables import BASE_URL


class LoginPage(BasePage):
    def access_login_page(self):
        self.driver.get(BASE_URL)
        assert self._find(LoginPageLocators.LOGIN_WRAPPER)

    def set_credentials(self, username, password):
        self._type(LoginPageLocators.USERNAME, username)
        self._type(LoginPageLocators.PASSOWRD, password)

    def click_login_button(self):
        self._click(LoginPageLocators.LOGIN_BUTTON)

    def login(self, username, password):
        self.set_credentials(username, password)
        self.click_login_button()

    def login_error(self):
        try:
            login_error = self.driver.find_element(
                By.XPATH, LoginPageLocators.ERROR["value"]
            )
            return login_error.text
        except:
            return False
