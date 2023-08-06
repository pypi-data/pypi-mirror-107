# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0,<1', 'python-jose>=3.2,<4.0']

setup_kwargs = {
    'name': 'fastapi-resource-server',
    'version': '0.1.0',
    'description': 'Build resource servers with FastAPI',
    'long_description': None,
    'author': 'Livio Ribeiro',
    'author_email': 'livio@codata.pb.gov.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
