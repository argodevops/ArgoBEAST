import sys
import io
from .create import create, create_all, init
from .helpers import warn, info, ARGO_BEAST
from .generate_feature_docs import generate_rst_documentation
from .build_lab import build_lab


def fix_windows_encoding():
    """
    Ensures python utf-8 encoding is added to the terminal output for a consistent experience across platforms,
    especially for Windows users.
    """
    if sys.platform == "win32":
        # Forces the standard output/input to use utf-8
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def _less_than_three_args(args):
    if args[0] == "init":
        print(ARGO_BEAST)
        init()
    elif args[0] == "help":
        print(
            "Usage: argobeast <command> <type> <name>\n\n"
            "Commands:\n"
            "  create - Create a new page, actions, feature, or steps file.\n"
            "  init   - Initialize a new ArgoBEAST project in the current directory.\n"
            "  hello  - Display a welcome message and introduction to ArgoBEAST.\n"
            "  generate-docs - Generate documentation for all features in the project.\n\n"
            "  build lab - Build the ArgoBEAST lab Docker image.\n\n"
            "Types (for create command):\n"
            "  page    - Create a new Page Object class.\n"
            "  actions - Create a new Actions class.\n"
            "  feature - Create a new feature file with scenarios.\n"
            "  steps   - Create a new steps definition file.\n"
            "  all     - Create all of the above with the given name."
        )
    elif args[0] == "hello":
        print(ARGO_BEAST)
        print(
            "                   ### Welcome to ArgoBEAST! ###"
            "\n___________________________________________________________________"
            "\nA Python-based test automation framework for web applications, "
            "\nbuilt on Behave, Selenium, and a clean Page Object Model. "
            "\nGet started by running 'argobeast init' to set up your first project."
        )
    elif args[0] == "generate-docs":
        generate_rst_documentation(args)
    else:
        info(
            "Usage: argobeast create <page|actions|feature> <Name> \n To initiate a new project try argobeast init"
        )


def main():
    """
    Main CLI entry point
    """
    fix_windows_encoding()

    args = sys.argv[1:]

    if len(args) < 1:
        info(
            "Usage: argobeast create <page|actions|feature> <Name> \n To initiate a new project try argobeast init"
        )
        return

    if args[0] == "build" and len(args) > 1 and args[1] == "lab":
        build_lab()
        return

    if len(args) < 3:
        _less_than_three_args(args)
        return

    if len(args) > 3:
        info(
            "Usage: argobeast create <page|actions|feature> <Name> \n To initiate a new project try argobeast init"
        )
        return

    command, type_, name = args[0], args[1], args[2]

    if command not in ["create", "init"]:
        warn(f"Unknown command {command}\n####Available Commands####\ncreate\ninit")
        return

    if type_ not in ["actions", "page", "feature", "steps", "all"]:
        warn(f"Unknown type {type}")
        info("Usage: argobeast create <page|actions|feature|steps> <Name>")
        return

    info(f"Creating {name}")
    if type_ == "all":
        create_all(name)
    else:
        create(name, type_)
