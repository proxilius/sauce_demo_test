import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.item_page import ItemPage
import unittest
from variables import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
from ddt import ddt, data
import os
from utils.common import assert_and_log, log_assert
from utils.common_steps import CommonSteps
from utils.common import capture_screenshot, compare_screenshots


# @ddt
class TestInventoryPage:
    # def setUp(self):
    #     self.logger = logging.getLogger(__name__)
    #     options = webdriver.ChromeOptions()
    #     self.driver = webdriver.Chrome(options=options)
    #     self.driver.maximize_window()
    #     loginPage = LoginPage(self.driver)
    #     self.driver.get(BASE_URL)
    #     # loginPage.access_login_page()
    #     # return loginPage

    @pytest.fixture(params=USERS_WITHOUT_LOCKED_OUT)
    def inventory_page(self, request):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        loginPage = LoginPage(self.driver)
        loginPage.access_login_page()
        loginPage.login(request.param, PASSWORD)
        inventoryPage = InventoryPage(self.driver)
        # Provide the driver instance to the test function
        yield [inventoryPage, request.param]
        # Teardown
        self.driver.quit()
        # return inventoryPage
        return [inventoryPage, request.param]

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    # @pytest.mark.parametrize("username", ["standard_user", "error_user", "visual_user"])
    def test_check_alignments(self, inventory_page):
        inventoryPage, username = inventory_page
        project_folder = os.getcwd()
        # base_screenshot_path = os.path.join(
        #     project_folder, "./screenshots/base_screenshot.png"
        # )
        base_screenshot_path = "./screenshots/base_screenshot.png"
        screenshot_to_compare_path = "./screenshots/screenshot_to_compare.png"
        # screenshot_to_compare_path = os.path.join(
        #     project_folder, "/screenshots/screenshot_to_compare.png"
        # )
        time.sleep(0.5)
        if username == "standard_user":
            capture_screenshot(self.driver, base_screenshot_path)

        capture_screenshot(self.driver, screenshot_to_compare_path)

        if compare_screenshots(base_screenshot_path, screenshot_to_compare_path):
            print("Misalignment detected!")
            log_assert(True, False, "Misalignment detected!")
            # assert False
        else:
            print("No misalignment.")
            log_assert(True, True, "No misalignment")
            # assert_and_log(True, "No misalignment.")
            # assert True

    # @data("standard_user")
    def test_add_to_cart(self, inventory_page):
        CommonSteps.add_everything_to_cart(self)

    def check_sort(self, counter, current_items):
        item_names = [i["name"] for i in current_items]
        item_prices = [i["price"] for i in current_items]

        if counter == 0:
            assert item_prices == sorted(item_prices, reverse=True)
            return
        if counter == 1:
            assert item_prices == sorted(item_prices)
            return
        if counter == 2:
            assert item_names == sorted(item_names)
            return
        if counter == 3:
            assert item_names == sorted(item_names, reverse=True)
            return

    # @data("error_user")
    def test_sort(self, inventory_page):
        inventoryPage, username = inventory_page
        sort_values = ["hilo", "lohi", "az", "za"]
        counter = 0
        for value in sort_values:
            time.sleep(1)
            inventoryPage.set_sort(value)
            items = inventoryPage.get_items_all()
            self.check_sort(counter, items)
            counter = counter + 1

    # @data("standard_user")
    def test_add_to_cart_some_element(self, inventory_page):
        inventoryPage, username = inventory_page
        items = inventoryPage.get_items_all()
        to_be_added = [items[0], items[1]]
        for item in to_be_added:
            if not item["in_cart"]:
                inventoryPage.add_item_to_cart_by_name(item["name"])
        items_in_cart = [
            item for item in inventoryPage.get_items_all() if item["in_cart"] == True
        ]

        # assert [item["name"] for item in items_in_cart] == [
        #     item["name"] for item in to_be_added
        # ]
        log_assert(
            [item["name"] for item in items_in_cart],
            [item["name"] for item in to_be_added],
        )
        time.sleep(1)
        inventoryPage.remove_item_by_name(to_be_added[0]["name"])
        items_in_cart = [
            item for item in inventoryPage.get_items_all() if item["in_cart"] == True
        ]

        # assert [item["name"] for item in items_in_cart] == [to_be_added[1]["name"]]
        log_assert([item["name"] for item in items_in_cart], [to_be_added[1]["name"]])

    # @data("standard_user")
    def test_logout(self, inventory_page):
        inventoryPage, username = inventory_page
        if not inventoryPage:
            return
        inventoryPage.logout()

    def test_remove_item_from_item_page(self, inventory_page):
        inventoryPage, username = inventory_page
        items_in_cart = CommonSteps.add_everything_to_cart(self)
        inventoryPage.click_item_by_name(items_in_cart[0]["name"])
        itemPage = ItemPage(self.driver)
        log_assert(True, itemPage.item_page_loaded())
        itemPage.click_add_remove_button("remove")
        itemPage.click_back_to_products()
        items_after_remove = [
            item for item in inventoryPage.get_items_all() if item["in_cart"] == True
        ]
        log_assert(items_after_remove, items_in_cart[1:])

    def test_add_item_from_item_page(self, inventory_page):
        inventoryPage, username = inventory_page
        items = inventoryPage.get_items_all()
        inventoryPage.click_item_by_name(items[0]["name"])
        itemPage = ItemPage(self.driver)
        log_assert(True, itemPage.item_page_loaded(), "Item page is loaded")
        log_assert(True, itemPage.check_item_loaded(items[0]), "Correct item is loaded")
        itemPage.click_add_remove_button("add")
        itemPage.click_back_to_products()
        items_after_adding = [
            item for item in inventoryPage.get_items_all() if item["in_cart"] == True
        ]
        items = inventoryPage.get_items_all()
        items_assert = []
        items_assert.append(items[0])
        log_assert(items_assert, items_after_adding)


if __name__ == "__main__":
    unittest.main()
