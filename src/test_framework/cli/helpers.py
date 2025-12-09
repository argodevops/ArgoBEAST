import os

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
PURPLE = "\033[95m"
RESET = "\033[0m"
ARGO_BEAST = """
           ___                  _____ _____  ___   _____ _____
          / _ \                | ___ \  ___|/ _ \ /  ___|_   _|
         / /_\ \_ __ __ _  ___ | |_/ / |__ / /_\ \\ `--.  | |
         |  _  | '__/ _` |/ _ \| ___ \  __||  _  | `--. \ | |
         | | | | | | (_| | (_) | |_/ / |___| | | |/\__/ / | |
         \_| |_/_|  \__, |\___/\____/\____/\_| |_/\____/  \_/
                     __/ |
                    |___/
          """


def ensure_dir(dir):
    if os.path.exists(dir):
        return
    create_dirs = dir.split("/")
    for i in range(len(create_dirs)):
        os.mkdir(f"{create_dirs[0]}/{create_dirs[i] if i > 0 else ''}")
    return


def ok(log: str):
    string = f"{GREEN}[OK]{RESET} {log}"
    print(string)
    return


def warn(log: str):
    string = f"{YELLOW}[WARN]{RESET} {log}"
    print(string)
    return


def info(log: str):
    string = f"{PURPLE}[INFO]{RESET} {log}"
    print(string)
    return


def error(log: str):
    string = f"{RED}[ERROR]{RESET} {log}"
    print(string)
    return


def get_class_name(name):
    capitals = [n.capitalize() for n in name.split(" ")]
    class_name = ""
    for c in capitals:
        class_name += c

    return class_name
