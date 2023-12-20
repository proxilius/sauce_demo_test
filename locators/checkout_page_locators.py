from selenium.webdriver.common.by import By


class CheckoutPageLocators(object):
    FIRST_NAME_INPUT = {"by": By.ID, "value": "first-name"}
    LAST_NAME_INPUT = {"by": By.ID, "value": "last-name"}
    POSTAL_CODE_INPUT = {"by": By.ID, "value": "postal-code"}
    CONTINUE_BUTTON = {"by": By.ID, "value": "continue"}
    CANCEL_BUTTON = {"by": By.ID, "value": "cancel"}
    ERROR_TEXT = {"by": By.CLASS_NAME, "value": "error-message-container"}
