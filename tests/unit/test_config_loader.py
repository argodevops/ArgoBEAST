import pytest
from unittest.mock import MagicMock, patch
from argo_beast.config.loader import ConfigLoader


# --- 1. Test the Merging Logic (Pure Logic) ---


@pytest.fixture
def loader():
    return ConfigLoader()


def test_deep_merge_functionality(loader):
    """Verify that overrides correctly overwrite base values."""
    base = {"browser": "chrome", "timeout": 10, "nested": {"key": 1}}
    override = {"timeout": 30, "nested": {"key": 2}}

    result = loader._deep_merge(base, override)

    assert result["browser"] == "chrome"  # Kept from base
    assert result["timeout"] == 30  # Overwritten
    assert result["nested"]["key"] == 2  # Nested overwrite works


# --- 2. Test YAML Loading (I/O) ---


def test_load_yaml_handles_errors(loader):
    """Verify loader returns empty dict on file errors instead of crashing."""
    with patch("builtins.open", side_effect=Exception("File locked")):
        with patch("logging.Logger.error") as mock_log:
            result = loader._load_yaml("dummy.yml")
            assert result == {}
            mock_log.assert_called()


# --- 3. Test Internal Resource Loading ---


@patch("argo_beast.config.loader.resources")
def test_load_internal_defaults(mock_res, loader):
    """Verify it uses importlib.resources to find the internal defaults."""
    # Setup mock for resources.files().joinpath()...
    mock_file_path = MagicMock()
    mock_res.files.return_value.joinpath.return_value = mock_file_path

    # Mock the 'with as_file' context manager
    with patch("argo_beast.config.loader.resources.as_file") as mock_as_file:
        mock_as_file.return_value.__enter__.return_value = "fake_path.yml"

        with patch.object(
            loader, "_load_yaml", return_value={"default": True}
        ) as mock_load:
            result = loader._load_internal_defaults()
            assert result == {"default": True}
            mock_load.assert_called_with("fake_path.yml")


# --- 4. Test The Main Public Method (Orchestration) ---


def test_load_orchestration_missing_user_path(loader):
    """Verify it falls back to empty dict if user path doesn't exist."""
    with patch.object(loader, "_load_internal_defaults", return_value={"a": 1}):
        with patch("os.path.exists", return_value=False):
            with patch("logging.Logger.warning") as mock_warn:
                result = loader.load("non_existent.yml")
                assert result == {"a": 1}
                mock_warn.assert_called_with(
                    "No user config can be found, using defaults"
                )
