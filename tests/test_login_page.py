import pytest
from pages.login_page import LoginPage

import unittest
from testcase.variables import *
from selenium import webdriver

import time
import logging
from ddt import ddt, data
from utils.common import assert_and_log, log_assert
import os

logging.basicConfig(
    filename="logfile.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


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
        yield loginPage
        # Teardown
        self.driver.quit()
        # return inventoryPage
        return loginPage

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    @pytest.mark.parametrize(
        "username",
        ["standard_user", "error_user", "visual_user"],
    )
    def test_login_valid(self, login_page, username):
        login_page.login(username, PASSWORD)
        # assert_and_log(
        #     self.driver.current_url == INVENTORY_URL,
        #     "Valid login attempt",
        # )
        log_assert(INVENTORY_URL, self.driver.current_url)
        # assert self.driver.current_url == INVENTORY_URL

    @pytest.mark.parametrize("username", ["standard_user", "error_user", "visual_user"])
    def test_login_invalid(self, login_page, username):
        login_page.login(username, "invalid_pw")
        error_msg = login_page.login_error()
        # assert_and_log(
        #     error_msg == ERROR_MSG_WRONG_PASSWORD,
        #     "Invalid login attempt",
        # )
        log_assert(ERROR_MSG_WRONG_PASSWORD, error_msg)
        # assert error_msg == ERROR_MSG_WRONG_PASSWORD

    def test_login_locked_out_user(self, login_page):
        # loginPage = LoginPage(self.driver)
        login_page.login(LOCKED_OUT_USER, PASSWORD)
        error_msg = login_page.login_error()
        # assert_and_log(
        #     error_msg == ERROR_LOCKED_OUT_USER,
        #     "Locked out user login attempt",
        # )
        log_assert(ERROR_LOCKED_OUT_USER, error_msg)
        # assert error_msg == ERROR_LOCKED_OUT_USER


if __name__ == "__main__":
    unittest.main()
