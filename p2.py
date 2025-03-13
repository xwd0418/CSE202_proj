'''
Stone(cost health) and Apple(gain health)
'''

from utils import Map, Player
EMPTY = 0
STONE = 1
APPLE = 2
GRASS = 3

from p1 import algo_brute_p1
def algo_brute_p2(matrix, start_point, initial_h):
    
    return algo_brute_p1(matrix, start_point, initial_h)

def algo_p2(matrix, start_point, initial_h):
    """
    algorithm to find the path with maximum sum of rewards.
    
    :param matrix: A numpy array of shape (size, size) representing the map
    :param start_point: A list [x, y] representing the starting point
    :param initial_h: Initial health points
    :return: the best reward
    """
    pass