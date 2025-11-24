from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging
import os


class BasePage():
    """
    Selenium Base class for all page objects
    """

    def __init__(self, driver: WebDriver, config: dict):
        self.logger = logging.getLogger(__name__)
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(self.driver, self.config["explicit_wait"])

    def _wait_for_visible(self, locator):
        """
        Wait for element to be visible
        :param locator: Locator tuple
        :return: WebElement
        """
        element = self.wait.until(ec.visibility_of_element_located(locator))
        return element

    def _wait_for_clickable(self, locator):
        """
        Wait for element to be clickable
        :param locator: Locator tuple
        :return: WebElement
        """
        element = self.wait.until(ec.element_to_be_clickable(locator))
        return element

    def _wait_for_presence(self, locator):
        """
        Wait for element to be present in DOM
        :param locator: Locator tuple
        :return: WebElement
        """
        element = self.wait.until(ec.presence_of_element_located(locator))
        return element

    def _wait_for_invisible(self, locator):
        """
        Wait for element to be invisible
        :param locator: Locator tuple
        :return: True if invisible, False if timeout
        """
        try:
            self.wait.until(ec.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def find(self, locator):
        """
        Find a single element
        :param locator: Locator tuple
        :return: WebElement or None"""
        try:
            element = self._wait_for_presence(locator)
            return element
        except TimeoutException:
            self.logger.warning("No element found")
            return None

    def find_all(self, locator):
        """
        Find multiple elements
        :param locator: Locator tuple
        :return: List of WebElements or empty list"""
        try:
            self._wait_for_presence(locator)
            elements = self.driver.find_elements(locator)
            return elements
        except TimeoutException:
            self.logger.warning("No elements found")
            return []

    def click(self, locator):
        """
        Click an element
        :param locator: Locator tuple
        :return: True if clicked, False if timeout
        """
        try:
            self._wait_for_clickable(locator).click()
            return True
        except TimeoutException:
            self.logger.warning(f"Unable to click locator {locator.id}")
            return False

    def type_text(self, locator, text: str, clear_first: bool = True):
        """
        Type text into an input field
        :param locator: Locator tuple
        :param text: Text to type
        :param clear_first: Whether to clear the field first
        :return: True if typed, False if timeout
        """
        try:
            element = self._wait_for_visible(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            return True
        except TimeoutException:
            return False

    def get_text(self, locator):
        """
        Get text of an element
        :param locator: Locator tuple
        :return: Text string or None if timeout
        """
        try:
            element = self._wait_for_visible(locator)
            return element.text
        except TimeoutException:
            return None

    def is_visible(self, locator):
        """
        Check if element is visible
        :param locator: Locator tuple
        :return: True if visible, False if timeout
        """
        try:
            self._wait_for_visible(locator)
            return True
        except TimeoutException:
            return False

    def scroll_into_view(self, locator):
        """
        Scroll element into view
        :param locator: Locator tuple
        :return: True if scrolled, False if timeout
        """
        try:
            element = self._wait_for_visible(locator)
            self.driver.execute_script(
                "arguments[0].scrollIntoView()", element)
            return True
        except TimeoutException:
            self.logger.warning(
                "Could not find element and scroll at this time")
            return False

    def scroll_to_bottom(self):
        """
        Scroll to the bottom of the page
        :return: True if scrolled, False if error
        """
        try:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)")
            return True
        except Exception as e:
            self.logger.warning(f"Scroll to bottom failed: {e}")
            return False

    def screenshot(self, name):
        """
        Take a screenshot and save to screenshots/ directory
        :param name: Name of the screenshot file (without extension)
        """
        if not os.path.exists("./screenshots"):
            os.makedirs("./screenshots")
        self.driver.save_screenshot(f"./screenshots/{name}.png")
