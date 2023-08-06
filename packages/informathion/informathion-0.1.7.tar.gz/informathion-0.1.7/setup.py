# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['informathion']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'informathion',
    'version': '0.1.7',
    'description': 'Measurements for Expected Opportunity Loss',
    'long_description': None,
    'author': 'migueltorrescosta',
    'author_email': 'miguelptcosta1995@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
