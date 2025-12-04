from behave import *
from behave.model_core import Status
from test_framework.base.driver_factory import WebDriverFactory
from test_framework.base.base_step_context import BaseStepContext
from test_framework.config.loader import ConfigLoader
from test_framework.cli.helpers import ensure_dir
from dotenv import load_dotenv
import os
import datetime

USER_CONFIG_PATH = "config/driver.yml"
load_dotenv()


def override_config_with_env_vars(config_data):
    """
    Checks for specific environment variables and overrides corresponding config values.
    """
    # Define a mapping from Environment Variable Name (UPPERCASE)
    # to the config dictionary key (lowercase/snake_case)
    ENV_OVERRIDES = {
        "BASE_URL": "base_url",
        "REMOTE_URL": "remote_url",
        "LOG_LEVEL": "log_level",
        # Add any other variables you want to be able to override here
    }

    print("Checking environment variables for config overrides...")

    for env_var, config_key in ENV_OVERRIDES.items():
        env_value = os.getenv(env_var)

        if env_value:
            # Assuming your config_data is a dictionary structure
            # and that 'base_url' and 'remote_url' are at the top level.
            # You may need to adjust this if they are nested (e.g., config_data['application_settings'][config_key] = env_value)

            config_data[config_key] = env_value
            print(
                f"  --> OVERRIDE: {config_key} set to '{env_value}' via {env_var}")

    return config_data


def before_all(context):
    loader = ConfigLoader()
    user_config = os.getenv("TEST_CONFIG") or USER_CONFIG_PATH
    config_data = loader.load(user_config)
    final_config = override_config_with_env_vars(config_data)
    context.config = final_config
    context.factory = WebDriverFactory(context.config)


def before_scenario(context, scenario):
    context.driver = context.factory.create_driver()
    context.app = BaseStepContext(context.driver, context.config)


def after_scenario(context, scenario):
    # Screenshot on failure
    if scenario.status == Status.failed:

        if "screenshot_on_failure" in context.config:
            if "output_directory" in context.config:
                output_dir = context.config.get("output_directory")
            else:
                output_dir = "output"
            if context.config.get("screenshot_on_failure") == "true" or context.config.get("screenshot_on_failure") == True:
                try:
                    x = datetime.datetime.now()
                    screenshot_name = (
                        f"fail_{x.hour}-{x.minute}_{x.year}{x.month}{x.day}.png"
                        .replace(" ", "_")
                    )
                    ensure_dir(output_dir)
                    context.driver.save_screenshot(
                        f"./{output_dir}/{screenshot_name}")
                except Exception:
                    pass

    # Quit driver normally
    try:
        context.driver.quit()
    except Exception:
        pass

    # Clear our own references
    context.driver = None
    context.app = None


def after_all(context):
    pass
