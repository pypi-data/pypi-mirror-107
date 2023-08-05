# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timeseries-cv']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.3,<2.0.0']

setup_kwargs = {
    'name': 'timeseries-cv',
    'version': '0.1.0',
    'description': 'Timeseries cross-validation for Neural Networks',
    'long_description': None,
    'author': 'didier',
    'author_email': 'dro.lopes@campus.fct.unl.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
