# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_licence_plugin']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'simple-licence-plugin',
    'version': '0.1.1',
    'description': 'Provides a plugin for pyarmor for checking a licence file is valid.',
    'long_description': None,
    'author': 'Alex Hunt',
    'author_email': 'alex.hunt@csiro.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
