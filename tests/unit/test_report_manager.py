from unittest.mock import patch
from argo_beast.behave_integration.report_manager import ReportManager


# --- Test Setup Logic ---


def test_setup_reporting_skips_if_disabled(mock_context):
    mock_context.beast_config["allure_reporting"] = False
    manager = ReportManager(mock_context)

    with patch("os.path.exists") as mock_exists:
        manager.setup_reporting()
        mock_exists.assert_not_called()


@patch("argo_beast.behave_integration.report_manager.AllureFormatter", create=True)
@patch("argo_beast.behave_integration.report_manager.os.path.exists")
@patch("argo_beast.behave_integration.report_manager.shutil.rmtree")
@patch("argo_beast.behave_integration.report_manager.ensure_dir")
def test_setup_reporting_cleans_and_registers_formatter(
    mock_ensure, mock_rmtree, mock_exists, mock_formatter, mock_context
):
    mock_exists.return_value = True
    manager = ReportManager(mock_context)

    manager.setup_reporting()

    # 1. Verify old results are wiped
    mock_rmtree.assert_called_once_with("allure-results")
    # 2. Verify new dir is created
    mock_ensure.assert_called_once_with("allure-results")
    # 3. Verify formatter is added to Behave's runner
    assert len(mock_context._runner.formatters) == 1


# --- Test Finalization Logic ---


@patch("argo_beast.behave_integration.report_manager.subprocess.run")
@patch("argo_beast.behave_integration.report_manager.cleanup_results")
@patch("argo_beast.behave_integration.report_manager.shutil.make_archive")
def test_finalise_reporting_runs_allure_cli(
    mock_zip, mock_cleanup, mock_run, mock_context
):
    manager = ReportManager(mock_context)

    manager.finalise_reporting()

    # Verify cleanup was called
    mock_cleanup.assert_called_once()
    # Verify subprocess called the Allure CLI
    mock_run.assert_called_once()
    args, _ = mock_run.call_args
    assert "allure" in args[0]
    assert "generate" in args[0]
    # Verify zip creation
    mock_zip.assert_called_once_with("allure-report", "zip", "allure-report")


def test_run_cli_handles_missing_allure_gracefully(mock_context):
    manager = ReportManager(mock_context)

    with patch(
        "argo_beast.behave_integration.report_manager.subprocess.run"
    ) as mock_run:
        # Simulate Allure not being installed in WSL/PATH
        mock_run.side_effect = FileNotFoundError

        with patch("logging.warning") as mock_log:
            manager._run_cli()
            mock_log.assert_called_with(
                "Allure CLI not found in PATH. Generation skipped."
            )
