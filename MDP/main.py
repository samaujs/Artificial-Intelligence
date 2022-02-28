#######################################################################################################
# This file defines the main method for solving the Markov Decision Process (MDP)
# - Calls the respective algorithms and save the results
# Filename    : main.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
Main method
"""

# Import common libraries
import os
import pprint
import copy
import random

import matplotlib.pyplot as plt

# Import the dependency files
from algorithms import value_iteration, policy_iteration
from config import *
from grid import generate_maze
from maze import Maze, MazeAction
from plot import plot_utility_vs_iteration


def solve_MDP(grid: list, algo: int, num_policy_evaluation: int = 1):
    """
    Calls the "Value Iteration" and "Policy Iteration" algorithms and saves the results
    """

    if (algo == 1):
        print()
        print("MDP : Value Iteration")
        print("---------------------")
        maze = Maze(
            grid=grid,
            reward_mapping=REWARD_MAPPING,
            starting_point=STARTING_POINT,
            discount_gamma=DISCOUNT_FACTOR
        )
        result = value_iteration(maze, max_error=MAX_ERROR)

        _show_maze_result(maze, result, 'value_iteration_result.txt')

        plot_utility_vs_iteration(
            result['iteration_utilities'],
            save_file_name='value_iteration_utilities.png'
        )
    elif (algo == 2):
        print("MDP : Policy Iteration")
        print("----------------------")
        maze = Maze(
            grid=grid,
            reward_mapping=REWARD_MAPPING,
            starting_point=STARTING_POINT,
            discount_gamma=DISCOUNT_FACTOR
        )
        result = policy_iteration(maze, num_policy_evaluation)  # num_policy_evaluation=25

        _show_maze_result(maze, result, 'policy_iteration_result.txt')

        plot_utility_vs_iteration(
            result['iteration_utilities'],
            save_file_name='policy_iteration_utilities.png'
        )
    else:
        print("Supported MDP algorithm option is only 1 or 2")

def _show_maze_result(maze, result, save_file_name=None):
    """
    params:
    - maze (Maze)
    - result (dict): result of solving a maze
    - save_file_name (str): name of file to save plot as; defaults to None (not saved)
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
        with open(RESULTS_DIR_PATH + save_file_name, 'w') as file:
            for line in lines:
                file.write(line + '\n')
            # print(optimal_policy_grid, file)


# Main Program
if __name__ == '__main__':
    # Make sure directory exist for saving results
    os.makedirs(RESULTS_DIR_PATH, exist_ok=True)

    print("--- Solving MDP with the following maze ---")
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(GRID)

    # Solve MDP with Value Iteration
    solve_MDP(GRID, MDP_ALGORITHM['VI'])

    # # Solve MDP with Policy Iteration (Original)
    solve_MDP(GRID, MDP_ALGORITHM['PI'], num_policy_evaluation=1)
