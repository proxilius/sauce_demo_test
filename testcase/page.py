from locator import * 
class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):

    def set_credentials(self):
        username_element = self.driver.find_element(*SearchLocators.USERNAME)
        element.send_keys("standard_user")
        password_element = self.driver.find_element(*SearchLocators.PASSWORD)
        element.send_keys("secret_sauce")
