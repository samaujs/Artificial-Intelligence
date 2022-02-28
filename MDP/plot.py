#######################################################################################################
# This file defines the method for plotting the results
# - Plot utility vs Number of Iterations
# Filename    : plot.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
Method for plotting the results
"""
import matplotlib.pyplot as plt

from config import RESULTS_DIR_PATH


def plot_utility_vs_iteration(iteration_utilities, save_file_name=None):
    """
    params:
    - iteration_utilities: {
        (row, col): [utility for each iteration (float)]
    }
    - save_file_name (str): name of file to save plot as; defaults to None (not saved)
    """
    plt.figure(figsize=(16, 8))

    for state_position in iteration_utilities:
        plt.plot(iteration_utilities[state_position])

    plt.legend(iteration_utilities, loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title('Estimated utility of each state in each iteration')
    plt.xlabel('Number of iterations')
    plt.ylabel('Utility estimates')

    if save_file_name is not None:
        plt.savefig(RESULTS_DIR_PATH + '/' + save_file_name)

    plt.show()
