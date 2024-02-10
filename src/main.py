import argparse
import os
import subprocess


def create_venv(venv_name="venv") -> None:
    subprocess.run(["python", "-m", "venv", venv_name])


def create_project(project_name, venv_name=None) -> tuple[bool, str]:
    print("Creating project folders...", end="")
    if os.path.exists(project_name):
        return False, "Folder already exists. Try renaming or deleting it."
    os.makedirs(f"{project_name}/src")
    print(" done.")

    print("Setting up project...", end="")
    with open("template.py") as template:
        with open(f"{project_name}/src/main.py", "w") as f:
            f.write(template.read())
    print(" done.")

    print("Setting up virtual environment...", end="")
    os.chdir(project_name)
    if venv_name:
        create_venv(venv_name)
    else:
        create_venv()
    os.chdir(os.path.split(os.getcwd())[0])
    print(" done.")

    return True, os.getcwd()


cli = argparse.ArgumentParser(
    prog="rollout",
    description="Your one-stop solution to bootstrap Python projects, including essentials like Git and a virtual "
                "environment."
)

cli.add_argument(
    "project_name", help="Name of the project"
)

if __name__ == "__main__":
    args = cli.parse_args()
    result = create_project(args.project_name)
    if not result[0]:
        raise Exception(result[1])
    else:
        print(f"Your new project can be found at {result[1]}")
