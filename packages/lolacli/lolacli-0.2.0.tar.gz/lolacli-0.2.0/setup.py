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
    'version': '0.2.0',
    'description': 'A simple cli tool to help beginners install apps in Linux',
    'long_description': "# Lola\n### `lola` : A simple CLI for installing packages on Linux easily \n\n![GitHub license](https://img.shields.io/github/license/arghyagod-coder/lola)\n\n#### Dependencies\n+ click\n\n## Installation\n```bash\npip install lolacli\n```\n\n## Supported Platforms:\n\n+ Operating System = Linux64\n    - Ubuntu 20.04 and Derivatives\n    - Mint 19.3\n    - Mint 20.1\n    - Debian 10 \n\n## Screenshots\n\n![](assets/help.png)\n\n![](assets/check-apps.png)\n\n![](assets/audacity-dl.png)\n\n## Usage\n\n**lola is made for linux newbies who can find it difficult to download software**\n\nNow many will tell, Why use lola when we have those software managers?\n\nWell, lola is a Command Line Interface and is used inside the terminal. And as we know, terminal downloads are way more faster than the software managers. While many softwares can be downloaded with a single `sudo apt install`, most common ones need some more commands.\n\nSo `lola` is here to make your life way more easier while installing software! This project targets both advanced and beginner users, because who doesn't like speedy and quicky stuff?\n\n### What can lola do?\n\n```bash\nlola --help\n```\n\nThis shows what lola can do. \nShe can install apps and display a list of supported apps in current version\n\n\n\n",
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
