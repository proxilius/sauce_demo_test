from ddt import ddt, data
import unittest
import time
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from variables import *
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.common import assert_and_log
from utils.common_steps import CommonSteps


class TestCartPage:
    # @pytest.mark.parametrize("username", ["standard_user", "b"], indirect=True)
    # def setUp(self, username):
    #     self.logger = logging.getLogger(__name__)
    #     options = webdriver.ChromeOptions()
    #     self.driver = webdriver.Chrome(options=options)
    #     self.driver.maximize_window()
    #     self.driver.get(BASE_URL)
    #     self.inventoryPage = InventoryPage(self.driver)
    #     self.cartPage = CartPage(self.driver)
    #     if not CommonSteps().login(self, username):
    #         return
    #         pass  # ¨return
    @pytest.fixture(params=USERS_WITHOUT_LOCKED_OUT)
    def cart_page(self, request):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        loginPage = LoginPage(self.driver)
        loginPage.access_login_page()
        loginPage.login(request.param, PASSWORD)
        assert not loginPage.login_error()
        inventoryPage = InventoryPage(self.driver)
        added_items_to_cart = CommonSteps.add_everything_to_cart(self)
        inventoryPage.click_shopping_cart()
        page = CartPage(self.driver)
        # Provide the driver instance to the test function
        yield [page, inventoryPage, added_items_to_cart, request.param]
        # Teardown
        self.driver.quit()
        # return inventoryPage
        return [page, inventoryPage, added_items_to_cart, request.param]

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    def test_continue_shopping(self, cart_page):
        cartPage, InventoryPage, items_added_to_cart, current_user = cart_page
        cartPage.click_continue_shopping()
        items = InventoryPage.get_items_all()
        items_in_cart = [item for item in items if item["in_cart"] == True]
        print("items: ", items, "items added to cart: ", items_added_to_cart)
        assert items_added_to_cart == items_in_cart

    def test_remove_item_from_cart(self, cart_page):
        cartPage, InventoryPage, items_added_to_cart, current_user = cart_page
        items_in_cart_original = cartPage.get_cart_items_all()
        time.sleep(1)
        cartPage.remove_item_by_name(items_in_cart_original[0]["name"])
        time.sleep(1)
        items_in_cart = cartPage.get_cart_items_all()
        assert items_in_cart == items_in_cart_original[1:]
        ## leaving cart back to shopping
        cartPage.click_continue_shopping()
        items = InventoryPage.get_items_all()
        items_in_cart = [item for item in items if item["in_cart"] == True]
        print("items: ", items, "items added to cart: ", items_added_to_cart)
        assert items_in_cart == items_added_to_cart[1:]

    # @data("locked_out_user", "standard_user")
    def test_checkout_cart(self, cart_page):
        cartPage, InventoryPage, items_added_to_cart, current_user = cart_page
        items_in_cart = cartPage.get_cart_items_all()
        print(
            "items_added_to_cart: ", items_added_to_cart, "items_in_cart", items_in_cart
        )

        assert items_in_cart == items_added_to_cart

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


if __name__ == "__main__":
    unittest.main()
