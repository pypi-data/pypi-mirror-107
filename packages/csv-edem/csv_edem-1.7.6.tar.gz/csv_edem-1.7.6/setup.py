# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['csv_edem']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.3,<2.0.0', 'openpyxl>=3.0.7,<4.0.0', 'rich>=10.2.1,<11.0.0']

extras_require = \
{'gui': ['PySimpleGUI>=4.41.2,<5.0.0', 'matplotlib>=3.4.2,<4.0.0']}

entry_points = \
{'console_scripts': ['csv-edem = csv_edem.cli:main',
                     'csv-edem-gui = csv_edem.gui:main']}

setup_kwargs = {
    'name': 'csv-edem',
    'version': '1.7.6',
    'description': 'Treats CSV files exported from EDEM',
    'long_description': '# csv_edem\nTreats CSV files exported from EDEM\n',
    'author': 'Marcus Bruno Fernandes Silva',
    'author_email': 'marcusbfs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
