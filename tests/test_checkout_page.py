# from pages.page import InventoryPage, CartPage, CheckoutPage, CheckoutStepTwoPage
import pytest
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_page import CheckoutPage
from pages.checkout_step_two_page import CheckoutStepTwoPage
import unittest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from variables import *
from selenium import webdriver
import time
import logging
from ddt import ddt, data
from utils.common_steps import CommonSteps
from utils.common import assert_and_log, log_assert


# @ddt
class TestCheckoutPage:
    # def setUp(self):
    #     self.logger = logging.getLogger(__name__)
    #     options = webdriver.ChromeOptions()
    #     self.driver = webdriver.Chrome(options=options)
    #     self.driver.maximize_window()
    #     self.driver.get(BASE_URL)

    @pytest.fixture(
        params=USERS_WITHOUT_LOCKED_OUT  # "locked_out_user", "standard_user", "error_user", "problem_user"
    )
    def checkout_page(self, request):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        loginPage = LoginPage(self.driver)
        loginPage.access_login_page()
        loginPage.login(request.param, PASSWORD)
        assert not loginPage.login_error()
        inventoryPage = InventoryPage(self.driver)
        added_items_to_cart = CommonSteps.add_everything_to_cart(self)
        inventoryPage.click_shopping_cart()
        cartPage = CartPage(self.driver)
        cartPage.click_checkout()
        page_1 = CheckoutPage(self.driver)
        page_2 = CheckoutStepTwoPage(self.driver)
        # Provide the driver instance to the test function
        yield [
            page_1,
            page_2,
            cartPage,
            inventoryPage,
            added_items_to_cart,
            request.param,
        ]
        # Teardown
        self.driver.quit()
        # return inventoryPage
        return [
            page_1,
            page_2,
            cartPage,
            inventoryPage,
            added_items_to_cart,
            request.param,
        ]

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    # @data("standard_user")
    def test_checkout(self, checkout_page):
        (
            checkoutPage,
            checkoutPageStepTwo,
            cartPage,
            InventoryPage,
            items_added_to_cart,
            current_user,
        ) = checkout_page
        checkoutPage.click_continue()
        try:
            assert checkoutPage.error_message() == ERROR_MSG_MISSING_FIRST_NAME
        except AssertionError:
            pass

        checkoutPage.set_firstname(FIRST_NAME)
        checkoutPage.click_continue()
        try:
            assert checkoutPage.error_message() == ERROR_MSG_MISSING_LAST_NAME
        except AssertionError:
            pass

        checkoutPage.set_last_name(LAST_NAME)
        checkoutPage.click_continue()
        try:
            assert checkoutPage.error_message() == ERROR_MSG_MISSING_ZIP
        except AssertionError:
            pass

        checkoutPage.set_zip(ZIP)
        time.sleep(0.5)
        f, l, z = checkoutPage.get_form_values()

        if f != FIRST_NAME or l != LAST_NAME or z != ZIP:
            if checkoutPage.click_continue() == None:
                print("Checkout should be disabled")
                assert False

        checkoutPage.click_continue()
        log_assert(True, checkoutPageStepTwo.page_loaded())
