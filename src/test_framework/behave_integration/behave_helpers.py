# test_framework/core/behave_helpers.py
import os
import json
from behave.parser import parse_file

# Constants needed by helpers
HOOKS_PATH = "features/_common"


class DummyStreamOpener:
    def __init__(self, path):
        self.name = path
        self.stream = None


def override_config_with_env_vars(config_data):
    """
    Checks for specific environment variables and overrides corresponding config values.
    """
    ENV_OVERRIDES = {
        "BASE_URL": "base_url",
        "REMOTE_URL": "remote_url",
        "LOG_LEVEL": "log_level",
    }

    # Only print if strictly necessary to avoid console noise
    # print("Checking environment variables for config overrides...")

    for env_var, config_key in ENV_OVERRIDES.items():
        env_value = os.getenv(env_var)
        if env_value:
            config_data[config_key] = env_value
            print(
                f"  --> OVERRIDE: {config_key} set to '{env_value}' via {env_var}")

    return config_data


def cleanup_results(context):
    """
    Cleans up the allure results directory based on internal rules and user config.
    """
    results_dir = "allure-results"
    user_wants_hide_skipped = context.beast_config.get(
        "hide_skipped_tests", False)

    if not os.path.exists(results_dir):
        return

    for filename in os.listdir(results_dir):
        if not filename.endswith("-result.json"):
            continue

        filepath = os.path.join(results_dir, filename)
        should_delete = False

        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            status = data.get("status")
            title_path = data.get("titlePath") or []
            full_name = data.get("fullName", "")

            # Combine checks: True if "_common" is in EITHER the titlePath OR the fullName
            is_magic_hook = "_common" in str(
                title_path) or "_common" in full_name

            if is_magic_hook and status == "skipped":
                should_delete = True
            elif user_wants_hide_skipped and status == "skipped":
                should_delete = True

        except Exception:
            continue

        if should_delete:
            try:
                os.remove(filepath)
            except OSError:
                pass


def parse_tags(file_path):
    hooks_found = {}
    feature = parse_file(file_path)

    for scenario in feature.scenarios:
        hook_id = None
        for tag in scenario.tags:
            if tag.startswith('setup:') or tag.startswith('teardown:'):
                continue
            hook_id = tag
            break

        if hook_id:
            step_block = ""
            for step in scenario.steps:
                step_block += f"{step.keyword} {step.name}\n"
                if step.table:
                    step_block += "  |" + "|".join(step.table.headings) + "|\n"
                    for row in step.table:
                        step_block += "  |" + "|".join(row.cells) + "|\n"
                if step.text:
                    step_block += f'  """\n{step.text}\n  """\n'
            hooks_found[hook_id] = step_block

    return hooks_found


def parse_hooks():
    beast_hooks = {}
    if not os.path.exists(HOOKS_PATH):
        return {}

    for root, dirs, files in os.walk(HOOKS_PATH):
        for filename in files:
            if filename.endswith(".feature"):
                file_path = os.path.join(root, filename)
                hooks = parse_tags(file_path)
                beast_hooks.update(hooks)

    return beast_hooks


def run_common_features(scenario, context, stage, fail_hard=True):
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
