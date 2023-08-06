# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rubric']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['rubric = rubric:cli_entrypoint']}

setup_kwargs = {
    'name': 'rubric',
    'version': '0.1.2',
    'description': 'Initialize your Python project with all the linting boilerplates you need',
    'long_description': '',
    'author': 'rednafi',
    'author_email': 'redowan.nafi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rednafi/rubric',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
