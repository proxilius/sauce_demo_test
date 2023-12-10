from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    USERNAME = (By.ID, "user-name")
    PASSOWRD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3")


class InventoryPageLocators(object):
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "btn_inventory")
    ADD_TO_CART_FIRST = (By.ID, "add-to-cart-sauce-labs-backpack")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SELECT_SORT = (By.CLASS_NAME, "product_sort_container")
