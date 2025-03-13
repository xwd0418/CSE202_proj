'''
Mission is defined as follows:
[required_apple, required_stones, required_grass, rewards]

WE also define a list of [total_apple, total_stones, total_grass] as what the player has collected so far

'''
# define the function as you like... i will add the brute force function later 
from itertools import permutations

def do_mission(mission, player_resources):
    """
    mission: list of required resources and rewards
    player_resources: list of player resources
    """
    if player_resources[0] < mission[0] or player_resources[1] < mission[1] or player_resources[2] < mission[2]:
        return None
    else:
        player_resources[0] -= mission[0]
        player_resources[1] -= mission[1]
        player_resources[2] -= mission[2]
        return mission[3]

def brute_force_p4(misson_list, player_resources):
    """
    misson_list: 2D list of missions
    player_resources: list of player resources
    """
    perms = permutations(misson_list)
    best_reward = 0
    for perm in perms:
        curr_rewards = 0
        curr_resources = player_resources.copy()
        for mission in perm:
            rewards_get = do_mission(mission, curr_resources)
            if rewards_get == None: # no doable mission
                break
            else:
                curr_rewards += rewards_get
        if curr_rewards > best_reward:
            best_reward = curr_rewards
    return best_reward

def algo_p4(misson_list, player_resources):
    """
    misson_list: 2D list of missions
    player_resources: list of player resources
    """
    pass