# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['consult']

package_data = \
{'': ['*'], 'consult': ['data/*']}

install_requires = \
['click>=7.1,<8.0', 'pyyaml==5.4.1']

entry_points = \
{'console_scripts': ['consult = consult:run_consult']}

setup_kwargs = {
    'name': 'consult',
    'version': '0.1.0',
    'description': 'Receive a quick consultation from Engineering!',
    'long_description': 'Receive a quick consultation from Engineering!\n',
    'author': 'Matt VanEseltine',
    'author_email': 'vaneseltine@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vaneseltine/consult',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
