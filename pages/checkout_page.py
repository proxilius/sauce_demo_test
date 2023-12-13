from locators.locator import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def set_firstname(self, value):
        self._type(CheckoutPageLocators.FIRST_NAME_INPUT, value)

    def set_last_name(self, value):
        self._type(CheckoutPageLocators.LAST_NAME_INPUT, value)

    def set_zip(self, value):
        self._type(CheckoutPageLocators.POSTAL_CODE_INPUT, value)

    def click_continue(self):
        return self._click(CheckoutPageLocators.CONTINUE_BUTTON)

    def error_message(self):
        error = self._find(CheckoutPageLocators.ERROR_TEXT).text
        return error
