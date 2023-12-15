import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
import unittest
from testcase.variables import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
from ddt import ddt, data
import os
from utils.common import assert_and_log
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

    @pytest.fixture(params=["standard_user", "error_user", "problem_user"])
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
        yield [self.driver, inventoryPage, request.param]
        # Teardown
        self.driver.quit()
        # return inventoryPage
        return [self.driver, inventoryPage, request.param]

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    # @pytest.mark.parametrize("username", ["standard_user", "error_user", "visual_user"])
    def test_check_alignments(self, inventory_page):
        username = inventory_page[2]
        if username == "standard_user":
            capture_screenshot(self.driver, "screenshot1.png")

        capture_screenshot(self.driver, "screenshot2.png")

        # Compare the screenshots for misalignment
        if compare_screenshots("screenshot1.png", "screenshot2.png"):
            print("Misalignment detected!")
            assert False
        else:
            print("No misalignment.")
            assert True

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
        inventoryPage = inventory_page[1]
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
        inventoryPage = inventory_page[1]
        items = inventoryPage.get_items_all()
        to_be_added = [items[0], items[1]]
        for item in to_be_added:
            if not item["in_cart"]:
                inventory_page.add_item_to_cart_by_name(item["name"])
        items_in_cart = [
            item for item in inventory_page.get_items_all() if item["in_cart"] == True
        ]

        assert [item["name"] for item in items_in_cart] == [
            item["name"] for item in to_be_added
        ]
        time.sleep(1)
        inventory_page.remove_item_by_name(to_be_added[0]["name"])
        items_in_cart = [
            item for item in inventory_page.get_items_all() if item["in_cart"] == True
        ]

        assert [item["name"] for item in items_in_cart] == [to_be_added[1]["name"]]

    # @data("standard_user")
    def test_logout(self, inventory_page):
        inventoryPage = inventory_page[1]
        print("PAGEEEEEEEEEEEEEEEEEEEE", inventoryPage)
        if not inventoryPage:
            return
        inventoryPage.logout()


if __name__ == "__main__":
    unittest.main()
