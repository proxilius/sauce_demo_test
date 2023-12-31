import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.item_page import ItemPage
import unittest
from variables import *
from selenium import webdriver
import time
import logging
from utils.common import assume_and_log
from utils.common_steps import CommonSteps
from utils.common import capture_screenshot, compare_screenshots


class TestInventoryPage:
    @pytest.fixture(params=USERS_WITHOUT_LOCKED_OUT)
    def inventory_page(self, request):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        loginPage = LoginPage(self.driver)
        loginPage.access_login_page()
        loginPage.login(request.param, PASSWORD)
        assert not loginPage.login_error()
        inventoryPage = InventoryPage(self.driver)
        # Provide the driver instance to the test function
        yield [inventoryPage, request.param]
        # Teardown
        self.driver.quit()

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    def test_check_alignments_inventory_page(self, inventory_page):
        inventoryPage, username = inventory_page
        base_screenshot_path = "./screenshots/base_screenshot_inventory_page.png"
        screenshot_to_compare_path = (
            "./screenshots/screenshot_to_compare_inventory_page.png"
        )
        time.sleep(0.5)
        if username == "standard_user":
            capture_screenshot(self.driver, base_screenshot_path)

        capture_screenshot(self.driver, screenshot_to_compare_path)

        if compare_screenshots(base_screenshot_path, screenshot_to_compare_path):
            print("Misalignment detected!")
            assume_and_log(True, False, "Misalignment detected!")
        else:
            print("No misalignment.")
            assume_and_log(True, True, "No misalignment")

    def test_add_to_cart_everything(self, inventory_page):
        inventoryPage, username = inventory_page
        CommonSteps.add_everything_to_cart(self)
        quantity = inventoryPage.get_cart_quantity()
        items = inventoryPage.get_items_all()
        assume_and_log(quantity, len(items))

    def check_sort(self, counter, current_items):
        item_names = [i["name"] for i in current_items]
        item_prices = [i["price"] for i in current_items]

        if counter == 0:
            assume_and_log(item_prices, sorted(item_prices, reverse=True))
            return
        if counter == 1:
            assume_and_log(item_prices, sorted(item_prices))
            return
        if counter == 2:
            assume_and_log(item_names, sorted(item_names))
            return
        if counter == 3:
            assume_and_log(item_names, sorted(item_names, reverse=True))
            return

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

        assume_and_log(
            [item["name"] for item in items_in_cart],
            [item["name"] for item in to_be_added],
        )
        time.sleep(1)
        inventoryPage.remove_item_by_name(to_be_added[0]["name"])
        items_in_cart = [
            item for item in inventoryPage.get_items_all() if item["in_cart"] == True
        ]

        assume_and_log(
            [item["name"] for item in items_in_cart], [to_be_added[1]["name"]]
        )

    def test_logout(self, inventory_page):
        inventoryPage, username = inventory_page
        if not inventoryPage:
            return
        inventoryPage.logout()

    def test_remove_item_from_item_page(self, inventory_page):
        inventoryPage, username = inventory_page
        itemPage = ItemPage(self.driver)
        items_in_cart = CommonSteps.add_everything_to_cart(self)
        for item in items_in_cart:
            inventoryPage.click_item_by_name(item["name"])
            assume_and_log(True, itemPage.item_page_loaded())
            itemPage.click_add_remove_button("remove")
            itemPage.click_back_to_products()

        items_after_remove = [
            item for item in inventoryPage.get_items_all() if item["in_cart"] == True
        ]
        quantity = inventoryPage.get_cart_quantity()
        assume_and_log(0, quantity, "Cart quantity equals")
        assume_and_log(items_after_remove, [])  # items_in_cart[1:]

    def test_add_item_from_item_page(self, inventory_page):
        inventoryPage, username = inventory_page
        items = inventoryPage.get_items_all()
        inventoryPage.click_item_by_name(items[0]["name"])
        itemPage = ItemPage(self.driver)
        assume_and_log(True, itemPage.item_page_loaded(), "Item page is loaded")
        assume_and_log(
            True, itemPage.check_item_loaded(items[0]), "Correct item is loaded"
        )
        itemPage.click_add_remove_button("add")
        itemPage.click_back_to_products()
        items_after_adding = [
            item for item in inventoryPage.get_items_all() if item["in_cart"] == True
        ]
        items = inventoryPage.get_items_all()
        assume_and_log([items[0]], items_after_adding)

    def test_reset_state(self, inventory_page):
        inventoryPage, username = inventory_page
        CommonSteps.add_everything_to_cart(self)
        inventoryPage.click_reset_state()
        items_in_cart = [
            item for item in inventoryPage.get_items_all() if item["in_cart"] == True
        ]
        quantity = inventoryPage.get_cart_quantity()
        # after reset, cart should be empty
        assume_and_log(0, quantity, "Cart is empty")
        assume_and_log([], items_in_cart, "Items should show Add to cart")


if __name__ == "__main__":
    unittest.main()
