from locators.locator import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys


class CheckoutPage(BasePage):
    def set_firstname(self, value):
        self._type(CheckoutPageLocators.FIRST_NAME_INPUT, value)

    def set_last_name(self, value):
        self._type(CheckoutPageLocators.LAST_NAME_INPUT, value)

    def set_zip(self, value):
        self._type(CheckoutPageLocators.POSTAL_CODE_INPUT, value)

    def send_tab(self):
        self._type(CheckoutPageLocators.POSTAL_CODE_INPUT, Keys.TAB)

    def get_form_values(self):
        first_name = self._value(CheckoutPageLocators.FIRST_NAME_INPUT)
        last_name = self._value(CheckoutPageLocators.LAST_NAME_INPUT)
        zip = self._value(CheckoutPageLocators.POSTAL_CODE_INPUT)
        return (str(first_name), str(last_name), str(zip))

    def click_continue(self):
        return self._click(CheckoutPageLocators.CONTINUE_BUTTON)

    def error_message(self):
        error = self._find(CheckoutPageLocators.ERROR_TEXT)
        if error:
            return error.text
        return ""
