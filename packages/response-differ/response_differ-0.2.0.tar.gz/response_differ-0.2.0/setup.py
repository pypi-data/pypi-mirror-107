# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['response_differ', 'response_differ.cassetes', 'response_differ.response_diff']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click-config-file>=0.6.0,<0.7.0',
 'click>=7.1.2,<8.0.0',
 'deepdiff>=5.3.0,<6.0.0',
 'grpc_requests>=0.0.10,<0.0.11',
 'requests>=2.25.1,<3.0.0',
 'vcrpy>=4.1.1,<5.0.0']

entry_points = \
{'console_scripts': ['differ = response_differ.response_diff.cli:differ']}

setup_kwargs = {
    'name': 'response-differ',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'vkytepov',
    'author_email': 'vkytepov@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
