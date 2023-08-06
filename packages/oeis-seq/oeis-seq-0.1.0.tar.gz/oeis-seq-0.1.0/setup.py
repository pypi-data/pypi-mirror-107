# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oeis', 'oeis.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'oeis-seq',
    'version': '0.1.0',
    'description': 'OEIS Integer sequences implemented in Python',
    'long_description': None,
    'author': 'Reid Hochstedler',
    'author_email': 'reidhoch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
