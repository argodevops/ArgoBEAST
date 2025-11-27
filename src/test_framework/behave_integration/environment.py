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


def before_all(context):
    loader = ConfigLoader()
    user_config = os.getenv("TEST_CONFIG") or USER_CONFIG_PATH
    context.config = loader.load(user_config)
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
