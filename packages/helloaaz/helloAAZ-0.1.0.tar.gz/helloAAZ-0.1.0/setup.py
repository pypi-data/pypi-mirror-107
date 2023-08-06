# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helloaaz']

package_data = \
{'': ['*']}

install_requires = \
['pyfiglet>=0.8.post1,<0.9', 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'helloaaz',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'jdan98',
    'author_email': '57507030+jdan98@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
