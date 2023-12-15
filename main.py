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


from utils.common import assert_and_log
from tests.test_login_page import TestLoginPage
from tests.test_inventory_page import TestInventoryPage
from tests.test_checkout_page import TestCheckoutPage
from tests.test_cart_page import TestCartPage


# test_suite = unittest.TestLoader().loadTestsFromTestCase(TestLoginPage)
# test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestInventoryPage))
# test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCheckoutPage))
# test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCartPage))

# unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == "__main__":
    unittest.main()
