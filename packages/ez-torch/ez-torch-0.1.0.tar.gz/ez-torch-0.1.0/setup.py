# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ez_torch']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.8.1,<2.0.0', 'torchvision>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'ez-torch',
    'version': '0.1.0',
    'description': 'Utility functions and fluent interface for pytorch tensors and modules',
    'long_description': None,
    'author': 'Iliya Zhecev',
    'author_email': 'iliya.zhechev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
