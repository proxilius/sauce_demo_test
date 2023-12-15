from ddt import ddt, data
import unittest
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from testcase.variables import *
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.common import assert_and_log
from utils.common_steps import CommonSteps


@ddt
class CartPageTests(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(BASE_URL)

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    @data("locked_out_user", "standard_user")
    def test_checkout_half(self, username):
        inventoryPage = InventoryPage(self.driver)
        cartPage = CartPage(self.driver)
        if not CommonSteps().login(self, username):
            return
            pass  # ¨return
        items_added_to_cart = CommonSteps.add_everything_to_cart(self)
        inventoryPage.click_shopping_cart()
        items_in_cart = cartPage.get_cart_items_all()
        print(
            "items_added_to_cart: ", items_added_to_cart, "items_in_cart", items_in_cart
        )

        assert items_in_cart == items_added_to_cart

        if len(items_in_cart) > 0:
            cartPage.click_checkout()
        else:
            if cartPage.click_checkout() == None:
                assert_and_log(
                    self,
                    False,
                    "Cart is empty, checkout should be disabled",
                )


if __name__ == "__main__":
    unittest.main()
