# environment.py
import os
import shutil
import datetime
import subprocess
from behave.model_core import Status
from dotenv import load_dotenv

# Internal Imports
from test_framework.base.driver_factory import WebDriverFactory
from test_framework.base.base_step_context import BaseStepContext
from test_framework.config.loader import ConfigLoader
from test_framework.cli.helpers import ensure_dir

# New Helper Imports
from test_framework.behave_integration.behave_helpers import (
    cleanup_results,
    parse_hooks,
    run_common_features,
    override_config_with_env_vars,
    DummyStreamOpener,
    HOOKS_PATH
)

USER_CONFIG_PATH = "config/driver.yml"
load_dotenv()


def before_all(context):
    loader = ConfigLoader()
    user_config = os.getenv("TEST_CONFIG") or USER_CONFIG_PATH
    config_data = loader.load(user_config)
    final_config = override_config_with_env_vars(config_data)

    if final_config.get("allure_reporting"):
        try:
            from allure_behave.formatter import AllureFormatter
        except ImportError:
            raise ImportError(
                "Allure reporting requested but 'allure-behave' is not installed.")

        allure_dir = "allure-results"
        if os.path.exists(allure_dir):
            shutil.rmtree(allure_dir)
        ensure_dir(allure_dir)

        hide_excluded = final_config.get("hide_excluded_tests", False)
        context.config.userdata['AllureFormatter.hide_excluded'] = str(
            hide_excluded).lower()

        allure_formatter = AllureFormatter(
            DummyStreamOpener(allure_dir), context.config)
        context._runner.formatters.append(allure_formatter)

    context.beast_config = final_config
    context.factory = WebDriverFactory(context.beast_config)
    context.beast_hooks = parse_hooks()


def before_scenario(context, scenario):
    # 1. Normalize path
    current_file = scenario.feature.filename.replace('\\', '/')

    # 2. Check if this is a Magic Hook (lives in _common)
    # We check if "_common" is a distinct part of the path to avoid partial matches
    if "/_common/" in current_file or "_common/" in current_file:

        should_run = False

        # CHECK A: Did the user ask for specific TAGS? (e.g. behave -t @login)
        if context.config.tags:
            should_run = True

        # CHECK B: Did the user explicitly point to this file/folder?
        else:
            user_args = [p.replace('\\', '/') for p in context.config.paths]
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
                f"Skipping Library Scenario '{scenario.name}' (Implicit Bulk Run)")
            return

    # --- STANDARD STARTUP ---
    context.driver = context.factory.create_driver()
    context.app = BaseStepContext(context.driver, context.beast_config)

    # Run Magic Setup
    run_common_features(scenario, context, "setup", fail_hard=True)


def after_scenario(context, scenario):
    # 1. LOGIC: Only run Teardown if the test actually ran (wasn't skipped)
    if scenario.status != Status.skipped:
        run_common_features(scenario, context, "teardown", fail_hard=False)

    # 2. DEBUG: Screenshot on Failure
    if scenario.status == Status.failed and getattr(context, 'driver', None):
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
    if getattr(context, 'driver', None):
        try:
            context.driver.quit()
        except Exception:
            pass

    # 4. RESET: Always nullify the reference
    context.driver = None
    context.app = None


def after_all(context):
    if context.beast_config.get("allure_reporting"):
        cleanup_results(context)

        if context.beast_config.get("auto_generate_report", True):
            allure_dir = "allure-results"
            report_dir = "allure-report"
            try:
                subprocess.run(
                    ["allure", "generate", allure_dir,
                        "--clean", "-o", report_dir],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                print(f"\n✨ Allure HTML report generated in './{report_dir}'")
                shutil.make_archive("allure-report", 'zip', report_dir)
                print(f"📦 Report zipped to './allure-report.zip'")

            except FileNotFoundError:
                # This explicitly catches "allure command not found"
                print(
                    f"\n🚫 Report Generation Skipped: 'allure' CLI is not installed or not in PATH.")
                print(f"   Action: Install Allure or add it to your system PATH.")
                print(
                    f"   Note: Raw JSON results are safely saved in './{allure_dir}'")

            except Exception as e:
                # This catches other issues (permissions, disk space, corrupt data)
                print(
                    f"\n⚠️  Report generation failed due to an unexpected error: {e}")
