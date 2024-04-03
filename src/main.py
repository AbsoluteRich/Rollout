import argparse
import new_project
import start_project


def setup_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rollout",
        description="Your one-stop solution to bootstrap Python projects, including essentials like Git and a virtual "
        "environment.",
    )
    subparsers = parser.add_subparsers()

    new = subparsers.add_parser(
        "new", help="Create a new Python project with virtual environment."
    )
    new.add_argument(
        "project_name",
        help="Name of the project.",
    )
    new.add_argument(
        "--venv-name",
        help="What to name the virtual environment (.venv by default).\nIf 'None', disables environment creation.",
        default=".venv",
    )
    new.add_argument(
        "--dependencies",
        "-d",
        help="Packages to install in the virtual environment (if any).",
        nargs="+",
    )
    new.set_defaults(func=handle_new)

    start = subparsers.add_parser(
        "start", help="Open a project in your editor of choice."
    )
    start.add_argument("project_path", help="Path to the project.")
    start.add_argument(
        "editor",
        help="The editor to open the project in. Supported: VS Code, PyCharm, IDLE, Notepad, and Notepad++.",
    )
    start.set_defaults(func=handle_start)

    return parser


def handle_new(args: argparse.Namespace, cli: argparse.ArgumentParser) -> None:
    venv_name = None if args.venv_name == "None" else args.venv_name
    if not args.venv_name and args.dependencies:
        print(
            "Packages will be ignored, as there is no virtual environment to install them to."
        )
    result = new_project.run(
        args.project_name, packages=args.dependencies, venv_name=venv_name
    )

    if result[0]:
        print(f"Your new project can be found at {result[1]}")
        if args.dependencies:
            print(
                "If you don't need to see the output for the commands, you can delete 'pip-log.txt'."
            )
        print(f"Maybe you'd like to open {args.project_name} using 'rollout start'?")
    else:
        error_message = result[1]
        if args.dependencies:
            error_message += (
                "\nReading 'pip-log.txt' might help you solve your problem."
            )
        cli.error(error_message)


def handle_start(args: argparse.Namespace, cli: argparse.ArgumentParser) -> None:
    valid_path, _ = start_project.check_project(args.project_path)
    if valid_path:
        start_project.run(args)
    else:
        cli.error("Couldn't find code files!")


if __name__ == "__main__":
    current_cli = setup_cli()
    current_args = current_cli.parse_args()

    if hasattr(current_args, "func"):
        current_args.func(current_args, current_cli)
    else:
        current_cli.print_help()
