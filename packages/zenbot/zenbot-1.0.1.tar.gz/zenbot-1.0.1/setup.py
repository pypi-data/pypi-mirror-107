# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zenbot']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'gunicorn>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'zenbot',
    'version': '1.0.1',
    'description': 'The Zen of Python in Slack',
    'long_description': None,
    'author': 'Bence Nagy',
    'author_email': 'bence@underyx.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
