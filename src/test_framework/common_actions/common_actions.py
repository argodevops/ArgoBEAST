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

    def upload_file(self, locator, filepath):
        self.page.set_value(locator=locator, keys=filepath)
        return True

    def populate_generic_form(self, form_map, data_input):
        """
        Iterates through data and populates the form using the provided map.
        Supports both explicit types: ((By.ID, 'x'), 'select')
        And implicit defaults: (By.ID, 'x') -> defaults to 'text'
        """

       # 1. auto-convert Behave Table if detected
        if hasattr(data_input, 'rows'):
            form_data = [row.as_dict() for row in data_input]
        else:
            form_data = data_input

        # 2. The Engine Loop
        for row in form_data:
            field = row['field']
            value = row['value']

            if field in form_map:
                definition = form_map[field]

                # --- SAFEGUARD: Check for Tuple structure ---
                # We check if the first item is ITSELF a tuple (a locator)
                # If yes: It's the full config -> ((By.ID, '1'), 'text')
                # If no:  It's just a locator  -> (By.ID, '1')

                if isinstance(definition, tuple) and len(definition) > 0 and isinstance(definition[0], tuple):
                    locator = definition[0]
                    input_type = definition[1].lower()
                else:
                    locator = definition
                    input_type = "text"  # Default fallback

                self.page.populate_form_field(locator, value, input_type)

            else:
                # Safe access to page name (handle if self.page isn't set)
                page_name = getattr(self.page, '__class__', {}).get(
                    '__name__', 'UnknownPage') if hasattr(self, 'page') else 'CurrentPage'
                raise ValueError(
                    f"Field '{field}' not found in map for {page_name}.")

    def verify_row_exists(self, table_locator, expected_data):
        """
        GOAL: Assert that at least one row matches the criteria.

        ARGS: 
        - expected_data: A dict subset, e.g., {'Name': 'Bob'}

        IMPLEMENTATION STRATEGY:
        1. Call self.page.get_table_data(table_locator).
        2. Loop through the returned list.
        3. Perform a "Subset Check":
        - Does row['Name'] == 'Bob'?
        - If expected_data has multiple keys (Name=Bob, Role=Admin), ALL must match.
        4. If a match is found, return True/Pass.
        5. If loop finishes without match, Raise AssertionError with a helpful message showing what was actually found.
        """
        pass

    def verify_row_does_not_exist(self, table_locator, expected_data):
        """
        GOAL: Assert that NO row matches the criteria.

        IMPLEMENTATION STRATEGY:
        1. Reuse the logic from `verify_row_exists`.
        2. If it returns True (found), Raise AssertionError immediately.
        3. If it finishes without finding it, Pass.
        """
        pass

    def verify_table_contains_count(self, table_locator, expected_data, count):
        """
        GOAL: Assert that exactly X rows match the criteria.

        IMPLEMENTATION STRATEGY:
        1. Get data.
        2. Initialize a counter = 0.
        3. Loop through rows and perform the subset check.
        4. If match, increment counter.
        5. Finally, assert counter == expected_count.
        """
        pass

    def verify_column_headers(self, table_locator, expected_headers):
        """
        GOAL: Ensure the table structure is correct (e.g. columns haven't disappeared).

        IMPLEMENTATION STRATEGY:
        1. Call self.page.get_table_headers(table_locator).
        2. Assert that every item in `expected_headers` is present in the actual list.
        3. (Optional) Assert order matches if strict ordering is required.
        """
        pass
