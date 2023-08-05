# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['naunet',
 'naunet.chemistry',
 'naunet.console',
 'naunet.console.commands',
 'naunet.dusts',
 'naunet.examples',
 'naunet.examples.deuterium',
 'naunet.examples.ism',
 'naunet.reactions']

package_data = \
{'': ['*'],
 'naunet': ['templates/cvode/*',
            'templates/cvode/include/*',
            'templates/cvode/src/*',
            'templates/data/*',
            'templates/odeint/*',
            'templates/odeint/include/*',
            'templates/odeint/src/*',
            'templates/patches/enzo/*',
            'templates/patches/enzo/hydro_rk/*'],
 'naunet.examples.deuterium': ['test/*'],
 'naunet.examples.ism': ['test/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'cleo>=0.8.1,<0.9.0',
 'lark>=0.11.1,<0.12.0',
 'tomlkit>=0.7.0,<0.8.0',
 'tqdm>=4.58.0,<5.0.0']

entry_points = \
{'console_scripts': ['naunet = naunet.console:main']}

setup_kwargs = {
    'name': 'naunet',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Chia-Jung Hsu',
    'author_email': 'appolloford@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
