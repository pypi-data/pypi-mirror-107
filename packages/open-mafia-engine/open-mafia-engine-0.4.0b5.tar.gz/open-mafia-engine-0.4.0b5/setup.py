# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['open_mafia_engine', 'open_mafia_engine.built_in', 'open_mafia_engine.util']

package_data = \
{'': ['*'], 'open_mafia_engine': ['prefabs/*']}

install_requires = \
['pydantic-yaml>=0.2.3,<0.3.0',
 'pydantic>=1.7.3,<2.0.0',
 'sortedcontainers>=2.3.0,<3.0.0']

extras_require = \
{'bay12': ['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.25.1,<3.0.0'],
 'docs': ['mkdocs>=1.1.2,<2.0.0'],
 'ruamel': ['ruamel.yaml>=0.17.4,<0.18.0']}

setup_kwargs = {
    'name': 'open-mafia-engine',
    'version': '0.4.0b5',
    'description': 'Open Mafia Engine - a framework for mafia/werewolf games.',
    'long_description': '# Open Mafia Engine\n\nThe Open Mafia Engine is a flexible, open-source game engine for Mafia-like games.\n\nSee the [Wikipedia article](https://en.wikipedia.org/wiki/Mafia_%28party_game%29)\nfor information on what Mafia/Werewolf is.\n\nThe Open Mafia Engine actually allows a much broader type of game to be played,\nwith custom roles and very intricate "setups". Most of these custom roles come\nfrom either "real-life" games or online forums such as\n[MafiaScum](https://wiki.mafiascum.net/index.php?title=Main_Page) and\n[Bay12Games Mafia Subforum](http://www.bay12forums.com/smf/index.php?board=20.0).\n\n## Features\n\n- Event-based architecture, which allows for very complex interactions.\n- Many built-in abilities, victory conditions, etc.\n  (This is a lie, but we\'re working on it!)\n- YAML `Prefab`s let you define a game in a (mostly) human-readable fashion.\n- Open source & extensible, with a plugin system in the works.\n\n## Installing\n\nInstall the latest stable version via pip:\n\n`pip install open_mafia_engine`\n\nSee the [dev docs](docs/development/installing_dev.md) to install for local\ndevelopment (using Poetry).\n\n## Getting started\n\nThis example starts a 5-player "vanilla" mafia game (1 mafioso vs 4 townies):\n\n```python\nfrom open_mafia_engine.api import Prefab\n\nprefab = Prefab.load("Vanilla")\nplayers = [\'Alice\', \'Bob\', \'Charlie\', \'Dave\', \'Eddie\']\ngame = prefab.create_game(players)\n```\n\nActually running commands in the engine is pretty complicated for now.\nWe\'re working to improve the experience.\n\nSee `playground.py` in the repository for an example game.\n',
    'author': 'Open Mafia Team',
    'author_email': 'openmafiateam@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://open-mafia-engine.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
