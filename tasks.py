from invoke import task

commands = ["pipenv update", "pipenv requirements > requirements.txt", "pipenv requirements --dev > requirements-dev.txt", "python -m black rollout", "python -m isort rollout --profile black"]

@task
def pc(c):
    for command in commands:
        c.run(command)