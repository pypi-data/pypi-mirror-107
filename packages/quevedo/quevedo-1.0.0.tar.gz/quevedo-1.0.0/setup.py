# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quevedo',
 'quevedo.annotation',
 'quevedo.darknet',
 'quevedo.network',
 'quevedo.web']

package_data = \
{'': ['*'], 'quevedo.web': ['static/*', 'static/i18n/*', 'static/lib/*']}

install_requires = \
['click>=8,<9', 'pillow>=8,<9', 'toml>=0.10.2,<0.11.0']

extras_require = \
{'force_layout': ['forcelayout>=1.0.6,<2.0.0'], 'web': ['flask>=1.1.2,<2.0.0']}

entry_points = \
{'console_scripts': ['quevedo = quevedo.cli:cli']}

setup_kwargs = {
    'name': 'quevedo',
    'version': '1.0.0',
    'description': 'Tool for managing datasets of images with compositional semantics',
    'long_description': None,
    'author': 'Antonio F. G. Sevilla',
    'author_email': 'afgs@ucm.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agarsev/quevedo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
