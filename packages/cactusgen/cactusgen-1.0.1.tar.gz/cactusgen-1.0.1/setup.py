# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cactusgen']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cactusgen',
    'version': '1.0.1',
    'description': 'Minecraft cactus generation simulation in python',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
