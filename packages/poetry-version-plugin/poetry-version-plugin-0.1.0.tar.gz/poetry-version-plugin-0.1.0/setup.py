# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_version_plugin']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a,<2.0.0']

entry_points = \
{'poetry.plugin': ['git-tag-version = '
                   'poetry_version_plugin.plugin:GitTagVersion',
                   'init-version = poetry_version_plugin.plugin:InitVersion']}

setup_kwargs = {
    'name': 'poetry-version-plugin',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Poetry Version\n\nA [Poetry](https://python-poetry.org/) plugin for dynamically extracting the version of a package from `__init__.py` or from a Git tag.\n\nSo you don't have to manually keep the version in two places, in `pyproject.toml` and in `__init__.py` or in a Git tag.\n",
    'author': 'Sebastián Ramírez',
    'author_email': 'tiangolo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
