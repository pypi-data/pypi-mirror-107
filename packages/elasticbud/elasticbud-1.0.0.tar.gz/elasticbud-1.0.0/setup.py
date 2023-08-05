# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elasticbud']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch-dsl>=7.3.0,<8.0.0',
 'elasticsearch>=7.12.1,<8.0.0',
 'pytest-depends>=1.0.1,<2.0.0',
 'retry>=0.9.2,<0.10.0']

setup_kwargs = {
    'name': 'elasticbud',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'tasker',
    'author_email': 'tasker@ialcloud.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
