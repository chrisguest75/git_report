# GIT REPORT

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

[![Repository](https://skillicons.dev/icons?i=python,git,linux,vscode)](https://skillicons.dev)

NOTE: This repo has switched to [conventional commits](https://www.conventionalcommits.org/en/v1.0.0). It requires `pre-commit` and `commitizen` to help with controlling this.

## Contents

- [GIT REPORT](#git-report)
  - [Contents](#contents)
  - [Conventional Commits](#conventional-commits)
  - [Overview](#overview)
  - [Prepare](#prepare)
  - [Start](#start)
  - [Docker](#docker)
  - [Debugging and Troubleshooting](#debugging-and-troubleshooting)
    - [Interpreter](#interpreter)
    - [Pipenv Environment](#pipenv-environment)
    - [Single step](#single-step)
      - [Application](#application)
      - [Tests](#tests)

## Conventional Commits

```sh
# install pre-commmit (prerequisite for commitizen)
brew install pre-commit
brew install commitizen
# conventional commits extension
code --install-extension vivaxy.vscode-conventional-commits

# install hooks
pre-commit install --hook-type commit-msg --hook-type pre-push
```

## Overview

Create a tool that helps me get an overview of lots of repos quickly.

Reasons:

- I leave WIP files and branches unpushed.
- I have many unmerged PRs that could be merged more quickly.

TODO:

- Setup the repo correctly
  - license
  - codeowners
- Add a pipeline
- Make the tool installable through brew and apt.

## Prepare

If using `vscode` remember to set your interpreter location to `.venv/bin/python`

## Start

```sh
# in vscode terminal
export PIPENV_IGNORE_VIRTUALENVS=1

# my preference
export PIPENV_VENV_IN_PROJECT=1
# install
pipenv install --dev

# lint and test code
pipenv run format
pipenv run lint
pipenv run test

# enter venv
pipenv shell

# create .env file
cp .env.template .env

# run with arguments
pipenv run start --path ./
pipenv run start:test
```

## Docker

```sh
pipenv run docker:build
pipenv run docker:start
# override path
pipenv run docker:start ./start.sh --path ./

# troubleshooting
docker run -it --entrypoint /bin/bash git_report
```

## Debugging and Troubleshooting

### Interpreter

Set the interpreter path to `./.venv/bin/python3.11`

### Pipenv Environment

```sh
# enter python
pipenv run python

> import main

> main.test.__doc__
```

### Single step

#### Application

- Copy the `launch.json` to the root `.vscode`
- `. ./.env` in the terminal

#### Tests

- Configure pytest using the beaker icon in `vscode`
- You can run and debug the discovered tests
