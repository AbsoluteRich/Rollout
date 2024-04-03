from subprocess import run, CompletedProcess
from sys import executable as python_exe
from pathlib import Path
from custom_types import pathlike


def venv(venv_name: pathlike, *args, **kwargs) -> CompletedProcess:
    return run([python_exe, "-m", "venv", venv_name], *args, **kwargs)


def pip_install(
    executable_path: pathlike, package_name: str, *args, **kwargs
) -> CompletedProcess:
    parameters = [executable_path, "install", package_name]
    return run(parameters, *args, **kwargs)


def pip_freeze(executable_path: pathlike, *args, **kwargs) -> CompletedProcess:
    parameters = [executable_path, "freeze"]
    return run(parameters, *args, **kwargs)


def vsc(project_path: pathlike) -> CompletedProcess:
    return run(["code", project_path])


def pycharm(project_path: pathlike) -> CompletedProcess:
    return run(["pycharm", project_path])


def idle(file_path: Path) -> CompletedProcess:
    return run([python_exe, "-m" "idlelib", file_path])


def notepad(file_path: Path) -> CompletedProcess:
    return run(["notepad", file_path])


def notepadplusplus(file_path: Path) -> CompletedProcess:
    return run(["start", "notepad++", file_path])
