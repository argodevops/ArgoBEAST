from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
            elements = self.driver.find_elements(*locator)
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

    def is_not_visible(self, locator):
        """
        Check if element is visible
        :param locator: Locator tuple
        :return: True if visible, False if timeout
        """
        try:
            self._wait_for_invisible(locator)
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

    def set_value(self, locator, keys):
        element = self.find(locator=locator)

        # Ensure element is visible before sending keys.
        self.logger.info("Making input visible.")
        self.driver.execute_script("arguments[0].style.clip='auto';"
                                   "arguments[0].style.clipPath='none';"
                                   "arguments[0].style.width='auto';"
                                   "arguments[0].style.height='auto';"
                                   "arguments[0].style.visibility='visible';"
                                   "arguments[0].style.display='block';"
                                   "arguments[0].style.opacity='1';", element)
        try:
            element.send_keys(keys)
            self.logger.info(f"{keys} sent to {locator}")
            return True
        except InvalidArgumentException:
            self.logger.error(
                f"Could not send keys {keys} to locator {locator}")
            return False

    def populate_dropdown(self, locator, value):
        """Selects a value from a standard <select> dropdown."""
        # Use wait_for_visible to ensure it's ready for interaction
        element = self._wait_for_visible(locator)
        if not element:
            raise ValueError(f"Dropdown not found: {locator}")

        self.logger.info(f"Selecting '{value}' in dropdown {locator}")
        try:
            Select(element).select_by_visible_text(value)
        except:
            Select(element).select_by_value(value)

    def populate_combobox(self, locator, value):
        """Types and enters a value into a combobox/autocomplete."""
        element = self._wait_for_visible(locator)
        if not element:
            raise ValueError(f"Combobox not found: {locator}")

        self.logger.info(f"Setting combobox {locator} to '{value}'")
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(value)
        element.send_keys(Keys.ENTER)

    def populate_checkbox(self, locator, value):
        """Toggles a checkbox based on boolean-like string value."""
        element = self._wait_for_clickable(locator)
        if not element:
            raise ValueError(f"Checkbox not found: {locator}")

        should_be_checked = str(value).lower() in ['true', 'yes', 'on', '1']

        if element.is_selected() != should_be_checked:
            self.logger.info(
                f"Toggling checkbox {locator} to {should_be_checked}")
            element.click()

    def populate_radio_group(self, locator, value):
        """Selects a radio button within a group by Label or Value."""
        # Find container (visible)
        container = self._wait_for_visible(locator)
        if not container:
            raise ValueError(f"Radio Group container not found: {locator}")

        target_element = None

        # Strategy A: Text Match
        try:
            target_element = container.find_element(
                By.XPATH,
                f".//label[contains(normalize-space(), '{value}')]"
            )
        except:
            pass

        # Strategy B: Value Match
        if not target_element:
            try:
                target_element = container.find_element(
                    By.XPATH,
                    f".//input[@type='radio'][@value='{value}']"
                )
            except:
                pass

        if target_element:
            self.logger.info(
                f"Clicking radio option '{value}' in group {locator}")
            target_element.click()
        else:
            raise ValueError(
                f"Radio option '{value}' not found in group {locator}")

    # --- THE DISPATCHER ---

    def populate_form_field(self, locator, value, input_type="text"):
        """
        Routes the population request to the specific atomic method.
        """
        if input_type == "text":
            # FIX: Added 'value' argument
            self.type_text(locator, value)

        elif input_type == "select":
            self.populate_dropdown(locator, value)

        elif input_type == "combobox":
            self.populate_combobox(locator, value)

        elif input_type == "checkbox":
            self.populate_checkbox(locator, value)

        elif input_type == "radio":
            # Simple click on specific locator
            self.click(locator)

        elif input_type == "radio_group":
            self.populate_radio_group(locator, value)

        else:
            raise ValueError(
                f"Unknown input_type '{input_type}' for locator {locator}")

    def get_table_headers(self, locator):
        """
        Returns the headers from a table
        """
        table = self._wait_for_visible(locator)
        headers = []
        header_elements = table.find_elements(By.XPATH, ".//thead//th")

        if not header_elements:
            # Fallback: look for <th> inside the first <tr>
            header_elements = table.find_elements(By.XPATH, ".//tr[1]//th")

        headers = [h.text.strip() for h in header_elements]
        return headers

    def get_table_data(self, locator):
        """
        Parses an HTML table into a list of dictionaries.

        Example Return:
        [
            {"Name": "Alice", "Role": "Admin", "Status": "Active"},
            {"Name": "Bob",   "Role": "User",  "Status": "Inactive"}
        ]
        """
        table = self._wait_for_visible(locator)
        headers = self.get_table_headers(locator)
        rows = table.find_elements(By.XPATH, ".//tbody//tr")
        if not rows:
            # Fallback for tables without explicit tbody
            rows = table.find_elements(By.XPATH, ".//tr[td]")
        table_data = []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            # Safety Check: Ensure cell count matches header count
            # Use zip to map Header -> Cell Value
            row_data = {}
            for i, header in enumerate(headers):
                if i < len(cells):
                    row_data[header] = cells[i].text.strip()
                else:
                    row_data[header] = None  # Handle missing cells gracefully
            table_data.append(row_data)
        return table_data
