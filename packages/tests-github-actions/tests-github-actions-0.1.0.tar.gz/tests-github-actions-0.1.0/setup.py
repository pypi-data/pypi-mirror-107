# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests_github_actions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tests-github-actions',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'William C. Canin',
    'author_email': 'william.costa.canin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/williamcanin/tests-github-actions',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
