import os
import pytest
from unittest.mock import MagicMock, patch
from argo_beast.behave_integration.behave_helpers import (override_config_with_env_vars,
                                                          cleanup_results,
                                                          parse_tags,
                                                          parse_hooks,
                                                          run_common_features)


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


def test_cleanup_results_removes_skipped_allure_json(tmp_path, create_allure_files):
    """Test that cleanup_results removes files marked as skipped."""
    # 1. Setup: Create a temporary allure-pytest-results directory
    results_dir = tmp_path / "allure-pytest-results"
    results_dir.mkdir()
    # 2. Action: Call cleanup_results on the temp dir
    # We pass hide_skipped=True to trigger the deletion
    skipped_file, magic_file, passed_file = create_allure_files(results_dir)
    cleanup_results(results_dir=str(results_dir), hide_skipped=True)

    # 3. Assert
    assert not os.path.exists(
        str(skipped_file)), "Skipped file was not deleted!"
    assert not os.path.exists(
        str(magic_file)), "Magic file was not deleted!"
    assert os.path.exists(
        str(passed_file)), "Passed file was accidentally deleted!"


def test_cleanup_results_keeps_non_skipped_allure_json(tmp_path, create_allure_files):
    """Test that cleanup_results keeps non-skipped files."""
    # 1. Setup: Create a temporary allure-pytest-results directory
    results_dir = tmp_path / "allure-pytest-results"
    results_dir.mkdir()
    # 2. Action: Call cleanup_results on the temp dir
    # We pass hide_skipped=False to avoid deletion
    skipped_file, magic_file, passed_file = create_allure_files(results_dir)
    cleanup_results(results_dir=str(results_dir), hide_skipped=False)

    # 3. Assert
    assert os.path.exists(
        str(skipped_file)), "Skipped file was accidentally deleted!"
    assert not os.path.exists(
        str(magic_file)), "Magic file was not deleted!"
    assert os.path.exists(
        str(passed_file)), "Passed file was accidentally deleted!"


def test_parse_tags_extracts_steps_correctly():
    """Test that parse_tags correctly maps a tag to a block of Gherkin steps."""

    # 1. Create a mock Feature object that mimics Behave's structure
    mock_feature = MagicMock()
    mock_scenario = MagicMock()

    # Setup tags: Logic says skip setup/teardown, pick the first other tag
    mock_scenario.tags = ["setup:ignore", "login"]

    # Setup steps
    mock_step = MagicMock()
    mock_step.keyword = "Given"
    mock_step.name = "I am logged in"
    mock_step.table = None
    mock_step.text = None
    mock_scenario.steps = [mock_step]

    mock_feature.scenarios = [mock_scenario]

    # 2. Patch 'parse_file' so it returns our mock instead of reading the disk
    with patch("argo_beast.behave_integration.behave_helpers.parse_file", return_value=mock_feature):
        # The path doesn't matter now because the mock intercepts it
        result = parse_tags("dummy_path.feature")

    # 3. Assertions
    assert "login" in result
    assert result["login"] == "Given I am logged in\n"


def test_parse_hooks_aggregates_multiple_files(tmp_path):
    """Test that parse_hooks crawls a directory and merges results from all .feature files."""

    # 1. Setup: Create a nested folder structure in tmp_path
    common_dir = tmp_path / "features" / "_common"
    auth_dir = common_dir / "auth"
    db_dir = common_dir / "database"

    auth_dir.mkdir(parents=True)
    db_dir.mkdir(parents=True)

    # Create dummy .feature files
    (auth_dir / "login.feature").write_text("...")
    (db_dir / "cleanup.feature").write_text("...")
    # Should be ignored (not .feature)
    (common_dir / "random.txt").write_text("...")

    # 2. Mock parse_tags:
    # We don't want to test parse_tags again. We just want to see if parse_hooks
    # collects what parse_tags returns.
    def side_effect(path):
        if "login.feature" in path:
            return {"login_hook": "Given I login"}
        if "cleanup.feature" in path:
            return {"db_hook": "Then I clean DB"}
        return {}

    with patch("argo_beast.behave_integration.behave_helpers.parse_tags", side_effect=side_effect):
        # 3. Action
        results = parse_hooks(hooks_path=str(common_dir))

    # 4. Assert
    assert "login_hook" in results
    assert "db_hook" in results
    assert len(results) == 2
    # Verify the values came through
    assert "Given I login" in results["login_hook"]


def test_run_common_features_executes_correct_hook(mock_context):
    """Verify that execute_steps is called with the Gherkin string from the library."""
    # 1. Setup Scenario with tags
    mock_scenario = MagicMock()
    mock_scenario.feature.tags = []
    mock_scenario.tags = ["setup:login", "smoke"]

    # 2. Setup Context with a mock library and execute_steps method
    mock_context.beast_hooks = {"login": "Given I am logged in"}
    # mock_context already has execute_steps if using our earlier fixture,
    # but let's ensure it's there for this test:
    mock_context.execute_steps = MagicMock()

    # 3. Action
    run_common_features(mock_scenario, mock_context, stage="setup")

    # 4. Assert
    mock_context.execute_steps.assert_called_once_with("Given I am logged in")


def test_run_common_features_fails_hard_on_error(mock_context):
    """Verify that if execute_steps raises an error, the test asserts False."""
    mock_scenario = MagicMock()
    mock_scenario.feature.tags = ["setup:db"]
    mock_scenario.tags = []

    mock_context.beast_hooks = {"db": "Given a broken DB"}
    mock_context.execute_steps = MagicMock(
        side_effect=Exception("Connection Timeout"))

    # 3. Action & Assert
    with pytest.raises(AssertionError) as excinfo:
        run_common_features(mock_scenario, mock_context,
                            stage="setup", fail_hard=True)

    assert "ArgoBEAST setup Failed" in str(excinfo.value)
    assert "Connection Timeout" in str(excinfo.value)
