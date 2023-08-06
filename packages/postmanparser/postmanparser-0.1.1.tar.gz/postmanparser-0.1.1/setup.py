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
    'version': '0.1.1',
    'description': 'Postman collection parser for python',
    'long_description': '# postmanparser\n![Build](https://github.com/appknox/postmanparser/actions/workflows/test.yml/badge.svg)\n[![codecov](https://codecov.io/gh/appknox/postmanparser/branch/main/graph/badge.svg?token=BXCg5XODJw)](https://codecov.io/gh/appknox/postmanparser)\n\n## Introduction\n\nPostman collection parser written in python3 to extract HTTP requests/responses.\nCurrently supports reading JSON schema two ways\n- Read from `.json` file\n- Fetch from url where schema is exposed\n\n## Installation\n - Using pip\n\n        pip install postmanparser\n\n- Using poetry\n\n        poetry add postmanparser\n\n## Getting Started\n\n### Parsing API Schema\nYou can parse API schema from file or from url as below.\n- From file\n\n```python\nfrom postmanparser import Collection\ncollection = Collection()\ncollection.parse_from_file("path/to/postman/schema.json")\n```\n\n- From url\n\n```python\nfrom postmanparser import Collection\ncollection = Collection()\ncollection.parse_from_url("http://example.com/schema")\n```\nURL should be a `GET` request.\n\npostmanparser also validates for the required fields mentioned by postman schema documentation which is available at https://schema.postman.com/\n\n### Reading the data\nPostman collection contains group of requests and one or more folders having group of requests and/or nested folders in it.\n\nYou can access requests in the collections as shown in below.\n```python\nfor item in collection.item:\n        if isinstance(item, ItemGroup):\n                continue #skip folders\n        print(item.request)\n```\n`item.request` could be a string or of type `Request` with all the attributes of requests according to schema.\n\n### Validation\nIf schema found to be invalid following exception will be thrown.\n- `MissingRequiredFieldException`\n- `InvalidPropertyValueException`\n- `InvalidObjectException`\n\n## Schema Support\npostmanparser is still in early stages and will be updated with missing schema components soon.\n\n### Version\npostmanparser supports collection schema v2.0.0 and v2.1.0.\n\n### Object support\npostmanparser currently does not support parsing of following objects. Might be added in future.\n\n- events\n- protocolProfileBehavior',
    'author': 'Appknox',
    'author_email': 'engineering@appknox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/appknox/postmanparser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
