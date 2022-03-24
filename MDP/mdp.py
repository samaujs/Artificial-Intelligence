#######################################################################################################
# This file defines the base class for Markov Decision Process (MDP)
# - states, s
# - actions, a
# - Transition model, P(s'|s,a)
# - Reward function, R(s)
# Filename    : mdp.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
Base class definitions

Abstract Classes :
- MarkovDecisionProcess
"""


class MarkovDecisionProcess:
    """
    Markov property - Transition properties depend only on the current state, not on
    previous history (how that state was reached)
    """
    def __init__(self, states, actions, discount):
        """
        Initialise states, actions and discount.
        """
        self.states = states
        self.actions = actions
        self.discount = discount

    def transition_model(self, state, action, next_state) -> float:
        """
        returns:
        the probability of transitioning into the next state (s'),
        given the current state (s) and action (a)
        """
        pass

    def reward_function(self, state):
        """
        returns:
        the reward obtained at the current state, R(s)
        """
        pass

    def get_next_states(self, state, action):
        """
        params:
        - state (tuple): x, y position
        - action (MazeAction): action to take at the given state

        returns:
        possible next states
        """
        pass
