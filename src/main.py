import argparse
import new_project


def setup_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rollout",
        description="Your one-stop solution to bootstrap Python projects, including essentials like Git and a virtual "
        "environment.",
    )

    parser.add_argument(
        "project_name",
        help="Name of the project.",
    )
    parser.add_argument(
        "--venv-name",
        help="What to name the virtual environment (.venv by default).\nIf called 'None', disables virtual environment creation.",
        default=".venv",
    )
    parser.add_argument(
        "--dependencies",
        "-d",
        help="Packages to install in the virtual environment (if any).",
        nargs="+",
    )

    return parser


if __name__ == "__main__":
    cli = setup_cli()
    args = cli.parse_args()

    if args.venv_name == "None":
        if args.dependencies:
            print(
                "Packages will be ignored, as there is no virtual environment to install them to."
            )
        result = new_project.main(args.project_name, packages=args.dependencies, venv_name=None)
    else:
        result = new_project.main(
            args.project_name, packages=args.dependencies, venv_name=args.venv_name
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
