# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakypy', 'snakypy.chamyleon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chamyleon',
    'version': '0.1.0a1',
    'description': '',
    'long_description': '',
    'author': 'William C. Canin',
    'author_email': 'william.costa.canin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
