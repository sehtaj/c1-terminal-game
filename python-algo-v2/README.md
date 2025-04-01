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

Terminal Game AI - Wall-less Defensive Strategy

This is a custom Terminal Game AI designed to execute a wall-less defensive strategy while maintaining a strong offense with Scout-only attacks. The strategy dynamically places Turrets, Supports, and Interceptors for defense while ensuring continuous pressure with Scouts.

⸻

## Strategy Overview

### Defense:
	•	No Walls: This strategy avoids using walls, focusing entirely on Turrets and Supports for defense.
	•	Turret Placement:
	•	Initial turrets are placed at key locations.
	•	Additional turrets are placed wherever the opponent scores to reinforce weak spots.
	•	Support Usage:
	•	Supports are deployed at predefined locations starting round 3 to enhance turret effectiveness.
	•	Support units are prioritized over turret upgrades if resources are limited.

### Offense:
	•	Scout-Only Attacks:
	•	Scouts are spawned every round from the safest available location.
	•	The spawn location is determined dynamically using the least_damage_spawn_location() function.
	•	No Demolishers: This strategy does not use Demolishers, keeping resources focused on Scouts and defense.

### Dynamic Resource Allocation:
	•	SP Usage:
	•	Prioritizes placing turrets where needed.
	•	Supports are placed starting from round 3 and upgraded dynamically.
	•	If all defensive structures are in place, extra turrets and supports are built in the center.
	•	MP Usage:
	•	Scouts are deployed every turn to apply constant pressure.
	•	If additional MP is available, Interceptors are deployed for defensive stalling.

⸻

### How It Works

### Key Functions:
	1.	starter_strategy(game_state):
	•	Calls defense and offense functions.
	•	Scouts are spawned every round.
	2.	build_defences(game_state):
	•	Places initial turrets and supports.
	•	Upgrades turrets if SP is available.
	3.	build_reactive_defense(game_state):
	•	Reacts to enemy scoring by placing turrets and supports at breached locations.
	•	Supports are deployed starting from turn 3.
	•	Upgrades existing structures dynamically based on available SP.
	4.	stall_with_interceptors(game_state):
	•	Deploys Interceptors when needed to counter enemy attacks.
	5.	least_damage_spawn_location(game_state, location_options):
	•	Chooses the safest path for deploying Scouts by analyzing enemy turret positions.
	6.	on_action_frame(turn_string):
	•	Records locations where the opponent scores for reactive defense placement.
