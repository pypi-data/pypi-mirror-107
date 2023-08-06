# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wj_credentials']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.14.52']

setup_kwargs = {
    'name': 'wj-credentials',
    'version': '0.1.1',
    'description': 'Whale&Jaguar Libary - Credentials',
    'long_description': None,
    'author': 'Sebastian Franco',
    'author_email': 'jsfranco@whaleandjaguar.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6.1,<4.0',
}


setup(**setup_kwargs)
