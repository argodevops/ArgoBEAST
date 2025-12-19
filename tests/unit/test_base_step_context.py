import pytest
from unittest.mock import MagicMock
from argo_beast.base.base_step_context import BaseStepContext


@pytest.fixture
def context_setup():
    mock_driver = MagicMock()
    mock_config = {"base_url": "http://test.com"}
    return BaseStepContext(mock_driver, mock_config), mock_driver, mock_config


def test_get_page_instantiation(context_setup):
    """Verify get_page returns an instance of the requested class with driver/config."""
    context, driver, config = context_setup

    # Define a dummy Page class
    class DummyPage:
        def __init__(self, driver, config):
            self.driver = driver
            self.config = config

    page_instance = context.get_page(DummyPage)

    assert isinstance(page_instance, DummyPage)
    assert page_instance.driver == driver
    assert page_instance.config == config


def test_get_actions_orchestration(context_setup):
    """Verify get_actions creates the required page before creating the actions."""
    context, driver, config = context_setup

    # Define the relationship between Actions and Pages
    class ExpectedPage:
        def __init__(self, driver, config):
            self.driver = driver

    class DummyActions:
        PageClass = ExpectedPage  # The link the factory uses

        def __init__(self, page):
            self.page = page

    actions_instance = context.get_actions(DummyActions)

    # Assertions
    assert isinstance(actions_instance, DummyActions)
    assert isinstance(actions_instance.page, ExpectedPage)
    assert actions_instance.page.driver == driver
