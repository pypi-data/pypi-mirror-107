# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melib']

package_data = \
{'': ['*'], 'melib': ['data/*']}

install_requires = \
['CoolPlot>=0.1.6,<0.2.0', 'PyLaTeX>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'melib',
    'version': '0.1.0',
    'description': 'Machine element design teaching library',
    'long_description': None,
    'author': 'Gurgenci',
    'author_email': 'h.gurgenci@uq.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
