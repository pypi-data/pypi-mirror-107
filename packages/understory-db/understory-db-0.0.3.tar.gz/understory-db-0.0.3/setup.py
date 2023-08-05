# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0',
 'redis>=3.5.3,<4.0.0',
 'sh>=1.14.2,<2.0.0',
 'understory-fx>=0.0.2,<0.0.3']

setup_kwargs = {
    'name': 'understory-db',
    'version': '0.0.3',
    'description': 'Tools for metamodern data management',
    'long_description': '# understory-db\nTools for metamodern data management\n',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@lahacker.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
