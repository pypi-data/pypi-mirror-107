# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gutsygit']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3', 'colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['gg = gutsygit.main:run']}

setup_kwargs = {
    'name': 'gutsygit',
    'version': '0.5.1',
    'description': 'Command-line tool for fast git usage',
    'long_description': None,
    'author': 'Sander Land',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
