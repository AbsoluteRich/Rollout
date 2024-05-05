from invoke import task

heavy_commands = ["pipenv update", "pipenv requirements > requirements.txt", "pipenv requirements --dev > requirements-dev.txt"]
commands = ["python -m black rollout", "python -m isort rollout --profile black"]

@task
def pc(c, lite=False):
    if not lite:
        for command in heavy_commands:
            c.run(command)
    
    for command in commands:
        c.run(command)