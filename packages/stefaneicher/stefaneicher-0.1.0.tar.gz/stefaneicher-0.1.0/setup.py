# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stefaneicher']

package_data = \
{'': ['*']}

install_requires = \
['conan>=1.36.0,<2.0.0']

setup_kwargs = {
    'name': 'stefaneicher',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Stefan Eicher',
    'author_email': 'stefan.eicher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
