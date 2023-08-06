# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polypuppet', 'polypuppet.agent', 'polypuppet.server']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'configparser>=5.0.2,<6.0.0',
 'distro>=1.5.0,<2.0.0',
 'grpcio>=1.38.0,<2.0.0',
 'protobuf>=3.15.7,<4.0.0',
 'python-vagrant>=0.5.15,<0.6.0',
 'requests-html>=0.10.0,<0.11.0']

extras_require = \
{':sys_platform == "linux"': ['systemd-python>=234,<235']}

entry_points = \
{'console_scripts': ['polypuppet = polypuppet.agent.cli:main',
                     'polypuppet-autosign = polypuppet.agent.cli:autosign']}

setup_kwargs = {
    'name': 'polypuppet',
    'version': '0.1.4',
    'description': 'Administration tool for SPBSTU',
    'long_description': None,
    'author': 'LLDay',
    'author_email': 'ssdenis99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
