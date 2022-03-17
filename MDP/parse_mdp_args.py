#######################################################################################################
# This file defines the method to parse the command line parameter for solving the MDP
# - Defines the parameters to be parsed and initialised with the respective default values
# Filename    : parse_mdp_args.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
Parsing the parameters from the command line with following formats and examples :

python3 main.py --algo=<ALGO> --discount_gamma=<DISCOUNT_GAMMA>
                --max_error=<MAX_ERROR> --num_pe=<NUM_PE>
                --save_filename_prefix=<SAVE_FILENAME_PREFIX> --datadir=<DATADIR>
                --gen_maze
                --num_g_states <NUM_G_STATES> —num_b_states <NUM_B_STATES>
                --num_w_states <NUM_W_STATES> --maze_width <MAZE_WIDTH>

Implements method :
- arg_parse
"""

import argparse

from config import *


# Set training parameters
def arg_parse():
    print("Attempt to parse arguments...")
    parser = argparse.ArgumentParser(description='Assignment 1 : Agent Decision Making project arguments.')

    # Add parsing arguments for Value Iteration and Policy Iteration
    parser.add_argument('--algo', dest='algo', type=int,
                        help='1: Value Iteration; 2: Policy Iteration.')
    parser.add_argument('--discount_gamma', dest='discount_gamma', type=float,
                        help='Discount factor for future state.')
    parser.add_argument('--max_error', dest='max_error', type=float,
                        help='Maximum error allowed in the utility of any state.')
    parser.add_argument('--num_pe', dest='num_pe', type=int,
                        help='Number of Policy Evaluation for Policy Iteration.')
    parser.add_argument('--save_filename_prefix', dest='save_filename_prefix', type=str,
                        help='Prefix for filename to be saved.')
    parser.add_argument('--datadir', dest='datadir', type=str,
                        help='Directory where results are stored.')

    # Add parsing arguments for generating maze with parameters
    # For constant, no value assignment is required for "--gen_maze", just check if exist in command line parameter
    parser.add_argument('--gen_maze', dest='gen_maze', action='store_const',
                        const=True, default=False, help='Whether to generate a maze.')

    parser.add_argument('--num_g_states', dest='num_g_states', type=int,
                        help='The number of green cells to be created.')
    parser.add_argument('--num_b_states', dest='num_b_states', type=int,
                        help='The number of brown cells to be created.')
    parser.add_argument('--num_w_states', dest='num_w_states', type=int,
                        help='The number of wall cells to be created.')
    parser.add_argument('--maze_width', dest='maze_width', type=int,
                        help='The width of the squared maze to be created.')

    # Set defaults for all program parameters unless provided by user
    parser.set_defaults(algo=MDP_ALGORITHM['VI'],                   # Value Iteration algorithm
                        discount_gamma=DISCOUNT_FACTOR,             # Discount factor for future state in Bellman's equation, γ
                        max_error=MAX_ERROR,                        # Maximum error allowed in the utility of any state, ε
                        num_pe=NUM_POLICY_EVALUATION,               # Number of Policy Evaluation for Policy Iteration, k
                        save_filename_prefix="value_iteration",     # Prefix for filename to be saved
                        datadir=RESULTS_DIR_PATH,                   # Directory where results are stored (io_parser)

                        num_g_states=MAZE_MAPPING['NUM_G_STATES'],  # Number of green cells to be created
                        num_b_states=MAZE_MAPPING['NUM_B_STATES'],  # Number of brown cells to be created
                        num_w_states=MAZE_MAPPING['NUM_W_STATES'],  # Number of wall cells to be created
                        maze_width=MAZE_MAPPING['MAZE_WIDTH'])      # Width of the squared maze to be created

    return parser.parse_args()
