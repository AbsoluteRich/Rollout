from pathlib import Path

from jinja2 import Environment

# This can't be a separate file, because where would that be stored?
TEMPLATE = """# Welcome to your new Python project!
{% if dependencies is defined %}{% for dependency in dependencies %}import {{ dependency }}
{% endfor %}{% endif %}
if __name__ == "__main__":
    pass

"""


def create_project_folders(project_name: str) -> bool:
    project_path = Path(project_name)
    if project_path.exists():
        return False

    project_path.mkdir()
    (project_path / "src").mkdir()
    return True


def create_entrypoint(project_name: str, packages: list) -> None:
    jinja = Environment()
    template = jinja.from_string(TEMPLATE)
    if packages:
        template = template.render(dependencies=packages)
    else:
        template = template.render()

    with open(Path(project_name) / "src" / "main.py", "w") as f:
        f.write(template)
