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
