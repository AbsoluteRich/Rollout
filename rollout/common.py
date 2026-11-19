import os
from pathlib import Path


def check_project(path: str) -> Path | None:
    path = Path(path)
    if (path / "src" / "main.py").exists():
        return path / "src" / "main.py"
    else:
        return None


pathlike = Path | str | os.PathLike
