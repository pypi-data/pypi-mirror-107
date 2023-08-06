# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spiel', 'spiel.demo']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'ipykernel>=5.5.3,<6.0.0',
 'ipython>=7.23.0,<8.0.0',
 'nbterm>=0.0.7,<0.0.11',
 'numpy>=1.20.3,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'rich>=10.2.2,<11.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.3.2,<0.4.0',
 'uniplot>=0.4.4,<0.5.0',
 'watchdog>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['spiel = spiel.main:app']}

setup_kwargs = {
    'name': 'spiel',
    'version': '0.2.1',
    'description': 'A framework for building and presenting richly-styled presentations in your terminal using Python.',
    'long_description': "# Spiel\n\n[![PyPI](https://img.shields.io/pypi/v/spiel)](https://pypi.org/project/spiel/)\n[![Documentation Status](https://readthedocs.org/projects/spiel/badge/?version=latest)](https://spiel.readthedocs.io/en/latest/?badge=latest)\n[![PyPI - License](https://img.shields.io/pypi/l/spiel)](https://pypi.org/project/spiel/)\n\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/JoshKarpel/spiel/main.svg)](https://results.pre-commit.ci/latest/github/JoshKarpel/spiel/main)\n[![codecov](https://codecov.io/gh/JoshKarpel/spiel/branch/main/graph/badge.svg?token=2sjP4V0AfY)](https://codecov.io/gh/JoshKarpel/spiel)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[![GitHub issues](https://img.shields.io/github/issues/JoshKarpel/spiel)](https://github.com/JoshKarpel/spiel/issues)\n[![GitHub pull requests](https://img.shields.io/github/issues-pr/JoshKarpel/spiel)](https://github.com/JoshKarpel/spiel/pulls)\n\nSpiel is a framework for building and presenting richly-styled presentations in your terminal using Python.\n\nTo see what Spiel can do without installing it, you can view the demonstration deck in a container:\n```bash\n$ docker run -it --rm ghcr.io/joshkarpel/spiel\n```\nAlternatively, install Spiel (`pip install spiel`) and run this command to view the demonstration deck:\n```bash\n$ spiel demo present\n```\n\n## Sandboxed Execution via Containers\n\nSpiel presentations are live Python code: they can do anything that Python can do.\nYou may want to run untrusted presentations (or even your own presentations) inside a container (but remember, even containers are not perfectly safe!).\nWe produce a [container image](https://github.com/users/JoshKarpel/packages/container/package/spiel)\nthat can be run by (for example) Docker.\n\nPresentations without extra Python dependencies might just need to be bind-mounted into the container.\nFor example, if your demo file is at `$PWD/presentation/deck.py`, you could do\n```bash\n$ docker run -it --rm --mount type=bind,source=$PWD/presentation,target=/presentation ghcr.io/joshkarpel/spiel spiel present /presentation/deck.py\n```\n\nIf the presentation has extra dependencies (like other Python packages),\nwe recommend building a new image that inherits our image (e.g., `FROM ghcr.io/joshkarpel/spiel:vX.Y.Z`).\nSpiel's image itself inherits from the [Python base image](https://hub.docker.com/_/python).\n\n## Supported Systems\n\nSpiel currently relies on underlying terminal mechanisms that are only available on POSIX systems (e.g., Linux and MacOS).\nIf you're on Windows, you can use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) to run Spiel.\n",
    'author': 'JoshKarpel',
    'author_email': 'josh.karpel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JoshKarpel/spiel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
