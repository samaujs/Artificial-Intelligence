#######################################################################################################
# This file defines the maze environment and variables used for solving the MDP
# - discount gamma factor in Value Iteration and Policy Iteration algorithms
# - accepted maximum error to terminate Value Iteration
# - accepted maximum number of iterations for Policy Iteration
# Filename    : config.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
Constants and Parameters.
"""

# Defines a 2-D array maze
GRID = [
    ['g', 'w', 'g', ' ', ' ', 'g'],
    [' ', 'b', ' ', 'g', 'w', 'b'],
    [' ', ' ', 'b', ' ', 'g', ' '],
    [' ', ' ', ' ', 'b', ' ', 'g'],
    [' ', 'w', 'w', 'w', 'b', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ']
]

# Mapping of character symbols to rewards
REWARD_MAPPING = {
    ' ': -0.04,  # white square
    'g': 1.0,    # green square
    'b': -1.0,   # brown square
}

# Start agent at 4th row, 3rd column
STARTING_POINT = { 'row': 3, 'col': 2 }

# Discount, γ, for Bellman's equation
DISCOUNT_FACTOR = 0.99

# Subdirectory to store results
RESULTS_DIR_PATH = './results/'

# Type of MDP algorithms
MDP_ALGORITHM = {
    'VI': 1, # Value Iteration
    'PI': 2, # Policy Iteration
}
# For value iteration utilities to match reference utilities (approximately)
REFERENCE_DISCOUNT_FACTOR = 0.95
REFERENCE_MAX_ERROR = 1.4

# For Value Iteration :
# ε, the maximum error allowed in the utility of any state
MAX_ERROR = 78 # 10, 30, 79

# To get close to equilibrium, we can use the formula to compute the Maximum error, ε = c · Rmax
# Used to compute δ, the maximum change in the utility of any state in an iteration (|U′(s) − U(s)| < ε(1−γ)/γ)
c = 0.1
Rmax = 1
EPSILON = c * Rmax

# For Policy Iteration :
NUM_POLICY_EVALUATION = 4 # 25

# Mapping of MazeAction to unicode directions for visualisation
DIRECTION = {
    1 : '\u2191',  # MazeAction.MOVE_UP.value = 1 (↑ : \U+2191)
    2 : '\u2193',  # MazeAction.MOVE_DOWN.value = 2 (↓ : \U+2193)
    3 : '\u2190',  # MazeAction.MOVE_LEFT.value = 3 (← : \U+2190)
    4 : '\u2192',  # MazeAction.MOVE_RIGHT.value = 4 (→ : \U+2192)
}
