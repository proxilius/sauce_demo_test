from selenium.webdriver.common.by import By


class CheckoutCompletePageLocators(object):
    FINISH_BUTTON = {"by": By.ID, "value": "checkout_complete_container"}
    BACK_TO_PRODUCTS_BUTTON = {"by": By.ID, "value": "back-to-products"}
