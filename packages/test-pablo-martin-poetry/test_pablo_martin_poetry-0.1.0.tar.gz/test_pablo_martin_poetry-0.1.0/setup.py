# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_pablo_martin_poetry']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'test-pablo-martin-poetry',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pablo Martin Fernandez',
    'author_email': 'pablo.martin.fernandez@pwc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
