import os

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
PURPLE = "\033[95m"
RESET = "\033[0m"


def ensure_dir(dir):
    if os.path.exists(dir):
        return
    os.mkdir(dir)
    return

def ok(log:str):
    string = f"{GREEN}[OK]{RESET} {log}"
    print(string)
    return

def warn(log:str):
    string = f"{YELLOW}[WARN]{RESET} {log}"
    print(string)
    return

def info(log:str):
    string = f"{PURPLE}[INFO]{RESET} {log}"
    print(string)
    return

def error(log:str):
    string = f"{RED}[ERROR]{RESET} {log}"
    print(string)
    return