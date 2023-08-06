# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kupala',
 'kupala.framework',
 'kupala.framework.commands',
 'kupala.framework.extensions',
 'kupala.security']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0,<4.0',
 'aiofiles>=0.6.0,<0.7.0',
 'click>=7.1.2,<8.0.0',
 'itsdangerous>=1.1.0,<2.0.0',
 'passlib>=1.7.4,<2.0.0',
 'python-dotenv>=0.17.1,<0.18.0',
 'python-multipart>=0.0.5,<0.0.6',
 'starlette>=0.14,<0.15']

setup_kwargs = {
    'name': 'kupala',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'alex.oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
