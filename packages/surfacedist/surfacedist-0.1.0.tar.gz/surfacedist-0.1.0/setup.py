# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['surfacedist']

package_data = \
{'': ['*']}

install_requires = \
['absl-py', 'numpy', 'scipy']

setup_kwargs = {
    'name': 'surfacedist',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Simon Biggs',
    'author_email': 'simon.biggs@radiotherapy.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
