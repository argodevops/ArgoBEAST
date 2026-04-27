from unittest.mock import patch, mock_open, MagicMock
import subprocess
import os
from argo_beast.cli.beast_lab import (
    build_lab,
    open_lab,
    close_lab,
    _update_driver_config,
)
from argo_beast.cli.templates import DOCKERFILE_TEMPLATE


## 1. Test Building the Lab
@patch("os.path.exists")
@patch("argo_beast.cli.beast_lab.ensure_dir")
@patch("builtins.open", new_callable=mock_open)
def test_build_lab_creates_files(mock_file, mock_ensure_dir, mock_exists):
    # Setup: Files don't exist yet
    mock_exists.return_value = False

    build_lab()

    # Verify directory was checked/created
    mock_ensure_dir.assert_called_with("argobeast_lab")

    # Verify Dockerfile and Compose were written
    # 2 files + potentially directory creation check
    assert mock_file.call_count >= 2
    mock_file().write.assert_any_call(DOCKERFILE_TEMPLATE)


## 2. Test Opening the Lab (Success Path)
@patch("os.path.exists")
@patch("subprocess.run")
@patch("argo_beast.cli.beast_lab._update_driver_config")
def test_open_lab_success(mock_update_cfg, mock_run, mock_exists):
    mock_exists.return_value = True
    mock_update_cfg.return_value = True

    # Simulate Docker Compose Up
    mock_run.return_value = MagicMock(returncode=0)

    open_lab()

    # Should run 'docker compose up' AND 'docker exec'
    assert mock_run.call_count == 2
    assert mock_run.call_args_list[0][0][0][1] == "compose"
    assert mock_run.call_args_list[1][0][0][1] == "exec"


## 3. Test Safety Guard (Already in Lab)
def test_open_lab_aborts_if_already_inside(monkeypatch):
    monkeypatch.setenv("IS_IN_LAB", "True")

    with patch("argo_beast.cli.beast_lab.warn") as mock_warn:
        open_lab()
        mock_warn.assert_called_with("You are already in the lab!")


## 4. Test Docker Permission Denied Handling
@patch("os.path.exists")
@patch("subprocess.run")
@patch("argo_beast.cli.beast_lab._update_driver_config")
def test_open_lab_permission_denied(mock_update_cfg, mock_run, mock_exists):
    mock_exists.return_value = True
    mock_update_cfg.return_value = True

    # Simulate the Permission Denied error from Docker
    error = subprocess.CalledProcessError(1, cmd="docker compose")
    error.stderr = "permission denied while trying to connect to the Docker daemon"
    mock_run.side_effect = error

    with patch("argo_beast.cli.beast_lab.warn") as mock_warn:
        open_lab()
        # Verify the custom permission instructions were triggered
        mock_warn.assert_any_call(
            "[SYSTEM] Permission Denied: Cannot connect to the Docker daemon."
        )


## 5. Test Config Wiring (driver.yml)
@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="browser: chrome\n")
def test_update_driver_config_appends_url(mock_file, mock_exists):
    mock_exists.return_value = True

    result = _update_driver_config()

    assert result is True
    # Verify it opened in append mode
    mock_file.assert_called_with("config/driver.yml", "a", encoding="utf-8")
    mock_file().write.assert_any_call("\n# Added by argobeast build lab\n")
    mock_file().write.assert_any_call('remote_url: "http://selenium-grid:4444/wd/hub"\n')


## 6. Test Closing the Lab
@patch("os.path.exists")
@patch("subprocess.run")
def test_close_lab(mock_run, mock_exists):
    # Ensure it doesn't think it's inside the lab
    with patch.dict(os.environ, {}, clear=True):
        close_lab()
        # Check if 'docker compose down' was called
        assert mock_run.call_args[0][0][4] == "down"
