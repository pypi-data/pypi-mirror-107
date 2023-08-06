# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poc_publish']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.5b1,<22.0',
 'mypy>=0.812,<0.813',
 'pyfiglet>=0.8.post1,<0.9',
 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'poc-publish',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gláuber Brennon',
    'author_email': 'glauberbrennon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
