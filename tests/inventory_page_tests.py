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


@ddt
class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(BASE_URL)

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    def login(self, username):
        loginPage = LoginPage(self.driver)
        loginPage.login(username, PASSWORD)
        time.sleep(1)
        if self.driver.current_url == INVENTORY_URL:
            return True

    def add_everything_to_cart(self):
        inventoryPage = InventoryPage(self.driver)
        cart_quantity = inventoryPage.get_cart_quantity()
        assert_and_log(self, cart_quantity == 0, "Cart is empty")
        result = inventoryPage.add_to_cart_all()
        quantity = result["count"]
        names = result["item_names"]
        cart_quantity = inventoryPage.get_cart_quantity()
        assert_and_log(
            self, cart_quantity == quantity, "Cart has " + str(quantity) + " elements"
        )
        assert cart_quantity == quantity
        return names

    @data("standard_user", "visual_user", "error_user")
    def test_check_alignments(self, username):
        logged_in = CommonSteps.login(self, username)
        print("LOGGED IN::: ", logged_in)
        if not logged_in:
            return
            pass  # ¨return
        # Capture the initial screenshot
        if username == "standard_user":
            capture_screenshot(self.driver, "screenshot1.png")

        capture_screenshot(self.driver, "screenshot2.png")

        # Compare the screenshots for misalignment
        if compare_screenshots("screenshot1.png", "screenshot2.png"):
            print("Misalignment detected!")
        else:
            print("No misalignment.")

    @data("standard_user")
    def test_add_to_cart(self, username):
        if not CommonSteps().login(self, username):
            return
            pass
        self.add_everything_to_cart()

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

    @data("error_user")
    def test_sort(self, username):
        # loginPage = LoginPage(self.driver)
        logged_in = CommonSteps.login(self, username)
        print("LOGGED IN::: ", logged_in)
        if not logged_in:
            return
            pass  # ¨return

        inventoryPage = InventoryPage(self.driver)
        sort_values = ["hilo", "lohi", "az", "za"]
        counter = 0
        # items = inventoryPage.get_items_all()
        # print(items)
        for value in sort_values:
            time.sleep(1)
            inventoryPage.set_sort(value)
            items = inventoryPage.get_items_all()
            self.check_sort(counter, items)
            counter = counter + 1
        # alert = self.driver.switch_to.alert
        # # Close the alert
        # if alert:
        #     alert.accept()

    @data("standard_user")
    def test_add_to_cart_some_element(self, username):
        inventoryPage = InventoryPage(self.driver)
        CommonSteps.login(self, username)
        items = inventoryPage.get_items_all()

        to_be_added = [items[0]["name"], items[1]["name"]]
        print("TO BE ADDED:: ", to_be_added)
        for item_name in to_be_added:
            inventoryPage.add_item_to_cart_by_name(item_name)
        items_in_cart = [
            item["name"]
            for item in inventoryPage.get_items_all()
            if item["in_cart"] == True
        ]
        print("ITEMS:INCART ", items_in_cart)
        assert items_in_cart == to_be_added
        time.sleep(1)
        inventoryPage.remove_item_by_name(to_be_added[0])
        items_in_cart = [
            item["name"]
            for item in inventoryPage.get_items_all()
            if item["in_cart"] == True
        ]
        print("TO BE ADDED:: ", to_be_added[1])
        print("ITEMS:INCART ", items_in_cart)
        project_folder = os.getcwd()

        # Define the relative path to the desired folder
        relative_folder_path = "screenshots"

        # Build the full path to the folder within the project
        folder_path = os.path.join(project_folder, relative_folder_path)
        self.driver.save_screenshot(folder_path + "/image.png")
        assert items_in_cart == [to_be_added[1]]


if __name__ == "__main__":
    unittest.main()
