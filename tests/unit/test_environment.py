import pytest
from unittest.mock import MagicMock, patch
from behave.model_core import Status
from argo_beast.behave_integration.environment import before_all, before_scenario, after_scenario


@patch("argo_beast.behave_integration.environment.ConfigLoader")
@patch("argo_beast.behave_integration.environment.ReportManager")
@patch("argo_beast.behave_integration.environment.WebDriverFactory")
@patch("argo_beast.behave_integration.environment.parse_hooks")
def test_before_all_initialises_framework(mock_parse, mock_factory, mock_report, mock_loader, mock_context):
    """Verify that before_all sets up all core ArgoBEAST components."""
    # Action
    before_all(mock_context)

    # Assert
    assert hasattr(mock_context, 'beast_config')
    assert hasattr(mock_context, 'report_manager')
    assert hasattr(mock_context, 'factory')
    mock_report.return_value.setup_reporting.assert_called_once()
    mock_parse.assert_called_once()

# --- TESTS FOR before_scenario (Skipping Logic) ---


def test_before_scenario_skips_common_library_on_bulk_run(mock_context, mock_scenario):
    """Verify that features in _common are skipped if not explicitly called."""
    # 1. Setup path that MUST trigger the "/_common/" check
    # Note the leading slash to ensure "/_common/" matches
    mock_scenario.feature.filename = "features/_common/setup_db.feature"

    # 2. Setup context to simulate a "Bulk Run" (behave features/)
    # Ensure paths is a list and doesn't contain the specific file
    mock_context.config.tags = []
    mock_context.config.paths = ["features/"]

    # 3. Action
    before_scenario(mock_context, mock_scenario)

    # 4. Assert
    # Verify the skip was called with your exact string
    expected_msg = f"Skipping Library Scenario '{mock_scenario.name}' (Implicit Bulk Run)"
    mock_scenario.skip.assert_called_with(expected_msg)


def test_before_scenario_runs_common_if_explicitly_targeted(mock_context, mock_scenario):
    """Verify that features in _common RUN if the user explicitly points to them."""
    path = "features/_common/login.feature"
    mock_scenario.feature.filename = path
    mock_context.config.tags = []
    mock_context.config.paths = [path]  # Explicit target

    # We mock the factory to avoid real driver creation
    mock_context.factory.create_driver.return_value = MagicMock()

    with patch("argo_beast.behave_integration.environment.run_common_features"):
        before_scenario(mock_context, mock_scenario)

    # Assert
    assert not mock_scenario.skip.called
    mock_context.factory.create_driver.assert_called()

# --- TESTS FOR after_scenario ---


def test_after_scenario_quits_driver_and_cleans_up(mock_context, mock_scenario):
    """Verify driver is closed and references are nulled."""
    mock_driver = MagicMock()
    mock_context.driver = mock_driver

    # Action
    after_scenario(mock_context, mock_scenario)

    # Assert
    mock_driver.quit.assert_called_once()
    assert mock_context.driver is None
    assert mock_context.app is None


def test_after_scenario_takes_screenshot_on_failure(mock_context, mock_scenario):
    """Verify screenshot logic is triggered on failure."""
    # 1. Setup
    mock_scenario.status = Status.failed
    mock_driver = MagicMock()
    mock_context.driver = mock_driver

    # Force config to enable screenshots
    mock_context.beast_config = {
        "screenshot_on_failure": "true",
        "output_directory": "test_output"
    }

    # 2. PATCH THE CONSUMER: Point to the environment module's reference
    with patch("argo_beast.behave_integration.environment.ensure_dir") as mock_ensure:
        after_scenario(mock_context, mock_scenario)

        # 3. Assert
        # Check if the folder creation was attempted
        mock_ensure.assert_called_once_with("test_output")
        # Check if Selenium tried to save the file
        assert mock_driver.save_screenshot.called
