import pytest
from unittest.mock import patch, MagicMock
from argo_beast.cli.main import main

# We patch the names inside the main.py module
MOCK_SCOPE = "argo_beast.cli.main"


def test_main_init_calls_init_func():
    with patch("sys.argv", ["argotest", "init"]):
        # We patch 'init' inside 'main.py'
        with patch(f"{MOCK_SCOPE}.init") as mock_init:
            with patch(f"{MOCK_SCOPE}.ARGO_BEAST", "LOGO"):
                with patch("builtins.print"):
                    main()
                    mock_init.assert_called_once()


def test_main_create_page_calls_create():
    with patch("sys.argv", ["argotest", "create", "page", "MyPage"]):
        with patch(f"{MOCK_SCOPE}.create") as mock_create:
            with patch(f"{MOCK_SCOPE}.info"):
                main()
                mock_create.assert_called_once_with("MyPage", "page")


def test_main_unknown_command_shows_warn():
    # Note: Using 4 args to satisfy your logic: argotest create page name
    with patch("sys.argv", ["argotest", "unknown", "type", "name"]):
        with patch(f"{MOCK_SCOPE}.warn") as mock_warn:
            main()
            mock_warn.assert_called()
