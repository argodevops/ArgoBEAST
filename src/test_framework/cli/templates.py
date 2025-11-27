PAGE_TEMPLATE = """
from test_framework.base.base_page import BasePage
from selenium.webdriver.common.by import By

class {Name}Page(BasePage):
    def __init__(self, driver, config):
        super().__init__(driver, config)

    # Add your locators here:
    # USERNAME = (By.ID, "username")
"""

ACTIONS_TEMPLATE = """
from test_framework.common_actions.common_actions import CommonActions
from pages.{name}_page import {Name}Page

class {Name}Actions(CommonActions):
    PageClass = {Name}Page

    def __init__(self, page):
        super().__init__(page)
"""

FEATURE_TEMPLATE = """
Feature: {Name}

  Scenario: Example {Name} scenario
    Given I am on the {Name} page
    When I perform an action
    Then I should see an expected result
"""

STEPS_TEMPLATE = """
from behave import given, when, then
from actions.{name}_actions import {Name}Actions

# Behave automatically injects `context`
# BaseStepContext gives you .get_page() and .get_actions()

@given("I am on the {{name}} page")
def step_go_to_page(context):
    actions = context.app.get_actions({Name}Actions)
    pass

@when("I perform an example action on the {{name}} page")
def step_example_action(context):
    actions = context.app.get_actions({Name}Actions)
    # Example: actions.login("user", "pass")
    pass

@then("I should see an example result")
def step_assert_result(context):
    actions = context.app.get_actions({Name}Actions)
    # Example: assert actions.page.is_visible(actions.page.SUCCESS_MESSAGE)
    pass
"""

CONFIG_TEMPLATE = """
# Webdriver Config

browser: chrome
headless: true
window_size: "1920,1080"

# Webdriver Constants

implicit_wait: 5
explicit_wait: 10
page_load_timeout: 30

# Application Settings

base_url: "http://localhost:8501"
default_route: "/"

# Framework Behaviour

screenshot_on_failure: true
output_directory: "test_output"
retry_failed_steps: false

# Logging Level (accepts INFO, ERROR, WARNING, DEBUG)

log_level: "INFO"
"""

REQUIREMENTS_TEMPLATE = """
selenium==4.23.1
behave==1.2.6
"""

ENVIRONMENT_TEMPLATE = """
# Automatically delegate hooks to the test framework.
from test_framework.behave_integration.environment import *
# You do not need to touch this file.
"""
