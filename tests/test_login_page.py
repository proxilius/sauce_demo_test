import pytest
from pages.login_page import LoginPage
import unittest
from variables import *
from selenium import webdriver
import time
import logging
from utils.common import assume_and_log

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

    def tearDown(self):
        time.sleep(1)
        self.driver.close()

    @pytest.mark.parametrize(
        "username",
        USERS_WITHOUT_LOCKED_OUT,
    )
    def test_login_valid(self, login_page, username):
        login_page.login(username, PASSWORD)
        assume_and_log(INVENTORY_URL, self.driver.current_url)

    @pytest.mark.parametrize("username", USERS_WITHOUT_LOCKED_OUT)
    def test_login_invalid(self, login_page, username):
        login_page.login(username, "invalid_pw")
        error_msg = login_page.login_error()
        assume_and_log(ERROR_MSG_WRONG_PASSWORD, error_msg)

    def test_login_locked_out_user(self, login_page):
        login_page.login(LOCKED_OUT_USER, PASSWORD)
        error_msg = login_page.login_error()
        assume_and_log(ERROR_LOCKED_OUT_USER, error_msg)


if __name__ == "__main__":
    unittest.main()
