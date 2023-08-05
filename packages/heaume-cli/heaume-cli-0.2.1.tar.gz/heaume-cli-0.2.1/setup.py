# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heaume_cli',
 'heaume_cli.commands.japscan',
 'heaume_cli.commands.plant',
 'heaume_cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'influxdb-client>=1.14.0,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.10.0,<10.0.0']

entry_points = \
{'console_scripts': ['heaume = heaume_cli:cli']}

setup_kwargs = {
    'name': 'heaume-cli',
    'version': '0.2.1',
    'description': 'The CLI of Heaume.',
    'long_description': None,
    'author': 'dylandoamaral',
    'author_email': 'do.amaral.dylan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
