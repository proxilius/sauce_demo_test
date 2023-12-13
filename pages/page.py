from locators.locator import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from pages.base_page import BasePage

# class UsernameElement(BasePageElement):
#     locator=LoginPageLocators.USERNAME

# class PasswordElement(BasePageElement):
#     locator=LoginPageLocators.PASSOWRD


# class BasePage(object):
#     def __init__(self, driver):
#         self.driver = driver


class Element:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    def set_value(self, value):
        driver = self.driver
        locator = self.locator
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element(*locator))
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(value)

    def get_value(self):
        driver = self.driver
        locator = self.locator
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element(*locator))
        element = driver.find_element(*locator)
        return element.get_attribute("value")

    def click(self):
        driver = self.driver
        locator = self.locator
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element(*locator))
        element = driver.find_element(*locator)
        element.click()

    def get_instances(self):
        driver = self.driver
        locator = self.locator
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element(*locator))
        elements = driver.find_elements(*locator)
        return elements
