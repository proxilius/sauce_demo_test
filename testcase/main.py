import unittest
from variables import *
from selenium import webdriver
import page
from selenium.webdriver.chrome.options import Options
import time
import pytest
import logging

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

    @pytest.mark.parametrize(
        "username, password",
        [("standard_user", "secret_sauce"), ("error_user", "pass2")],
    )
    def test_login_valid(self):
        loginPage = page.LoginPage(self.driver)
        loginPage.set_credentials("standard_user", "secret_sauce")
        # mainPage.username_element = 'standard_user'
        loginPage.click_login_button()
        assert self.driver.current_url == INVENTORY_URL
        assert_and_log(self, self.driver.current_url == INVENTORY_URL, "Login")
        self.logger.info("Performed an action successfully")

    def test_login_invalid(self):
        loginPage = page.LoginPage(self.driver)
        loginPage.set_credentials("standard_user", "-")
        # mainPage.username_element = 'standard_user'
        loginPage.click_login_button()
        error_msg = loginPage.seek_error()
        assert error_msg == ERROR_MSG_WRONG_PASSWORD
        assert_and_log(self, self.driver.current_url == INVENTORY_URL, "Login")
        self.logger.info("Performed an action successfully")

    def test_add_to_cart(self):
        self.test_login_valid()
        time.sleep(1)
        inventoryPage = page.InventoryPage(self.driver)
        x = inventoryPage.get_cart_quantity()
        assert x == 0
        quantity = inventoryPage.add_to_cart_all()
        x = inventoryPage.get_cart_quantity()
        assert x == quantity

    def test_sort(self):
        self.test_login_valid()
        inventoryPage = page.InventoryPage(self.driver)
        sort_values = ["hilo", "lohi", "az", "za"]
        for value in sort_values:
            time.sleep(1)
            inventoryPage.set_sort(value)

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    def smoke_suite():
        suiteFew = unittest.TestSuite()
        suiteFew.addTest(LogintTests("test_login"))
        return suiteFew


if __name__ == "__main__":
    unittest.main()
