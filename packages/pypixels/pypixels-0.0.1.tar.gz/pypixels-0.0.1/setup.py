# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypixels']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0', 'aiohttp>=3.7.4,<4.0.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'pypixels',
    'version': '0.0.1',
    'description': "A Python interface for the Python Discord's Pixels project.",
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
