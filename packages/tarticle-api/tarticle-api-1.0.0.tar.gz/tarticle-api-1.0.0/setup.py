# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tarticle_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tarticle-api',
    'version': '1.0.0',
    'description': 'Tarticle API',
    'long_description': None,
    'author': 'billyoobones',
    'author_email': 'tribidpahi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
