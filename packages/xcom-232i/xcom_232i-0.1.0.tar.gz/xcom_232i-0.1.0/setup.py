# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xcom_232i']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'xcom-232i',
    'version': '0.1.0',
    'description': 'Python library to access Studer-Innotec Xcom-232i device through RS-232 over a serial port',
    'long_description': '# xcom-232i\nPython library to access Studer-Innotec Xcom-232i device through RS-232 over a serial port\n',
    'author': 'zocker-160',
    'author_email': 'zocker1600@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zocker-160/xcom-232i',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
