import pytest
from selenium import webdriver
import re
from testcase.variables import *
import logging


def pytest_addoption(parser):
    parser.addoption(
        "--baseurl",
        action="store",
        default="https://www.saucedemo.com/",
        help="Base URL for the application under test",
    )


@pytest.fixture
def driver(request):
    driver_ = webdriver.Chrome()

    driver_.base_url = BASE_URL
    driver_.base_domain = re.sub(".*//", "", BASE_URL)

    def quit_browser():
        driver_.quit()

    request.addfinalizer(quit_browser)
    return driver_


@pytest.fixture(scope="session")
def logger():
    # Configure the logger
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)
