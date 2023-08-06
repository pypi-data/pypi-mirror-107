# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hintable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hintable',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Sebastián Ramírez',
    'author_email': 'tiangolo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
