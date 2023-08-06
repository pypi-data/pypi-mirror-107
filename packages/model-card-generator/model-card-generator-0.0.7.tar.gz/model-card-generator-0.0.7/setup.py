# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['model_card_generator']

package_data = \
{'': ['*']}

install_requires = \
['requests[security]>=2.13,<3.0', 'toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'model-card-generator',
    'version': '0.0.7',
    'description': 'ML Model Card generator',
    'long_description': '# model-card-generator\nML model card generator\n\n## Run \n```shell\n$ make run\n```\n\n## Install\n```shell\n$ poetry install\n```\n\n## Package\nBump version with Poetry (or manually in `setup.cfg`), \n```shell\n$ poetry version (patch|minor|major)\n```\n\nThen:\n```shell\n$ make package\n```',
    'author': 'Gustavo Salvador',
    'author_email': 'gustavocsalvador@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/g1stavo/model-card-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*',
}


setup(**setup_kwargs)
