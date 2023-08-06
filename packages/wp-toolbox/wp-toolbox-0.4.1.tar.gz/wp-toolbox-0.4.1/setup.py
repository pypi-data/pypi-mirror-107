# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wp_toolbox']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.12.1,<8.0.0']

setup_kwargs = {
    'name': 'wp-toolbox',
    'version': '0.4.1',
    'description': 'Library for accessing linguistic annotated texts (https://wp-toolbox.thomas-zastrow.de)',
    'long_description': None,
    'author': 'Thomas Zastrow',
    'author_email': 'thomas.zastrow@mpcdf.mpg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
