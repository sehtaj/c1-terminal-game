# Starter Algo

## File Overview

```
starter-algo
 │
 ├──gamelib
 │   ├──__init__.py
 │   ├──algocore.py
 │   ├──game_map.py
 │   ├──game_state.py
 │   ├──navigation.py
 │   ├──tests.py
 │   ├──unit.py
 │   └──util.py
 │
 ├──algo_strategy.py
 ├──documentation
 ├──README.md
 ├──run.ps1
 └──run.sh
```

### Creating an Algo

To create an algo, simply modify the `algo_strategy.py` file. 
To upload to terminal, upload the entire python-algo folder.

### `algo_strategy.py`

This file contains the `AlgoStrategy` class which you should modify to implement
your strategy.

At a minimum you must implement the `on_turn` method which handles responding to
the game state for each turn. Refer to the `starter_strategy` method for inspiration.

If your algo requires initialization then you should also implement the
`on_game_start` method and do any initial setup there.

### `documentation`

A directory containing the sphinx generated programming documentation, as well as the files required
to build it. You can view the docs by opening index.html in documents/_build.
You can remake the documentation by running 'make html' in the documentation folder.
You will need to install sphinx for this command to work.

### `run.sh`

A script that contains logic to invoke your code. You do not need to run this directly.
See the 'scripts' folder in the Starterkit for information about testing locally.

### `run.ps1`

A script that contains logic to invoke your code. You shouldn't need to change
this unless you change file structure or require a more customized process
startup.

### `gamelib/__init__.py`

This file tells python to treat `gamelib` as a bundled python module. This
library of functions and classes is intended to simplify development by
handling tedious tasks such as communication with the game engine, summarizing
the latest turn, and estimating paths based on the latest board state.

### `gamelib/algocore.py`

This file contains code that handles the communication between your algo and the
core game logic module. You shouldn't need to change this directly. Feel free to 
just overwrite the core methods that you would like to behave differently. 

### `gamelib/game_map.py`

This module contains the `GameMap` class which is used to parse the game state
and provide functions for querying it.

### `gamelib/navigation.py`

Functions and classes used to implement path-finding.

### `gamelib/tests.py`

Unit tests. You can write your own if you would like, and can run them using
the following command:

    python3 -m unittest discover

### `gamelib/unit.py`

This module contains the `GameUnit` class which holds information about a Unit.

### `gamelib/util.py`

Helper functions and values that do not yet have a better place to live.


The starter strategy is designed to highlight a few common `GameMap` functions
and give the user a functioning example to work with. It's gameplan is to
draw the C1 logo, place turrets in its corners, and randomly spawn units.

Terminal Game Strategy

## Strategy Overview

This is a custom algorithm for Terminal, a strategy-based game where players build defenses and deploy attacking units. This strategy focuses on a wall-less defensive approach, relying on turrets, supports, and interceptors for stalling while maintaining an aggressive Scout-only attack strategy.

Strategy Breakdown

Defense
	•	No Walls: The strategy avoids using walls and instead relies on turrets and supports for protection.
	•	Reactive Turret Placement: A turret is immediately placed at any location where the opponent scores to reinforce defenses.
	•	Dynamic SP Usage: Available Structure Points (SP) are used dynamically, prioritizing placing turrets before upgrading them.
	•	Support Placement: Early supports are placed to boost turret efficiency and help defending interceptors.

Offense
	•	Scout-Only Attacks: Scouts are deployed every turn to maintain constant offensive pressure.
	•	Adaptive Spawn Locations: Scouts are sent through the least defended enemy path using a damage estimation function.

Other Features
	•	Interceptor Stalling: If needed, interceptors are deployed to disrupt enemy attacks.
	•	No Fixed Attack Patterns: The strategy adapts attack locations based on enemy defenses.

File Structure
	•	algo_strategy.py – Main algorithm file containing the custom game logic.
	•	README.md – This documentation file.
	•	Other default files from the C1GamesStarterKit are also included in the repository.
