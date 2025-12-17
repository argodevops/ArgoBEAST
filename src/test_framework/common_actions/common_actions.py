from test_framework.base.base_page import BasePage
from selenium.common.exceptions import (TimeoutException, ElementClickInterceptedException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
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
        """
        Executes the logic to upload a file to a
        standard file input element

        :param locator: The locator for the file input
        :param filepath: The path where the file is located
        """
        self.page.set_value(locator=locator, keys=filepath)
        return True

    def populate_generic_form(self, form_map, data_input):
        """
        Iterates through data and populates the form using the provided map.
        Supports both explicit types: ((By.ID, 'x'), 'select')
        And implicit defaults: (By.ID, 'x') -> defaults to 'text'

        :param form_map: A dictionary of form elements (tuples)
        :param data_input: A dictionary of data the user wishes to add to the form 
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

    def verify_row_exists(self, table_locator, expected_data: dict):
        """
        Asserts that at least one row matches ALL keys/values in expected_data.

        :param table_locator: Locator for the table
        :param expected_data: Dictionary of expected key-value pairs
        :return: True if a matching row is found, raises AssertionError otherwise
        """
        table_data = self.page.get_table_data(table_locator)

        found = False
        for row in table_data:
            # We assume it matches until we find a mismatch
            match = True
            for key, expected_value in expected_data.items():
                actual_value = row.get(key)

                if actual_value != expected_value:
                    match = False
                    break
            if match:
                found = True
                break

        if not found:
            raise AssertionError(
                f"Could not find row matching {expected_data}.\n"
                f"Actual Table Data: {table_data}"
            )
        return found

    def verify_row_does_not_exist(self, table_locator, expected_data: dict):
        """
        Asserts that NO row matches the criteria.
        """
        table_data = self.page.get_table_data(table_locator)

        for row in table_data:
            match = True
            for key, expected_value in expected_data.items():
                if row.get(key) != expected_value:
                    match = False
                    break
            if match:
                # If we found a match, that's a FAILURE
                raise AssertionError(
                    f"Found unexpected row: {row} matching filter criteria: {expected_data}")
        return True

    def verify_table_contains_count(self, table_locator, count: int, filter_data=None):
        """
        Asserts that exactly X rows match the filter criteria.

        :param table_locator: Locator for the table
        :param count: Expected number of rows (int or str convertible to int)
        :param filter_data: Optional dict of filter criteria
        :return: True if count matches, raises AssertionError otherwise.

        If filter_data is None, checks total row count.
        """
        table_data = self.page.get_table_data(table_locator)

        # Scenario A: Just check total rows
        if filter_data is None:
            actual_count = len(table_data)

        # Scenario B: Count specific rows
        else:
            actual_count = 0
            for row in table_data:
                match = True
                for key, val in filter_data.items():
                    if row.get(key) != val:
                        match = False
                        break
                if match:
                    actual_count += 1

        if actual_count != int(count):
            raise AssertionError(
                f"Expected count: {count}, but found: {actual_count}. Filter: {filter_data}"
            )
        return True

    def verify_column_headers(self, table_locator, expected_headers):
        """
        Verifies that the table contains all expected column headers.

        :param table_locator: Locator for the table
        :param expected_headers: List of expected column header names
        :return: True if all headers are present, raises AssertionError otherwise
        """
        actual_headers = self.page.get_table_headers(table_locator)

        missing = []
        for h in expected_headers:
            if h not in actual_headers:
                missing.append(h)

        if missing:
            raise AssertionError(
                f"Missing columns: {missing}. Actual headers: {actual_headers}"
            )
        return True

    def send_keyboard_input(self, locator, *keys):
        """
            Send keyboard input to an element using string names.
            Usage: self.send_keyboard_input(LOCATOR, "CONTROL", "ENTER")
            """
        new_keys = []
        for k in keys:
            key_name = k.upper()
            try:
                # getattr(obj, name) looks for an attribute named 'name' inside 'obj'
                # This is equivalent to doing Keys.ENTER, Keys.CONTROL, etc.
                valid_key = getattr(Keys, key_name)
                new_keys.append(valid_key)
            except AttributeError:
                # Optional: Handle cases where the key doesn't exist
                print(f"Warning: {key_name} is not a valid Selenium Key")

        # We must unpack (*) the list so they are passed as separate arguments
        self.page.press_keys(locator, *new_keys)
