from locator import *
from element import BasePageElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

# class UsernameElement(BasePageElement):
#     locator=LoginPageLocators.USERNAME

# class PasswordElement(BasePageElement):
#     locator=LoginPageLocators.PASSOWRD


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


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


class LoginPage(BasePage):
    def set_credentials(self, username, password):
        username_element = Element(self.driver, LoginPageLocators.USERNAME)
        password_element = Element(self.driver, LoginPageLocators.PASSOWRD)

        username_element.set_value(username)
        password_element.set_value(password)
        x = username_element.get_value()

    def click_login_button(self):
        element = self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        element.click()

    def login(self, username, password):
        self.set_credentials(username, password)
        self.click_login_button()

    def seek_error(self):
        try:
            element = self.driver.find_element(*LoginPageLocators.ERROR)
            print("ERRORRRR ELEMENT:::::: ", element)
            return element.text
        except:
            return 0


class InventoryPage(BasePage):
    def add_to_cart_all(self):
        # buttons = self.driver.find_elements(*InventoryPageLocators.ADD_TO_CART_BUTTON)
        buttonsElement = Element(self.driver, InventoryPageLocators.ADD_TO_CART_BUTTON)
        buttons = buttonsElement.get_instances()
        for x in buttons:
            time.sleep(0.2)
            x.click()
        return len(buttons)

    def get_cart_quantity(self):
        try:
            shopping_cart_badge_element = self.driver.find_element(
                *InventoryPageLocators.SHOPPING_CART_BADGE
            )
            return int(shopping_cart_badge_element.text)
        except:
            return 0

    def set_sort(self, value):
        try:
            select_element = Select(
                self.driver.find_element(*InventoryPageLocators.SELECT_SORT)
            )
            select_element.select_by_value(value)
            time.sleep(1)
        except:
            return 0
