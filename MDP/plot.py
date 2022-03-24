#######################################################################################################
# This file defines the method for plotting the results
# - Plot utility vs Number of Iterations
# Filename    : plot.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
To plot utility against iterations and save the plot in a specified sub-directory with filename.

Implements method :
- plot_utility_vs_iteration
"""

import matplotlib.pyplot as plt


def plot_utility_vs_iteration(iteration_utilities, save_file_name=None):
    """
    params:
    - iteration_utilities: {
        (row, col): [utility for each iteration (float)]
    }
    - save_file_name (str): file name with directory path to save plot; default is None (which is not saved)
    """
    plt.figure(figsize=(16, 8))

    for state_position in iteration_utilities:
        plt.plot(iteration_utilities[state_position])

    plt.legend(iteration_utilities, loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title('Estimated utility of each state in each iteration')
    plt.xlabel('Number of iterations')
    plt.ylabel('Utility estimates')

    if save_file_name is not None:
        plt.savefig(save_file_name)

    plt.show()
