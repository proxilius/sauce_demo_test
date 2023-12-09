from locator import * 
from element import BasePageElement
from selenium.webdriver.support.ui import WebDriverWait

# class UsernameElement(BasePageElement):
#     locator=LoginPageLocators.USERNAME

# class PasswordElement(BasePageElement):
#     locator=LoginPageLocators.PASSOWRD

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class Element():
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator
    
    def set_value(self, value):
        driver = self.driver
        locator=self.locator
        print('set value: ',value, 'locator:: ')
        WebDriverWait(driver, 100).until(lambda driver: driver.find_element(*locator))
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(value)

class LoginPage(BasePage):

    #username_element = UsernameElement()
    #password_element = PasswordElement()
    def set_credentials(self,username,password):
        print('suername',username,'passowrd',password)
        username_element = Element(self.driver,LoginPageLocators.USERNAME)
        password_element = Element(self.driver,LoginPageLocators.PASSOWRD)
       # password_element = PasswordElement()
        username_element.set_value(username)
        password_element.set_value(password)
        # username_element=username
        #password_element=password
        # username_element=self.driver.find_element(*LoginPageLocators.USERNAME)
        # username_element.send_keys(username)

        # username_element=self.driver.find_element(*LoginPageLocators.PASSOWRD)
        # username_element.send_keys(password)

    def click_login_button(self):
        element = self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        element.click()