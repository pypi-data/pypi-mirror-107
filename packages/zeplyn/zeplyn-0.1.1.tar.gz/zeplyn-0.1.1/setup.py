# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeplyn']

package_data = \
{'': ['*']}

install_requires = \
['twine==3.4.1', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['zeplyn = zeplyn.zeplyn:app']}

setup_kwargs = {
    'name': 'zeplyn',
    'version': '0.1.1',
    'description': 'Zeplyn allows to you release python package fastly and easily in one command',
    'long_description': "# Zeplyn\n\n## Usage\n\nZeplyn allows to you release python package fastly and easily in one command: \n\n```zeplyn publish```\n\nYou should run that command in your command prompt in the folder directory where you want to put your package\n\nZeplyn also have a ```zeplyn create``` command which automatically create a readme file, a setup.py file and a src folder where your package's code is going to be stored.\n\nFull documentation here : https://github.com/ssantoshp/zeplyn",
    'author': 'ssantoshp',
    'author_email': 'santoshpassoubady@gmail.com',
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
