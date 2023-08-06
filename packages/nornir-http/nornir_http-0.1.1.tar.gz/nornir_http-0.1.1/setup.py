# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_http']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.1,<0.19.0', 'nornir>=3,<4']

setup_kwargs = {
    'name': 'nornir-http',
    'version': '0.1.1',
    'description': 'http plugins for nornir',
    'long_description': None,
    'author': 'ubaumann',
    'author_email': 'github@m.ubaumann.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
