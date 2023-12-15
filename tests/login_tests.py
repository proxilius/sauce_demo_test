from pages.login_page import LoginPage

import unittest
from testcase.variables import *
from selenium import webdriver

import time
import logging
from ddt import ddt, data
from utils.common import assert_and_log


class LogintTests(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        # options.add_argument('--window-size=1420,1080')
        # options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)
        # self.driver.implicitly_wait(3)
        self.driver.maximize_window()
        loginPage = LoginPage(self.driver)
        # self.driver.get(BASE_URL)
        loginPage.access_login_page()

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    def test_login_valid(self):
        loginPage = LoginPage(self.driver)
        loginPage.login(STANDARD_USER, PASSWORD)
        assert_and_log(self, self.driver.current_url == INVENTORY_URL, "Login")
        assert self.driver.current_url == INVENTORY_URL

    def test_login_invalid(self):
        loginPage = LoginPage(self.driver)
        loginPage.login(STANDARD_USER, "invalid_pw")
        error_msg = loginPage.login_error()
        assert_and_log(self, error_msg == ERROR_MSG_WRONG_PASSWORD, "Login")


if __name__ == "__main__":
    unittest.main()
