from locators.checkout_step_two_page import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    def page_loaded(self):
        return bool(self._find(CheckoutStepTwoPageLocators.CHECKOUT_SUMMARY_CONTAINER))

    def click_finish(self):
        return self._click(CheckoutStepTwoPageLocators.FINISH_BUTTON)

    def click_cancel(self):
        return self._click(CheckoutStepTwoPageLocators.CANCEL_BUTTON)

    def get_items(self):
        items = []
        item_elements = self._find_all(CheckoutStepTwoPageLocators.CART_ITEM)
        for i in item_elements:
            items.append(
                {
                    "name": self._find_child(
                        i, CheckoutStepTwoPageLocators.ITEM_NAME
                    ).text,
                    "description": self._find_child(
                        i, CheckoutStepTwoPageLocators.ITEM_DESCRIPTION
                    ).text,
                    "price": float(
                        self._find_child(
                            i, CheckoutStepTwoPageLocators.ITEM_PRICE
                        ).text[1:]
                    ),
                }
            )

        return items

    def check_price(self, final_price):
        total_price = float(
            self._find(CheckoutStepTwoPageLocators.TOTAL_PRICE_LABEL).text.split("$")[1]
        )
        return total_price == final_price
