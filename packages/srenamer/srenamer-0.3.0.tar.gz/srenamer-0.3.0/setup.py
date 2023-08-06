# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['srenamer']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'tmdbsimple>=2.8.0,<3.0.0']

entry_points = \
{'console_scripts': ['srenamer = srenamer.__main__:main']}

setup_kwargs = {
    'name': 'srenamer',
    'version': '0.3.0',
    'description': 'This is a simple file renamer for TV shows and anime.',
    'long_description': "# srenamer\n\nsrenamer is the simple renaming tool for TV shows and anime.\n\n### Installation\nIt's recomended to install with [pipx](https://pipxproject.github.io/pipx/)\nto not mess with default python installation.\n```\n$ pipx install srenamer\n```\n",
    'author': 'Maxim Makovskiy',
    'author_email': 'makovskiyms@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/evorition/srenamer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
