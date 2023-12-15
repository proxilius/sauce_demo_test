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
from tests.login_tests import LogintTests
from tests.inventory_page_tests import InventoryTests
from tests.checkout_page_tests import CheckoutTests
from tests.cart_page_tests import CartPageTests


# test_suite = unittest.TestLoader().loadTestsFromTestCase(LogintTests)
# test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CartPageTests))
# test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(InventoryTests))
# test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CheckoutTests))

# unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == "__main__":
    unittest.main()
