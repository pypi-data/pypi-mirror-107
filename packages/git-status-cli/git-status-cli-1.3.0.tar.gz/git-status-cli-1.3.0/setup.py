# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_status_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click>=7.1.2,<8.0.0', 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['gitstatus = git_status_cli.cli:main']}

setup_kwargs = {
    'name': 'git-status-cli',
    'version': '1.3.0',
    'description': 'Get the status of all your gits in one command!',
    'long_description': '# gitstatus\n\nGet the status of all your gits in one command!\n\n# Installation\n\n```\npipx install gitstatus\n```\nInstallation with pipx (or pip but pipx is preferred) will make the gitstatus command available globally:\n<p align="center">\n    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/install_1.png">\n</p>\n\n# CLI Usage\n\n```\nUsage: gitstatus [OPTIONS]\n\n  Get the status of all your gits in one command!\n\nOptions:\n  --help  Show this message and exit.\n```\nBefore use, gitstatus must be configured by editing the config.yaml file (it will automatically be created if it does not exist):\n<p align="center">\n    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/config_1.png">\n</p>\nThe syntax is plain YAML:\n<p align="center">\n    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/config_2.png">\n</p>\ngitstatus will execute git status for each of your repositories and will repeatedly ask you to issue commands until all of your repositories are in a clean state:\n<p align="center">\n    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/usage_1.png">\n    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/usage_2.png">\n</p>\n\nAny submodule is automatically handled\n\n# Authors\n\n* Alexandre Janvrin, penetration tester at Beijaflore (https://www.beijaflore.com/en/)\n\n# License\n\nAGPLv3+, see LICENSE.txt for more details.\n\n# URLs\n\n* https://pypi.org/project/git-status-cli/\n* https://github.com/LivinParadoX/gitstatus/\n',
    'author': 'Alexandre Janvrin',
    'author_email': 'alexandre.janvrin@reseau.eseo.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LivinParadoX/gitstatus/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
