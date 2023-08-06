# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bankreader',
 'bankreader.migrations',
 'bankreader.readers',
 'bankreader_demo',
 'bankreader_demo.demoapp',
 'bankreader_demo.demoapp.migrations']

package_data = \
{'': ['*'], 'bankreader': ['locale/cs/LC_MESSAGES/*']}

install_requires = \
['Django>=3.0,<4']

setup_kwargs = {
    'name': 'django-bankreader',
    'version': '1.0.1',
    'description': 'Pluggable django application for reading and processing various formats of bank account statements',
    'long_description': 'django-bankreader\n=================\n\nPluggable django application for reading and processing various formats of bank account statements.\n\nInstallation\n------------\n\n* install ``django-bankreader`` either from source or using pip\n* add `bankreader` to ``settings.INSTALLED_APPS``\n* use ``post_save`` signal to process newly created ``Transaction`` objects\n* see the ``demoapp`` application in ``bankreader_demo`` project for more details\n',
    'author': 'Jakub Dorňák',
    'author_email': 'jakub.dornak@misli.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/misli/django-bankreader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
