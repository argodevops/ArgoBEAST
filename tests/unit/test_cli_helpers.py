import pytest
from unittest.mock import patch
from argo_beast.cli.helpers import ensure_dir, get_class_name, ok, error, GREEN, RESET

# --- 1. Testing Path Logic ---


def test_ensure_dir_creates_path(tmp_path):
    """Verify that ensure_dir creates nested directories."""
    target_dir = tmp_path / "deeply" / "nested" / "folder"

    # Action
    ensure_dir(target_dir)

    # Assert
    assert target_dir.exists()
    assert target_dir.is_dir()


# --- 2. Testing String Formatting Logic ---


@pytest.mark.parametrize(
    "input_name, expected_class",
    [
        ("login", "Login"),
        ("user profile", "UserProfile"),
        ("submit order form", "SubmitOrderForm"),
        ("Sidebar", "Sidebar"),
    ],
)
def test_get_class_name_converts_correctly(input_name, expected_class):
    """Verify that names are converted to PascalCase for class generation."""
    assert get_class_name(input_name) == expected_class


# --- 3. Testing Console Output ---


def test_ok_prints_green_message():
    """Verify the [OK] log contains the correct ANSI color codes."""
    message = "Successfully created"
    expected_output = f"{GREEN}[OK]{RESET} {message}"

    with patch("builtins.print") as mock_print:
        ok(message)
        mock_print.assert_called_once_with(expected_output)


def test_error_prints_red_message():
    """Verify the [ERROR] log contains the red color code."""
    from argo_beast.cli.helpers import RED

    message = "Failed to write"
    expected_output = f"{RED}[ERROR]{RESET} {message}"

    with patch("builtins.print") as mock_print:
        error(message)
        mock_print.assert_called_once_with(expected_output)
