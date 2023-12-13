import pytest

# from pages.page import InventoryPage, CartPage, CheckoutPage, CheckoutStepTwoPage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.checkout_step_two_page import CheckoutStepTwoPage
import unittest
from testcase.variables import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
from ddt import ddt, data
import os


logging.basicConfig(
    filename="logfile.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class CommonSteps:
    @staticmethod
    def login(self, username):
        loginPage = LoginPage(self.driver)
        loginPage.login(username, PASSWORD)
        time.sleep(1)
        if self.driver.current_url == INVENTORY_URL:
            return True

    @staticmethod
    def add_everything_to_cart(self):
        inventoryPage = InventoryPage(self.driver)
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
        inventoryPage = InventoryPage(self.driver)
        cartPage = CartPage(self.driver)
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
        loginPage = LoginPage(self.driver)
        loginPage.login(STANDARD_USER, PASSWORD)
        assert_and_log(self, self.driver.current_url == INVENTORY_URL, "Login")

    def test_login_invalid(self):
        loginPage = LoginPage(self.driver)
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
        loginPage = LoginPage(self.driver)
        loginPage.login(username, PASSWORD)
        time.sleep(1)
        if self.driver.current_url == INVENTORY_URL:
            return True

    def add_everything_to_cart(self):
        inventoryPage = InventoryPage(self.driver)
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
        inventoryPage = InventoryPage(self.driver)
        cartPage = CartPage(self.driver)
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
        loginPage = LoginPage(self.driver)
        loginPage.login(CURRENT_USER, "secret_sauce")
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
        checkoutPage = CheckoutPage(self.driver)
        checkoutPageStepTwo = CheckoutStepTwoPage(self.driver)
        checkoutPage.click_continue()
        assert_and_log(
            self,
            checkoutPage.error_message() == ERROR_MSG_MISSING_FIRST_NAME,
            "First name is required",
        )
        checkoutPage.set_firstname("a")
        checkoutPage.click_continue()
        assert_and_log(
            self,
            checkoutPage.error_message() == ERROR_MSG_MISSING_LAST_NAME,
            "First name is required",
        )
        checkoutPage.set_last_name("b")
        checkoutPage.click_continue()
        assert_and_log(
            self,
            checkoutPage.error_message() == ERROR_MSG_MISSING_ZIP,
            "ZIP is required",
        )
        checkoutPage.set_zip("c")
        time.sleep(1)
        checkoutPage.click_continue()
        time.sleep(1)
        data = checkoutPageStepTwo.get_items()
        final_price = sum(item["price"] for item in data)
        price_equal = checkoutPageStepTwo.check_price(final_price)
        assert_and_log(self, price_equal, "Total price is equal: ")
        if price_equal:
            checkoutPageStepTwo.click_finish()

        time.sleep(1)


if __name__ == "__main__":
    unittest.main()
