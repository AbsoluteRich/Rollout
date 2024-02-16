from subprocess import run, CompletedProcess


def venv(venv_name: str, *args, **kwargs) -> CompletedProcess:
    return run(["python", "-m", "venv", venv_name], *args, **kwargs)


def pip_install(executable_path: str, package_name: str, *args, **kwargs) -> CompletedProcess:
    parameters = [executable_path, "install", package_name]
    return run(parameters, *args, **kwargs)


def pip_freeze(executable_path: str, *args, **kwargs) -> CompletedProcess:
    parameters = [executable_path, "freeze"]
    return run(parameters, *args, **kwargs)
