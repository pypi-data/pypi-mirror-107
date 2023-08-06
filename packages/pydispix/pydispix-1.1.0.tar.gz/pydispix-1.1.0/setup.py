# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydispix']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'matplotlib>=3.4.2,<3.5.0',
 'pillow>=8.2.0,<8.3.0',
 'requests>=2.25.1,<2.26.0']

setup_kwargs = {
    'name': 'pydispix',
    'version': '1.1.0',
    'description': "API wrapper for python-discord's pixels.",
    'long_description': None,
    'author': 'ItsDrike',
    'author_email': 'itsdrikeofficial@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
