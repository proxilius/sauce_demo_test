import time

import pytest
from testcase.variables import *
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.common import assert_and_log, log_assert
from pages.cart_page import CartPage


class CommonSteps:
    @staticmethod
    def login(self, username):
        loginPage = LoginPage(self.driver)
        loginPage.login(username, PASSWORD)
        time.sleep(0.5)
        if self.driver.current_url == INVENTORY_URL:
            return True
        else:
            return False

    @staticmethod
    @pytest.mark.xfail
    def add_everything_to_cart(self):
        inventoryPage = InventoryPage(self.driver)
        x = inventoryPage.get_cart_quantity()
        # assert x == 0
        # assert_and_log(self, x == 0, "Cart is empty")
        # assert x == 0
        log_assert(0, x)
        result = inventoryPage.add_to_cart_all()
        quantity = result["count"]
        items = result["items"]
        time.sleep(1)
        x = inventoryPage.get_cart_quantity()
        print("X: ", x, "Quantity", quantity)
        # assert_and_log(self, x == quantity, "Cart has " + str(quantity) + " elements")
        # assert x == quantity
        log_assert(quantity, x)
        try:
            pytest.assume(x == quantity)
            return items
        except:
            return items

    @staticmethod
    def checkout(self, items_added_to_cart):
        inventoryPage = InventoryPage(self.driver)
        cartPage = CartPage(self.driver)
        items_added_to_cart = items_added_to_cart
        inventoryPage.click_shopping_cart()
        items_in_cart = cartPage.get_cart_items_all()
        # print(
        #     "items_added_to_cart: ", items_added_to_cart, "items_in_cart", items_in_cart
        # )
        # assert_and_log(
        #     self,
        #     items_added_to_cart == items_in_cart,
        #     "Cart items are the same as items added previously",
        # )
        assert items_added_to_cart == items_in_cart
        if len(items_in_cart) > 0:
            cartPage.click_checkout()
        else:
            if cartPage.click_checkout() == None:
                # assert_and_log(
                #     self,
                #     False,
                #     "Cart is empty, checkout should be disabled",
                # )
                assert False
