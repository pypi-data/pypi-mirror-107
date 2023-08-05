# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stringcompare']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stringcompare',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'Marsel Muzafarov, Ravil Nurgaliev',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
