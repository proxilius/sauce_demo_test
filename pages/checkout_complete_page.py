from pages.base_page import BasePage
from locators.checkout_complete_page_locators import CheckoutCompletePageLocators


class CheckoutCompletePage(BasePage):
    def checkout_complete(self):
        return bool(self._find(CheckoutCompletePageLocators.FINISH_BUTTON))

    def return_to_store(self):
        self._click(CheckoutCompletePageLocators.BACK_TO_PRODUCTS_BUTTON)
