import json
import pytest
from unittest.mock import MagicMock
from behave.model_core import Status


@pytest.fixture
def mock_context():
    """Provides a mocked Behave context object."""
    context = MagicMock()
    # Simulate the structure Behave uses
    context.scenario = MagicMock()
    context.scenario.tags = []
    return context


@pytest.fixture
def create_allure_files():
    """Fixture to create a set of standard test files in a given directory."""
    def _create(directory):
        skipped_file = directory / "skipped-result.json"
        skipped_file.write_text(json.dumps(
            {"status": "skipped", "fullName": "test1"}))

        magic_file = directory / "magic-result.json"
        magic_file.write_text(json.dumps(
            {"status": "skipped", "fullName": "features/_common/login"}))

        passed_file = directory / "passed-result.json"
        passed_file.write_text(json.dumps(
            {"status": "passed", "fullName": "test2"}))

        return skipped_file, magic_file, passed_file
    return _create


@pytest.fixture
def mock_context():
    context = MagicMock()
    # Mocking beast_config for after_scenario logic
    context.beast_config = {
        "screenshot_on_failure": "true", "output_directory": "test_output"}
    return context


@pytest.fixture
def mock_scenario():
    scenario = MagicMock()
    scenario.effective_tags = []
    scenario.feature.filename = "features/login.feature"
    scenario.status = Status.passed
    return scenario


@pytest.fixture
def mock_context():
    context = MagicMock()
    context.beast_config = {
        "allure_reporting": True,
        "hide_excluded_tests": True,
        "auto_generate_report": True
    }
    # Behave runner structure
    context._runner.formatters = []
    return context
