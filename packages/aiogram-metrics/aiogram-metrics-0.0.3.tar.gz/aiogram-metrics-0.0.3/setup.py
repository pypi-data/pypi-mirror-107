# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_metrics']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=2.13,<3.0', 'aiopg>=1.2.1,<2.0.0', 'betterlogging>=0.0.8,<0.0.9']

setup_kwargs = {
    'name': 'aiogram-metrics',
    'version': '0.0.3',
    'description': 'Message metrics exporter for aiogram framework',
    'long_description': None,
    'author': 'Benyamin Ginzburg',
    'author_email': 'benyomin.94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
