from os import PathLike
from pathlib import Path


def check_project(path: str) -> tuple[True, Path] | tuple[False, None]:
    path = Path(path)
    if (path / "src" / "main.py").exists():
        return True, path / "src" / "main.py"
    else:
        return False, None


pathlike = Path | str | PathLike
