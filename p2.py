'''
Stone(cost health) and Apple(gain health)
'''

# from utils import Map, Player
# EMPTY = 0
# STONE = 1
# APPLE = 2
# GRASS = 3
#
# from p1 import algo_brute_p1
# def algo_brute_p2(matrix, start_point, initial_h):
#
#     return algo_brute_p1(matrix, start_point, initial_h)
#
# def algo_p2(matrix, start_point, initial_h):
#     """
#     algorithm to find the path with maximum sum of rewards.
#
#     :param matrix: A numpy array of shape (size, size) representing the map
#     :param start_point: A list [x, y] representing the starting point
#     :param initial_h: Initial health points
#     :return: the best reward
#     """
#     pass

from utils import Map, Player
import heapq

EMPTY = 0
STONE = 1
APPLE = 2
GRASS = 3


from p1 import algo_brute_p1
from itertools import permutations
def algo_brute_p2(matrix, start_point, initial_h):
    """
    Brute force algorithm to find the path with maximum sum of rewards.
    Supports both stones (STONE) and apples (APPLE).

    :param matrix: A numpy array of shape (size, size) representing the map
    :param start_point: A list [x, y] representing the starting point
    :param initial_h: Initial health points
    :return: the best reward
    """
    player = Player(start_point, initial_h, matrix)
    game_map = Map(matrix)

    # Combine stones and apples into a single list of resources
    resources = game_map.stones + game_map.apples

    best_reward = 0
    print("perm")
    # Generate all possible permutations of resources
    for perm in permutations(resources):

        player = Player(start_point, initial_h, deepcopy(matrix))
        for resource in perm:
            if player.able_to_go_and_collect(resource[0], resource[1]):
                player.go_and_collect_resource(resource[0], resource[1])
            else:
                break  # If unable to collect, stop this permutation
        if player.rewards > best_reward:
            best_reward = player.rewards

    return best_reward


import heapq
from copy import deepcopy


def heuristic(health, rewards, remaining_resources):
    return rewards + min(len(remaining_resources), health // 10)

def algo_p2(matrix, start_point, initial_h):
    game_map = Map(matrix)
    resources = game_map.stones + game_map.apples
    initial_state = (
    -heuristic(initial_h, 0, resources), 0, start_point[0], start_point[1], initial_h, 0, set())
    pq = []
    heapq.heappush(pq, initial_state)
    best_reward = 0
    visited = {}

    while pq:
        _, steps, x, y, health, reward, collected = heapq.heappop(pq)
        best_reward = max(best_reward, reward)
        state_key = (x, y, health, frozenset(collected))
        if state_key in visited and visited[state_key] >= reward:
            continue
        visited[state_key] = reward

        for rx, ry in resources:
            if (rx, ry) in collected:
                continue

            move_cost = abs(x - rx) + abs(y - ry)
            new_health = health - move_cost
            if new_health <= 0:
                continue

            new_reward = reward
            if matrix[rx][ry] == 'S':
                new_health -= 10
                new_reward += 1
            elif matrix[rx][ry] == 'A':
                new_health += 10
                new_reward += 1

            if new_health > 0:
                new_collected = collected | {(rx, ry)}
                heapq.heappush(pq, (
                -heuristic(new_health, new_reward, resources), steps + 1, rx, ry, new_health, new_reward,
                new_collected))

    return best_reward
