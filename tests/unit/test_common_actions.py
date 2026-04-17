import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from argo_beast.common_actions.common_actions import CommonActions


@pytest.fixture
def mock_page():
    page = MagicMock()
    # Mocking the nested driver/logger/config inside page
    page.driver = MagicMock()
    page.logger = MagicMock()
    page.config = {"explicit_wait": 5}
    return page


@pytest.fixture
def actions(mock_page):
    return CommonActions(mock_page)


# --- 1. Testing Text Search Logic ---


def test_get_element_with_text_finds_exact_match(actions, mock_page):
    """Verify exact text matching ignores whitespace but matches case."""
    mock_el1 = MagicMock()
    mock_el1.text = "  Submit  "
    mock_el2 = MagicMock()
    mock_el2.text = "Cancel"
    mock_page.find_all.return_value = [mock_el1, mock_el2]

    result = actions.get_element_with_text(("id", "any"), "Submit")

    assert result == mock_el1
    mock_page.logger.warning.assert_not_called()


def test_get_element_with_text_returns_none_on_miss(actions, mock_page):
    """Verify warning is logged when no text matches."""
    mock_page.find_all.return_value = []

    result = actions.get_element_with_text(("id", "any"), "Missing")

    assert result is None
    actions.logger.warning.assert_called_with(
        "No element found with exact text 'Missing'"
    )


# --- 2. Testing The Flaky Click (Retry Logic) ---


def test_retry_click_succeeds_on_second_attempt(actions, mock_page):
    """Verify that if the first click fails with an exception, it retries."""
    locator = ("id", "flaky")

    # Simulate: 1st attempt raises Exception, 2nd attempt returns True
    mock_page.click.side_effect = [ElementClickInterceptedException, True]

    with patch("time.sleep"):  # Don't actually wait during tests
        result = actions.retry_click(locator, retries=2)

    assert result is True
    assert mock_page.click.call_count == 2


# --- 3. Testing Form Dispatcher (The Engine) ---


def test_populate_generic_form_handles_behave_table(actions, mock_page):
    """Verify that Behave-style tables are converted and processed."""
    # 1. Setup a Mock that mimics a Behave Table
    # We use MagicMock so it can be iterated over like a list
    mock_table = MagicMock()

    # 2. Setup the "Row" mocks
    row_mock = MagicMock()
    row_mock.as_dict.return_value = {"field": "username", "value": "paul"}

    # Configure the mock table to return our row when iterated
    mock_table.__iter__.return_value = [row_mock]
    # This is the line your framework uses to detect it's a Behave Table
    mock_table.rows = True

    form_map = {"username": (("id", "user"), "text")}

    # 3. Action
    actions.populate_generic_form(form_map, mock_table)

    # 4. Assert
    mock_page.populate_form_field.assert_called_once_with(
        ("id", "user"), "paul", "text"
    )


# --- 4. Testing Table Assertions ---


def test_verify_row_exists_success(actions, mock_page):
    """Verify assertion passes when a matching row is found."""
    mock_page.get_table_data.return_value = [
        {"ID": "1", "User": "Alice"},
        {"ID": "2", "User": "Bob"},
    ]

    result = actions.verify_row_exists(("id", "table"), {"User": "Bob"})
    assert result is True


def test_verify_row_exists_raises_assertion_error(actions, mock_page):
    """Verify custom error message is raised when data is missing."""
    mock_page.get_table_data.return_value = [{"User": "Alice"}]

    with pytest.raises(AssertionError) as exc:
        actions.verify_row_exists(("id", "table"), {"User": "Charlie"})

    assert "Could not find row matching {'User': 'Charlie'}" in str(exc.value)


def test_send_keyboard_input_mapping(actions, mock_page):
    """Verify string names like 'ENTER' are converted to Selenium Keys objects."""
    from selenium.webdriver.common.keys import Keys

    locator = ("id", "search")

    # Action: We pass strings, the framework should find the Selenium Constants
    actions.send_keyboard_input(locator, "control", "enter")

    # Assert
    # We verify that the Page's press_keys was called with the actual Keys objects
    mock_page.press_keys.assert_called_once_with(locator, Keys.CONTROL, Keys.ENTER)


def test_verify_table_contains_count_with_filter(actions, mock_page):
    """Verify specific count of filtered rows."""
    mock_page.get_table_data.return_value = [
        {"Status": "Active", "Name": "A"},
        {"Status": "Active", "Name": "B"},
        {"Status": "Inactive", "Name": "C"},
    ]

    # Should find exactly 2 'Active' rows
    result = actions.verify_table_contains_count(
        ("id", "table"), 2, filter_data={"Status": "Active"}
    )
    assert result is True


def test_verify_row_does_not_exist_failure(actions, mock_page):
    """Verify that finding a forbidden row raises an AssertionError."""
    mock_page.get_table_data.return_value = [{"User": "Admin"}]

    with pytest.raises(AssertionError) as exc:
        actions.verify_row_does_not_exist(("id", "table"), {"User": "Admin"})

    assert "Found unexpected row" in str(exc.value)


# --- 1. Testing Text Search Variants ---


def test_get_element_containing_text_success(actions, mock_page):
    """Verify partial text matching logic."""
    mock_el = MagicMock()
    mock_el.text = "Welcome, Paul"
    mock_page.find_all.return_value = [mock_el]

    result = actions.get_element_containing_text(("id", "msg"), "Paul")
    assert result == mock_el


def test_click_element_with_text_mismatch_warning(actions, mock_page):
    """Verify behavior when an element is found but text doesn't match exactly."""
    mock_el = MagicMock()
    mock_el.text = "Submit Order"
    # Setup get_element_with_text to return the element
    with patch.object(actions, "get_element_with_text", return_value=mock_el):
        # We try to click "Submit" (Partial) using the exact-match method
        result = actions.click_element_with_text(("id", "btn"), "Submit")
        assert result is False
        actions.logger.warning.assert_called()


# --- 2. Testing The Wait-For Logic (Lambdas) ---


def test_wait_for_text_logic(actions, mock_page):
    """Verify the lambda function used in WebDriverWait."""
    locator = ("id", "status")
    mock_el = MagicMock()
    mock_el.text = "Completed"
    mock_page._wait_for_visible.return_value = mock_el

    # We simulate the lambda being executed by Behave/Selenium
    actions.wait_for_text(locator, "Completed")

    # Extract the lambda passed to until()
    args, _ = mock_page.wait.until.call_args
    wait_condition = args[0]

    # Execute the lambda against a dummy driver to verify its logic
    assert wait_condition("driver") is True


# --- 3. Testing Retry Logic (Stale Elements) ---


def test_retry_click_handles_stale_element(actions, mock_page):
    """Verify retry_click catches StaleElementReferenceException and tries again."""
    mock_page.click.side_effect = [StaleElementReferenceException, True]

    with patch("time.sleep"):  # Don't slow down the test
        result = actions.retry_click(("id", "stale-link"), retries=2)

    assert result is True
    assert mock_page.click.call_count == 2
    actions.logger.warning.assert_called()


# --- 4. Testing Complex Form Population ---


def test_populate_generic_form_default_to_text(actions, mock_page):
    """Verify that if form_map doesn't specify a type, it defaults to 'text'."""
    form_map = {"user": ("id", "u-1")}  # No explicit 'text' or 'select'
    data_input = [{"field": "user", "value": "paul"}]

    actions.populate_generic_form(form_map, data_input)

    # Check if it called populate_form_field with the default 'text' type
    mock_page.populate_form_field.assert_called_once_with(("id", "u-1"), "paul", "text")


# --- 5. Testing Keyboard Logic ---


def test_send_keyboard_input_handles_invalid_key(actions, mock_page):
    """Verify that an invalid key name prints a warning but doesn't crash."""
    with patch("builtins.print") as mock_print:
        actions.send_keyboard_input(("id", "in"), "INVALID_KEY_NAME")
        # Should not raise AttributeError
        mock_print.assert_called()
        # Should still call press_keys with an empty list of valid keys
        mock_page.press_keys.assert_called_once()
