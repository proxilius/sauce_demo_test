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
from utils.common_steps import CommonSteps
from utils.common import assume_and_log


class TestCheckoutStepTwoPage:
    @pytest.fixture(
        params=USERS_WITHOUT_LOCKED_OUT
        # USERS_WITHOUT_LOCKED_OUT  # "locked_out_user", "standard_user", "error_user", "problem_user"
    )
    def checkout_step_two_page(self, request):
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
        page_1.set_firstname(FIRST_NAME)
        page_1.set_last_name(LAST_NAME)
        page_1.set_zip(ZIP)
        time.sleep(1)
        f, l, z = page_1.get_form_values()

        if f != FIRST_NAME or l != LAST_NAME or z != ZIP:
            if page_1.click_continue() == None:
                print("Checkout should be disabled")
                assert False

        page_1.click_continue()
        assert page_2.page_loaded()
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
    def test_complete_order(self, checkout_step_two_page):
        (
            checkoutPage,
            checkoutPageStepTwo,
            cartPage,
            inventoryPage,
            items_added_to_cart,
            current_user,
        ) = checkout_step_two_page
        time.sleep(1)
        data = checkoutPageStepTwo.get_items()
        names1 = [item["name"] for item in items_added_to_cart]
        names2 = [item["name"] for item in data]
        print("NAMES:::", names2, names1)
        assume_and_log(names1, names2)
        final_price = sum(item["price"] for item in data)
        price_equal = checkoutPageStepTwo.check_price(final_price)
        # assert_and_log(self, price_equal, "Total price is equal: ")
        assume_and_log(True, price_equal, "Price equals")

        if price_equal:
            checkoutPageStepTwo.click_finish()

        checkoutCompletePage = CheckoutCompletePage(self.driver)
        time.sleep(1)
        # assert checkoutCompletePage.checkout_complete()
        assume_and_log(
            True, checkoutCompletePage.checkout_complete(), "Checkout completed"
        )
        checkoutCompletePage.return_to_store()
        # assert self.driver.current_url == INVENTORY_URL
        assume_and_log(
            True, self.driver.current_url == INVENTORY_URL, "Return to products"
        )
        time.sleep(1)
