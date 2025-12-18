PAGE_TEMPLATE = """
from argo_beast.base.base_page import BasePage
from selenium.webdriver.common.by import By

class {ClassName}Page(BasePage):
    def __init__(self, driver, config):
        super().__init__(driver, config)

    # Add your locators here:
    # USERNAME = (By.ID, "username")
"""

ACTIONS_TEMPLATE = """
from argo_beast.common_actions.common_actions import CommonActions
from pages.{name}_page import {ClassName}Page

class {ClassName}Actions(CommonActions):
    PageClass = {ClassName}Page

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
from actions.{name}_actions import {ClassName}Actions

# Behave automatically injects `context`
# BaseStepContext gives you .get_page() and .get_actions()

@given("I am on the {{name}} page")
def step_go_to_page(context):
    actions = context.app.get_actions({ClassName}Actions)
    pass

@when("I perform an example action on the {{name}} page")
def step_example_action(context):
    actions = context.app.get_actions({ClassName}Actions)
    # Example: actions.login("user", "pass")
    pass

@then("I should see an example result")
def step_assert_result(context):
    actions = context.app.get_actions({ClassName}Actions)
    # Example: assert actions.page.is_visible(actions.page.SUCCESS_MESSAGE)
    pass
"""

CONFIG_TEMPLATE = """
# Webdriver Config

browser: chrome
headless: true
window_size: "1920,1080"
remote_url: ""

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

# Optional: Add any extra flags here.
# WARNING: Ensure these flags match your selected browser!
# browser_args:
#   - "--incognito"
#   - "--disable-gpu"
#   - "--ignore-certificate-errors"

# Allure reporting

allure_reporting: false # Set this to 'true' to enable allure reporting (will need to be installed)
hide_skipped_tests: false # Add a @skip tag to any scenario to skip it - setting this to 'true' will hide the test from the report
auto_generate_report: false # Setting this to 'true' will tell ArgoBEAST to attempt to generate an HTML report at the end of the run.
allure_keep_history: false # Setting this to 'true' will keep a running history of the last 20 runs.

# Logging Level (accepts INFO, ERROR, WARNING, DEBUG)

log_level: "INFO"

"""

REQUIREMENTS_TEMPLATE = """
selenium==4.23.1
behave==1.2.6
"""

ENVIRONMENT_TEMPLATE = """
# Automatically delegate hooks to the test framework.
from argo_beast.behave_integration.environment import *
# You do not need to touch this file.
"""

COMMON_FEATURE_EXAMPLE = """
# ==============================================================================
#  This file contains reusable scenarios (Hooks).
#  These scenarios do NOT run as standalone tests.
#
#  HOW TO USE:
#  1. Define a scenario here and tag it with a unique ID (e.g. @login_admin).
#  2. To run it BEFORE a test, tag your test with @setup:login_admin
#  3. To run it AFTER a test, tag your test with @teardown:login_admin
# ==============================================================================

Feature: Authentication Hooks

  @login_admin
  Scenario: Login as Administrator
    Given I navigate to the login page
    When I enter "admin" into the username field
    And I enter "password123" into the password field
    And I click the login button
    Then I should be on the dashboard

  @login_guest
  Scenario: Login as Guest User
    Given I navigate to the login page
    When I click the "Continue as Guest" link
    Then I should be on the home page
"""
