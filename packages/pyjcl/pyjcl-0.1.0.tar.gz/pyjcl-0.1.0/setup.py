# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jcl', 'jcl.cli']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jcl = jcl.cli:main']}

setup_kwargs = {
    'name': 'pyjcl',
    'version': '0.1.0',
    'description': 'Jammy commandline',
    'long_description': None,
    'author': 'Qinsheng',
    'author_email': 'qsh.zh27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
