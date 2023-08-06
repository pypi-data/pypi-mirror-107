# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lightshield', 'lightshield.proxy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'aioredis>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'lightshield',
    'version': '0.1.1b0',
    'description': '',
    'long_description': None,
    'author': 'Doctress',
    'author_email': 'lightshielddev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
