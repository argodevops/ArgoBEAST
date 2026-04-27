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
def step_go_to_page(context, name):
    actions = context.app.get_actions({ClassName}Actions)
    pass

@when("I perform an example action on the {{name}} page")
def step_example_action(context,name):
    actions = context.app.get_actions({ClassName}Actions)
    # Example: actions.login("user", "pass")
    pass

@then("I should see an expected result")
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
retry_failed_scenarios: false
# max_retries: 2 # Optional: Number of retries for failed scenarios (requires retry_failed_scenarios: true)

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

DOCKERFILE_TEMPLATE = """
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt* . 
RUN pip install --no-cache-dir argobeast \
    && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
RUN useradd -m argouser
RUN echo "export PS1='[argobeast lab]: \\w \\$ '" >> /home/argouser/.bashrc
USER argouser
ENV PS1="[argobeast lab]: " \
    IS_IN_LAB=True 
"""

DOCKER_COMPOSE_TEMPLATE = """
services:
  selenium-grid:
    image: selenium/standalone-chrome:latest
    ports:
      - "4444:4444"
      - "7900:7900" # NoVNC - lets users WATCH the tests in a browser
    shm_size: 2gb

  argobeast_runner:
    image: argobeast_runner
    container_name: argobeast-runner
    build: 
      context: .
      dockerfile: argobeast.dockerfile
    volumes:
      - .:/app
    working_dir: /app
    environment:
      - SE_REMOTE_URL=http://selenium-grid:4444/wd/hub
      - ARGO_ENV=container
      - IS_IN_LAB=True
    depends_on:
      - selenium-grid
    tty: true
    stdin_open: true
"""
