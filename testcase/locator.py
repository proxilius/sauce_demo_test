from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    USERNAME = {"by": By.ID, "value": "user-name"}
    PASSOWRD = {"by": By.ID, "value": "password"}
    LOGIN_BUTTON = {"by": By.ID, "value": "login-button"}
    ERROR = {
        "by": By.XPATH,
        "value": "/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3",
    }


class InventoryPageLocators(object):
    ADD_TO_CART_BUTTON = {"by": By.CLASS_NAME, "value": "btn_inventory"}
    INVENTORY_ITEM = {"by": By.CLASS_NAME, "value": "inventory_item"}
    ADD_TO_CART_FIRST = {"by": By.ID, "value": "add-to-cart-sauce-labs-backpack"}
    SHOPPING_CART_BADGE = {"by": By.CLASS_NAME, "value": "shopping_cart_badge"}
    SHOPPING_CART_LINK = {"by": By.CLASS_NAME, "value": "shopping_cart_link"}
    SELECT_SORT = {"by": By.CLASS_NAME, "value": "product_sort_container"}
    ITEM_NAME = {"by": By.CLASS_NAME, "value": "inventory_item_name"}
    ITEM_DESCRIPTION = {"by": By.CLASS_NAME, "value": "inventory_item_desc"}
    ITEM_PRICE = {"by": By.CLASS_NAME, "value": "inventory_item_price"}


class CartPageLocators(object):
    CART_LIST = {"by": By.CLASS_NAME, "value": "cart_list"}
    CART_ITEM = {"by": By.CLASS_NAME, "value": "cart_item"}
    INVENTORY_ITEM = {"by": By.CLASS_NAME, "value": "inventory_item"}
    ITEM_NAME = {"by": By.CLASS_NAME, "value": "inventory_item_name"}
    ITEM_DESCRIPTION = {"by": By.CLASS_NAME, "value": "inventory_item_desc"}
    ITEM_PRICE = {"by": By.CLASS_NAME, "value": "inventory_item_price"}
    CHECKOUT_BUTTON = {"by": By.ID, "value": "checkout"}


class CheckoutPageLocators(object):
    FIRST_NAME_INPUT = {"by": By.ID, "value": "first-name"}
    LAST_NAME_INPUT = {"by": By.ID, "value": "last-name"}
    POSTAL_CODE_INPUT = {"by": By.ID, "value": "postal-code"}
    CONTINUE_BUTTON = {"by": By.ID, "value": "continue"}
    CANCEL_BUTTON = {"by": By.ID, "value": "cancel"}


class CheckoutPageStepTwoLocators(object):
    FINISH_BUTTON = {"by": By.ID, "value": "finish"}
    CANCEL_BUTTON = {"by": By.ID, "value": "cancel"}
    CART_ITEM = {"by": By.CLASS_NAME, "value": "cart_item"}
    ITEM_NAME = {"by": By.CLASS_NAME, "value": "inventory_item_name"}
    ITEM_DESCRIPTION = {"by": By.CLASS_NAME, "value": "inventory_item_desc"}
    ITEM_PRICE = {"by": By.CLASS_NAME, "value": "inventory_item_price"}
    TOTAL_PRICE_LABEL = {"by": By.CLASS_NAME, "value": "summary_subtotal_label"}
