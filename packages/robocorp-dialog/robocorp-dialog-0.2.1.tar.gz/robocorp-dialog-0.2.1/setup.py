# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robocorp_dialog']

package_data = \
{'': ['*']}

install_requires = \
['pywebview>=3.4,<4.0']

extras_require = \
{':sys_platform == "linux"': ['PyQt5>=5.15.2,<6.0.0',
                              'PyQtWebEngine>=5.15.2,<6.0.0']}

entry_points = \
{'console_scripts': ['robocorp-dialog = robocorp_dialog.main:main']}

setup_kwargs = {
    'name': 'robocorp-dialog',
    'version': '0.2.1',
    'description': 'Dialog for querying user input',
    'long_description': '# Robocorp Dialog\n\nA separate executable which opens a dialog window for querying user input.\nContent created dynamically based on JSON spec.\n\nUsed in [Dialogs](https://github.com/robocorp/rpaframework/tree/master/packages/dialogs) library.\n',
    'author': 'Ossi Rajuvaara',
    'author_email': 'ossi@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rpaframework.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
