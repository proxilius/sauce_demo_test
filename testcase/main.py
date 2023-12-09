import unittest
from selenium import webdriver
import page
from selenium.webdriver.chrome.options import Options
import time 
chrome_options = Options()

class StandardUser(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com")


    def test_login(self):
        print ('test')
        assert True


    def tearDown(self):
        time.sleep(5)
        self.driver.close()


if __name__ == "__main__":
    unittest.main()