# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymystiko_cli']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.75,<2.0.0', 'click>=8.0.0,<9.0.0']

entry_points = \
{'console_scripts': ['mystiko = pymystiko_cli.cli:main']}

setup_kwargs = {
    'name': 'pymystiko-cli',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Clayton',
    'author_email': 'dan@azwebmaster.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
