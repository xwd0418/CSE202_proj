'''
Mission is defined as follows:
[required_apple, required_stones, required_grass, rewards]

We also define a list of [total_apple, total_stones, total_grass] as what the player has collected so far

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
    # print("perms: ", perms)
    # print("player_resources: ", player_resources)
    
    selected_missions = []
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
            selected_missions = perm
        
    return best_reward, selected_missions


def algo_p4(mission_list, player_resources):
    """
    Find the subset of missions that maximizes reward points without exceeding available resources.
    
    Args:
        mission_list: List of tuples (apple_req, stone_req, grass_req, reward)
        player_resources: Tuple (apples, stones, grass) of available resources
    
    Returns:
        Tuple (max_reward, selected_missions) - maximum possible reward and list of selected mission indices
    """
    n = len(mission_list)
    if n == 0:
        return 0, []  # Early return for empty mission list
    
    missions = mission_list
    
    dp = [[[[-1 for _ in range(player_resources[2] + 1)] 
           for _ in range(player_resources[1] + 1)]
          for _ in range(player_resources[0] + 1)]
         for _ in range(n + 1)]
    
    choices = [[[[-1 for _ in range(player_resources[2] + 1)]
               for _ in range(player_resources[1] + 1)]
              for _ in range(player_resources[0] + 1)]
             for _ in range(n + 1)]
    
    def solve(i, a_left, s_left, g_left):
        # Base case: no more missions left or out of range
        if i >= n:
            return 0
        
        # DP memoization check
        if dp[i][a_left][s_left][g_left] != -1:
            return dp[i][a_left][s_left][g_left]
        
        a_req, s_req, g_req, reward = missions[i]
        
        # Option 1: Skip this mission
        skip_reward = solve(i + 1, a_left, s_left, g_left)
        
        # Option 2: Take this mission if enough resources are available
        take_reward = 0
        if a_left >= a_req and s_left >= s_req and g_left >= g_req:
            take_reward = reward + solve(i + 1, a_left - a_req, s_left - s_req, g_left - g_req)
        
        # Store the best decision in DP table and choices tracker
        if take_reward > skip_reward:
            dp[i][a_left][s_left][g_left] = take_reward
            choices[i][a_left][s_left][g_left] = 1
        else:
            dp[i][a_left][s_left][g_left] = skip_reward
            choices[i][a_left][s_left][g_left] = 0
        
        return dp[i][a_left][s_left][g_left]
    
    max_reward = solve(0, player_resources[0], player_resources[1], player_resources[2])
    
    # # Backtrack to find selected missions
    selected_missions = []
    i, a_left, s_left, g_left = 0, player_resources[0], player_resources[1], player_resources[2]
    
    while i < n:
        if choices[i][a_left][s_left][g_left] == 1:
            selected_missions.append(i)
            a_req, s_req, g_req, _ = missions[i]
            a_left -= a_req
            s_left -= s_req
            g_left -= g_req
        i += 1
    
    return max_reward, selected_missions