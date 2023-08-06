# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests_github_actions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tests-github-actions',
    'version': '0.1.1',
    'description': 'Package only tests Github Actions',
    'long_description': 'Package only tests Github Actions.\n\nLicense\n-------\n\nThe gem is available as open source under the terms of the `MIT License`_ ©\n\nCredits\n-------\n\nSee, `AUTHORS`_.\n\n.. _`AUTHORS`: https://github.com/williamcanin/tests-github-actions/blob/master/AUTHORS.rst\n.. _MIT License: https://github.com/williamcanin/tests-github-actions/blob/master/LICENSE\n',
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
