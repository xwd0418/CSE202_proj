'''Only Stone'''

from utils import Map, Player, Player_P3
EMPTY = 0
STONE = 1
APPLE = 2
GRASS = 3

from copy import deepcopy
from itertools import permutations

def algo_brute_p1(matrix, start_point, initial_h, player_class=Player):
    """
    Brute force algorithm to find the path with maximum sum of rewards.
    
    :param matrix: A numpy array of shape (size, size) representing the map
    :param start_point: A list [x, y] representing the starting point
    :param initial_h: Initial health points
    :return: the best reward
    """
    game_map = Map(matrix)
    perms = (permutations(game_map.stones))
    # print("len stones", len(game_map.stones))
    best_reward = 0
    for perm in perms:
        # print("new perm")
        # best_reward = 1
        player = player_class(start_point, initial_h, deepcopy(matrix))
        for stone in perm:
            if player.able_to_go_and_collect(stone[0], stone[1]):
                player.go_and_collect_resource(stone[0], stone[1])
            else:
                break
        if player.rewards > best_reward:
            best_reward = player.rewards
            # best_path = perm
    return best_reward

def algo_p1(matrix, start_point, initial_h):
    """
    Our algorithm to find the path with maximum sum of rewards.
    
    :param matrix: A numpy array of shape (size, size) representing the map
    :param start_point: A list [x, y] representing the starting point
    :param initial_h: Initial health points
    :return: the best reward
    """
    # time.sleep(matrix.size * 1)  # Simulate a long running algorithm
    return
    

