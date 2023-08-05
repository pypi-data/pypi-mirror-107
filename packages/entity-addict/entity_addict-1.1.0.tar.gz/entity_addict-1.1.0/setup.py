# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entity_addict', 'entity_addict.test']

package_data = \
{'': ['*']}

install_requires = \
['addict>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'entity-addict',
    'version': '1.1.0',
    'description': 'An extended version of [addict](https://github.com/mewwts/addict).',
    'long_description': None,
    'author': 'longhao',
    'author_email': 'hal.long@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/loonghao/entity_addict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
