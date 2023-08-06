# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lnpanda']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.4,<2.0.0',
 'pdir2>=0.3.2,<0.4.0',
 'protobuf3-to-dict>=0.1.5,<0.2.0',
 'py-lnd-grpc>=0.2.3,<0.3.0']

setup_kwargs = {
    'name': 'lnpanda',
    'version': '0.1.0',
    'description': 'A tool which pairs Pandas to LND Lightning Network Data for Data Science',
    'long_description': '# lnpanda\n',
    'author': 'Sam Korn',
    'author_email': 'korn94sam@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
