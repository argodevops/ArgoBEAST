# environment.py
import os
import datetime
from behave.model_core import Status
from dotenv import load_dotenv

# Internal Imports
from argo_beast.base.driver_factory import WebDriverFactory
from argo_beast.base.base_step_context import BaseStepContext
from argo_beast.config.loader import ConfigLoader
from argo_beast.cli.helpers import ensure_dir
from argo_beast.behave_integration.report_manager import ReportManager

# New Helper Imports
from argo_beast.behave_integration.behave_helpers import (
    parse_hooks,
    run_common_features,
    override_config_with_env_vars,
)

USER_CONFIG_PATH = "config/driver.yml"
load_dotenv()


def _patch_with_driver_healing(scenario, context):
    original_run = scenario.run
    max_retries = context.beast_config.get("max_retries", 2)

    def run_with_healing(runner):
        ctx = runner.context
        original_run(runner)

        if scenario.status != Status.failed:
            return

        for attempt in range(max_retries):
            if getattr(ctx, "driver", None):
                try:
                    ctx.driver.quit()
                except:  # pylint: disable=bare-except  # noqa: E722
                    pass
                ctx.driver = None

            scenario.reset()
            # Mark steps as untested so they show up in logs correctly
            for step in scenario.steps:
                step.status = Status.untested

            # 3. Fresh Start
            try:
                ctx.driver = ctx.factory.create_driver()
                context.driver = ctx.driver  # Update main context reference as well
                base_url = context.beast_config.get("base_url")
                if base_url:
                    ctx.driver.get(base_url)
                run_common_features(scenario, context, "setup", fail_hard=True)

                # 4. Execute
                original_run(runner)

                if scenario.status != Status.failed:
                    return
            except Exception as e:
                print(f"Retry {attempt + 1} aborted due to: {e}")
                continue

    scenario.run = run_with_healing


def before_all(context):
    """
    Behave hook to run before all tests.
    :param context: Default Behave context object
    """
    loader = ConfigLoader()
    user_config = os.getenv("TEST_CONFIG") or USER_CONFIG_PATH
    config_data = loader.load(user_config)
    context.beast_config = override_config_with_env_vars(config_data)

    context.report_manager = ReportManager(context)
    context.report_manager.setup_reporting()

    context.factory = WebDriverFactory(context.beast_config)
    context.beast_hooks = parse_hooks()


def before_feature(context, feature):
    """
    Run once per feature file.
    Decides if we need to wrap scenarios in retry logic.
    """
    global_retry = context.beast_config.get("retry_failed_scenarios", False)

    for scenario in feature.walk_scenarios():
        if global_retry or "autoretry" in scenario.effective_tags:
            _patch_with_driver_healing(scenario, context)


def before_scenario(context, scenario):
    """
    Behave hook to run before each scenario.
    :param context: Default Behave context object
    :param scenario: The scenario about to be executed
    """

    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
    # 1. Normalise path
    current_file = scenario.feature.filename.replace("\\", "/")

    # 2. Check if this is a Magic Hook (lives in _common)
    # We check if "_common" is a distinct part of the path to avoid partial matches
    if "/_common/" in current_file or "_common/" in current_file:
        should_run = False

        # CHECK A: Did the user ask for specific TAGS? (e.g. behave -t @login)
        if context.config.tags:
            should_run = True

        # CHECK B: Did the user explicitly point to this file/folder?
        else:
            user_args = [p.replace("\\", "/") for p in context.config.paths]
            for arg in user_args:
                # If arg is specific (features/_common/login.feature) -> Run
                if arg == current_file:
                    should_run = True
                    break
                # If arg is the _common folder -> Run
                if "_common" in arg and arg in current_file:
                    should_run = True
                    break

        # EXECUTE SKIP
        if not should_run:
            scenario.skip(
                f"Skipping Library Scenario '{scenario.name}' (Implicit Bulk Run)"
            )
            return

    # --- STANDARD STARTUP ---
    context.driver = context.factory.create_driver()
    context.app = BaseStepContext(context.driver, context.beast_config)

    base_url = context.beast_config.get("base_url")
    if base_url:
        context.driver.get(base_url)

    # Run Magic Setup
    run_common_features(scenario, context, "setup", fail_hard=True)


def after_scenario(context, scenario):
    """
    Behave hook to run after each scenario.

    :param context: Default Behave context object
    :param scenario: The scenario that just finished executing
    """
    # 1. LOGIC: Only run Teardown if the test actually ran (wasn't skipped)
    if scenario.status != Status.skipped:
        run_common_features(scenario, context, "teardown", fail_hard=False)

    # 2. DEBUG: Screenshot on Failure
    if scenario.status == Status.failed and getattr(context, "driver", None):
        should_snap = context.beast_config.get("screenshot_on_failure", False)
        if str(should_snap).lower() == "true":
            output_dir = context.beast_config.get("output_directory", "output")
            try:
                x = datetime.datetime.now()
                name = f"fail_{x.strftime('%H-%M_%Y%m%d')}.png"
                ensure_dir(output_dir)
                context.driver.save_screenshot(f"./{output_dir}/{name}")
            except Exception:
                pass

    # 3. CLEANUP: Always quit the driver if it exists, regardless of status
    # We use getattr() to safely check if 'driver' exists to avoid AttributeErrors
    if getattr(context, "driver", None):
        try:
            context.driver.quit()
        except Exception:
            pass

    # 4. RESET: Always nullify the reference
    context.driver = None
    context.app = None


def after_all(context):
    """
    Behave hook to run after all tests.
    :param context: Default Behave context object
    """
    context.report_manager.finalise_reporting()
