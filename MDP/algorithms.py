#######################################################################################################
# This file implements Reinforcement Learning algorithms to solve the Markov Decision Process (MDP)
# - Bellman's Equation U′(s) ← R(s) + γ max a∈A(s) ∑s′ P(s′|s,a) U(s′)
# - Value Iteration (Bellman Equation, Maximum Expected Utility)
# - Policy Iteration (Policy Evaluation, Policy Improvement)
#
# Reference   : Chapters 16 & 17 “Artificial Intelligence: A Modern Approach” by S. Russell and
#               P. Norvig. Prentice-Hall, third edition, 2010
#
# Filename    : algorithms.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
Implements methods :
- value_iteration
- policy_iteration

Internal methods
- _bellman_equation
- _policy_evaluation
- _policy_improvement
- _get_expected_utility
"""

from mdp import MarkovDecisionProcess
from maze import MazeAction


# Reference: Figure 17.4 of “Artificial Intelligence: A Modern Approach”
# MarkovDecisionProcess implements transition_model, reward_function and get_next_states
# Value Iteration algorithm
def value_iteration(mdp: MarkovDecisionProcess, max_error=1, verbose: bool=False):
    """
    params:
    - mdp (MarkovDecisionProcess): an MDP with 
        - possible states, S
        - possible actions, A(s)
        - transition model, P(s′|s, a)
        - reward for state, R(s)
        - discount factor, γ
    - max_error (float): the maximum error, ε, allowed in the utility of any state
    - verbose (bool): True to print debugging information

    return:
    {
        'utilities': {
            (row, col): utility value (float)
        },
        'optimal_policy': {
            (row, col): best action to take at this state (MazeAction)
        },
        'num_iterations': num_iterations (int),
        'iteration_utilities': {
            (row, col): [utility for each iteration (float)]
        }
    }
    """
    # U, U′, vectors of utilities for states in S, are initially zero
    current_utilities, new_utilities, optimal_policy = {}, {}, {}

    # Use for plotting the Utility estimates as a function of the number of iterations
    # Reference: Figure 17.5 of “Artificial Intelligence: A Modern Approach”
    iteration_utilities = {}

    # For all states in S, initialise U and U′ vectors of utilities to zero
    # For all states, initialise actions to None
    for state_position in mdp.states:
        current_utilities[state_position] = 0
        new_utilities[state_position] = 0
        optimal_policy[state_position] = None

        # start with empty list since it is updated at start of iteration
        iteration_utilities[state_position] = []

    converged = False
    num_iterations = 0

    while not converged:
        for state_position in mdp.states:
            # For all states in S, perform U ← U′
            current_utilities[state_position] = new_utilities[state_position]
            iteration_utilities[state_position].append(current_utilities[state_position])

        max_utility_change = 0  # δ ← 0

        # for each state s in S do 
        for state_position in mdp.states:
            # U′[s] ← R(s) + γ max a∈A(s) ∑s′ P(s′|s, a)U[s′]
            new_utility, new_action = _bellman_equation(mdp,
                                                        state_position,
                                                        current_utilities)

            new_utilities[state_position] = new_utility
            optimal_policy[state_position] = new_action

            # if |U′[s]−U[s]| > δ then δ ← |U′[s]−U[s]|
            abs_utility_difference = abs(new_utilities[state_position] - current_utilities[state_position])

            if abs_utility_difference > max_utility_change:
                max_utility_change = abs_utility_difference

        num_iterations += 1

        if verbose:
            print(
                'iteration:', num_iterations,
                ' with maximum change in the utility of any state:',
                '{:.4f}'.format(max_utility_change),
            )

        # Repeat until δ < ϵ(1−γ)/γ
        converged = max_utility_change < (max_error * (1 - mdp.discount) / mdp.discount)

    # Actual algorithm returns U vector utilities
    #
    # Adaptation :
    # Besides U, the optimal policy, number of iterations and iteration utilities are returned for plotting
    return {
        'utilities': current_utilities,
        'optimal_policy': optimal_policy,
        'num_iterations': num_iterations,
        'iteration_utilities': iteration_utilities,
    }


def _bellman_equation(mdp: MarkovDecisionProcess, state_position: tuple, current_utilities: dict):
    """
    Implementation of U′[s] ← R(s) + γ max a∈A(s) ∑s′P(s′|s, a)U[s′]

    params:
    - mdp (MarkovDecisionProcess): the defined MDP task with initialised data structure
    - state_position (tuple): row, col
    - current_utilities (dict): maps any (row, col) state to its current utility value

    return:
    (
        updated utility value of the provided state (float),
        best action to take at the provided state (MazeAction)
    )
    """
    # Initialise with an infinitely large negative Maximum Expected Utility value and None best action
    max_expected_utility = float('-inf')
    best_action = None

    state_with_action = mdp.states[state_position]

    # MazeAction.MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT
    for action in state_with_action:
        # get the expected utility of each available actions
        expected_utility = _get_expected_utility(mdp,
                                                 state_position,
                                                 action,
                                                 current_utilities)

        # Get the maximum Expected Utility with the best action for the state
        if expected_utility > max_expected_utility:
            max_expected_utility = expected_utility
            best_action = action

    # returns computed U′[s] with 2 parts, Reward and discounted Max Expected Utility
    return (mdp.reward_function(state_position) + mdp.discount * max_expected_utility,
            best_action)


def _get_expected_utility(mdp: MarkovDecisionProcess,
                          state_position: tuple,
                          action: MazeAction,
                          current_utilities: dict
                          ) -> float:
    """
    Implementation of ∑s′ P(s′|s, a)U[s′]

    params:
    - mdp (MarkovDecisionProcess): the defined MDP task with initialised data structure
    - state_position (tuple): row, col
    - action (MazeAction): action to take at the provided state
    - current_utilities:
    {
        (row, col): current utility value of state (float)
    }

    return:
    Expected Utility value of the provided state (float)
    """
    expected_utility = 0

    # <MazeAction.MOVE_DOWN: 2>:
    #  {(4, 2): {'actual': (4, 2), 'probability': 0.1},
    #   (4, 4): {'actual': (4, 4), 'probability': 0.1},
    #   (5, 3): {'actual': (5, 3), 'probability': 0.8}}
    possible_next_states = mdp.get_next_states(state_position, action)

    for intended_next_state_position in possible_next_states:
        probability = mdp.transition_model(state_position,
                                           action,
                                           intended_next_state_position)

        # actual state used to calculate utility, adjusted for invalid state (out of grid or going into wall)
        actual_next_state_position = possible_next_states[intended_next_state_position]['actual']

        # obtain next state utility from current utilities of all possible states
        next_state_utility = current_utilities[actual_next_state_position]

        # ∑s′ P(s′|s, a)U[s′] with action, a
        expected_utility += probability * next_state_utility

    return expected_utility


# Reference: Figure 17.7 of “Artificial Intelligence: A Modern Approach”
# MarkovDecisionProcess implements transition_model, reward_function and get_next_states
# Policy Iteration algorithm
def policy_iteration(mdp: MarkovDecisionProcess, num_policy_evaluation: int = 1, verbose: bool = False):
    """
    params:
    - mdp (MarkovDecisionProcess): an MDP with
        - possible states, S
        - possible actions, A(s)
        - transition model, P(s′|s, a)
        - reward for state, R(s)
        - discount factor, γ
    - num_policy_evaluation (int): number of times to do policy evaluation (k) to obtain
                                   better estimates for the utilities, U_i+1(s) with default value of 1
    - verbose (bool): True to print debugging information

    return:
    {
        'utilities': {
            (row, col): utility value (float)
        },
        'optimal_policy': {
            (row, col): best action to take at this state (MazeAction)
        },
        'num_iterations': num_iterations (int),
        'iteration_utilities': {
            (row, col): [utility for each iteration (float)]
        }
    }
    """
    # U, vector of utilities for all states in S
    # π, policy vector for all states in S
    utilities, policy = {}, {}

    # Use for plotting the Utility estimates as a function of the number of iterations
    # Reference: Figure 17.5 of “Artificial Intelligence: A Modern Approach”
    iteration_utilities = {}

    # For all states in S, initialise U, a vector of utilities to zero
    # For all states, initialise π, a policy vector of a state, initially "Move Up" (or random)
    for state_position in mdp.states:
        utilities[state_position] = 0
        policy[state_position] = MazeAction.MOVE_UP

        # ** could start with iteration_utilities[state_position] = [] **
        # start with first utility in place since it is updated at end of iteration
        iteration_utilities[state_position] = [0]

    # Keep track if policy for all states in S become unchanged after Policy Improvement
    unchanged = False
    num_iterations = 0

    while not unchanged:
        # U ← POLICY-EVALUATION (π, U, mdp)
        # U_i+1(s) ← R(s) + γ ∑s′ P(s'|s, π_i(s)) U_i(s')
        utilities, new_iteration_utilities = _policy_evaluation(mdp,
                                                                policy,
                                                                utilities,
                                                                num_policy_evaluation)

        # POLICY-IMPROVEMENT : π′(s) ← max a∈A(s) ∑s′ P(s′|s, a) Uπ(s′)
        policy, unchanged = _policy_improvement(mdp, policy, utilities)

        num_iterations += num_policy_evaluation
        print('unchanged:', unchanged, 'at iteration:', num_iterations)

        if verbose:
            print('iteration:', num_iterations)

        for state_position in mdp.states:
            # extends list by appending elements from the iterable (ie. each element of the iterable gets appended onto the list)
            iteration_utilities[state_position].extend(new_iteration_utilities[state_position])

            if verbose:
                print('at', state_position, '-best action:', policy[state_position])

        # Repeat until policy for all states in S become unchanged

    # Actual algorithm returns the optimal policy π
    #
    # Adaptation :
    # Besides the optimal policy π, current utilities, number of iterations and iteration utilities are returned for plotting
    return {
        'utilities': utilities,
        'optimal_policy': policy,
        'num_iterations': num_iterations,
        'iteration_utilities': iteration_utilities,
    }

# Step 1 of Policy Iteration algorithm : Policy Evaluation
def _policy_evaluation(mdp: MarkovDecisionProcess,
                       policy: dict,
                       utilities: dict,
                       num_policy_evaluation: int):
    """
    Simplified version of Bellman equation with fixed policy or action for a number of iterations

    params:
    - mdp (MarkovDecisionProcess): an MDP with 
        - possible states, S
        - possible actions, A(s)
        - transition model, P(s′|s, a)
        - reward for state, R(s)
        - discount factor, γ
    - policy: {
        (row, col): best action to take at this state (MazeAction)
    }
    - utilities: {
        (row, col): utility value (float)
    }
    - num_policy_evaluation (int): number of times to do policy evaluation (k) to obtain
                                   better estimates for the utilities, U_i+1(s) with default value of 1

    return:
    (
        { (row, col): updated current utility value (float) },
        { (row, col: [utility for each value iteration (float)] }
    )
    """
    current_utilities, updated_utilities = {}, {}
    new_iteration_utilities = {}

    # For all states in S, initialise U vectors of utilities to current values of utilities
    for state_position in mdp.states:
        # U_i ← U
        current_utilities[state_position] = utilities[state_position]
        new_iteration_utilities[state_position] = []


    # Iterate to get state utilities for specified "num_policy_evaluation" of rounds (ie. k times)
    # Modified Policy Iteration
    # - U_i+1(s) ← R(s) + γ ∑s′ P(s'|s, π_i(s)) U_i(s'), repeat k times to produce the next utility estimate
    # - k number of simplified value iteration steps (with fixed policy, π_i)
    # - these utility estimates give reasonably good approximation of the utilities.
    # - π_i+1(s) ← max a∈A(s) ∑s′ P(s′|s, a) U_i+k_π_i(s′)
    for eval_num in range(num_policy_evaluation):

        # print("\nWithin Policy Evaluation iteration no. :", eval_num + 1)
        # for each state s in S do
        for state_position in mdp.states:
            # Get the reward for each state
            reward = mdp.reward_function(state_position)

            # ∑s′P (s'|s, π_i(s)) Uπ_i(s')
            expected_utility = _get_expected_utility(mdp,
                                                     state_position,
                                                     policy[state_position], # action to be taken
                                                     current_utilities)

            # U_i+1(s) ← R(s) + γ ∑s′ P(s'|s, π_i(s)) U_i(s')
            updated_utilities[state_position] = reward + mdp.discount * expected_utility

        # In Policy Evaluation, adapt to use Policy Iteration to improve estimated state utilities that are
        # used in Policy Improvement
        # Only updates the current utilities after getting Expected Utility for each state so that the neighbouring
        # utilities are not changed prematurely in the computation for next round
        # U_i ← U_i+1
        for state_position in mdp.states:
            current_utilities[state_position] = updated_utilities[state_position]
            new_iteration_utilities[state_position].append(current_utilities[state_position])

            # if (((eval_num + 1) % 2) == 0):
            #     print("state : {}; new_iteration_utilities : {}".format(state_position,
            #                                                             new_iteration_utilities[state_position]))

    # return the better estimated utilities after "num_policy_evaluation" rounds of iteration
    return current_utilities, new_iteration_utilities


# Step 2 of Policy Iteration algorithm : Policy Improvement
def _policy_improvement(mdp,
                        policy,
                        utilities):
    """
    params:
    - mdp (MarkovDecisionProcess): an MDP with
        - possible states, S
        - possible actions, A(s)
        - transition model, P(s′|s, a)
        - reward for state, R(s)
        - discount factor, γ
    - policy: {
        (row, col): best action to take at this state (MazeAction)
    }
    - utilities: {
        (row, col): utility value (float)
    }

    return:
    (
        updated_policy (dict),
        unchanged (bool),
    )
    """
    updated_policy = {}
    unchanged = True  # unchanged? ← true

    # for each state s in S do
    for state_position in mdp.states:
        # get max a∈A(s) ∑s′ P(s'|s, a) U(s')
        max_expected_utility = float('-inf')
        best_action = None

        state_with_action = mdp.states[state_position]

        for action in state_with_action:
            # ∑s′P (s'|s, π_i(s)) Uπ_i(s')
            expected_utility = _get_expected_utility(mdp,
                                                     state_position,
                                                     action,
                                                     utilities)

            # Modified (right-indentation) to get the best action with the Max Expected Utility
            if expected_utility > max_expected_utility:
                max_expected_utility = expected_utility
                best_action = action

        # Obtain the expected utility with policy π(s), ∑s′ P(s'|s, π(s))U(s')
        policy_expected_utility = _get_expected_utility(mdp,
                                                        state_position,
                                                        policy[state_position],
                                                        utilities)

        # if max a∈A(s) ∑s′ P(s'|s, a) U_π_i(s') > ∑s′ P(s'|s, π[s]) U(s') then update the best policy, π_i+1(s)
        if max_expected_utility > policy_expected_utility:
            updated_policy[state_position] = best_action
            unchanged = False
        else:
            updated_policy[state_position] = policy[state_position]

    return updated_policy, unchanged
