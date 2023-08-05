# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toppics']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'ghapi>=0.1.16,<0.2.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['toppics = toppics.cli:main']}

setup_kwargs = {
    'name': 'toppics',
    'version': '0.1.0',
    'description': 'A Python CLI for adding pre-defined topics to a GitHub repository.',
    'long_description': '# toppics\n\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA Python CLI for adding pre-defined topics to a GitHub repository.\n\n## Development\n\n- `poetry install`\n- `poetry shell`\n\n## Tech Stack\n\n- [Click](https://click.palletsprojects.com/) (for the interface)\n\n### Packaging and Development\n\n- [Poetry](https://python-poetry.org/)\n- [Mypy](http://mypy-lang.org/)\n- [isort](https://pycqa.github.io/isort/)\n- [Black](https://github.com/psf/black)\n- [Flake8](https://flake8.pycqa.org/)\n  - [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)\n  - [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)\n  - [pep8-naming](https://github.com/PyCQA/pep8-naming)\n  - [flake8-builtins](https://github.com/gforcada/flake8-builtins)\n- [Bandit](https://bandit.readthedocs.io/)\n\nThis CLI was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`joaopalmeiro/cookiecutter-templates/python-cli`](https://github.com/joaopalmeiro/cookiecutter-templates) project template.\n\n## Notes\n\n- [Replace all repository topics](https://docs.github.com/en/rest/reference/repos#replace-all-repository-topics).\n- [ghapi](https://ghapi.fast.ai/) documentation:\n  - `repos.replace_all_topics(owner, repo, names)`.\n- [regex101](https://regex101.com/) website.\n- [Click 7](https://click.palletsprojects.com/en/7.x/) documentation:\n  - [Utils](https://click.palletsprojects.com/en/7.x/utils/).\n- [Click 8](https://click.palletsprojects.com/en/8.0.x/) documentation.\n- `toppics https://github.com/joaopalmeiro/toppics "Python CLI"`.\n',
    'author': 'João Palmeiro',
    'author_email': 'joaommpalmeiro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joaopalmeiro/toppics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
