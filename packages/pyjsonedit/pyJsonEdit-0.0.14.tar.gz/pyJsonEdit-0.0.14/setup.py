# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyjsonedit']

package_data = \
{'': ['*']}

install_requires = \
['coverage==5.5', 'pylint==2.8.2', 'pytest==6.2.4']

entry_points = \
{'console_scripts': ['pyjsonedit = pyjsonedit.cli:main']}

setup_kwargs = {
    'name': 'pyjsonedit',
    'version': '0.0.14',
    'description': 'Edit parts of json strings & files while keeping the orginal, inconsistent formating',
    'long_description': '# pyJsonEdit\n\n[![PyPi version](https://pypip.in/v/jsoneditor/badge.png)](https://crate.io/packages/jsoneditor/)\n[![license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)]()\n[![tests](https://github.com/UrbanskiDawid/pyJsonEditor/actions/workflows/tests.yaml/badge.svg)](https://github.com/UrbanskiDawid/pyJsonEditor/actions/workflows/tests.yaml)\n\n[![](https://forthebadge.com/images/badges/made-with-python.svg)]()\n[![](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()\n[![](https://forthebadge.com/images/badges/uses-badges.svg)]()\n[![](https://forthebadge.com/images/badges/works-on-my-machine.svg)]()\n\n\n\n\nEdit parts of inconsistently formatted json.\n\nIt\'s just a bit slower that doint this by hand!\n\n\n## how to install\n\n> pip install --upgrade pyjsonedit\n\n\n# json in python\n\n**Pure pyhon** implementation of json encoder/decoder.\n\nIts slow and unnecessary!\n# matcher\n\nNow you can select **nodes** in json tree\n\nsyntax!\n\n  *  | select all children in current node\n-----|-----\n [n] | select n-th item of curent node\n {n} | select n-th item of curent node\n key | select node chilld by name \n"key"| select node chilld by name\n \\>  | go to next node\n\n## example: mask multiple nodes\n> $ ./pyjsonedit/print_color **"quiz > * > q1 >*"** DOC/example.json\n\n```\n{\n    "quiz": {\n        "sport": {\n            "q1": {\n                "question": XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX,\n                "options": XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX,\n                "answer": XXXXXXXXXXXXXXX\n            }\n        },\n        "maths": {\n            "q1": {\n                "question": XXXXXXXXXXX,\n                "options": XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX,\n                "answer": XXXX\n            },\n            "q2": {\n                "question": "12 - 8 = ?",\n                "options": [\n                    "1",\n                    "2",\n                    "3",\n                    "4"\n                ],\n                "answer": "4"\n            }\n        }\n    }\n}\n```\n\n## example: mask selected nodes\n\n```bash\n$ import pyjsonedit\n$ pyjsonedit.string_match_mark("{\'pass\':123}","pass")\n{\'pass\':XXX}\n```\n![](DOC/mask_pass.gif)[]()\n\n\n',
    'author': 'Dawid Urbanski',
    'author_email': 'kontakt@dawidurbanski.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UrbanskiDawid/pyJsonEditor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
