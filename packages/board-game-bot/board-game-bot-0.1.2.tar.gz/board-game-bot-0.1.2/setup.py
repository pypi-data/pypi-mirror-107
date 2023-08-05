# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['board_game_bot']

package_data = \
{'': ['*']}

install_requires = \
['board-game-utils>=0.1.1,<0.2.0',
 'pytility>=0.3.0,<0.4.0',
 'tweepy>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'board-game-bot',
    'version': '0.1.2',
    'description': 'Board game recommender bots 🤖',
    'long_description': '# 🎲 Board Game Bot 🤖\n',
    'author': 'Markus Shepherd',
    'author_email': 'markus@recommend.games',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://recommend.games/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
