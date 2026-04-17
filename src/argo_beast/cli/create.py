import os
import sys
import subprocess
from .helpers import ensure_dir, ok, warn, error, get_class_name
from .templates import (
    PAGE_TEMPLATE,
    STEPS_TEMPLATE,
    ACTIONS_TEMPLATE,
    FEATURE_TEMPLATE,
    CONFIG_TEMPLATE,
    REQUIREMENTS_TEMPLATE,
    ENVIRONMENT_TEMPLATE,
    COMMON_FEATURE_EXAMPLE,
)


def create_common_features():
    directory = "features/_common"
    with open(f"{directory}/login.feature", "w", encoding="utf-8") as f:
        f.write(COMMON_FEATURE_EXAMPLE)


def create(name, component_type):
    """
    Create a new component file
    :param name: Name of the component
    :param type: Type of the component (page, actions, steps, feature)
    """
    file_ext = "py"
    if component_type == "feature":
        file_ext = "feature"
    snake = name.lower().replace(" ", "_")
    class_name = get_class_name(name)
    capital_name = snake.capitalize()
    snake_name = snake

    if component_type == "actions":
        directory = component_type
    elif component_type == "steps":
        directory = "features/steps"
    else:
        directory = f"{component_type}s"

    path = f"{directory}/{snake}_{component_type}.{file_ext}"

    if os.path.exists(path):
        warn(f"{component_type} '{snake}' already exists")
        return

    ensure_dir(directory)
    with open(f"{path}", "w", encoding="utf-8") as f:
        if component_type == "page":
            f.write(
                PAGE_TEMPLATE.format(
                    Name=capital_name, name=snake_name, ClassName=class_name
                )
            )
        elif component_type == "actions":
            f.write(
                ACTIONS_TEMPLATE.format(
                    Name=capital_name, name=snake_name, ClassName=class_name
                )
            )
        elif component_type == "steps":
            f.write(
                STEPS_TEMPLATE.format(
                    Name=capital_name, name=snake_name, ClassName=class_name
                )
            )
        elif component_type == "feature":
            f.write(
                FEATURE_TEMPLATE.format(
                    Name=capital_name, name=snake_name, ClassName=class_name
                )
            )
        else:
            error(f"Unknown type {component_type}")
            return

    ok(f"created {component_type} {snake}")


def create_all(name):
    all_requirements = ["page", "actions", "steps"]

    for i in all_requirements:
        create(name, i)


def pip_install(requirements_path: str):
    """
    Install dependencies from a requirements file using pip
    :param requirements_path: Path to the requirements.txt file
    """
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", requirements_path]
    )


def init():
    """
    Initialize a new test framework structure
    """
    directories = [
        "pages",
        "actions",
        "features",
        "features/steps",
        "config",
        "features/_common",
    ]
    examples = ["page", "actions", "feature", "steps"]
    accepted_response = ["y", "yes", "n", "no"]

    user_input = False
    while not user_input:
        include_examples = input(
            "Would you like to include example files within the directories? [Y]es,[N]o: "
        )
        if include_examples.lower() in accepted_response:
            user_input = True
        else:
            warn("Please select a valid option")

    for d in directories:
        ensure_dir(d)

    with open("config/driver.yml", "w", encoding="utf-8") as f:
        f.write(CONFIG_TEMPLATE)

    with open("features/environment.py", "w", encoding="utf-8") as f:
        f.write(ENVIRONMENT_TEMPLATE)

    with open("features/_common/.gitkeep", "w", encoding="utf-8") as f:
        f.write("# Keep this folder")

    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(REQUIREMENTS_TEMPLATE)

    if include_examples in ["y", "yes"]:
        create_common_features()
        for e in examples:
            create("login", e)

    user_input = False
    while not user_input:
        install_deps = input(
            "Would you like to attempt to install the required dependencies? [Y]es,[N]o: "
        )
        if install_deps.lower() in accepted_response:
            user_input = True
        else:
            warn("Please select a valid option")

    if install_deps.lower() in ["y", "yes"]:
        pip_install("requirements.txt")
