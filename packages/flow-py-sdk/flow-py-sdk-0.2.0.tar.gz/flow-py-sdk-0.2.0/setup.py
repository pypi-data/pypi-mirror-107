# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flow_py_sdk',
 'flow_py_sdk.cadence',
 'flow_py_sdk.client',
 'flow_py_sdk.frlp',
 'flow_py_sdk.proto',
 'flow_py_sdk.proto.flow']

package_data = \
{'': ['*']}

install_requires = \
['betterproto[compiler]>=1.2.5,<2.0.0',
 'ecdsa>=0.16.1,<0.17.0',
 'grpcio-tools>=1.33.2,<2.0.0',
 'grpclib>=0.4.1,<0.5.0',
 'rlp>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['examples = examples.main:run']}

setup_kwargs = {
    'name': 'flow-py-sdk',
    'version': '0.2.0',
    'description': 'A python SKD for the flow blockchain',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/flow-py-sdk.svg)](https://pypi.org/project/flow-py-sdk/) \n\n\nSee the [DOCS](https://janezpodhostnik.github.io/flow-py-sdk)!\n\n# flow-py-sdk\n\nAnother unofficial flow blockchain python sdk.\n\nUnder development! Currently this is close to an "MVP" it is mostly missing more of: docs, tests, examples and organization.\n\nIf you do want to use it, install it with:\n\n`pip install flow-py-sdk`\n\nor if using poetry:\n\n`poetry add flow-py-sdk`\n\nIt supports python version 3.9 or higher\n\n',
    'author': 'Janez Podhostnik',
    'author_email': 'janez.podhostnik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/janezpodhostnik/flow-py-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
