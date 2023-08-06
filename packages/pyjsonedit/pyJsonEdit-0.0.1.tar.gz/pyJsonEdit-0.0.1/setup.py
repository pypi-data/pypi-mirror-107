# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyjsonedit']

package_data = \
{'': ['*']}

install_requires = \
['coverage==5.5', 'pylint==2.8.2', 'pytest==6.2.4']

setup_kwargs = {
    'name': 'pyjsonedit',
    'version': '0.0.1',
    'description': 'Edit parts of json strings & files while keeping the orginal, inconsistent formating',
    'long_description': '# pyJsonEdit\n\nEdit parts of inconsistently formatted json',
    'author': 'Dawid Urbanski',
    'author_email': 'kontakt@dawidurbanski.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UrbanskiDawid/pyJsonEditor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
