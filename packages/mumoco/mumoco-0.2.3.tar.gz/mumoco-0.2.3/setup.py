# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['mumoco']
install_requires = \
['conan>=1.36.0,<2.0.0']

entry_points = \
{'console_scripts': ['mumoco = src.mumoco:main']}

setup_kwargs = {
    'name': 'mumoco',
    'version': '0.2.3',
    'description': 'This is tool helps to work with multiple conan modules simultaneously.',
    'long_description': None,
    'author': 'michel',
    'author_email': 'michel.meyer@disroop.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/disroop/mumoco',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
