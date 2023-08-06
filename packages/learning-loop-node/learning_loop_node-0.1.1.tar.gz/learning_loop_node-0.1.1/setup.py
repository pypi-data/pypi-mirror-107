# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['learning_loop_node',
 'learning_loop_node.converter',
 'learning_loop_node.tests',
 'learning_loop_node.trainer',
 'learning_loop_node.trainer.tests']

package_data = \
{'': ['*'],
 'learning_loop_node': ['dist/*'],
 'learning_loop_node.trainer.tests': ['test_data/*']}

install_requires = \
['fastapi-socketio>=0.0.6,<0.0.7',
 'fastapi-utils>=0.2.1,<0.3.0',
 'fastapi>=0.63.0,<0.64.0',
 'python-socketio[asyncio_client]>=5.0.4,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'simplejson>=3.17.2,<4.0.0',
 'uvicorn>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'learning-loop-node',
    'version': '0.1.1',
    'description': 'Python Library for Nodes which connect to the Zauberzeug Learning Loop',
    'long_description': None,
    'author': 'Zauberzeug GmbH',
    'author_email': 'info@zauberzeug.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
