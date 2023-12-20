from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def _visit(self, url):
        if url.startswith("http"):
            self.driver.get(url)
        else:
            self.driver.get(config.baseurl + url)

    def _find(self, locator):
        # TODO: facilitate using data-test attribute as well as selenium 'By' locators
        try:
            return self._find_all(locator)[0]
        except IndexError:
            return False

    def _find_child(self, parent, locator):
        children = parent.find_elements(locator["by"], locator["value"])
        try:
            return children[0]
        except IndexError:
            return False

    def _find_children(self, parent, locator):
        children = parent.find_elements(locator["by"], locator["value"])
        try:
            return children
        except IndexError:
            return False

    def _find_all(self, locator):
        try:
            driver = self.driver
            locator = locator
            WebDriverWait(driver, 10).until(
                lambda driver: driver.find_elements(locator["by"], locator["value"])
            )
            elements = self.driver.find_elements(locator["by"], locator["value"])
            return elements
        except NoSuchElementException:
            return False

    def _click(self, locator):
        try:
            element = self._find(locator)
            element.click()
        except TypeError:
            raise AssertionError("Input should be a locator object")
        # assert element, f"Click action failed, cannot locate an element with {locator}"
        # self._find(locator).click()

    def _type(self, locator, input_text):
        self._find(locator).send_keys(input_text)

    def _value(self, locator):
        return self._find(locator).get_attribute("value")
