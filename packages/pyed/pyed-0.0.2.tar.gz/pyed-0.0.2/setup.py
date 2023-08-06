# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyed']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyed',
    'version': '0.0.2',
    'description': 'A simple command-line AST editor for Python files.',
    'long_description': '# pyed\nA simple command-line AST editor for Python files.\n',
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
