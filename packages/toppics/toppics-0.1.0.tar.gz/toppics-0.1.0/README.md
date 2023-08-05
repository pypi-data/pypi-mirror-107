# toppics

[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python CLI for adding pre-defined topics to a GitHub repository.

## Development

- `poetry install`
- `poetry shell`

## Tech Stack

- [Click](https://click.palletsprojects.com/) (for the interface)

### Packaging and Development

- [Poetry](https://python-poetry.org/)
- [Mypy](http://mypy-lang.org/)
- [isort](https://pycqa.github.io/isort/)
- [Black](https://github.com/psf/black)
- [Flake8](https://flake8.pycqa.org/)
  - [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)
  - [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)
  - [pep8-naming](https://github.com/PyCQA/pep8-naming)
  - [flake8-builtins](https://github.com/gforcada/flake8-builtins)
- [Bandit](https://bandit.readthedocs.io/)

This CLI was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`joaopalmeiro/cookiecutter-templates/python-cli`](https://github.com/joaopalmeiro/cookiecutter-templates) project template.

## Notes

- [Replace all repository topics](https://docs.github.com/en/rest/reference/repos#replace-all-repository-topics).
- [ghapi](https://ghapi.fast.ai/) documentation:
  - `repos.replace_all_topics(owner, repo, names)`.
- [regex101](https://regex101.com/) website.
- [Click 7](https://click.palletsprojects.com/en/7.x/) documentation:
  - [Utils](https://click.palletsprojects.com/en/7.x/utils/).
- [Click 8](https://click.palletsprojects.com/en/8.0.x/) documentation.
- `toppics https://github.com/joaopalmeiro/toppics "Python CLI"`.
