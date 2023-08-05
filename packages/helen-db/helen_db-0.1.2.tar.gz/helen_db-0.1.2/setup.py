# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['helen_db']
setup_kwargs = {
    'name': 'helen-db',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Andrew',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
