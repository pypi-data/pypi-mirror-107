# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elasticbud']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch-dsl>=7.3.0,<8.0.0',
 'elasticsearch[async]>=7.13.0,<8.0.0',
 'pytest-asyncio>=0.15.1,<0.16.0',
 'pytest-depends>=1.0.1,<2.0.0',
 'tenacity>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'elasticbud',
    'version': '1.2.0',
    'description': 'Wrappers for writing concise Elasticsearch-integrated python APIs.',
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
