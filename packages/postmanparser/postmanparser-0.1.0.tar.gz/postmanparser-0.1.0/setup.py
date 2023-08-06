# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postmanparser']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.5b1,<22.0',
 'coverage>=5.5,<6.0',
 'flake8-import-order>=0.18.1,<0.19.0',
 'flake8>=3.9.2,<4.0.0',
 'httpx>=0.18.1,<0.19.0',
 'respx>=0.17.0,<0.18.0',
 'zimports>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'postmanparser',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Appknox',
    'author_email': 'engineering@appknox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
