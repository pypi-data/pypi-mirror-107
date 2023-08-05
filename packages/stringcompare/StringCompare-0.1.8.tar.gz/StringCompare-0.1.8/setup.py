# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['stringcompare']
install_requires = \
['click>=8.0.1,<9.0.0', 'matplotlib>=3.4.2,<4.0.0']

entry_points = \
{'console_scripts': ['stringcompare = stringcompare:main']}

setup_kwargs = {
    'name': 'stringcompare',
    'version': '0.1.8',
    'description': 'This package contains functions for comparing strings, finding substrings (the first occurrence of the desired string) ',
    'long_description': None,
    'author': 'Marsel Muzafarov, Ravil Nurgaliev',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
