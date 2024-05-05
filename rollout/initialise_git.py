from pathlib import Path

import commands
import requests
from halo import Halo


def get_gitignore(language: str) -> str:
    return requests.get(
        f"https://api.github.com/gitignore/templates/{language}",
        headers={
            "accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    ).json()["source"]


def get_all_licences() -> dict:
    return requests.get(
        f"https://api.github.com/licenses",
        headers={
            "accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    ).json()


def get_licence(licence: str) -> str:
    return requests.get(
        f"https://api.github.com/licenses/{licence}",
        headers={
            "accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    ).json()["body"]


def run(project_path: str, licence: str) -> tuple[False, str] | tuple[True, None]:
    project_path = Path(project_path)
    commands.git_init(project_path)

    with Halo("Creating gitignore...", spinner="dots").start() as spin:
        with open(project_path / ".gitignore", "w") as f:
            f.write(get_gitignore("Python"))
        spin.succeed(spin.text + " Done!")

    with Halo("Creating licence...", spinner="dots").start() as spin:
        with open(project_path / "LICENSE", "w") as f:
            f.write(get_licence(licence))
        spin.succeed(spin.text + " Done!")

    return True, None
