#######################################################################################################
# This file defines the maze environment to be solved with Markov Decision Process (MDP)
# - states, s
# - actions, a
# - Transition model, P(s'|s,a)
# - Reward function, R(s)
# - setup the dictionary structure for each valid/possible states with s', a and P(s'|s,a)
# Filename    : maze.py
# Created by  : Au Jit Seah
#######################################################################################################
"""
Classes :
- MazeAction
- Maze

Implements class methods :
- transition_model
- reward_function
- get_next_states

Internal method
- _form_action_next_state_map
"""

import enum
from mdp import MarkovDecisionProcess


class MazeAction(enum.Enum):
    """
    Actions that are available in the maze environment.
    - MazeAction.MOVE_UP.value = 1
    - MazeAction.MOVE_DOWN.value = 2
    - MazeAction.MOVE_LEFT.value = 3
    - MazeAction.MOVE_RIGHT.value = 4
    """
    MOVE_UP = enum.auto()
    MOVE_DOWN = enum.auto()
    MOVE_LEFT = enum.auto()
    MOVE_RIGHT = enum.auto()

# Derived class from base class, MarkovDecisionProcess
class Maze(MarkovDecisionProcess):
    """
    Define Maze as a 2D array where squares of different colour have different rewards :
    - ' ': white, reward = -0.04
    - 'g': green, reward = +1
    - 'b': brown, reward = -1
    - 'w': wall (if agent moves into a wall, it will stays put at the current state)
    """
    # Initialisation with specific order
    def __init__(self, grid, reward_mapping, starting_point, discount_gamma):
        """
        Initialises:
        - states: {
            (row, col): {
                action_1 (MazeAction): {
                    next_state_1 (tuple): probability,
                    next_state_2 (tuple): probability,
                    next_state_3 (tuple): probability
                },
                ...,
                action_4: {
                    next_state_1 (tuple): probability,
                    next_state_2 (tuple): probability,
                    next_state_3 (tuple): probability,
                }
            }
        }
        - actions: list of available actions
        - discount (the future individual state, 0 < γ < 1)
        """
        self.grid = grid
        self.reward_mapping = reward_mapping
        self.starting_point = starting_point

        self.height = len(grid)    # row
        self.width = len(grid[0])  # col

        possible_states = {
            (row, col): {}
            for row in range(self.height)
            for col in range(self.width)
            if grid[row][col] != 'w'  # non-wall states
        }

        # All possible actions for any non-wall states
        possible_actions = [
            MazeAction.MOVE_UP,
            MazeAction.MOVE_DOWN,
            MazeAction.MOVE_LEFT,
            MazeAction.MOVE_RIGHT
        ]

        # Initialise class object
        super().__init__(possible_states, possible_actions, discount_gamma)

        # For all possible state positions, get the next state
        for state_position in possible_states:
            possible_states[state_position] = \
                self._form_action_next_state_map(state_position, possible_actions)


    # Internal method :
    # For all possible actions, initialise all possible states with respective next steps with uncertainties
    def _form_action_next_state_map(self, state, actions):
        """
        params:
        - state (tuple): row, col position
        - actions (list): possible actions can be taken at the given state

        return:
        - For each possible action, return the next states with respective probabilities
        {
            <MazeAction.MOVE_UP: 1>: {
                intended_next_state (tuple): {
                    'actual': actual_next_state (tuple),
                    'probability': 0.8 (float)
                },
                unintended_next_state_1 (tuple): {
                    'actual': unintended_next_state_1 (tuple),
                    'probability': 0.1 (float)
                },
                unintended_next_state_2 (tuple): {
                    'actual': unintended_next_state_2 (tuple),
                    'probability': 0.1 (float)
                },
            }

            <MazeAction.MOVE_DOWN: 2>: { ... similar format as MazeAction.MOVE_UP... },
            <MazeAction.MOVE_LEFT: 3>: { ... similar format as MazeAction.MOVE_UP... },
            <MazeAction.MOVE_RIGHT: 4>: {... similar format as MazeAction.MOVE_UP... }
        }
        """
        return {
            action: self.get_next_states(state, action)
            for action in actions
        }


    def get_next_states(self, state, action: MazeAction):
        """
        params:
        - state (tuple): row, col position
        - action (MazeAction): possible actions can be taken at the given state

        return:
        - dictionary keys (intended_next_state, unintended_next_state_1, unintended_next_state_2) are the
        - next state positions which are adjusted to actual legitimate positions (remain outside wall, within grid)
        {
            intended_next_state (tuple): {
                'actual': actual_next_state (tuple),
                'probability': 0.8 (float)
            },
            unintended_next_state_1 (tuple): {
                'actual': unintended_next_state_1 (tuple),
                'probability': 0.1 (float)
            },
            unintended_next_state_2 (tuple): {
                'actual': unintended_next_state_2 (tuple),
                'probability': 0.1 (float)
            },
        }
        """
        if action is MazeAction.MOVE_UP:
            # Find the above state (row-1, col)
            above_state = (state[0] - 1, state[1])

            if above_state in self.states:
                actual_above_state = above_state 
            else:
                # For invalid state (wall or outside grid), agent remains in the same spot
                actual_above_state = state

            # Find the left state (row, col-1)
            left_state = (state[0], state[1] - 1)

            if left_state in self.states:
                actual_left_state = left_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_left_state = state

            # Find the right state (row, col+1)
            right_state = (state[0], state[1] + 1)

            if right_state in self.states:
                actual_right_state = right_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_right_state = state

            next_states = { 
                above_state: {
                    'actual': actual_above_state,
                    'probability': 0.8,
                }, 
                left_state: {
                    'actual': actual_left_state,
                    'probability': 0.1,
                }, 
                right_state: {
                    'actual': actual_right_state,
                    'probability': 0.1,
                }
            }

        elif action is MazeAction.MOVE_DOWN:
            # Find the below state (row+1, col)
            below_state = (state[0] + 1, state[1])
            
            if below_state in self.states:
                actual_below_state = below_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_below_state = state

            # Find the left state (row, col-1)
            left_state = (state[0], state[1] - 1)
            
            if left_state in self.states:
                actual_left_state = left_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_left_state = state

            # Find the right state (row, col+1)
            right_state = (state[0], state[1] + 1)

            if right_state in self.states:
                actual_right_state = right_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_right_state = state

            next_states = {
                below_state: {
                    'actual': actual_below_state,
                    'probability': 0.8,
                }, 
                left_state: {
                    'actual': actual_left_state,
                    'probability': 0.1,
                }, 
                right_state: {
                    'actual': actual_right_state,
                    'probability': 0.1,
                }
            }

        elif action is MazeAction.MOVE_LEFT:
            # Find the left state (row, col-1)
            left_state = (state[0], state[1] - 1)
            
            if left_state in self.states:
                actual_left_state = left_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_left_state = state

            # Find the above state (row-1, col)
            above_state = (state[0] - 1, state[1])

            if above_state in self.states:
                actual_above_state = above_state
            else:
                # For invalid state, agent remains in the same spot
                actual_above_state = state

            # Find the below state (row+1, col)
            below_state = (state[0] + 1, state[1])

            if below_state in self.states:
                actual_below_state = below_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_below_state = state

            next_states = {
                left_state: {
                    'actual': actual_left_state,
                    'probability': 0.8,
                },
                above_state: {
                    'actual': actual_above_state,
                    'probability': 0.1,
                }, 
                below_state: {
                    'actual': actual_below_state,
                    'probability': 0.1,
                }
            }

        else:  # action is MazeAction.MOVE_RIGHT

            # Find the right state (row, col+1)
            right_state = (state[0], state[1] + 1)

            if right_state in self.states:
                actual_right_state = right_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_right_state = state

            # Find the above state (row-1, col)
            above_state = (state[0] - 1, state[1])

            if above_state in self.states:
                actual_above_state = above_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_above_state = state

            # Find the below state (row+1, col)
            below_state = (state[0] + 1, state[1])

            if below_state in self.states:
                actual_below_state = below_state 
            else:
                # For invalid state, agent remains in the same spot
                actual_below_state = state

            next_states = {
                right_state: {
                    'actual': actual_right_state,
                    'probability': 0.8,
                },
                above_state: {
                    'actual': actual_above_state,
                    'probability': 0.1,
                }, 
                below_state: {
                    'actual': actual_below_state,
                    'probability': 0.1,
                }
            }

        return next_states


    def transition_model(self, state, action, next_state) -> float:
        """
        params
        - state (tuple): row, col position
        - action (MazeAction): take this action at this given state
        - next_state (tuple): intended row, col position

        return:
        probability of the action going to next state from current state
        """

        # Assumes calling method provides value next state (ie key for retrieving the probability)
        # Actual state has been corrected in get_next_states for invalid cases (out of grid or going into wall)
        # Obtain next state based on action
        next_states_with_action = self.states[state][action]

        # If key not found returns default value of 0
        # Returns probability of the selected action going to next state, which ranges from 0 to 1, inclusive (float)
        return next_states_with_action.get(next_state, 0)['probability']


    def reward_function(self, state):
        """
        params:
        - state (tuple): row, col position

        return:
        reward value (float) based on the colour
        """
        # Access list to retrieve colour from grid and used as key for reward_mapping
        colour = self.grid[state[0]][state[1]]
        return self.reward_mapping[colour]
