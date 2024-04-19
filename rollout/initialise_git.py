import commands
import requests


def get_gitignore(language: str = "Python") -> str:
    return requests.get(
        f"https://api.github.com/gitignore/templates/{language}",
        headers={
            "accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    ).json()["source"]


def run() -> tuple[False, str] | tuple[True, None]:
    commands.git_init()
    with open(".gitignore", "w") as f:
        f.write(get_gitignore())
