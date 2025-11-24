from test_framework.base.base_page import BasePage
from selenium.common.exceptions import (TimeoutException, ElementClickInterceptedException,
                                        StaleElementReferenceException)
import time


class CommonActions:

    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver
        self.config = page.config
        self.logger = page.logger

    def get_element_with_text(self, locator, text):
        elements = self.page.find_all(locator)
        for el in elements:
            if text == el.text.strip():
                return el
        self.logger.warning(f"No element found with exact text '{text}'")
        return None

    def get_element_containing_text(self, locator, text):
        elements = self.page.find_all(locator)
        for el in elements:
            if text in el.text.strip():
                return el
        self.logger.warning(f"No element found containing text '{text}'")
        return None

    def click_element_with_text(self, locator, text):
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
        element = self.get_element_containing_text(locator, text)
        if not element:
            return False
        element.click()
        return True

    def find_in_list(self, elements: list, text: str, partial: bool = False):
        for el in elements:
            if partial:
                if el.text.strip() in text:
                    return el
            if el.text.strip() == text:
                return el
        return None

    def wait_for_text(self, locator, text):
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
        TODO: Implement URL wait logic when navigation behaviours are added.
        """
        raise NotImplementedError(
            "wait_for_url_contains is not implemented yet."
            "This will be added when navigation actions are introduced.")

    def retry_click(self, locator: tuple, retries: int = 3, delay: float = 0.5):
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
