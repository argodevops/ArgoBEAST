import os
import subprocess
from .helpers import ensure_dir, ok, warn, error
from .templates import DOCKERFILE_TEMPLATE, DOCKER_COMPOSE_TEMPLATE


def _update_driver_config():
    config_path = "config/driver.yml"
    remote_url = "http://selenium-grid:4444/wd/hub"

    if not os.path.exists(config_path):
        warn("No driver.yml found, skipping lab configuration.")
        ok(
            "if you are using a custom configuration, you can add the following to your driver.yml to connect to the lab Grid:\n"
        )
        ok(f'remote_url: "{remote_url}"\n')
        return False

    with open(config_path, "r") as f:
        content = f.readlines()

    # Check if we've already added the lab config
    if any("remote_url:" in line for line in content):
        if any(line.strip().startswith("#") and remote_url in line for line in content):
            ok(
                "The lab configuration is already present but commented out in driver.yml."
            )
            ok("Uncomment the remote_url line to connect to the lab Grid.")
        elif any(f'remote_url: "{remote_url}"' in line for line in content):
            ok("The lab configuration looks ok in driver.yml.")
            return True
        else:
            warn(
                "remote_url configuration already exists in driver.yml but it does not match the lab Grid URL.\n"
                "To use the lab, please update the remote_url in your driver.yml to point to {}. \n"
                "or remove the existing remote_url configuration to allow argobeast to add the correct one automatically.".format(
                    remote_url
                )
            )
        return False

    ok("Wiring up the driver.yml to the lab Grid...")

    # We append it to the end or modify the specific key
    # Adding it as a commented-out toggle is often the friendliest way
    with open(config_path, "a") as f:
        f.write("\n# Added by argobeast build lab\n")
        f.write(f'remote_url: "{remote_url}"\n')
    return True


def build_lab():

    if os.environ.get("IS_IN_LAB"):
        warn("You are already in the lab! No need to build it again.!")
        return

    ensure_dir("argobeast_lab")
    if os.path.exists("argobeast_lab/argobeast.dockerfile"):
        warn("The ArgoBEAST lab already exists")
    else:
        ok("Adding furniture and equipment...")
        with open("argobeast_lab/argobeast.dockerfile", "w", encoding="utf-8") as f:
            f.write(DOCKERFILE_TEMPLATE)
    if os.path.exists("argobeast_lab/argobeast.dockercompose.yml"):
        warn("The ArgoBEAST lab already exists")
    else:
        warn("Somebody dropped a test tube and it broke!")
        ok("replacing equipment...")
        with open(
            "argobeast_lab/argobeast.dockercompose.yml", "w", encoding="utf-8"
        ) as f:
            f.write(DOCKER_COMPOSE_TEMPLATE)
    ok("cleaning up the mess...")
    ok("The ArgoBEAST lab is ready to use! run `argobeast open lab` to get started")


def open_lab():

    if os.environ.get("IS_IN_LAB"):
        warn("You are already in the lab!")
        return
    if not os.path.exists("argobeast_lab/argobeast.dockerfile") or not os.path.exists(
        "argobeast_lab/argobeast.dockercompose.yml"
    ):
        warn(
            "The lab is either not built or there are missing files. "
            "Please run `argobeast build lab` first."
        )
        return

    if not _update_driver_config():
        return
    
    ok("Setting things up and opening the lab door...")
    cmd = [
        "docker",
        "compose",
        "-f",
        "argobeast_lab/argobeast.dockercompose.yml",
        "up",
        "-d",
    ]
    cmd_enter = ["docker", "exec", "-it", "argobeast-runner", "/bin/bash"]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        ok("The door to the lab swings open...")
        try:
            subprocess.run(cmd_enter, check=True)
        except subprocess.CalledProcessError as e:
            error("Error entering the lab: " + str(e.stderr))
            warn(
                "The door is open but something went wrong when you tried to enter. "
                "Please ensure the container is running and try again."
            )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.lower()

        if "permission denied" in error_msg:
            warn("[SYSTEM] Permission Denied: Cannot connect to the Docker daemon.")
            ok(
                "To fix this, please run the following commands and restart your terminal:"
            )
            print("\n  sudo usermod -aG docker $USER")
            print("  newgrp docker\n")
        else:
            error("Error details: " + str(e.stderr))
            warn(
                "The door is jammed shut, please ensure you have Docker installed and running and then try again."
            )
            warn(
                "If you would prefer to use a different container or VM solution, "
                "you can use the provided Dockerfile to build your own image and set up the lab environment manually."
            )
            return


def close_lab():
    if os.environ.get("IS_IN_LAB"):
        ok(
            "You must leave the lab before you can close it. "
            "Type `exit` to leave and then run this command again."
        )
        return
    cmd = [
        "docker",
        "compose",
        "-f",
        "argobeast_lab/argobeast.dockercompose.yml",
        "down",
    ]
    try:
        ok("Shutting down the lab and cleaning up...")
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        ok("The lab is now closed. See you next time!")
    except subprocess.CalledProcessError as e:
        error("Error closing the lab: " + str(e.stderr))
        warn(
            "Something went wrong while trying to close the lab. Please ensure Docker is running and try again."
        )
