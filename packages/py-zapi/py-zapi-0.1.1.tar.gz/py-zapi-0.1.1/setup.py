# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zapi', 'zapi.mdp']

package_data = \
{'': ['*']}

install_requires = \
['pyzmq>=22.0']

setup_kwargs = {
    'name': 'py-zapi',
    'version': '0.1.1',
    'description': 'ZeroMQ Devices API',
    'long_description': '# Python ZAPI Library\n\nPre-alpha state, this will change without warning.\n\nZeroMQ devices used in `plantd`.\n\n* MDP broker\n* MDP client and worker\n',
    'author': 'Geoff Johnson',
    'author_email': 'geoff.jay@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/plantd/py-zapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
