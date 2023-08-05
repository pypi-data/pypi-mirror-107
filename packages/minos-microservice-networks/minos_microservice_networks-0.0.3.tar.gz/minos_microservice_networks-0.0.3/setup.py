# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minos',
 'minos.networks',
 'minos.networks.brokers',
 'minos.networks.handlers',
 'minos.networks.handlers.abc',
 'minos.networks.handlers.command_replies',
 'minos.networks.handlers.commands',
 'minos.networks.handlers.events',
 'minos.networks.rest',
 'minos.networks.snapshots']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'aiokafka>=0.7.0,<0.8.0',
 'aiomisc>=14.0.3,<15.0.0',
 'aiopg>=1.2.1,<2.0.0',
 'dependency-injector>=4.32.2,<5.0.0',
 'minos-microservice-common>=0.0,<0.1']

setup_kwargs = {
    'name': 'minos-microservice-networks',
    'version': '0.0.3',
    'description': 'Python Package with the common network classes and utilities used in Minos Microservice.',
    'long_description': 'Minos Microservice Networks\n===========================\n\n[![codecov](https://codecov.io/gh/Clariteia/minos_microservice_networks/branch/main/graph/badge.svg)](https://codecov.io/gh/Clariteia/minos_microservice_networks)\n\n![Tests](https://github.com/Clariteia/minos_microservice_networks/actions/workflows/python-tests.yml/badge.svg)\n\nPython Package with the common network classes and utlities used in Minos Microservice\n\n\nCredits\n-------\n\nThis package was created with ![Cookiecutter](https://github.com/audreyr/cookiecutter)\nand the ![Minos Package](https://github.com/Clariteia/minos-pypackage) project template.\n',
    'author': 'Clariteia Devs',
    'author_email': 'devs@clariteia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://clariteia.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
