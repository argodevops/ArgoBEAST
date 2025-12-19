import pytest
from unittest.mock import patch, mock_open, MagicMock
from argo_beast.cli.create import create, create_all, init, pip_install

# Targeting helpers and builtins for file operations
CREATE_PATH = "argo_beast.cli.create"

# --- 1. Testing Component Creation ---


@patch(f"{CREATE_PATH}.ensure_dir")
@patch(f"{CREATE_PATH}.os.path.exists", return_value=False)
@patch(f"{CREATE_PATH}.get_class_name", return_value="LoginPage")
@patch(f"{CREATE_PATH}.ok")
def test_create_page_writes_correct_file(mock_ok, mock_class, mock_exists, mock_ensure):
    """Verify that create('login', 'page') writes to pages/login_page.py."""
    m = mock_open()
    with patch("builtins.open", m):
        create("login", "page")

    # Verify directory check and file opening
    mock_ensure.assert_called_once_with("pages")
    m.assert_called_once_with("pages/login_page.py", "w")

    # Verify template content was written (checking for ClassName injection)
    handle = m()
    handle.write.assert_called()
    written_content = handle.write.call_args[0][0]
    assert "class LoginPage" in written_content


def test_create_all_triggers_multiple_calls():
    """Verify create_all calls create for page, actions, and steps."""
    with patch(f"{CREATE_PATH}.create") as mock_create:
        create_all("Search")
        assert mock_create.call_count == 3
        # Ensure it hit the core three
        calls = [call[0][1] for call in mock_create.call_args_list]
        assert "page" in calls
        assert "actions" in calls
        assert "steps" in calls

# --- 2. Testing Project Initialization (init) ---


@patch(f"{CREATE_PATH}.ensure_dir")
@patch(f"{CREATE_PATH}.pip_install")
def test_init_creates_project_structure(mock_pip, mock_ensure):
    """Verify init() creates the standard folder and file set."""
    # We mock input to simulate user saying 'Yes' to examples and 'No' to pip
    with patch("builtins.input", side_effect=["y", "n"]):
        with patch("builtins.open", mock_open()) as m:
            with patch(f"{CREATE_PATH}.create_common_features"):
                with patch(f"{CREATE_PATH}.create"):
                    init()

    # Verify key framework files are created
    written_files = [call[0][0] for call in m.call_args_list]
    assert "config/driver.yml" in written_files
    assert "features/environment.py" in written_files
    assert "requirements.txt" in written_files

# --- 3. Testing Subprocess Calls ---


@patch(f"{CREATE_PATH}.subprocess.check_call")
@patch(f"{CREATE_PATH}.sys.executable", "/usr/bin/python")
def test_pip_install_calls_correct_command(mock_call):
    """Verify pip_install triggers a 'pip install -r' subprocess."""
    pip_install("reqs.txt")

    mock_call.assert_called_once_with([
        "/usr/bin/python", "-m", "pip", "install", "-r", "reqs.txt"
    ])
