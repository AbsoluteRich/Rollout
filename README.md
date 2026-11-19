# Rollout

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![wakatime](https://wakatime.com/badge/user/018daccf-84a6-42a4-b6f7-339559cb10c8/project/018dc050-e1e3-42b5-ad16-de47afc6cad6.svg)](https://wakatime.com/badge/user/018daccf-84a6-42a4-b6f7-339559cb10c8/project/018dc050-e1e3-42b5-ad16-de47afc6cad6)

> Rollout is your one-stop solution to bootstrap Python projects, including essentials like Git and a virtual environment.

## Background

Rollout was made to learn more about CLIs and how to make them using Python. If you...

* ...want a **simple project maker** without any fancy bells or whistles, this is the place.
* ...want **customisable project templates** and a rich ecosystem of them, use [Cookiecutter](https://www.cookiecutter.io/) or [Copier](https://github.com/copier-org/copier).
* ...have **Node.js installed** or want an alternative to Cookiecutter, you can use [generator-python](https://github.com/thejohnfreeman/generator-python), a project generator built with [Yeoman](https://yeoman.io/).
* ...have Git installed and **use high-level Python tools** like [tox](https://tox.wiki/en/4.15.0/), use [skeleton](https://blog.jaraco.com/skeleton/).

This also supports initialising projects with dependency managers other than PIP. Currently, only support for [pipenv](https://pipenv.pypa.io/en/latest/) is implemented, but [Poetry](https://python-poetry.org/) and [PDM](https://pdm-project.org/en/latest/) is planned.

## Install

> [!CAUTION]
> This is still a work in progress. Use at your own risk!

Ensure that you have [Python](https://www.python.org/downloads/) 3.10 or above.

pipenv is the recommended way to work with this. `requirements.txt` files will no longer be distributed.

### From source

```shell
git clone https://github.com/AbsoluteRich/Rollout.git
pipenv install
```

### pipx

When this actually releases:

```shell
pip install pipx  # If you don't already have it
pipx install rollout
```

## Usage

```shell
rollout my-new-project -d numpy pandas matplotlib
# Or, if you installed the program from source...
pipenv run python rollout my-new-project -d numpy pandas matplotlib 
```

## Contributing

```shell
git clone https://github.com/AbsoluteRich/Rollout.git
pipenv install -d
```

## Licence

This project is licenced under [GPL-3.0](https://github.com/AbsoluteRich/rollout/tree/main/LICENSE).
