# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich', 'rich.tui', 'rich.tui.examples', 'rich.tui.widgets']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rich.tui',
    'version': '0.1.0',
    'description': 'Build Text User Interfaces with Rich',
    'long_description': None,
    'author': 'Will McGugan',
    'author_email': 'willmcgugan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
