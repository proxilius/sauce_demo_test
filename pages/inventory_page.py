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
                        "in_cart": item_in_cart,
                    }
                )

        return {"count": len(item_elements), "item_names": items}

    def click_shopping_cart(self):
        self._click(InventoryPageLocators.SHOPPING_CART_LINK)

    def get_cart_quantity(self):
        try:
            shopping_cart_badge_element = self.driver.find_element(
                *InventoryPageLocators.SHOPPING_CART_BADGE
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
