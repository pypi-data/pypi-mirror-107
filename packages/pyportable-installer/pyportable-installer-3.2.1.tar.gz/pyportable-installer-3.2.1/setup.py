# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyportable_installer',
 'pyportable_installer.bat_2_exe',
 'pyportable_installer.checkup']

package_data = \
{'': ['*'], 'pyportable_installer': ['template/*', 'venv_assets/*']}

install_requires = \
['lk-logger>=3.6,<4.0', 'lk-utils>=1.4.4,<2.0.0', 'pyarmor']

setup_kwargs = {
    'name': 'pyportable-installer',
    'version': '3.2.1',
    'description': 'Build and distribute portable Python application by all-in-one configuration file.',
    'long_description': None,
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
