# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory', 'understory.term']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete>=1.12.3,<2.0.0', 'understory-code>=0.0.22,<0.0.23']

setup_kwargs = {
    'name': 'understory-term',
    'version': '0.0.3',
    'description': 'Tools for metamodern terminal development',
    'long_description': '# understory-term\nTools for metamodern terminal development\n',
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
