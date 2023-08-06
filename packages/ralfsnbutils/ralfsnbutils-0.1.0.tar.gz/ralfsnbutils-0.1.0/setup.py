# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ralfsnbutils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.23,<0.24']

setup_kwargs = {
    'name': 'ralfsnbutils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'rschmidtner',
    'author_email': 'RSchmidtner@NewYorker.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
