# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyloxone_api']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.1,<0.19.0',
 'pycryptodome>=3.10.1,<4.0.0',
 'websockets>=9.0.1,<10.0.0']

setup_kwargs = {
    'name': 'pyloxone-api',
    'version': '0.2.0',
    'description': 'A package for interacting at a low(ish) level with a Loxone miniserver via the Loxone websocket API',
    'long_description': '# pyloxone-api\nApi for pyloxone.\n',
    'author': 'Joachim Dehli',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JoDehli/pyloxone-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
