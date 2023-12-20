from selenium.webdriver.common.by import By


class ItemPageLocators(object):
    ADD_REMOVE_CART_BUTTON = {"by": By.CLASS_NAME, "value": "btn_inventory"}
    BACK_BUTTON = {"by": By.ID, "value": "back-to-products"}
    DETAILS_CONTAINER = {"by": By.CLASS_NAME, "value": "inventory_details_container"}
    DETAILS_NAME = {"by": By.CLASS_NAME, "value": "inventory_details_name"}
    DETAILS_PRICE = {"by": By.CLASS_NAME, "value": "inventory_details_price"}
