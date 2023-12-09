from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    USERNAME = (By.ID, 'user-name')
    PASSOWRD = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')