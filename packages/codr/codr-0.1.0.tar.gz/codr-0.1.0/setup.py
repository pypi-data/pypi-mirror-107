# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codr']

package_data = \
{'': ['*']}

install_requires = \
['bullet>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['codr = codr.cli:main']}

setup_kwargs = {
    'name': 'codr',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Adam Parkin',
    'author_email': 'pzelnip@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
