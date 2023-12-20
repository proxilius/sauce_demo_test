from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    USERNAME = {"by": By.ID, "value": "user-name"}
    PASSOWRD = {"by": By.ID, "value": "password"}
    LOGIN_BUTTON = {"by": By.ID, "value": "login-button"}
    ERROR = {
        "by": By.XPATH,
        "value": "/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3",
    }
    LOGIN_WRAPPER = {"by": By.CLASS_NAME, "value": "login_wrapper"}
