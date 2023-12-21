import pytest
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_page import CheckoutPage
from pages.checkout_step_two_page import CheckoutStepTwoPage
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
        params=["standard_user", "performance_glitch_user", "visual_user"]
    )  # problem_user and error_user cant checkout
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

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    def test_check_total_price(self, checkout_step_two_page):
        (
            checkoutPage,
            checkoutPageStepTwo,
            cartPage,
            inventoryPage,
            items_added_to_cart,
            current_user,
        ) = checkout_step_two_page
        time.sleep(1)
        items = checkoutPageStepTwo.get_items()
        names1 = [item["name"] for item in items_added_to_cart]
        names2 = [item["name"] for item in items]
        assume_and_log(names1, names2)
        final_price = sum(item["price"] for item in items)
        price_equal = checkoutPageStepTwo.check_price(final_price)
        assume_and_log(True, price_equal, "Price equals")

    def test_complete_order(self, checkout_step_two_page):
        (
            checkoutPage,
            checkoutPageStepTwo,
            cartPage,
            inventoryPage,
            items_added_to_cart,
            current_user,
        ) = checkout_step_two_page
        checkoutCompletePage = CheckoutCompletePage(self.driver)
        time.sleep(1)
        checkoutPageStepTwo.click_finish()
        assume_and_log(
            True, checkoutCompletePage.checkout_complete(), "Checkout completed"
        )
        checkoutCompletePage.return_to_store()
        assume_and_log(
            True, self.driver.current_url == INVENTORY_URL, "Return to products"
        )
        time.sleep(1)

    def test_cancel_order(self, checkout_step_two_page):
        (
            checkoutPage,
            checkoutPageStepTwo,
            cartPage,
            inventoryPage,
            items_added_to_cart,
            current_user,
        ) = checkout_step_two_page
        checkoutPageStepTwo.click_cancel()
        assume_and_log(self.driver.current_url, INVENTORY_URL)
