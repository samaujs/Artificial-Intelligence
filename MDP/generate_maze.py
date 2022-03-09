#######################################################################################################
# This file defines the methods for creating a maze based on the following parameters
# - number of green cells (Reward: +1)
# - number of brown cells (Reward: -1)
# - number of wall cells
# - maze_width for constructing squared maze (Default: 2)
#
# Note : The remaining cells will be white (Reward: -0.04)
#
# Filename    : generate_maze.py
# Created by  : Au Jit Seah
#######################################################################################################
import random


def _random_states(num_g_states: int = 1,
                   num_b_states: int = 1,
                   num_w_states: int = 1,
                   maze_width: int = 2):

    # Initialise all states
    states_g = []
    states_b = []
    states_w = []

    for i in range(num_g_states):
        # Using random function to generate state position
        g_row = random.randint(0, maze_width - 1)
        g_col = random.randint(0, maze_width - 1)

        # Generate another state that already exists in 'g' states
        while [g_row, g_col] in states_g:
            g_row = random.randint(0, maze_width - 1)
            g_col = random.randint(0, maze_width - 1)

        states_g.append([g_row, g_col])
        # print("g_row : {}, g_col : {}".format(g_row, g_col))

    for i in range(num_b_states):
        # Using random function to generate state position
        b_row = random.randint(0, maze_width - 1)
        b_col = random.randint(0, maze_width - 1)

        # Generate another state that already exists in 'g' or 'b' states 
        while [b_row, b_col] in states_g or [b_row, b_col] in states_b:
            b_row = random.randint(0, maze_width - 1)
            b_col = random.randint(0, maze_width - 1)

        states_b.append([b_row, b_col])
        # print("b_row : {}, b_col : {}".format(b_row, b_col))

    for i in range(num_w_states):
        # Using random function to generate state position
        w_row = random.randint(0, maze_width - 1)
        w_col = random.randint(0, maze_width - 1)

        # Generate another state that already exists in 'g', 'b' or 'w' states
        while [w_row, w_col] in states_g or [w_row, w_col] in states_b or [w_row, w_col] in states_w:
            w_row = random.randint(0, maze_width - 1)
            w_col = random.randint(0, maze_width - 1)

        states_w.append([w_row, w_col])
        # print("w_row : {}, w_col : {}".format(w_row, w_col))

    # sort() changes the original list
    states_g.sort()
    states_b.sort()
    states_w.sort()

    return states_g, states_b, states_w


def random_maze(num_g_states: int = 1, num_b_states: int = 1, num_w_states: int = 1, maze_width: int = 2):
    # Check parameters are valid
    if num_g_states < 1 or num_b_states < 1 or num_w_states < 1:
        print("The maze must have at least one green, one brown and one wall state!")
        return []

    if (num_g_states + num_b_states + num_w_states) >= pow(maze_width, 2):
        print("The maze dimensions must be larger than sum of all the green, brown and wall states!")
        return []

    # Sorted list of 'g', 'b' and 'w'
    states_g, states_b, states_w = _random_states(num_g_states, num_b_states, num_w_states, maze_width)

    print("Sorted {} Green states : {}".format(len(states_g), states_g))
    print("Sorted {} Brown states : {}".format(len(states_b), states_b))
    print("Sorted {} Wall states : {}".format(len(states_w), states_w))

    maze = []
    maze_height = maze_width  # Squared maze

    cur_state_g_idx = 0
    cur_state_b_idx = 0
    cur_state_w_idx = 0

    for row in range(maze_height):
        maze.append([])

        for col in range(maze_width):
            cur_state_g = states_g[cur_state_g_idx]
            cur_state_b = states_b[cur_state_b_idx]
            cur_state_w = states_w[cur_state_w_idx]

            if row == cur_state_g[0] and col == cur_state_g[1]:
                # print("Current state_g index :", cur_state_g_idx)
                maze[row].append('g')  # green
                if (cur_state_g_idx + 1) < num_g_states:
                    cur_state_g_idx += 1
            elif row == cur_state_b[0] and col == cur_state_b[1]:
                # print("Current state_b index :", cur_state_b_idx)
                maze[row].append('b')  # brown
                if (cur_state_b_idx + 1) < num_b_states:
                    cur_state_b_idx += 1
            elif row == cur_state_w[0] and col == cur_state_w[1]:
                # print("Current state_w index :", cur_state_w_idx)
                maze[row].append('w')  # wall
                if (cur_state_w_idx + 1) < num_w_states:
                    cur_state_w_idx += 1
            else:
                maze[row].append(' ')  # white

    return maze
