# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['playwrighting', 'playwrighting.navigation']

package_data = \
{'': ['*']}

install_requires = \
['12factor-configclasses>=0.3,<0.4',
 'anyio>=3.1.0,<4.0.0',
 'asyncclick>=8.0.1,<9.0.0',
 'beautifulsoup4>=4.9,<5.0',
 'html5lib>=1.1,<2.0',
 'lxml>=4.6.3,<5.0.0',
 'more-itertools>=8.7,<9.0',
 'pandas>=1.2.4,<2.0.0',
 'playwright>=1.11,<2.0',
 'python-dotenv>=0.15,<0.16',
 'rich>=10.2.2,<11.0.0',
 'selectolax>=0.2,<0.3',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['pying = playwrighting.pying:cli']}

setup_kwargs = {
    'name': 'playwrighting',
    'version': '0.4.0',
    'description': 'Get your ING account data',
    'long_description': None,
    'author': 'Pablo Cabezas',
    'author_email': 'headsrooms@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
