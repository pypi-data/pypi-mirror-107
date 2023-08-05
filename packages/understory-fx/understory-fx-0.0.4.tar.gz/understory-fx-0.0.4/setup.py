# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.9.0,<3.0.0', 'emoji>=1.2.0,<2.0.0', 'lxml>=4.6.3,<5.0.0']

setup_kwargs = {
    'name': 'understory-fx',
    'version': '0.0.4',
    'description': 'Tools for metamodern audiovisual effects',
    'long_description': '# understory-fx\nTools for metamodern audiovisual effects\n',
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
