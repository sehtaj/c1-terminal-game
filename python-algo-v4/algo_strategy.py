import gamelib
import random
import math
import warnings
from sys import maxsize
import json

#SPAWN TURRETS BEFORE UPGRADING

""" 
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        # This is a good place to do initial setup
        self.scored_on_locations = []

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)

        # if (int(game_state.turn_number) == 0):
        #     gamelib.debug_write(" ")
        #     gamelib.debug_write("game_start")
        #     gamelib.debug_write(game_state.config["unitInformation"][0])
        #     gamelib.debug_write("game)end")
        #     gamelib.debug_write(" ")

        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()


    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

    def starter_strategy(self, game_state):
        """
        For defense we will use a spread out layout and some interceptors early on.
        We will place turrets near locations the opponent managed to score on.
        For offense we will use long range demolishers if they place stationary units near the enemy's front.
        If there are no stationary units to attack in the front, we will send Scouts to try and score quickly.
        """
        # First, place basic defenses
        self.build_defences(game_state)
        # Now build reactive defenses based on where the enemy scored
        self.build_reactive_defense(game_state)

        # If the turn is less than 5, stall with interceptors and wait to see enemy's base
        # if game_state.turn_number < 0:
        #     self.stall_with_interceptors(game_state)
        # else:
        #     # Now let's analyze the enemy base to see where their defenses are concentrated.
        #     # If they have many units in the front we can build a line for our demolishers to attack them at long range.
        #     # if self.detect_enemy_unit(game_state, unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
        #         # self.demolisher_line_strategy(game_state)
        #     if False:
        #         pass
        #     else:
        #         # They don't have many units in the front so lets figure out their least defended area and send Scouts there.

        #         # Only spawn Scouts every other turn
        #         # Sending more at once is better since attacks can only hit a single scout at a time
        #         if game_state.turn_number % 16 == 15:
        #             # every four turns try sending demolishers protected by interceptors
        #             demolisher_spawn_location_options = [[13, 0], [14, 0]]
        #             interceptor_spawn_location_options = [[13, 9], [14, 9]]
        #             i = 0
        #             while True:
        #                 if i == 0:
        #                     if game_state.attempt_spawn(DEMOLISHER, demolisher_spawn_location_options[0]) != 1:
        #                         break
        #                 elif i == 1:
        #                     if game_state.attempt_spawn(INTERCEPTOR, interceptor_spawn_location_options[0]) != 1:
        #                         break
        #                 elif i == 2:
        #                     if game_state.attempt_spawn(DEMOLISHER, demolisher_spawn_location_options[1]) != 1:
        #                         break
        #                 elif i == 3:
        #                     if game_state.attempt_spawn(INTERCEPTOR, interceptor_spawn_location_options[1]) != 1:
        #                         break
        #                 i += 1
        #                 i %= 4
                        
        if game_state.turn_number == 0:
            # To simplify we will just check sending them from back left and right
            scout_spawn_location_options = [[13, 0], [14, 0]]
            best_location = self.least_damage_spawn_location(game_state, scout_spawn_location_options)
            game_state.attempt_spawn(SCOUT, best_location, 1000)

        elif game_state.turn_number % 1 == 0:
            scout_spawn_location_options = [[5, 8], [6, 7], [7, 6], [8, 5], [9, 4], [10, 3], [11, 2], [12, 1], [13, 0], [14, 0], [15, 1], [16, 2], [17, 3], [18, 4], [19, 5], [20, 6], [21, 7], [22, 8]]

            best_location = self.least_damage_spawn_location(game_state, scout_spawn_location_options)


        if best_location:  # ✅ Ensure it is not None before using it
            game_state.attempt_spawn(SCOUT, best_location, 1000)

        else:
            game_state.attempt_spawn(SCOUT, [[13,0]], 1000)


        # # Lastly, if we have spare SP, let's build some supports
        # support_locations = [[13, 2], [14, 2], [13, 3], [14, 3]]
        # game_state.attempt_spawn(SUPPORT, support_locations)

    def build_defences(self, game_state):
        """
        Build initial defenses and dynamically upgrade turrets and supports.
        """
        turret_locations = [[3, 12], [9, 12], [18, 12], [24, 12], [13, 9], [14, 9]]
        support_locations = [[13, 8], [14, 8], [13, 7], [14, 7]]
        
        game_state.attempt_spawn(TURRET, turret_locations)
        
        if game_state.turn_number == 0:
            game_state.attempt_spawn(SUPPORT, support_locations)
            game_state.attempt_upgrade(support_locations)
        
        # Upgrade turrets dynamically if SP is available
        turret_upgrade_priority = [[3, 12], [24, 12], [9, 12], [18, 12]]
        available_sp = game_state.get_resource(SP)

        for turret in turret_upgrade_priority:
            if available_sp >= 6 and game_state.contains_stationary_unit(turret):
                game_state.attempt_upgrade(turret)
                available_sp -= 6

    def build_reactive_defense(self, game_state):
        """
        Builds defenses in this priority order:
        1. Build turrets at locations where I got scored on.
        2. Rebuild supports if they were destroyed at the same positions.
        3. Rebuild turrets if they were destroyed at the same positions.
        4. Upgrade turrets that were built in step 1.
        5. Upgrade supports that were built in step 2.
        6. Upgrade any remaining turrets and supports.
        7. If everything is upgraded, add new turrets and supports.
        """

        available_sp = game_state.get_resource(SP)
        built_turrets = []  # Track newly built turrets (Step 1)
        built_supports = []  # Track newly built supports (Step 2)

        # **1️⃣ Build turrets where I got scored on**
        for loc in self.scored_on_locations:
            if available_sp < 4:
                break
            if game_state.can_spawn(TURRET, loc):  
                game_state.attempt_spawn(TURRET, loc)
                available_sp -= 4
                built_turrets.append(loc)  # Save for upgrading later

        # **2️⃣ Rebuild supports if destroyed at the same position**
        for loc in built_turrets:  # Supports go under the same turrets
            if available_sp < 2:
                break
            if not game_state.contains_stationary_unit(loc):  # If destroyed, rebuild
                game_state.attempt_spawn(SUPPORT, loc)
                available_sp -= 2
                built_supports.append(loc)  # Save for upgrading later

        # **3️⃣ Rebuild turrets if destroyed at the same position**
        for loc in built_turrets:
            if available_sp < 4:
                break
            if not game_state.contains_stationary_unit(loc):  # If destroyed, rebuild
                game_state.attempt_spawn(TURRET, loc)
                available_sp -= 4

        # **4️⃣ Upgrade turrets built in step 1**
        for loc in built_turrets:
            if available_sp < 6:
                break
            if game_state.contains_stationary_unit(loc):  
                game_state.attempt_upgrade(loc)
                available_sp -= 6

        # **5️⃣ Upgrade supports built in step 2**
        for loc in built_supports:
            if available_sp < 2:
                break
            if game_state.contains_stationary_unit(loc):
                game_state.attempt_upgrade(loc)
                available_sp -= 2

        # **6️⃣ Upgrade any remaining turrets and supports**
        for loc in built_turrets + built_supports:
            if available_sp < 2:
                break
            if game_state.contains_stationary_unit(loc):
                game_state.attempt_upgrade(loc)
                available_sp -= 6 if game_state.game_map[loc][0].unit_type == TURRET else 2

        # **7️⃣ If everything is upgraded, add new turrets and supports**
        all_upgraded = all(
            unit.upgraded for loc in built_turrets + built_supports for unit in game_state.game_map[loc]
        )

        if available_sp >= 8 and all_upgraded:
            extra_turrets = [[12, 11], [15, 11], [13, 10], [14, 10]]
            extra_supports = [[11, 7], [16, 7], [13, 6], [14, 6]]

            for loc in extra_turrets:
                if available_sp < 4:
                    break
                if game_state.can_spawn(TURRET, loc):
                    game_state.attempt_spawn(TURRET, loc)
                    available_sp -= 4

            for loc in extra_supports:
                if available_sp < 2:
                    break
                if game_state.can_spawn(SUPPORT, loc):
                    game_state.attempt_spawn(SUPPORT, loc)
                    available_sp -= 2
                if available_sp >= 2:
                    game_state.attempt_upgrade(loc)
                    available_sp -= 2

    def stall_with_interceptors(self, game_state):
        """
        Send out interceptors at random locations to defend our base from enemy moving units.
        """
        # We can spawn moving units on our edges so a list of all our edge locations
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        
        # Remove locations that are blocked by our own structures 
        # since we can't deploy units there.
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        
        # While we have remaining MP to spend lets send out interceptors randomly.
        while game_state.get_resource(MP) >= game_state.type_cost(INTERCEPTOR)[MP] and len(deploy_locations) > 0:
            # Choose a random deploy location.
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            
            game_state.attempt_spawn(INTERCEPTOR, deploy_location)
            """
            We don't have to remove the location since multiple mobile 
            units can occupy the same space.
            """

    def demolisher_line_strategy(self, game_state):
        """
        Build a line of the cheapest stationary unit so our demolisher can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [WALL, TURRET, SUPPORT]
        cheapest_unit = WALL
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost[game_state.MP] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[game_state.MP]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our demolisher from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        for x in range(27, 5, -1):
            game_state.attempt_spawn(cheapest_unit, [x, 11])

        # Now spawn demolishers next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        game_state.attempt_spawn(DEMOLISHER, [24, 10], 1000)

    def least_damage_spawn_location(self, game_state, location_options):
        """
        Determines the safest location to spawn mobile units by estimating damage along the path.
        """
        damages = []
        
        for location in location_options:
            path = game_state.find_path_to_edge(location)

            # ✅ FIX: Ensure path is valid before calculating damage
            if path is None:
                damages.append(float('inf'))  # Assign high damage to invalid paths
                continue  

            damage = 0
            for path_location in path:
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(TURRET, game_state.config).damage_i

            damages.append(damage)

        # ✅ FIX: Avoid crashing when all paths are invalid
        if all(d == float('inf') for d in damages):
            return None  # No valid paths exist, return None safely

        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x = None, valid_y = None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly, 
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
