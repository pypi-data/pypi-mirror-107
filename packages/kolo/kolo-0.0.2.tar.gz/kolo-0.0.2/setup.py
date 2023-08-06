# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kolo']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'kolo',
    'version': '0.0.2',
    'description': 'Runtime inspection for Django',
    'long_description': None,
    'author': 'Wilhelm Klopp',
    'author_email': 'team@kolo.app',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kolo.app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
