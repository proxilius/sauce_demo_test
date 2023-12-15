import pytest
from pages.login_page import LoginPage

import unittest
from testcase.variables import *
from selenium import webdriver

import time
import logging
from ddt import ddt, data
from utils.common import assert_and_log


class TestLoginPage:
    @pytest.fixture
    def login_page(self):
        self.logger = logging.getLogger(__name__)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        loginPage = LoginPage(self.driver)
        self.driver.get(BASE_URL)
        loginPage.access_login_page()
        return loginPage

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    @pytest.mark.parametrize("username", ["standard_user", "error_user", "visual_user"])
    def test_login_valid(self, login_page, username):
        # loginPage = LoginPage(self.driver)
        login_page.login(username, PASSWORD)
        assert_and_log(self, self.driver.current_url == INVENTORY_URL, "Login")
        assert self.driver.current_url == INVENTORY_URL

    @pytest.mark.parametrize("username", ["standard_user", "error_user", "visual_user"])
    def test_login_invalid(self, login_page, username):
        # loginPage = LoginPage(self.driver)
        login_page.login(username, "invalid_pw")
        error_msg = login_page.login_error()
        assert_and_log(self, error_msg == ERROR_MSG_WRONG_PASSWORD, "Login")
        assert error_msg == ERROR_MSG_WRONG_PASSWORD

    def test_login_locked_out_user(self, login_page):
        # loginPage = LoginPage(self.driver)
        login_page.login(LOCKED_OUT_USER, PASSWORD)
        error_msg = login_page.login_error()
        assert_and_log(self, error_msg == ERROR_MSG_WRONG_PASSWORD, "Login")
        assert error_msg == ERROR_LOCKED_OUT_USER


if __name__ == "__main__":
    unittest.main()
