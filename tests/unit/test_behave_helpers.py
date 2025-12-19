import os
import pytest
from argo_beast.behave_integration.behave_helpers import override_config_with_env_vars


def test_override_config_base_url(monkeypatch):
    """Verify that BASE_URL env var overrides the config dictionary."""
    # Setup
    initial_config = {"base_url": "http://original.com", "other_key": "stays"}

    # Use monkeypatch to safely set an env var for this test only
    monkeypatch.setenv("BASE_URL", "https://overridden.com")

    # Action
    updated_config = override_config_with_env_vars(initial_config)

    # Assert
    assert updated_config["base_url"] == "https://overridden.com"
    assert updated_config["other_key"] == "stays"


def test_no_override_when_env_not_set(initial_config={"base_url": "http://original.com"}):
    """Verify config remains unchanged if no env vars are present."""
    updated_config = override_config_with_env_vars(initial_config)
    assert updated_config["base_url"] == "http://original.com"
