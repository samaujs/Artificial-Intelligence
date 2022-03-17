#######################################################################################################
# This file defines the maze environment and variables used for solving the MDP
# - discount gamma factor in Value Iteration and Policy Iteration algorithms
# - maximum permitted error to terminate Value Iteration
# - number of Policy Evaluations for Modified Policy Iteration
# Filename    : config.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
Defines the constant values required for the MDP problem.
"""

# Pre-defines a 2-D array maze
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
    ' ': -0.04,  # white cells
    'g': 1.0,    # green cells
    'b': -1.0,   # brown cells
}

# Mapping of MazeAction to unicode directions for visualisation
DIRECTION = {
    1 : '\u2191',  # MazeAction.MOVE_UP.value = 1 (↑ : \U+2191)
    2 : '\u2193',  # MazeAction.MOVE_DOWN.value = 2 (↓ : \U+2193)
    3 : '\u2190',  # MazeAction.MOVE_LEFT.value = 3 (← : \U+2190)
    4 : '\u2192',  # MazeAction.MOVE_RIGHT.value = 4 (→ : \U+2192)
}

# Start agent at 4th row, 3rd column
STARTING_POINT = { 'row': 3, 'col': 2 }

# Type of MDP algorithms
MDP_ALGORITHM = {
    'VI': 1, # Value Iteration
    'PI': 2, # Policy Iteration
}

# Discount factor for future state in Bellman's equation, γ
DISCOUNT_FACTOR = 0.99

# For Value Iteration :
# Maximum error allowed in the utility of any state, ε
MAX_ERROR = 78 # 10, C1:80, C2:77, C3:25

# To get close to equilibrium, we can use the formula to compute the Maximum error, ε = c · Rmax
# Used to compute δ, the maximum change in the utility of any state in an iteration (|U′(s) − U(s)| < ε(1−γ)/γ)
c = 0.1
Rmax = 1
EPSILON = c * Rmax

# For Policy Iteration :
# Number of Policy Evaluation for Policy Iteration, k :
NUM_POLICY_EVALUATION = 4 # C1:2, C2:4, C3:3

# Subdirectory to store results
RESULTS_DIR_PATH = './results/'

# Parameters for maze creation
MAZE_MAPPING = {
    'NUM_G_STATES': 6,  # green cells
    'NUM_B_STATES': 5,  # brown cells
    'NUM_W_STATES': 5,  # wall cells
    'MAZE_WIDTH':  6     # width of the squared maze
}
