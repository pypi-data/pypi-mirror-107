# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logger_es_handler']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.13.0,<8.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'logger-es-handler',
    'version': '0.1.1',
    'description': 'ES handler for logging module ',
    'long_description': None,
    'author': 'Gustavo Freitas',
    'author_email': 'gustavo@gmf-tech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
