import json
import pytest
from unittest.mock import MagicMock, patch
from argo_beast.base.driver_factory import WebDriverFactory


@pytest.fixture
def mock_webdriver():
    # Patch the 'webdriver' name inside your driver_factory.py
    with patch("argo_beast.base.driver_factory.webdriver") as mock_wd:
        yield mock_wd


def test_create_driver_chrome_headless(mock_webdriver):
    """Verify that Chrome options receive the exact --headless=new argument."""
    config = {"browser": "chrome", "headless": True}
    factory = WebDriverFactory(config)

    # 1. Setup the mocks
    mock_options = MagicMock()
    mock_webdriver.ChromeOptions.return_value = mock_options

    mock_driver = MagicMock()
    mock_webdriver.Chrome.return_value = mock_driver

    # 2. Action
    factory.create_driver()

    # 3. Assert
    # Check that the factory requested ChromeOptions and added the right flag
    mock_webdriver.ChromeOptions.assert_called_once()
    mock_options.add_argument.assert_any_call("--headless=new")

    # Check that the driver was actually created
    mock_webdriver.Chrome.assert_called_once()


def test_create_driver_fallback_to_chrome(mock_webdriver):
    """Verify factory builds Chrome if browser is unrecognized."""
    config = {"browser": "commodore_64"}
    factory = WebDriverFactory(config)

    factory.create_driver()

    # In your logic, anything not 'firefox' or 'edge' defaults to Chrome
    assert mock_webdriver.Chrome.called
    assert not mock_webdriver.Firefox.called
    assert not mock_webdriver.Edge.called


def test_window_size_parsing(mock_webdriver):
    """Test the logic that splits '1920,1080'."""
    config = {"browser": "chrome", "window_size": "1280, 720"}
    factory = WebDriverFactory(config)

    mock_driver = MagicMock()
    mock_webdriver.Chrome.return_value = mock_driver

    factory.create_driver()

    # Verify the math/parsing worked
    mock_driver.set_window_size.assert_called_once_with(1280, 720)


@pytest.mark.parametrize(
    "browser, options_factory",
    [("chrome", "ChromeOptions"), ("edge", "EdgeOptions")],
)
def test_auto_select_certificates_sets_managed_prefs(
    mock_webdriver, browser, options_factory
):
    """Ensure cert auto-select prefs are added for Chromium-based browsers."""
    config = {"browser": browser, "auto_select_certificates": True}
    factory = WebDriverFactory(config)

    mock_options = MagicMock()
    # Simulate already-present prefs so we verify they are preserved.
    mock_options.experimental_options = {
        "prefs": {"download.default_directory": "/tmp"}
    }
    getattr(mock_webdriver, options_factory).return_value = mock_options

    mock_driver = MagicMock()
    if browser == "edge":
        mock_webdriver.Edge.return_value = mock_driver
    else:
        mock_webdriver.Chrome.return_value = mock_driver

    factory.create_driver()

    mock_options.add_argument.assert_any_call("--ignore-certificate-errors")

    expected_prefs = {
        "download.default_directory": "/tmp",
        "profile.managed_auto_select_certificate_for_urls": [
            json.dumps({"pattern": "*", "filter": {}})
        ],
    }
    mock_options.add_experimental_option.assert_called_once_with(
        "prefs", expected_prefs
    )
