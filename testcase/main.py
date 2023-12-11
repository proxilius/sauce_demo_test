import unittest
from variables import *
from selenium import webdriver
import page
from selenium.webdriver.chrome.options import Options
import time
import pytest
import logging
import sys
import argparse
from ddt import ddt, data


logging.basicConfig(
    filename="logfile.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class CommonSteps:
    @staticmethod
    def login(self, username):
        loginPage = page.LoginPage(self.driver)
        loginPage.login(username, PASSWORD)
        time.sleep(1)
        if self.driver.current_url == INVENTORY_URL:
            return True

    @staticmethod
    def add_everything_to_cart(self):
        inventoryPage = page.InventoryPage(self.driver)
        x = inventoryPage.get_cart_quantity()
        # assert x == 0
        assert_and_log(self, x == 0, "Cart is empty")
        result = inventoryPage.add_to_cart_all()
        quantity = result["count"]
        names = result["item_names"]
        x = inventoryPage.get_cart_quantity()
        assert_and_log(self, x == quantity, "Cart has " + str(quantity) + " elements")
        return names

    @staticmethod
    def checkout(self, items_added_to_cart):
        inventoryPage = page.InventoryPage(self.driver)
        cartPage = page.CartPage(self.driver)
        items_added_to_cart = items_added_to_cart
        inventoryPage.click_shopping_cart()
        items_in_cart = cartPage.get_cart_items_all()
        # print(
        #     "items_added_to_cart: ", items_added_to_cart, "items_in_cart", items_in_cart
        # )
        assert_and_log(
            self,
            items_added_to_cart == items_in_cart,
            "Cart items are the same as items added previously",
        )
        if len(items_in_cart) > 0:
            cartPage.click_checkout()
        else:
            if cartPage.click_checkout() == None:
                assert_and_log(
                    self,
                    False,
                    "Cart is empty, checkout should be disabled",
                )


def assert_and_log(self, condition, message):
    try:
        assert condition
        self.logger.info(message + " PASSED")
    except AssertionError as e:
        self.logger.error(message + " FAILED" + f": {str(e)}")


@pytest.mark.parametrize(
    "username, password",
    [("standard_user", "secret_sauce"), ("error_user", "pass2")],
)
class LogintTests(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        # options.add_argument('--window-size=1420,1080')
        # options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)
        # self.driver.implicitly_wait(3)
        self.driver.maximize_window()
        self.driver.get(BASE_URL)

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    def test_login_valid(self):
        loginPage = page.LoginPage(self.driver)
        loginPage.login(STANDARD_USER, PASSWORD)
        assert_and_log(self, self.driver.current_url == INVENTORY_URL, "Login")

    def test_login_invalid(self):
        loginPage = page.LoginPage(self.driver)
        loginPage.login(STANDARD_USER, "invalid_pw")
        error_msg = loginPage.seek_error()
        assert_and_log(self, error_msg == ERROR_MSG_WRONG_PASSWORD, "Login")

    def smoke_suite():
        suiteFew = unittest.TestSuite()
        suiteFew.addTest(LogintTests("test_login"))
        return suiteFew


@ddt
class CartTests(unittest.TestCase):
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
        loginPage = page.LoginPage(self.driver)
        loginPage.login(username, PASSWORD)
        time.sleep(1)
        if self.driver.current_url == INVENTORY_URL:
            return True

    def add_everything_to_cart(self):
        inventoryPage = page.InventoryPage(self.driver)
        x = inventoryPage.get_cart_quantity()
        # assert x == 0
        assert_and_log(self, x == 0, "Cart is empty")
        result = inventoryPage.add_to_cart_all()
        quantity = result["count"]
        names = result["item_names"]
        x = inventoryPage.get_cart_quantity()
        assert_and_log(self, x == quantity, "Cart has " + str(quantity) + " elements")
        return names

    @data("standard_user")
    def test_add_to_cart(self, username):
        if not self.login(
            username
        ):  # check if login is successfull, otherwise end test
            pass  # ¨return
        self.add_everything_to_cart()

    @data("standard_user")
    def test_checkout(self, username):
        inventoryPage = page.InventoryPage(self.driver)
        cartPage = page.CartPage(self.driver)
        if not self.login(
            username
        ):  # check if login is successfull, otherwise end test
            pass  # ¨return
        items_added_to_cart = self.add_everything_to_cart()
        inventoryPage.click_shopping_cart()
        items_in_cart = cartPage.get_cart_items_all()
        # print(
        #     "items_added_to_cart: ", items_added_to_cart, "items_in_cart", items_in_cart
        # )
        assert_and_log(
            self,
            items_added_to_cart == items_in_cart,
            "Cart items are the same as items added previously",
        )
        if len(items_in_cart) > 0:
            cartPage.click_checkout()
        else:
            if cartPage.click_checkout() == None:
                assert_and_log(
                    self,
                    False,
                    "Cart is empty, checkout should be disabled",
                )

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

    def test_sort(self):
        loginPage = page.LoginPage(self.driver)
        loginPage.login(CURRENT_USER, "secret_sauce")
        inventoryPage = page.InventoryPage(self.driver)
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


@ddt
class CheckoutTests(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(BASE_URL)

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    @data("standard_user")
    def test_checkout_final(self, username):
        CommonSteps().login(self, username)
        added_to_cart = CommonSteps().add_everything_to_cart(self)
        CommonSteps.checkout(self, added_to_cart)
        checkoutPage = page.CheckoutPage(self.driver)
        checkoutPage.set_firstname("a")
        checkoutPage.set_last_name("b")
        checkoutPage.set_zip("c")
        time.sleep(1)
        checkoutPage.click_continue()
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()
