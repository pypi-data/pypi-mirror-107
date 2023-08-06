# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['px4test']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'psy-taliro>=1.0.0a3,<2.0.0',
 'px4ctl>=1.0.0a1,<2.0.0',
 'px4stack>=1.0.0a1,<2.0.0',
 'pyulog>=0.9.0,<0.10.0']

extras_require = \
{'docs': ['Sphinx>=3.5.4,<4.0.0',
          'sphinx-autodocgen>=1.2,<2.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0']}

entry_points = \
{'console_scripts': ['px4test = px4test.__main__:px4test']}

setup_kwargs = {
    'name': 'px4test',
    'version': '1.0.0a1',
    'description': 'Run PX4 falsification tests',
    'long_description': None,
    'author': 'Quinn Thibeault',
    'author_email': 'quinn.thibeault96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
