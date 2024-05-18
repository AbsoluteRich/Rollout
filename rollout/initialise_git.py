import requests


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
