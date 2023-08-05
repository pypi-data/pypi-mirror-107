# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lolacli']

package_data = \
{'': ['*'], 'lolacli': ['scripts/*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['lola = lolacli.lolacli:main']}

setup_kwargs = {
    'name': 'lolacli',
    'version': '0.1.9',
    'description': 'A simple cli tool to help beginners install apps in Linux',
    'long_description': '## LOLA\n`lola` : A simple CLI for installing packages on Linux easily \n\n[![GitHub license](https://github.com/arghyagod-coder/lola/blob/master/LICENSE)\n\n\n#### Dependencies\n+ click\n\n',
    'author': 'Arghya Sarkar',
    'author_email': 'arghyasarkar.joker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arghyagod-coder/lola',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
