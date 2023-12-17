from locators.locator import *
from pages.base_page import BasePage
from variables import BASE_URL


class ItemPage(BasePage):
    def item_page_loaded(self):
        return bool(self._find(ItemPageLocators.DETAILS_CONTAINER))

    def check_item_loaded(self, item):
        return bool(
            self._find(ItemPageLocators.DETAILS_NAME).text == item["name"]
            and self._find(ItemPageLocators.DETAILS_PRICE).text[1:]
            == str(item["price"])
        )

    def click_add_remove_button(self, text):
        if text in self._find(ItemPageLocators.ADD_REMOVE_CART_BUTTON).text.lower():
            self._click(ItemPageLocators.ADD_REMOVE_CART_BUTTON)
        else:
            print("Button functionality is wrong!")
            assert False

    def click_back_to_products(self):
        self._click(ItemPageLocators.BACK_BUTTON)
