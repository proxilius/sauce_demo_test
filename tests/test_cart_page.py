from ddt import ddt, data
import unittest
import time
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.item_page import ItemPage
from variables import *
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.common import assert_and_log, assume_and_log
from utils.common_steps import CommonSteps
from utils.common import capture_screenshot, compare_screenshots
import os


class TestCartPage:
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
        items_added_to_cart = CommonSteps.add_everything_to_cart(self)
        inventoryPage.click_shopping_cart()
        page = CartPage(self.driver)
        # Provide the driver instance to the test function
        yield [page, inventoryPage, items_added_to_cart, request.param]
        # Teardown
        self.driver.quit()
        # return inventoryPage
        return [page, inventoryPage, items_added_to_cart, request.param]

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    def test_continue_shopping(self, cart_page):
        cartPage, inventoryPage, items_added_to_cart, current_user = cart_page
        cartPage.click_continue_shopping()
        items = inventoryPage.get_items_all()
        items_in_cart = [item for item in items if item["in_cart"] == True]
        print("items: ", items, "items added to cart: ", items_added_to_cart)
        assert items_added_to_cart == items_in_cart

    def test_remove_item_from_cart(self, cart_page):
        cartPage, inventoryPage, items_added_to_cart, current_user = cart_page
        items_in_cart_original = cartPage.get_cart_items_all()
        time.sleep(1)
        cartPage.remove_item_by_name(items_in_cart_original[0]["name"])
        time.sleep(1)
        items_in_cart = cartPage.get_cart_items_all()
        assume_and_log(items_in_cart_original[1:], items_in_cart)
        ## leaving cart back to shopping
        cartPage.click_continue_shopping()
        items = inventoryPage.get_items_all()
        items_in_cart = [item for item in items if item["in_cart"] == True]
        print("items: ", items, "items added to cart: ", items_added_to_cart)
        assume_and_log(items_added_to_cart[1:], items_in_cart)

    def test_from_item_page_remove_item_from_cart(self, cart_page):
        cartPage, InventoryPage, items_added_to_cart, current_user = cart_page
        items_in_cart_original = cartPage.get_cart_items_all()
        time.sleep(1)
        cartPage.click_item_by_name(items_in_cart_original[0]["name"])
        itemPage = ItemPage(self.driver)
        assume_and_log(True, itemPage.item_page_loaded(), "Item page is loaded")
        assume_and_log(
            True,
            itemPage.check_item_loaded(items_in_cart_original[0]),
            "Correct item is loaded",
        )
        itemPage.click_add_remove_button("remove")
        itemPage.click_back_to_products()
        InventoryPage.click_shopping_cart()
        items_in_cart_after_remove = cartPage.get_cart_items_all()
        assume_and_log(items_in_cart_original[1:], items_in_cart_after_remove)
        ## leaving cart back to shopping
        cartPage.click_continue_shopping()
        items = InventoryPage.get_items_all()
        items_in_cart = [item for item in items if item["in_cart"] == True]
        print("items: ", items, "items added to cart: ", items_added_to_cart)
        assume_and_log(items_added_to_cart[1:], items_in_cart)

    # @data("locked_out_user", "standard_user")
    def test_checkout_cart(self, cart_page):
        cartPage, InventoryPage, items_added_to_cart, current_user = cart_page
        items_in_cart = cartPage.get_cart_items_all()
        print(
            "items_added_to_cart: ", items_added_to_cart, "items_in_cart", items_in_cart
        )

        assume_and_log(items_added_to_cart, items_in_cart)

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

    def test_checkout2_cart_with_zero_elements(self, cart_page):
        cartPage, InventoryPage, items_added_to_cart, current_user = cart_page
        items_in_cart = cartPage.get_cart_items_all()
        time.sleep(2)

        for item in items_in_cart:
            cartPage.remove_item_by_name(item["name"])

        quantity = cartPage.get_cart_quantity()
        assume_and_log(0, quantity)
        if quantity == 0:
            if cartPage.click_checkout() == None:
                assume_and_log(
                    True, False, "Checkout should be disabled with empty cart"
                )
        else:
            print("Cart is not empty")

    def test_check_alignments_cart_page(self, cart_page):
        cartPage, InventoryPage, items_added_to_cart, current_user = cart_page
        items_in_cart = cartPage.get_cart_items_all()
        time.sleep(2)

        for item in items_in_cart:
            cartPage.remove_item_by_name(item["name"])
        time.sleep(2)
        project_folder = os.getcwd()
        # base_screenshot_path = os.path.join(
        #     project_folder, "./screenshots/base_screenshot.png"
        # )
        base_screenshot_path = "./screenshots/base_screenshot_cart_page.png"
        screenshot_to_compare_path = "./screenshots/screenshot_to_compare_cart_page.png"
        # screenshot_to_compare_path = os.path.join(
        #     project_folder, "/screenshots/screenshot_to_compare.png"
        # )
        time.sleep(0.5)
        if current_user == "standard_user":
            capture_screenshot(self.driver, base_screenshot_path)

        capture_screenshot(self.driver, screenshot_to_compare_path)

        if compare_screenshots(base_screenshot_path, screenshot_to_compare_path, 0.2):
            print("Misalignment detected!")
            assume_and_log(True, False, "Misalignment detected!")
            # assert False
        else:
            print("No misalignment.")
            assume_and_log(True, True, "No misalignment")
            # assert_and_log(True, "No misalignment.")
            # assert True


if __name__ == "__main__":
    unittest.main()
