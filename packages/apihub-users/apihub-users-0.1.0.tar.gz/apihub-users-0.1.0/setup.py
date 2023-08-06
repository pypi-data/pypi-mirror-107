# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apihub_users',
 'apihub_users.common',
 'apihub_users.security',
 'apihub_users.subscription']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.37.4,<0.38.0',
 'SQLAlchemy>=1.4.15,<2.0.0',
 'fastapi-jwt-auth>=0.5.0,<0.6.0',
 'fastapi>=0.65.1,<0.66.0',
 'prometheus-client>=0.7.0,<0.8.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'python-dotenv>=0.17.1,<0.18.0',
 'python-multipart>=0.0.5,<0.0.6',
 'redis>=3.5.3,<4.0.0',
 'tanbih-pipeline>=0.11.8,<0.12.0',
 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'apihub-users',
    'version': '0.1.0',
    'description': 'user and subscription management for APIHub',
    'long_description': None,
    'author': 'Yifan Zhang',
    'author_email': 'freqyifan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
