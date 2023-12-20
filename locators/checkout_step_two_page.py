from selenium.webdriver.common.by import By


class CheckoutStepTwoPageLocators(object):
    FINISH_BUTTON = {"by": By.ID, "value": "finish"}
    CANCEL_BUTTON = {"by": By.ID, "value": "cancel"}
    CART_ITEM = {"by": By.CLASS_NAME, "value": "cart_item"}
    ITEM_NAME = {"by": By.CLASS_NAME, "value": "inventory_item_name"}
    ITEM_DESCRIPTION = {"by": By.CLASS_NAME, "value": "inventory_item_desc"}
    ITEM_PRICE = {"by": By.CLASS_NAME, "value": "inventory_item_price"}
    TOTAL_PRICE_LABEL = {"by": By.CLASS_NAME, "value": "summary_subtotal_label"}
    CHECKOUT_SUMMARY_CONTAINER = {"by": By.ID, "value": "checkout_summary_container"}
