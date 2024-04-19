from argparse import Namespace
from os.path import split
from pathlib import Path

import commands


def check_project(path: Path) -> tuple[True, Path] | tuple[False, None]:
    if (path / "src" / "main.py").exists():
        return True, path / "src" / "main.py"
    else:
        return False, None


def run(args: Namespace) -> None:
    # Valid paths are checked in the CLI handler, so assume check_directory returns something
    _, file_path = check_project(args.project_path)
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
    print(check_project(Path.cwd()))
