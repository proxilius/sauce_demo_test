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

    def click_continue_shopping(self):
        return self._click(CartPageLocators.CONTINUE_SHOPPING_BUTTON)

    def cart_item(self, name):
        item_elements = self._find_all(CartPageLocators.CART_ITEM)
        for i in item_elements:
            if self._find_child(i, CartPageLocators.ITEM_NAME).text == name:
                return i

        return False

    def get_cart_quantity(self):
        try:
            shopping_cart_badge_element = self.driver.find_element(
                By.CLASS_NAME, CartPageLocators.SHOPPING_CART_BADGE["value"]
            )
            return int(shopping_cart_badge_element.text)
        except:
            return 0

    def remove_item_by_name(self, name):
        item = self.cart_item(name)
        assert item, f"Cannot remove item '{name}' from cart, item not found"
        if (
            "remove"
            in self._find_child(item, CartPageLocators.CART_BUTTON).text.lower()
        ):
            self._find_child(item, CartPageLocators.CART_BUTTON).click()
            print("REMOVING:::: ", name)

    def click_item_by_name(self, name):
        item_elements = self._find_all(CartPageLocators.CART_ITEM)
        for i in item_elements:
            if self._find_child(i, CartPageLocators.ITEM_NAME).text == name:
                self._find_child(i, CartPageLocators.ITEM_NAME).click()
                time.sleep(0.5)
                return True

        return False
