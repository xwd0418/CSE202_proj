from utils import Map, Player_P3
EMPTY = 0
STONE = 1
APPLE = 2
GRASS = 3
from p1 import algo_brute_p1

def algo_brute_p3(matrix, start_point, initial_h):
    
    return algo_brute_p1(matrix, start_point, initial_h, player_class=Player_P3)

def algo_p3(matrix, start_point, initial_h):
    pass