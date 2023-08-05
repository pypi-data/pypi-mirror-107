# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastql_packages']

package_data = \
{'': ['*'], 'fastql_packages': ['templates/*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'fastapi>=0.65.1,<0.66.0',
 'graphene-pydantic>=0.2.0,<0.3.0',
 'graphene>=3.0b5',
 'inflect>=5.3.0,<6.0.0',
 'orator>=0.9.9,<0.10.0',
 'passlib>=1.7.4,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'uvicorn>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['fastql = fastql_packages.main:main']}

setup_kwargs = {
    'name': 'fastql-packages',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Muhammad Abdurrahman',
    'author_email': 'rachman.sd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
