from locators.locator import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    def page_loaded(self):
        return bool(self._find(CheckoutPageStepTwoLocators.CHECKOUT_SUMMARY_CONTAINER))

    def click_finish(self):
        return self._click(CheckoutPageStepTwoLocators.FINISH_BUTTON)

    def click_cancel(self):
        return self._click(CheckoutPageStepTwoLocators.CANCEL_BUTTON)

    def get_items(self):
        items = []
        item_elements = self._find_all(CheckoutPageStepTwoLocators.CART_ITEM)
        for i in item_elements:
            items.append(
                {
                    "name": self._find_child(
                        i, CheckoutPageStepTwoLocators.ITEM_NAME
                    ).text,
                    "description": self._find_child(
                        i, CheckoutPageStepTwoLocators.ITEM_DESCRIPTION
                    ).text,
                    "price": float(
                        self._find_child(
                            i, CheckoutPageStepTwoLocators.ITEM_PRICE
                        ).text[1:]
                    ),
                }
            )

        return items

    def check_price(self, final_price):
        total_price = float(
            self._find(CheckoutPageStepTwoLocators.TOTAL_PRICE_LABEL).text.split("$")[1]
        )
        # print(total_price, final_price)
        return total_price == final_price
