# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raftel']

package_data = \
{'': ['*']}

install_requires = \
['s2sphere>=0.2.5,<0.3.0', 'staticmap>=0.5.5,<0.6.0']

setup_kwargs = {
    'name': 'raftel',
    'version': '0.1.0',
    'description': 'package to plot s2id easily',
    'long_description': None,
    'author': 'mitbal',
    'author_email': 'mit.iqi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
