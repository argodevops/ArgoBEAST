from .helpers import ensure_dir, ok, warn, error
from .templates import PAGE_TEMPLATE, STEPS_TEMPLATE, ACTIONS_TEMPLATE, FEATURE_TEMPLATE, CONFIG_TEMPLATE, REQUIREMENTS_TEMPLATE, ENVIRONMENT_TEMPLATE
import os
import sys
import subprocess

"""
CLI functions for creating test framework components
"""


def create(name, type):
    """
    Create a new component file
    :param name: Name of the component
    :param type: Type of the component (page, actions, steps, feature)
    """
    file_ext = "py"
    if type == "feature":
        file_ext = "feature"
    snake = name.lower().replace(" ", "_")
    Name = snake.capitalize()
    name = snake

    if type == "actions":
        directory = type
    elif type == "steps":
        directory = "features/steps"
    else:
        directory = f"{type}s"

    path = f"{directory}/{snake}_{type}.{file_ext}"

    if os.path.exists(path):
        warn(f"{type} '{snake}' already exists")
        return

    ensure_dir(f"{directory}")
    with open(f"{path}", "w") as f:
        if type == "page":
            f.write(PAGE_TEMPLATE.format(Name=Name, name=name))
        elif type == "actions":
            f.write(ACTIONS_TEMPLATE.format(Name=Name, name=name))
        elif type == "steps":
            f.write(STEPS_TEMPLATE.format(Name=Name, name=name))
        elif type == "feature":
            f.write(FEATURE_TEMPLATE.format(Name=Name, name=name))
        else:
            error(f"Unknown type {type}")
            return

    ok(f"created {type} {snake}")


def pip_install(requirements_path: str):
    """
    Install dependencies from a requirements file using pip
    :param requirements_path: Path to the requirements.txt file
    """
    subprocess.check_call([
        sys.executable,
        "-m", "pip",
        "install",
        "-r",
        requirements_path
    ])


def init():
    """
    Initialize a new test framework structure
    """
    directories = ["pages", "actions", "features", "features/steps", "config"]
    examples = ["page", "actions", "feature", "steps"]
    accepted_response = ["y", "yes", "n", "no"]

    user_input = False
    while not user_input:
        include_examples = input(
            "Would you like to include example files within the directories? [Y]es,[N]o: ")
        if include_examples.lower() in accepted_response:
            user_input = True
        else:
            warn("Please select a valid option")

    for d in directories:
        ensure_dir(d)

    with open("config/driver.yml", "w") as f:
        f.write(CONFIG_TEMPLATE)

    with open("features/environment.py", "w") as f:
        f.write(ENVIRONMENT_TEMPLATE)

    with open("requirements.txt", "w") as f:
        f.write(REQUIREMENTS_TEMPLATE)

    if include_examples in ["y", "yes"]:
        for e in examples:
            create("login", e)

    user_input = False
    while not user_input:
        install_deps = input(
            "Would you like to attempt to install the required dependencies? [Y]es,[N]o: ")
        if install_deps.lower() in accepted_response:
            user_input = True
        else:
            warn("Please select a valid option")

    if install_deps.lower() in ["y", "yes"]:
        pip_install("requirements.txt")
