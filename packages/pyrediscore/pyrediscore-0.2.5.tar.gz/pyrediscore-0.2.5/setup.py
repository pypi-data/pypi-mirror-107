# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrediscore']

package_data = \
{'': ['*']}

install_requires = \
['decorator>=5.0.9,<6.0.0', 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'pyrediscore',
    'version': '0.2.5',
    'description': 'Low-level decorators for redis instance I/O operations',
    'long_description': None,
    'author': 'glaunay',
    'author_email': 'pitooon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MMSB-MOBI/pyrediscore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
