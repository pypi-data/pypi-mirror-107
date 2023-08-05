# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['floyd_warshall_alg', 'floyd_warshall_alg.common_func']

package_data = \
{'': ['*']}

install_requires = \
['Cycler==0.10.0',
 'Pillow==8.2.0',
 'click>=8.0.1,<9.0.0',
 'kiwisolver==1.3.1',
 'matplotlib==3.4.2',
 'numpy==1.20.3',
 'pandas==1.2.4',
 'pyparsing==2.4.7',
 'python-dateutil==2.8.1',
 'pytz==2021.1',
 'six==1.16.0']

entry_points = \
{'console_scripts': ['floyd_alg = floyd_warshall_alg.simple_algorithm:main']}

setup_kwargs = {
    'name': 'floyd-warshall-alg',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
