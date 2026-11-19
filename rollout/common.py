import os
from pathlib import Path


def check_project(path: Path) -> Path | None:
    path = path / "src" / "main.py"
    if path.exists():
        return path
    else:
        return None
