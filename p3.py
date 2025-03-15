import math
import numpy as np
from itertools import combinations, permutations
from copy import deepcopy
from utils import Map, Player_P3, STONE, GRASS, EMPTY, cost_of_resource_collecting

def algo_p3(missions, matrix, start_point, initial_h):
    """
    Optimized algorithm for Problem 3 (all missions are (2,1)).
    
    Inputs:
      - missions: List of missions (each mission is a tuple (2,1)).
                  (This parameter is not used further since all missions are assumed identical.)
      - matrix: A NumPy array representing the map.
      - start_point: Tuple (x, y) for the player's starting position.
      - initial_h: Initial health of the player.
    
    Output:
      - best_reward: The maximum number of missions (reward points) completed.
      
    Explanation:
      The algorithm repeatedly tries to complete a (2,1) mission. For each mission, it:
        1. Extracts the current resource list (both stones and grass) from the player's matrix.
        2. Uses exhaustive search (combinations and permutations) to select 3 resource points that meet
           the (2,1) requirement.
        3. Simulates the route on a copy of the player to compute its total cost.
        4. If a feasible route is found (i.e., cost <= player's current health), it executes that route on
           the real player (updating position, health, and marking collected resources as EMPTY).
        5. Increments the reward and resets bag counters.
      The process stops when no feasible route is found.
    """
    # Initialize Map and Player_P3 from the given matrix.
    game_map = Map(matrix)
    player = Player_P3(start_point, initial_h, matrix)
    
    # Helper: Extract resource points (only STONE and GRASS) from the current matrix.
    def extract_resource_list(mat):
        resources = []
        n = mat.shape[0]
        for i in range(n):
            for j in range(n):
                if mat[i, j] == STONE:
                    resources.append((i, j, STONE))
                elif mat[i, j] == GRASS:
                    resources.append((i, j, GRASS))
        return resources
    
    # Manhattan distance.
    def manhattan_distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
    
    # Simulate route execution on a copy of the player to compute the total cost.
    def simulate_route(order, player_obj):
        sim_player = deepcopy(player_obj)
        total_cost = 0
        actions = []
        for (rx, ry, rtype) in order:
            move_cost = manhattan_distance(sim_player.x, sim_player.y, rx, ry)
            collect_cost = cost_of_resource_collecting(rtype)
            if move_cost + collect_cost > sim_player.h:
                return (None, None)
            total_cost += (move_cost + collect_cost)
            sim_player.h -= (move_cost + collect_cost)
            # Update position using the property setters.
            sim_player.x, sim_player.y = rx, ry
            actions.append(("move", (rx, ry)))
            actions.append(("collect", (rx, ry), rtype))
        return (total_cost, actions)
    
    # Check if a combination of 3 resources meets the (2,1) requirement.
    def meets_requirement(combo):
        stone_count = sum(1 for (x, y, rtype) in combo if rtype == STONE)
        grass_count = sum(1 for (x, y, rtype) in combo if rtype == GRASS)
        return stone_count == 2 and grass_count == 1
    
    # Plan a single mission with requirement (2,1).
    def plan_single_mission(startX, startY, health, resource_list):
        best_cost = math.inf
        best_plan = None
        for combo in combinations(resource_list, 3):
            if not meets_requirement(combo):
                continue
            for order in permutations(combo):
                cost, actions = simulate_route(order, player)
                if cost is not None and cost < best_cost and cost <= health:
                    best_cost = cost
                    best_plan = actions
        return (best_plan, best_cost)
    
    best_reward = 0
    # Repeatedly try to complete a (2,1) mission.
    while True:
        current_resource_list = extract_resource_list(player.matrix)
        plan_actions, plan_cost = plan_single_mission(player.x, player.y, player.h, current_resource_list)
        if plan_actions is None or plan_cost > player.h:
            break  # No feasible mission can be completed.
        # Execute the plan on the real player.
        for act in plan_actions:
            if act[0] == "move":
                (tx, ty) = act[1]
                cost_move = manhattan_distance(player.x, player.y, tx, ty)
                if cost_move > player.h:
                    break
                player.h -= cost_move
                # Update position using the property setters.
                player.x, player.y = tx, ty
            elif act[0] == "collect":
                (tx, ty, rtype) = (act[1][0], act[1][1], act[2])
                ccost = cost_of_resource_collecting(rtype)
                if ccost > player.h:
                    break
                player.h -= ccost
                if player.matrix[tx][ty] != EMPTY:
                    player.matrix[tx][ty] = EMPTY
        best_reward += 1
        # Reset bag counters.
        player.num_stones = 0
        player.num_grass = 0
    return best_reward

from p1 import algo_brute_p1

def algo_brute_p3(matrix, start_point, initial_h):
    
    #return algo_brute_p1(matrix, start_point, initial_h, player_class=Player_P3)


