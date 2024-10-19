# GIT REPORT

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)  

[![Repository](https://skillicons.dev/icons?i=python,git,linux,vscode)](https://skillicons.dev)

NOTE: This repo has switched to [conventional commits](https://www.conventionalcommits.org/en/v1.0.0). It requires `pre-commit` and `commitizen` to help with controlling this.  

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

* I leave WIP files and branches unpushed.  
* I have many unmerged PRs that could be merged more quickly.  

TODO:

* Write a python TUI tool that given a path will list directories that are git repos and show me useful stats as I highlight them.  
* Setup the repo correctly
  * conventional commits
  * license
  * codeowners
  * extensions
* Add a pipeline
* Make the tool installable through brew and apt.  
