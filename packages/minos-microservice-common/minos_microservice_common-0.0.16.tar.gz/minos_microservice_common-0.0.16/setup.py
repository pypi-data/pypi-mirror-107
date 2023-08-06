# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minos',
 'minos.common',
 'minos.common.configuration',
 'minos.common.messages',
 'minos.common.model',
 'minos.common.model.abc',
 'minos.common.protocol',
 'minos.common.protocol.avro',
 'minos.common.repository',
 'minos.common.storage']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'aiomisc>=14.0.3,<15.0.0',
 'aiopg>=1.2.1,<2.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'dependency-injector>=4.32.2,<5.0.0',
 'fastavro>=1.4.0,<2.0.0',
 'lmdb>=1.2.1,<2.0.0',
 'orjson>=3.5.2,<4.0.0']

setup_kwargs = {
    'name': 'minos-microservice-common',
    'version': '0.0.16',
    'description': 'Python Package with common Classes and Utilities used in Minos Microservices.',
    'long_description': 'Minos Microservice Common\n=========================\n\n[![codecov](https://codecov.io/gh/Clariteia/minos_microservice_common/branch/main/graph/badge.svg)](https://codecov.io/gh/Clariteia/minos_microservice_common)\n\n![Tests](https://github.com/Clariteia/minos_microservice_common/actions/workflows/python-tests.yml/badge.svg)\n\nPython Package with common Classes and Utilities used in Minos Microservices\n\nCredits\n-------\n\nThis package was created with ![Cookiecutter](https://github.com/audreyr/cookiecutter)  and the ![Minos Package](https://github.com/Clariteia/minos-pypackage) project template.\n\n',
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
