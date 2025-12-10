from behave import *
from behave.parser import parse_file
from behave.model_core import Status
from test_framework.base.driver_factory import WebDriverFactory
from test_framework.base.base_step_context import BaseStepContext
from test_framework.config.loader import ConfigLoader
from test_framework.cli.helpers import ensure_dir
from dotenv import load_dotenv
import os
import shutil
import datetime
import subprocess

USER_CONFIG_PATH = "config/driver.yml"
HOOKS_PATH = "features/_common"
load_dotenv()


class DummyStreamOpener:
    def __init__(self, path):
        self.name = path
        self.stream = None


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


def _parse_tags(file_path):
    """
    Reads a feature file and extracts scenarios tagged as hooks.
    Returns a dict: {'hook_name': 'step_content_string'}
    """
    hooks_found = {}

    # Behave's built-in parser does the heavy lifting
    feature = parse_file(file_path)

    for scenario in feature.scenarios:
        hook_id = None

        for tag in scenario.tags:
            # Skip triggers, look for the ID
            if tag.startswith('setup:') or tag.startswith('teardown:'):
                continue

            hook_id = tag
            break

        if hook_id:
            step_block = ""
            for step in scenario.steps:
                # 1. Add the main step line
                step_block += f"{step.keyword} {step.name}\n"

                # 2. Reconstruct Data Tables (Critical for your forms!)
                if step.table:
                    # Add headings
                    step_block += "  |" + "|".join(step.table.headings) + "|\n"
                    # Add rows
                    for row in step.table:
                        step_block += "  |" + "|".join(row.cells) + "|\n"

                # 3. Reconstruct Multiline Strings (""" ... """)
                if step.text:
                    step_block += f'  """\n{step.text}\n  """\n'

            hooks_found[hook_id] = step_block

    return hooks_found


def _parse_hooks():
    beast_hooks = {}

    if not os.path.exists(HOOKS_PATH):
        return {}

    for root, dirs, files in os.walk(HOOKS_PATH):
        for filename in files:
            if filename.endswith(".feature"):
                file_path = os.path.join(root, filename)

                # Get the hooks from this specific file
                hooks = _parse_tags(file_path)

                # Merge them into the main registry
                beast_hooks.update(hooks)

    return beast_hooks


def _run_common_features(scenario, context, stage, fail_hard=True):
    all_tags = list(scenario.feature.tags) + list(scenario.tags)
    for tag in all_tags:
        if tag.startswith(f"{stage}:"):
            hook_id = tag.split(':', 1)[1]

            if hasattr(context, 'beast_hooks') and hook_id in context.beast_hooks:
                try:
                    context.execute_steps(context.beast_hooks[hook_id])
                except Exception as e:
                    error_msg = f"ArgoBEAST {stage} Failed: Hook '@{hook_id}' encountered an error.\n{str(e)}"
                    if fail_hard:
                        assert False, error_msg
                    else:
                        print(f"WARNING: {error_msg}")
            else:
                print(
                    f"WARNING: Scenario requested @{stage}:{hook_id}, but it was not found in features/_common.")


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
                "You have requested Allure reporting but 'allure-behave is not installed. run `pip install allure-behave`")

        allure_dir = "allure-results"

        if os.path.exists(allure_dir):
            shutil.rmtree(allure_dir)
        ensure_dir(allure_dir)

        stream_opener = DummyStreamOpener(allure_dir)
        allure_formatter = AllureFormatter(stream_opener, context.config)
        context._runner.formatters.append(allure_formatter)

    context.beast_config = final_config
    context.factory = WebDriverFactory(context.beast_config)
    context.beast_hooks = _parse_hooks()


def before_scenario(context, scenario):
    current_file = scenario.feature.filename.replace('\\', '/')

    if HOOKS_PATH in current_file:
        user_targets = [p.replace('\\', '/') for p in context.config.paths]

        is_explicit_target = False
        for target in user_targets:
            if target == current_file or (target in current_file and "_common" in target):
                is_explicit_target = True
                break

        if not is_explicit_target:
            scenario.skip("Skipping Library Scenario during bulk run")
            return
    context.driver = context.factory.create_driver()
    context.app = BaseStepContext(context.driver, context.beast_config)
    # Run setup with fail_hard=True
    _run_common_features(scenario, context, "setup", fail_hard=True)


def after_scenario(context, scenario):
    # Run teardown with fail_hard=False (Log errors, don't overwrite test status)
    _run_common_features(scenario, context, "teardown", fail_hard=False)

    if scenario.status == Status.failed:
        if "screenshot_on_failure" in context.beast_config:
            # Handle config retrieval safely
            should_snap = context.beast_config.get("screenshot_on_failure")
            # Allow for string "true" or boolean True
            if str(should_snap).lower() == "true":
                output_dir = context.beast_config.get(
                    "output_directory", "output")
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

    try:
        context.driver.quit()
    except Exception:
        pass

    context.driver = None
    context.app = None


def after_all(context):
    # --- ALLURE REPORT GENERATION ---
    # Only run if reporting was enabled in the first place
    if context.beast_config.get("allure_reporting"):

        # Get directory paths
        allure_dir = context.beast_config.get("allure_dir", "allure-results")
        report_dir = "allure-report"

        # Check if the user wants this auto-generation (default to True if not specified)
        # You can add 'auto_generate_report: false' to config to disable this
        if context.beast_config.get("auto_generate_report", True):
            try:
                # 1. Run the generation command
                # 'allure generate <results> --clean -o <report>'
                subprocess.run(
                    ["allure", "generate", allure_dir,
                        "--clean", "-o", report_dir],
                    check=True,
                    stdout=subprocess.DEVNULL,  # Keep the console clean
                    stderr=subprocess.DEVNULL
                )

                print(f"\n✨ Allure HTML report generated in './{report_dir}'")

                # 2. (Optional) Create a ZIP archive for easy download
                shutil.make_archive("allure-report", 'zip', report_dir)
                print(f"📦 Report zipped to './allure-report.zip' (Easy download)")

            except FileNotFoundError:
                # This catches the case where 'allure' is not in the system PATH
                print(f"\nℹ️  'allure' CLI not found. Skipping HTML generation.")
                print(
                    f"""   (You can still view results by installing Allure and running 'allure serve sdsa'
                    alternatively, generate a local HTML report with 'allure generate allure-results --clean -o allure-report')""")

            except Exception as e:
                # Catches other errors (permissions, corrupted data, etc.)
                print(f"\n⚠️  Could not generate Allure report: {e}")
