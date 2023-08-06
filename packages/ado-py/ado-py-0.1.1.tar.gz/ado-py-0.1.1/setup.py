# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ado']
entry_points = \
{'console_scripts': ['ado = ado:main']}

setup_kwargs = {
    'name': 'ado-py',
    'version': '0.1.1',
    'description': 'Do stuff with python. Quickly access functions defied in do.py from the command-line.',
    'long_description': '# ado-py\n\nDo stuff with python. Quickly access functions from the command-line.\n\nAutomate stuff and save time.\n\nInspired by make. 😂\n\nTo avoid repetition of lines in the terminal, we often create a make alias and call\n`make func`\n\nIn `make` you write stuff in shell, in `ado`, you write in python.\n\n## Installation\n\n```shell\npip install ado-py\n```\n\n## Usage\n\nCreate a `do.py` file in your directory.\n\nWrite functions in it like this\n\nNote: the functions in `do.py` should not take any arguments.\nFor user input use `input()` function.\n\nCall any function from the terminal by running `ado func`.\n\nRunning only `ado` would print the docstring of `do.py`.\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/ado-py',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
