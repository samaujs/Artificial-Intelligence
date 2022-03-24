#######################################################################################################
# This file defines the main method for solving the Markov Decision Process (MDP)
# - Calls the respective algorithms and save the results
# Filename    : main.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
Implements the main method to call the methods for solving the MDP, print and save the maze results.

Implements methods :
- solve_MDP
- _show_maze_result
"""

# Import common libraries
import os
import pprint
import copy

# Import the dependency files
from algorithms import value_iteration, policy_iteration
from config import *
from generate_maze import random_maze
from maze import Maze
from plot import plot_utility_vs_iteration

# Parsing input parameters
import parse_mdp_args

# Global pretty print setup with indentation
pp = pprint.PrettyPrinter(indent=2)


def solve_MDP(grid: list, algo: int, discount_gamma: float = 1.0,
              max_error: float = 1.0, num_policy_evaluation: int = 1,
              save_filename_prefix=None):
    """
    params:
    - grid (list): maze environment
    - algo (int): Value Iteration (1) and Policy Iteration (2)
    - discount_gamma (float): discount factor for future state
    - max_error (float): maximum error allowed in the utility of any state
    - num_policy_evaluation (int): number of times to do policy evaluation (k) to obtain
                                   better estimates for the utilities, U_i+1(s) with default value of 1

    Calls the "Value Iteration" and "Policy Iteration" methods and saves the results
    """

    # Initialise the MDP, maze environment
    maze = Maze(
        grid=grid,
        reward_mapping=REWARD_MAPPING,
        starting_point=STARTING_POINT,
        discount_gamma=discount_gamma
    )

    # δ, the maximum change in the utility of any state in an iteration
    delta = "%.3f" % (max_error * (1 - discount_gamma) / discount_gamma)

    if algo == MDP_ALGORITHM['VI']:
        print("MDP : Value Iteration (ε={}, δ={})".format(max_error, delta))
        print("---------------------------------------")

        result = value_iteration(maze, max_error=max_error)

        # 'value_iteration_result_(δ={}).txt'.format(delta)
        _show_maze_result(maze, result, save_filename_prefix + '_result_(δ={}).txt'.format(delta))

        # 'value_iteration_plot_(δ={}).png'.format(delta)
        plot_utility_vs_iteration(
            result['iteration_utilities'],
            save_file_name=save_filename_prefix + '_plot_(δ={}).png'.format(delta)
        )
    elif algo == MDP_ALGORITHM['PI']:
        print("MDP : Policy Iteration")
        print("----------------------")

        result = policy_iteration(maze, num_policy_evaluation)

        # 'policy_iteration_result_(npe={}).txt'.format(num_policy_evaluation)
        _show_maze_result(maze, result, save_filename_prefix + '_result_(npe={}).txt'.format(num_policy_evaluation))

        # 'policy_iteration_plot_(npe={}).png'.format(num_policy_evaluation)
        plot_utility_vs_iteration(
            result['iteration_utilities'],
            save_file_name=save_filename_prefix + '_plot_(npe={}).png'.format(num_policy_evaluation)
        )
    else:
        print("Supported MDP algorithm option is only 1 or 2")


def _show_maze_result(maze, result, save_file_name=None):
    """
    params:
    - maze (Maze)
    - result (dict): result of solving a maze
    - save_file_name (str): file name with directory path to save information; default is None (which is not saved)
    """
    lines = []

    line = '\nTotal number of iterations : ' + str(result['num_iterations'])
    print(line)
    lines.append(line)

    utilities, optimal_policy = result['utilities'], result['optimal_policy']

    # Deep copy constructs a new compound object and recursively inserts copies of the objects from
    # the original into it.  This retains the original maze and use only the copy for updates.
    optimal_utility_grid = copy.deepcopy(maze.grid)
    optimal_policy_grid = copy.deepcopy(maze.grid)

    line = '--- (row, column) : Utility for each state with best action  ---'
    print(line)
    lines.append(line)

    for state_position in maze.states:
        if state_position[1] == 0:
            print()
            lines.append(' ')

        # Keep ending zero after rounding : "%.2f" % round(utilities[state_position], 2) but it becomes a string
        optimal_utility_grid[state_position[0]][state_position[1]] = round(utilities[state_position], 2)

        action = optimal_policy[state_position]
        action_symbol = DIRECTION[action.value]
        optimal_policy_grid[state_position[0]][state_position[1]] = action_symbol

        line = str(state_position) + ' - utility: {:.2f}; action: {}'.format(utilities[state_position], action_symbol)
        print(line)
        lines.append(line)

    print('\n--- Optimal utility grid (w = wall) ---')
    pp.pprint(optimal_utility_grid)
    print()
    print('--- Optimal policy grid (w = wall) ---')
    pp.pprint(optimal_policy_grid)
    print()

    if save_file_name is not None:
        # RESULTS_DIR_PATH subdirectory ('./results') has been created
        with open(save_file_name, 'w') as file:
            for line in lines:
                file.write(line + '\n')
            # print(optimal_policy_grid, file)


# Start of Program from command line
def main():
    # Parsing defaults for all program parameters unless provided by user
    prog_args = parse_mdp_args.arg_parse()

    # Make sure directory exist for saving results
    os.makedirs(prog_args.datadir, exist_ok=True)

    # Use the pre-defined maze environment (GRID, GRID_C1, GRID_C2, GRID_C3)
    generated_maze = GRID  # default

    # Check if --gen_maze exists in the command line parameter
    if prog_args.gen_maze:
        print()
        print("Generate maze with parameters :")
        print("---------------------------------------")
        print('g : {}, b : {}, w : {}, maze_width : {}'.format(prog_args.num_g_states,
                                                               prog_args.num_b_states,
                                                               prog_args.num_w_states,
                                                               prog_args.maze_width))
        print()

        # Generate maze environment
        generated_maze = random_maze(num_g_states=prog_args.num_g_states,
                                     num_b_states=prog_args.num_b_states,
                                     num_w_states=prog_args.num_w_states,
                                     maze_width=prog_args.maze_width)

    print()
    print('γ : {}, ε : {}, k : {}, fn_prefix : {}, datadir : {}'.format(prog_args.discount_gamma,
                                                                        prog_args.max_error,
                                                                        prog_args.num_pe,
                                                                        prog_args.save_filename_prefix,
                                                                        prog_args.datadir))

    if prog_args.algo == MDP_ALGORITHM['VI']:
        # Solve MDP with Value Iteration (ε, set max_error=0.1)
        solve_MDP(grid=generated_maze, algo=MDP_ALGORITHM['VI'], discount_gamma=prog_args.discount_gamma,
                  max_error=prog_args.max_error,
                  save_filename_prefix='./' + prog_args.datadir + '/' + prog_args.save_filename_prefix)

    elif prog_args.algo == MDP_ALGORITHM['PI']:
        # Solve MDP with Policy Iteration (Standard, set num_pe=1)
        solve_MDP(grid=generated_maze, algo=MDP_ALGORITHM['PI'], discount_gamma=prog_args.discount_gamma,
                  num_policy_evaluation=prog_args.num_pe,
                  save_filename_prefix='./' + prog_args.datadir + '/' + prog_args.save_filename_prefix)

    else:
          print("Supported MDP algorithm option is only; 1: Value Iteration or 2: Policy Iteration")

    print("\n--- Solving MDP with the following maze ---")
    pp.pprint(generated_maze)
    print()


# Main Program
if __name__ == "__main__":
    main()

