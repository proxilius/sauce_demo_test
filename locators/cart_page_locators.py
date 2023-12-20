from selenium.webdriver.common.by import By


class CartPageLocators(object):
    CART_LIST = {"by": By.CLASS_NAME, "value": "cart_list"}
    CART_ITEM = {"by": By.CLASS_NAME, "value": "cart_item"}
    INVENTORY_ITEM = {"by": By.CLASS_NAME, "value": "inventory_item"}
    ITEM_NAME = {"by": By.CLASS_NAME, "value": "inventory_item_name"}
    ITEM_DESCRIPTION = {"by": By.CLASS_NAME, "value": "inventory_item_desc"}
    ITEM_PRICE = {"by": By.CLASS_NAME, "value": "inventory_item_price"}
    CHECKOUT_BUTTON = {"by": By.ID, "value": "checkout"}
    CONTINUE_SHOPPING_BUTTON = {"by": By.ID, "value": "continue-shopping"}
    CART_BUTTON = {"by": By.CLASS_NAME, "value": "cart_button"}
    SHOPPING_CART_BADGE = {"by": By.CLASS_NAME, "value": "shopping_cart_badge"}
