# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['consoom']
install_requires = \
['mistune==2.0.0rc1', 'urllib3>=1.26.5,<2.0.0']

setup_kwargs = {
    'name': 'consoom',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'nhanb',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
