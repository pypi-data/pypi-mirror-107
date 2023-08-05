# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_web3', 'async_web3.types']

package_data = \
{'': ['*']}

install_requires = \
['eth-abi>=2.1.1,<3.0.0',
 'eth-brownie>=1.14.6,<2.0.0',
 'eth-utils>=1.10.0,<2.0.0',
 'pytest-asyncio>=0.15.1,<0.16.0',
 'web3>=5.18.0,<6.0.0',
 'websockets>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'async-web3',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'Guanqun Lu',
    'author_email': 'guanqunlu@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
