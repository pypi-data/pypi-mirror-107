# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fileshare', 'fileshare.testing']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'tqdm>=4.61.0,<5.0.0', 'volapi>=5.22.0,<6.0.0']

entry_points = \
{'console_scripts': ['fdl = fileshare.main:download',
                     'fup = fileshare.main:upload']}

setup_kwargs = {
    'name': 'fileshare',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'aidan',
    'author_email': 'achaplin3@gatech.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
