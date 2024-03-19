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

    new = subparsers.add_parser("new", help="Placeholder")
    new.add_argument(
        "project_name",
        help="Name of the project.",
    )
    new.add_argument(
        "--venv-name",
        help="What to name the virtual environment (.venv by default).\nIf called 'None', disables virtual environment creation.",
        default=".venv",
    )
    new.add_argument(
        "--dependencies",
        "-d",
        help="Packages to install in the virtual environment (if any).",
        nargs="+",
    )
    new.set_defaults(func=handle_new)

    start = subparsers.add_parser("start", help="Placeholder 2")
    start.add_argument(
        "editor", help="The text editor to open the project in. Supported:"
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
    else:
        error_message = result[1]
        if args.dependencies:
            error_message += (
                "\nReading 'pip-log.txt' might help you solve your problem."
            )
        cli.error(error_message)


def handle_start(args: argparse.Namespace, cli: argparse.ArgumentParser) -> None:
    start_project.run(args)


if __name__ == "__main__":
    cli = setup_cli()
    args = cli.parse_args()

    if hasattr(args, "func"):
        args.func(args, cli)
    else:
        cli.print_help()
