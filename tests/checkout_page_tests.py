# from pages.page import InventoryPage, CartPage, CheckoutPage, CheckoutStepTwoPage

from pages.checkout_page import CheckoutPage
from pages.checkout_step_two_page import CheckoutStepTwoPage
import unittest
from testcase.variables import *
from selenium import webdriver
import time
import logging
from ddt import ddt, data
from utils.common_steps import CommonSteps
from utils.common import assert_and_log


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
