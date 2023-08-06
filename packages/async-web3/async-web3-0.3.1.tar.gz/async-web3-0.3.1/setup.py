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
    'version': '0.3.1',
    'description': 'Async Web3 library',
    'long_description': 'This is an opinionated web3 library.\n\n1. async as the first citizen.\n2. websocket support as the first citizen.\n3. it supports `eth_subscribe()` and `eth_unsubscribe()`.\n\n```\n        w3 = AsyncWeb3(WebsocketTransport("ws://127.0.0.1:8546"))\n        await w3.connect()\n        block_stream = await w3.subscribe_block()\n        async for new_block in block_stream:\n            print(f"got new block: {new_block}")\n```\n4. It has no middleware support.\n\n\nThis library tries to simplify the interaction with the *deployed* contracts. If you want to deploy a new smart contract, please checkout the awesome `brownie` tool.\n\nHow to Contribute:\n\n1. install `poetry`\n2. under this folder, run `poetry install`\n3. then run `poetry shell`\n4. start the development\n5. run `poetry run pytest`\n6. send PR\n',
    'author': 'Guanqun Lu',
    'author_email': 'guanqunlu@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guanqun/async-web3.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
