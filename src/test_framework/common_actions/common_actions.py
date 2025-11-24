from test_framework.base.base_page import BasePage
from selenium.common.exceptions import (TimeoutException, ElementClickInterceptedException,
                                        StaleElementReferenceException)
import time

"""
Common actions for interacting with web elements
"""


class CommonActions:

    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver
        self.config = page.config
        self.logger = page.logger

    def get_element_with_text(self, locator, text):
        """
        Get the first element matching the locator with exact text
        :param locator: Locator tuple
        :param text: Exact text to match
        :return: WebElement or None
        """
        elements = self.page.find_all(locator)
        for el in elements:
            if text == el.text.strip():
                return el
        self.logger.warning(f"No element found with exact text '{text}'")
        return None

    def get_element_containing_text(self, locator, text):
        """
        Get the first element matching the locator that contains the text
        :param locator: Locator tuple
        :param text: Text to search for
        :return: WebElement or None
        """
        elements = self.page.find_all(locator)
        for el in elements:
            if text in el.text.strip():
                return el
        self.logger.warning(f"No element found containing text '{text}'")
        return None

    def click_element_with_text(self, locator, text):
        """
        Click the first element matching the locator with exact text
        :param locator: Locator tuple
        :param text: Exact text to match
        :return: True if clicked, False otherwise
        """
        element = self.get_element_with_text(locator, text)
        if not element:
            return False
        elif element.text == text:
            element.click()
            return True
        else:
            self.logger.warning(
                f"The element text '{element.text}' does not exactly match '{text}'")
            return False

    def click_element_containing_text(self, locator: tuple, text: str):
        """
        Click the first element matching the locator that contains the text
        :param locator: Locator tuple
        :param text: Text to search for
        :return: True if clicked, False otherwise
        """
        element = self.get_element_containing_text(locator, text)
        if not element:
            return False
        element.click()
        return True

    def find_in_list(self, elements: list, text: str, partial: bool = False):
        """
        Find an element in a list by text
        :param elements: List of WebElements
        :param text: Text to search for
        :param partial: Whether to match partially
        :return: WebElement or None
        """
        for el in elements:
            if partial:
                if el.text.strip() in text:
                    return el
            if el.text.strip() == text:
                return el
        return None

    def wait_for_text(self, locator, text):
        """
        Wait for an element to have exact text
        :param locator: Locator tuple
        :param text: Exact text to wait for
        :return: True if text matches, False if timeout
        """
        try:
            self.page.wait.until(
                lambda d: self.page._wait_for_visible(
                    locator).text.strip() == text
            )
            return True
        except TimeoutException:
            self.logger.warning(
                f"Element {locator} did not have exact text '{text}'")
            return False

    def wait_for_text_contains(self, locator: tuple, text: str):
        """
        Wait for an element to contain text
        :param locator: Locator tuple
        :param text: Text to wait for
        :return: True if text is contained, False if timeout
        """
        try:
            self.page.wait.until(
                lambda d: text in self.page.find(
                    locator).text.strip()
            )
            return True
        except TimeoutException:
            self.logger.warning(
                f"Element {locator} did not contain text '{text}'")
            return False

    def wait_for_url_contains(self, partial_url: str):
        """
        Wait for the current URL to contain a substring
        :param partial_url: Substring to wait for in the URL
        :return: True if URL contains substring, False if timeout
        """
        # TODO: Implement URL wait logic when navigation behaviours are added.

        raise NotImplementedError(
            "wait_for_url_contains is not implemented yet."
            "This will be added when navigation actions are introduced.")

    def retry_click(self, locator: tuple, retries: int = 3, delay: float = 0.5):
        """
        Retry clicking an element multiple times to handle flaky clicks
        :param locator: Locator tuple
        :param retries: Number of retry attempts
        :param delay: Delay between attempts in seconds
        :return: True if clicked, False otherwise
        """
        for attempt in range(0, retries):
            try:
                clicked = self.page.click(locator)
                if clicked:
                    return True

                # click() returned False → retry
                self.logger.warning(
                    f"Click returned False on attempt {attempt + 1}/{retries} for locator {locator}"
                )
                time.sleep(delay)

            except (ElementClickInterceptedException, StaleElementReferenceException):
                # click threw an expected flaky exception → retry
                self.logger.warning(
                    f"Click failed with exception on attempt {attempt + 1}/{retries} for locator {locator}"
                )
                time.sleep(delay)

        return False
