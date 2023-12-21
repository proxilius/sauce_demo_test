from selenium.webdriver.common.by import By


class CommonLocators(object):
    BURGER_BUTTON = {"by": By.ID, "value": "react-burger-menu-btn"}
    LOGOUT_BUTTON = {"by": By.ID, "value": "logout_sidebar_link"}
    ALL_ITEMS_BUTTON = {"by": By.ID, "value": "inventory_sidebar_link"}
    RESET_STATE_BUTTON = {"by": By.ID, "value": "reset_sidebar_link"}
