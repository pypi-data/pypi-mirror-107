# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autodeploy-tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'autodeploy-tests',
    'version': '2.0.1.dev1622140005',
    'description': '',
    'long_description': None,
    'author': 'Marco Acierno',
    'author_email': 'marcoaciernoemail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
