import commands
from pathlib import Path
from argparse import Namespace
from os.path import split


def check_directory() -> tuple[True, Path] | tuple[False, None]:
    cwd = Path.cwd()
    if (cwd / "src" / "main.py").exists():
        return True, cwd / "src" / "main.py"
    # elif (cwd / "main.py").exists():  The command should only be runnable in the root of a project
    #    return True, cwd / "main.py"
    else:
        return False, None


def run(args: Namespace) -> None:
    # Valid paths are checked in the CLI handler, so assume check_directory returns something
    _, file_path = check_directory()
    project_path = split(file_path)[0]

    match args.editor:
        case "vsc":
            # Todo
            commands.vsc(project_path)

        case "pycharm":
            # Todo
            commands.pycharm(project_path)

        case "idle":
            commands.idle(file_path)

        case "notepad":
            commands.notepad(file_path)

        case "notepad++":
            # Todo
            commands.notepadplusplus(file_path)


if __name__ == "__main__":
    print(check_directory())
