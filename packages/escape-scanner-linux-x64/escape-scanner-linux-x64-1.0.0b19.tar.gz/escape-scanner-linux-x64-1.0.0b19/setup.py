# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['escape_scanner_wrapper', 'escape_scanner_wrapper.static']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['escape-scanner-linux-x64 = escape_scanner_wrapper:main']}

setup_kwargs = {
    'name': 'escape-scanner-linux-x64',
    'version': '1.0.0b19',
    'description': 'Escape Scanner binary used by Escape CLI for Python',
    'long_description': None,
    'author': 'Escape Technologies SAS',
    'author_email': 'ping@escape.tech',
    'maintainer': 'Antoine Carossio',
    'maintainer_email': 'antoine.carossio@me.com',
    'url': 'https://escape.tech/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
