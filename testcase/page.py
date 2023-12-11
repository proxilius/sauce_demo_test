from locator import *
from element import BasePageElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from _base_page import BasePage

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


class LoginPage(BasePage):
    def set_credentials(self, username, password):
        self._type(LoginPageLocators.USERNAME, username)
        self._type(LoginPageLocators.PASSOWRD, password)

    def click_login_button(self):
        self._click(LoginPageLocators.LOGIN_BUTTON)

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
        items = []
        item_elements = self._find_all(InventoryPageLocators.INVENTORY_ITEM)
        for i in item_elements:
            item_in_cart = False
            cart_button_text = self._find_child(
                i, InventoryPageLocators.ADD_TO_CART_BUTTON
            ).text
            if "remove" in cart_button_text.lower():
                item_in_cart = True
            else:
                button = self._find_child(i, InventoryPageLocators.ADD_TO_CART_BUTTON)
                button.click()
                items.append(
                    {
                        "name": self._find_child(
                            i, InventoryPageLocators.ITEM_NAME
                        ).text,
                        "description": self._find_child(
                            i, InventoryPageLocators.ITEM_DESCRIPTION
                        ).text,
                        "price": float(
                            self._find_child(i, InventoryPageLocators.ITEM_PRICE).text[
                                1:
                            ]
                        ),
                    }
                )

        return {"count": len(item_elements), "item_names": items}

    def click_shopping_cart(self):
        self._click(InventoryPageLocators.SHOPPING_CART_LINK)

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
            select_element = Select(self._find(InventoryPageLocators.SELECT_SORT))
            print("FOUND ELEMENT::::::", select_element)
            select_element.select_by_value(value)
            time.sleep(1)
        except:
            return 0

    def get_items_all(self):
        items = []
        item_elements = self._find_all(InventoryPageLocators.INVENTORY_ITEM)
        for i in item_elements:
            item_in_cart = False
            cart_button_text = self._find_child(
                i, InventoryPageLocators.ADD_TO_CART_BUTTON
            ).text
            if "remove" in cart_button_text.lower():
                item_in_cart = True
            items.append(
                {
                    "name": self._find_child(i, InventoryPageLocators.ITEM_NAME).text,
                    "description": self._find_child(
                        i, InventoryPageLocators.ITEM_DESCRIPTION
                    ).text,
                    "price": float(
                        self._find_child(i, InventoryPageLocators.ITEM_PRICE).text[1:]
                    ),
                    "in_cart": item_in_cart,
                }
            )

        return items


class CartPage(BasePage):
    def get_cart_items_all(self):
        items = []
        item_elements = self._find_all(CartPageLocators.CART_ITEM)
        for i in item_elements:
            items.append(
                {
                    "name": self._find_child(i, CartPageLocators.ITEM_NAME).text,
                    "description": self._find_child(
                        i, CartPageLocators.ITEM_DESCRIPTION
                    ).text,
                    "price": float(
                        self._find_child(i, CartPageLocators.ITEM_PRICE).text[1:]
                    ),
                }
            )
        return items

    def click_checkout(self):
        return self._click(CartPageLocators.CHECKOUT_BUTTON)


class CheckoutPage(BasePage):
    def set_firstname(self, value):
        self._type(CheckoutPageLocators.FIRST_NAME_INPUT, value)

    def set_last_name(self, value):
        self._type(CheckoutPageLocators.LAST_NAME_INPUT, value)

    def set_zip(self, value):
        self._type(CheckoutPageLocators.POSTAL_CODE_INPUT, value)

    def click_continue(self):
        return self._click(CheckoutPageLocators.CONTINUE_BUTTON)
