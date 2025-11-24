from behave import *
from behave.model_core import Status
from test_framework.base.driver_factory import WebDriverFactory
from test_framework.base.base_step_context import BaseStepContext
from test_framework.config.loader import ConfigLoader
from dotenv import load_dotenv
import os


USER_CONFIG_PATH = "config/driver.yml"
load_dotenv()


def before_all(context):
    loader = ConfigLoader()
    user_config = os.getenv("TEST_CONFIG") or USER_CONFIG_PATH
    config = loader.load(user_config)
    context.config = config
    context.factory = WebDriverFactory(context.config)


def before_scenario(context, scenario):
    context.driver = context.factory.create_driver()
    context.app = BaseStepContext(context)


def after_scenario(context, scenario):
    if scenario.status == Status.failed:
        context.driver.save_screenshot("./screenshot.png")
    context.factory.quit_driver()


def after_all(context):
    pass
