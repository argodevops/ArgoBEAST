from pathlib import Path

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


def _beast_print(prefix, color, *args, **kwargs):
    prefix_str = f"{color}[{prefix}]{RESET}"
    if args:
        args = list(args)
        args[0] = f"{prefix_str} {args[0]}"
    else:
        args = [prefix_str]
    print(*args, **kwargs)

def error(*args, **kwargs):
    _beast_print("ERROR", RED, *args, **kwargs)

def ok(*args, **kwargs):
    _beast_print("OK", GREEN, *args, **kwargs)

def warn(*args, **kwargs):
    _beast_print("WARN", YELLOW, *args, **kwargs)

def info(*args, **kwargs):
    _beast_print("INFO", PURPLE, *args, **kwargs)


def get_class_name(name):
    capitals = [n.capitalize() for n in name.split(" ")]
    class_name = ""
    for c in capitals:
        class_name += c  # pylint: disable=consider-using-join

    return class_name
