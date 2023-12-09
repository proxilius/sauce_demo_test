import unittest
from selenium import webdriver
import page
from selenium.webdriver.chrome.options import Options
import time 

class StandardUser(unittest.TestCase):
    def setUp(self):
        
        options = webdriver.ChromeOptions()
        
        # options.add_argument('--window-size=1420,1080')
        #options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)
        # self.driver.implicitly_wait(3)
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com")


    def test_login(self):
        mainPage = page.LoginPage(self.driver)
        mainPage.set_credentials('standard_user','secret_sauce')
       # mainPage.username_element = 'standard_user'
        mainPage.click_login_button()
        assert True


    def tearDown(self):
        time.sleep(2)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()