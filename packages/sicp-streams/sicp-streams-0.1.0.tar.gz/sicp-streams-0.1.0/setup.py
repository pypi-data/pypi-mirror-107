# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sicp_streams', 'streamdemo', 'streamtools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sicp-streams',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Xu Siyuan',
    'author_email': 'inqb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
