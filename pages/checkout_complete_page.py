from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from locators.locator import CheckoutCompletePageLocators


class CheckoutCompletePage(BasePage):
    def checkout_complete(self):
        return bool(self._find(CheckoutCompletePageLocators.FINISH_BUTTON))

    def return_to_store(self):
        self._click(CheckoutCompletePageLocators.BACK_TO_PRODUCTS_BUTTON)
