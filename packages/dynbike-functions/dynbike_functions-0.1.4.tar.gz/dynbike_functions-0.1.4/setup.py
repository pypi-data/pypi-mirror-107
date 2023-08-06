# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynbike_functions', 'dynbike_functions..ipynb_checkpoints']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dynbike-functions',
    'version': '0.1.4',
    'description': 'A small package with collection of useful functions for the Dynamic Bike',
    'long_description': None,
    'author': 'pomkos',
    'author_email': 'albeithome@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
