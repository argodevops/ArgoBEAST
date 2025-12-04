import sys
from .create import create, init, build_docs
from .helpers import warn, info, ARGO_BEAST


def main():
    """
    Main CLI entry point
    """
    args = sys.argv[1:]

    if len(args) < 1:
        info(f"Usage: argotest create <page|actions|feature> <Name> \n To initiate a new project try argotest init")
        return
    if len(args) < 3:
        if args[0] == "init":
            print(ARGO_BEAST)
            init()
            return
        elif args[0] == "hello":
            print(ARGO_BEAST)
            print("                   ### Welcome to ArgoBEAST! ###"
                  "\n___________________________________________________________________"
                  "\nA Python-based test automation framework for web applications, "
                  "\nbuilt on Behave, Selenium, and a clean Page Object Model. "
                  "\nGet started by running 'argotest init' to set up your first project.")
            return
        elif args[0] == "docs":
            build_docs()
            return

        else:
            info(f"Usage: argotest create <page|actions|feature> <Name> \n To initiate a new project try argotest init")
            return

    command, type_, name = args[0], args[1], args[2]

    if command not in ["create", "init"]:
        warn(
            f"Unknown command {command}\n####Available Commands####\ncreate\ninit")
        return

    if type_ not in ["actions", "page", "feature", "steps"]:
        warn(f"Unknown type {type}")
        info("Usage: argotest create <page|actions|feature|steps> <Name>")
        return

    info(f"Creating {name}")
    create(name, type_)
