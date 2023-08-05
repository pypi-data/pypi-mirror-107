# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opyv', 'tests']

package_data = \
{'': ['*']}

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

setup_kwargs = {
    'name': 'opyv',
    'version': '0.1.1',
    'description': 'Python library for working with organic photovoltaic materials and device data.',
    'long_description': '# <a href="https://opyv.org" target="_blank"><img src="artwork/opyv_readme_header.png" width=300 alt="OPyV"> </a>\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/opyv">\n<img src="https://img.shields.io/pypi/v/opyv.svg" alt = "Release Status">\n</a>\n<!-- uncomment once a release version is done -->\n<!-- <a href="https://github.com/bluginbuhl/opyv/actions">\n<img src="https://github.com/bluginbuhl/opyv/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a> -->\n<a href="https://codecov.io/gh/bluginbuhl/opyv">\n  <img src="https://codecov.io/gh/bluginbuhl/opyv/branch/main/graph/badge.svg?token=3W7WQW2MTL"/>\n</a>\n<a href="https://opyv.readthedocs.io/en/latest/?badge=latest">\n<img src="https://readthedocs.org/projects/opyv/badge/?version=latest" alt="Documentation Status">\n</a>\n</p>\n\n\nA Python library for working with organic photovoltaic materials and device data.\n\n\n* Free software: GPL-3.0-only\n* Documentation: <https://opyv.readthedocs.io>\n\n\n## Features\n\n* Stay Tuned!\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Benjamin R. Luginbuhl',
    'author_email': 'bluginbuhl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bluginbuhl/opyv',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
