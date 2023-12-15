from locators.locator import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage


class CartPage(BasePage):
    def get_cart_items_all(self):
        items = []
        item_elements = self._find_all(CartPageLocators.CART_ITEM)
        for i in item_elements:
            items.append(
                {
                    "name": self._find_child(i, CartPageLocators.ITEM_NAME).text,
                    "description": self._find_child(
                        i, CartPageLocators.ITEM_DESCRIPTION
                    ).text,
                    "price": float(
                        self._find_child(i, CartPageLocators.ITEM_PRICE).text[1:]
                    ),
                    "in_cart": True,
                }
            )
        return items

    def click_checkout(self):
        return self._click(CartPageLocators.CHECKOUT_BUTTON)
