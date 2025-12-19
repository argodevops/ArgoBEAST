from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.webdriver.common.by import By
from argo_beast.base.base_page import BasePage


@pytest.fixture
def mock_driver():
    return MagicMock()


@pytest.fixture
def base_page(mock_driver):
    config = {"explicit_wait": 10, "base_url": "http://test.com"}
    return BasePage(mock_driver, config)

# --- 1. Testing Atomic Waiters ---


def test_wait_for_visible_calls_selenium_wait(base_page, mock_driver):
    """Verify that _wait_for_visible uses WebDriverWait correctly."""
    locator = (By.ID, "submit")
    mock_element = MagicMock()

    # We mock the 'until' method of the WebDriverWait object
    with patch("selenium.webdriver.support.wait.WebDriverWait.until", return_value=mock_element):
        element = base_page._wait_for_visible(locator)
        assert element == mock_element

# --- 2. Testing High-Level Actions ---


def test_click_success(base_page):
    """Verify click() waits for element and then clicks it."""
    locator = (By.ID, "btn")
    mock_element = MagicMock()

    with patch.object(base_page, "_wait_for_clickable", return_value=mock_element):
        result = base_page.click(locator)
        assert result is True
        mock_element.click.assert_called_once()


def test_click_timeout_returns_false(base_page):
    """Verify click() returns False and logs warning on timeout without crashing."""
    locator = (By.ID, "btn")

    # We simulate the timeout
    with patch.object(base_page, "_wait_for_clickable", side_effect=TimeoutException):
        # We catch the logger to ensure the message is correct
        with patch.object(base_page, "logger") as mock_log:
            result = base_page.click(locator)

            assert result is False
            # Ensure the log was called with the tuple, not an .id attribute
            mock_log.warning.assert_called_with(
                f"Unable to click locator {locator}")
# --- 3. Testing Form Helpers (The Dispatcher) ---


def test_populate_form_field_text_routing(base_page):
    """Verify dispatcher routes 'text' type to type_text."""
    locator = (By.ID, "username")
    with patch.object(base_page, "type_text") as mock_type:
        base_page.populate_form_field(locator, "paul", input_type="text")
        mock_type.assert_called_once_with(locator, "paul")

# --- 4. Testing Table Logic (The Complex Stuff) ---


def test_get_table_data_parsing(base_page):
    """Verify HTML table rows are converted to a list of dicts."""
    locator = (By.ID, "user-table")

    # Mock Table Structure
    mock_table = MagicMock()
    mock_header_1 = MagicMock()
    mock_header_1.text = "Name"
    mock_header_2 = MagicMock()
    mock_header_2.text = "Role"

    mock_row = MagicMock()
    mock_cell_1 = MagicMock()
    mock_cell_1.text = "Alice"
    mock_cell_2 = MagicMock()
    mock_cell_2.text = "Admin"

    # Setup the 'find_elements' returns
    mock_table.find_elements.side_effect = [
        [mock_header_1, mock_header_2],  # Call 1: Headers
        [mock_row]                      # Call 2: Rows
    ]
    mock_row.find_elements.return_value = [mock_cell_1, mock_cell_2]

    with patch.object(base_page, "_wait_for_visible", return_value=mock_table):
        data = base_page.get_table_data(locator)

        assert len(data) == 1
        assert data[0]["Name"] == "Alice"
        assert data[0]["Role"] == "Admin"


def test_populate_dropdown_logic(base_page):
    """Test standard select dropdown logic."""
    locator = ("id", "my-select")
    mock_el = MagicMock()

    with patch.object(base_page, "_wait_for_visible", return_value=mock_el):
        # We need to patch the Select class that BasePage imports
        with patch("argo_beast.base.base_page.Select") as mock_select:
            base_page.populate_dropdown(locator, "Option 1")
            # Verify it tries to select by visible text
            mock_select.return_value.select_by_visible_text.assert_called_with(
                "Option 1")


def test_populate_checkbox_toggle(base_page):
    """Test checkbox logic: only clicks if state needs to change."""
    locator = ("id", "my-check")
    mock_el = MagicMock()

    with patch.object(base_page, "_wait_for_clickable", return_value=mock_el):
        # Case 1: Already selected, want it ON -> Should NOT click
        mock_el.is_selected.return_value = True
        base_page.populate_checkbox(locator, "true")
        assert mock_el.click.call_count == 0

        # Case 2: Not selected, want it ON -> Should click
        mock_el.is_selected.return_value = False
        base_page.populate_checkbox(locator, "true")
        assert mock_el.click.call_count == 1


def test_make_element_interactable_js(base_page, mock_driver):
    """Verify JS script is executed to force visibility."""
    mock_el = MagicMock()
    base_page._make_element_interactable(mock_el)

    # Check that the driver's execute_script was called with the style-fixing code
    args, _ = mock_driver.execute_script.call_args
    assert "arguments[0].style.visibility='visible'" in args[0]
    assert args[1] == mock_el


def test_find_all_returns_empty_list_on_timeout(base_page):
    """Verify find_all returns [] and logs on timeout."""
    locator = (By.ID, "items")

    # 1. Simulate the timeout
    with patch.object(base_page, "_wait_for_presence", side_effect=TimeoutException):

        # 2. Patch the logger instance already attached to the base_page
        with patch.object(base_page, "logger") as mock_logger:
            result = base_page.find_all(locator)

            # 3. Assertions
            assert result == []
            # Use mock_logger.warning.assert_called_with since it's an instance mock
            mock_logger.warning.assert_called_with("No elements found")


def test_get_table_data_with_missing_cells(base_page):
    """Verify table parsing handles rows with fewer cells than headers (covers lines 313-330)."""
    locator = (By.ID, "broken-table")

    # Mock headers: Name, Age
    # Mock row: Alice (Missing the 'Age' cell)
    mock_table = MagicMock()
    mock_header = MagicMock()
    mock_header.text = "Name"
    mock_header_2 = MagicMock()
    mock_header_2.text = "Age"

    mock_row = MagicMock()
    mock_cell = MagicMock()
    mock_cell.text = "Alice"

    # find_elements returns: [headers], then [rows]
    mock_table.find_elements.side_effect = [
        [mock_header, mock_header_2], [mock_row]]
    # the row's find_elements returns only one cell
    mock_row.find_elements.return_value = [mock_cell]

    with patch.object(base_page, "_wait_for_visible", return_value=mock_table):
        data = base_page.get_table_data(locator)

        assert data[0]["Name"] == "Alice"
        # Verifies the 'else: row_data[header] = None' branch
        assert data[0]["Age"] is None


def test_get_table_headers_fallback_logic(base_page):
    """Test the fallback from thead to tr[1] (covers lines 270-280)."""
    mock_table = MagicMock()
    # Simulate: thead find fails (returns empty), but tr[1] find succeeds
    mock_header = MagicMock()
    mock_header.text = "FallBackHeader"
    mock_table.find_elements.side_effect = [[], [mock_header]]

    with patch.object(base_page, "_wait_for_visible", return_value=mock_table):
        headers = base_page.get_table_headers((By.ID, "table"))
        assert headers == ["FallBackHeader"]

# --- 2. Testing Radio Groups and Dispatcher (The branch-heavy parts) ---


def test_populate_radio_group_text_strategy(base_page):
    """Verify XPATH strategy for radio buttons by label (covers lines 196-211)."""
    mock_container = MagicMock()
    mock_radio = MagicMock()
    mock_container.find_element.return_value = mock_radio

    with patch.object(base_page, "_wait_for_visible", return_value=mock_container):
        base_page.populate_radio_group((By.ID, "group"), "OptionA")
        mock_radio.click.assert_called_once()
        # Verify it used the Label XPATH strategy first
        args, _ = mock_container.find_element.call_args
        assert "label" in args[1]

# --- 3. Testing JS Executions (Scrolling and Visibility) ---


def test_scroll_into_view_timeout(base_page):
    """Verify scroll_into_view handles timeout and logs warning."""
    # 1. Manually overwrite the real logger with a MagicMock
    base_page.logger = MagicMock()

    with patch.object(base_page, "_wait_for_visible", side_effect=TimeoutException):
        result = base_page.scroll_into_view(("id", "footer"))

        assert result is False
        # 2. Assert against our explicit mock
        base_page.logger.warning.assert_called()


def test_set_value_handles_invalid_argument(base_page):
    """Verify set_value handles InvalidArgumentException and logs error."""
    # 1. Manually overwrite the real logger with a MagicMock
    base_page.logger = MagicMock()

    mock_el = MagicMock()
    mock_el.send_keys.side_effect = InvalidArgumentException

    with patch.object(base_page, "find", return_value=mock_el):
        with patch.object(base_page, "_make_element_interactable"):
            result = base_page.set_value(("id", "input"), "data")

            assert result is False
            # 2. Assert against our explicit mock
            base_page.logger.error.assert_called()

# --- 4. Testing Visibility variants ---


def test_is_not_visible_logic(base_page):
    """Covers lines 124-125."""
    with patch.object(base_page, "_wait_for_invisible", return_value=True):
        assert base_page.is_not_visible((By.ID, "loader")) is True


def test_populate_checkbox_toggle_logic(base_page):
    """Verify checkbox only clicks when the state needs to change (Lines 214-227)."""
    mock_el = MagicMock()
    # Mocking _wait_for_clickable to return our element
    with patch.object(base_page, "_wait_for_clickable", return_value=mock_el):

        # Case 1: Target is 'true', element is NOT selected -> Should click
        mock_el.is_selected.return_value = False
        base_page.populate_checkbox(("id", "check"), "true")
        assert mock_el.click.call_count == 1

        # Case 2: Target is 'true', element IS already selected -> Should NOT click
        mock_el.click.reset_mock()
        mock_el.is_selected.return_value = True
        base_page.populate_checkbox(("id", "check"), "true")
        assert mock_el.click.call_count == 0


def test_populate_form_field_dispatcher_routing(base_page):
    """Verify the dispatcher routes to correct atomic methods (Lines 232-240)."""
    locator = ("id", "field")

    # We patch the atomic methods we already tested to verify routing
    with patch.object(base_page, "populate_dropdown") as mock_drop:
        with patch.object(base_page, "populate_checkbox") as mock_check:
            with patch.object(base_page, "populate_radio_group") as mock_radio:

                base_page.populate_form_field(locator, "value", "select")
                mock_drop.assert_called_once_with(locator, "value")

                base_page.populate_form_field(locator, "true", "checkbox")
                mock_check.assert_called_once_with(locator, "true")

                base_page.populate_form_field(locator, "option", "radio_group")
                mock_radio.assert_called_once_with(locator, "option")


def test_populate_form_field_unknown_type_raises_error(base_page):
    """Verify ValueError is raised for unknown input types (Line 240)."""
    with pytest.raises(ValueError) as exc:
        base_page.populate_form_field(("id", "x"), "val", "unknown_widget")
    assert "Unknown input_type 'unknown_widget'" in str(exc.value)
