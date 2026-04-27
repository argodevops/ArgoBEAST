from pathlib import Path
import string

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
PURPLE = "\033[95m"
RESET = "\033[0m"
ARGO_BEAST = r"""
           ___                  _____ _____  ___   _____ _____
          / _ \                | ___ \  ___|/ _ \ /  ___|_   _|
         / /_\ \_ __ __ _  ___ | |_/ / |__ / /_\ \\ `--.  | |
         |  _  | '__/ _` |/ _ \| ___ \  __||  _  | `--. \ | |
         | | | | | | (_| | (_) | |_/ / |___| | | |/\__/ / | |
         \_| |_/_|  \__, |\___/\____/\____/\_| |_/\____/  \_/
                     __/ |
                    |___/
          """


def ensure_dir(directory):
    """
    Creates the directory and all intermediate parents if they don't exist.
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def ok(*args, **kwargs):
    prefix = f"{GREEN}[OK]{RESET}"
    if args:
        args = list(args)
        args[0] = f"{prefix} {args[0]}"
    else:
        args = [prefix]
    print(*args, **kwargs)


def warn(*args, **kwargs):
    prefix = f"{YELLOW}[WARN]{RESET}"
    if args:
        args = list(args)
        args[0] = f"{prefix} {args[0]}"
    else:
        args = [prefix]
    print(*args, **kwargs)


def info(*args, **kwargs):
    prefix = f"{PURPLE}[INFO]{RESET}"
    if args:
        args = list(args)
        args[0] = f"{prefix} {args[0]}"
    else:
        args = [prefix]
    print(*args, **kwargs)


def error(*args, **kwargs):
    prefix = f"{RED}[ERROR]{RESET}"
    if args:
        args = list(args)
        args[0] = f"{prefix} {args[0]}"
    else:
        args = [prefix]
    print(*args, **kwargs)


def get_class_name(name):
    capitals = [n.capitalize() for n in name.split(" ")]
    class_name = ""
    for c in capitals:
        class_name += c  # pylint: disable=consider-using-join

    return class_name
