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

logging.basicConfig(
    filename="logfile.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def assert_and_log(self, condition, message):
    try:
        assert condition
        self.logger.info(message + " PASSED")
    except AssertionError as e:
        self.logger.error(message + " FAILED" + f": {str(e)}")


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

    @pytest.mark.parametrize(
        "username, password",
        [("standard_user", "secret_sauce"), ("error_user", "pass2")],
    )
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

    def login(self):
        loginPage = page.LoginPage(self.driver)
        loginPage.login(CURRENT_USER, PASSWORD)
        time.sleep(1)
        if self.driver.current_url == INVENTORY_URL:
            return True

    def test_add_to_cart(self):
        if not self.login():  # check if login is successfull, otherwise end test
            pass  # ¨return
        inventoryPage = page.InventoryPage(self.driver)
        x = inventoryPage.get_cart_quantity()
        # assert x == 0
        assert_and_log(self, x == 0, "Cart is empty")
        quantity = inventoryPage.add_to_cart_all()
        x = inventoryPage.get_cart_quantity()
        # assert x == quantity
        assert_and_log(self, x == quantity, "Cart has " + str(quantity) + " elements")

    def test_sort(self):
        loginPage = page.LoginPage(self.driver)
        loginPage.login(CURRENT_USER, "secret_sauce")
        inventoryPage = page.InventoryPage(self.driver)
        sort_values = ["hilo", "lohi", "az", "za"]
        for value in sort_values:
            time.sleep(1)
            inventoryPage.set_sort(value)


if __name__ == "__main__":
    unittest.main()
