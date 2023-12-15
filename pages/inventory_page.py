from locators.locator import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def add_to_cart_all(self):
        items = []
        item_elements = self._find_all(InventoryPageLocators.INVENTORY_ITEM)
        for i in item_elements:
            item_in_cart = False
            cart_button_text = self._find_child(
                i, InventoryPageLocators.ADD_TO_CART_BUTTON
            ).text
            if "remove" in cart_button_text.lower():
                item_in_cart = True
            else:
                button = self._find_child(i, InventoryPageLocators.ADD_TO_CART_BUTTON)
                if item_in_cart == False:
                    button.click()
                items.append(
                    {
                        "name": self._find_child(
                            i, InventoryPageLocators.ITEM_NAME
                        ).text,
                        "description": self._find_child(
                            i, InventoryPageLocators.ITEM_DESCRIPTION
                        ).text,
                        "price": float(
                            self._find_child(i, InventoryPageLocators.ITEM_PRICE).text[
                                1:
                            ]
                        ),
                        "in_cart": True,
                    }
                )

        return {"count": len(item_elements), "items": items}

    def inventory_item(self, name):
        item_elements = self._find_all(InventoryPageLocators.INVENTORY_ITEM)
        for i in item_elements:
            if self._find_child(i, InventoryPageLocators.ITEM_NAME).text == name:
                return i

        return False

    def add_item_to_cart_by_name(self, name):
        item = self.inventory_item(name)
        assert item, f"Cannot add item '{name}' to cart, item not found"
        if (
            "remove"
            not in self._find_child(item, InventoryPageLocators.ADD_TO_CART_BUTTON).text
        ):
            self._find_child(item, InventoryPageLocators.ADD_TO_CART_BUTTON).click()

    def remove_item_by_name(self, name):
        item = self.inventory_item(name)
        assert item, f"Cannot remove item '{name}' from cart, item not found"
        if (
            "remove"
            in self._find_child(
                item, InventoryPageLocators.ADD_TO_CART_BUTTON
            ).text.lower()
        ):
            self._find_child(item, InventoryPageLocators.ADD_TO_CART_BUTTON).click()

    def click_shopping_cart(self):
        self._click(InventoryPageLocators.SHOPPING_CART_LINK)

    def get_cart_quantity(self):
        try:
            shopping_cart_badge_element = self.driver.find_element(
                By.CLASS_NAME, InventoryPageLocators.SHOPPING_CART_BADGE["value"]
            )
            return int(shopping_cart_badge_element.text)
        except:
            return 0

    def set_sort(self, value):
        try:
            select_element = Select(self._find(InventoryPageLocators.SELECT_SORT))
            print("FOUND ELEMENT::::::", select_element)
            select_element.select_by_value(value)
            time.sleep(1)
        except:
            return 0

    def get_items_all(self):
        items = []
        item_elements = self._find_all(InventoryPageLocators.INVENTORY_ITEM)
        for i in item_elements:
            item_in_cart = False
            cart_button_text = self._find_child(
                i, InventoryPageLocators.ADD_TO_CART_BUTTON
            ).text
            if "remove" in cart_button_text.lower():
                item_in_cart = True
            items.append(
                {
                    "name": self._find_child(i, InventoryPageLocators.ITEM_NAME).text,
                    "description": self._find_child(
                        i, InventoryPageLocators.ITEM_DESCRIPTION
                    ).text,
                    "price": float(
                        self._find_child(i, InventoryPageLocators.ITEM_PRICE).text[1:]
                    ),
                    "in_cart": item_in_cart,
                }
            )

        return items
