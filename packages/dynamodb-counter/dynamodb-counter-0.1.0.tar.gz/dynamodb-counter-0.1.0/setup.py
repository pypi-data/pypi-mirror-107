# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamodb_counter']

package_data = \
{'': ['*']}

extras_require = \
{'boto': ['boto3>=1.17.23,<2.0.0']}

setup_kwargs = {
    'name': 'dynamodb-counter',
    'version': '0.1.0',
    'description': 'An atomic DynamoDB counter',
    'long_description': None,
    'author': 'Imtiaz Mangerah',
    'author_email': 'Imtiaz_Mangerah@a2d24.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a2d24/dynamodb-counter',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
