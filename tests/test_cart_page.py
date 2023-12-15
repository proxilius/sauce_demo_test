from ddt import ddt, data
import unittest
import time
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from testcase.variables import *
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.common import assert_and_log
from utils.common_steps import CommonSteps


class TestCartPage:
    @pytest.mark.parametrize("username", ["standard_user", "b"], indirect=True)
    def setUp(self, username):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(BASE_URL)
        self.inventoryPage = InventoryPage(self.driver)
        self.cartPage = CartPage(self.driver)
        if not CommonSteps().login(self, username):
            return
            pass  # ¨return

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    def test_remove_item_from_cart(self, username):
        items_added_to_cart = CommonSteps.add_everything_to_cart(self)
        self.inventoryPage.click_shopping_cart()
        items_in_cart_original = self.cartPage.get_cart_items_all()
        time.sleep(1)
        self.cartPage.remove_item_by_name(items_in_cart_original[0]["name"])
        time.sleep(1)
        items_in_cart = self.cartPage.get_cart_items_all()
        assert items_in_cart == items_in_cart_original[1:]

    @data("locked_out_user", "standard_user")
    def test_checkout_half(self, username):
        inventoryPage = InventoryPage(self.driver)
        cartPage = CartPage(self.driver)
        if not CommonSteps().login(self, username):
            return
            pass  # ¨return
        items_added_to_cart = CommonSteps.add_everything_to_cart(self)
        inventoryPage.click_shopping_cart()
        items_in_cart = cartPage.get_cart_items_all()
        print(
            "items_added_to_cart: ", items_added_to_cart, "items_in_cart", items_in_cart
        )

        assert items_in_cart == items_added_to_cart

        if len(items_in_cart) > 0:
            cartPage.click_checkout()
        else:
            if cartPage.click_checkout() == None:
                assert_and_log(
                    self,
                    False,
                    "Cart is empty, checkout should be disabled",
                )


if __name__ == "__main__":
    unittest.main()
