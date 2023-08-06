# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brain_games', 'brain_games.games', 'brain_games.scripts']

package_data = \
{'': ['*']}

install_requires = \
['prompt>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['brain-calc = brain_games.scripts.brain_calc:main',
                     'brain-even = brain_games.scripts.brain_even:main',
                     'brain-games = brain_games.scripts.brain_games:main',
                     'brain-gcd = brain_games.scripts.brain_gcd:main',
                     'brain-prime = brain_games.scripts.brain_prime:main',
                     'brain-progression = '
                     'brain_games.scripts.brain_progression:main']}

setup_kwargs = {
    'name': 'artemy64-brain-games',
    'version': '0.1.0',
    'description': 'Brain Games Education Project',
    'long_description': None,
    'author': '_artemy',
    'author_email': 'artemy.andrienko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArtemyAndrienko/python-project-lvl1',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
