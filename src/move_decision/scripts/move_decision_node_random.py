#!/usr/bin/env python

import rospy
import numpy as np
from board_detection.msg import BoardState
from move_decision.msg import Move  # Import the custom Move message

Rows = 6
Columns = 7
Grid = np.zeros((Rows, Columns), dtype=int)

def print_grid(grid):
    # Now print without reversing, as the camera feed aligns with the indexing
    for row in range(Rows):
        print(grid[row])
    print("")

def check_for_winner(grid, player):
    for row in range(Rows):
        for column in range(Columns):
            if grid[row, column] == player:
                if column + 3 < Columns:
                    if ((grid[row, column + 1] == player) and (grid[row, column + 2] == player) and (grid[row, column + 3] == player)):
                        return True
                if row + 3 < Rows:
                    if ((grid[row + 1, column] == player) and (grid[row + 2, column] == player) and (grid[row + 3, column] == player)):
                        return True
                if column + 3 < Columns and row + 3 < Rows:
                    if ((grid[row + 1, column + 1] == player) and (grid[row + 2, column + 2] == player) and (grid[row + 3, column + 3] == player)):
                        return True
                if column - 3 >= 0 and row + 3 < Rows:
                    if ((grid[row + 1, column - 1] == player) and (grid[row + 2, column - 2] == player) and (grid[row + 3, column - 3] == player)):
                        return True
    return False

def find_valid_moves(grid):
    valid_moves = []
    for col in range(Columns):
        if grid[0, col] == 0:  # Check the top row now, as that's row 0 in the camera feed
            valid_moves.append(col)
    return valid_moves

def make_random_move(grid, player):
    valid_moves = find_valid_moves(grid)
    return np.random.choice(valid_moves)

def board_state_callback(msg):
    global Grid
    Grid = np.array(msg.state).reshape((Rows, Columns))

    print("Current Board State:")
    print_grid(Grid)

    if check_for_winner(Grid, 1):
        rospy.loginfo("Player 1 wins!")
        return
    if check_for_winner(Grid, 2):
        rospy.loginfo("Player 2 wins!")
        return

    next_move = make_random_move(Grid, 2)
    rospy.loginfo("AI chooses column: {}".format(next_move + 1))

    # Publish the move
    move_msg = Move()
    move_msg.column = next_move
    move_pub.publish(move_msg)

def main():
    global move_pub  # Make the publisher accessible globally
    rospy.init_node('move_decision_node')
    rospy.Subscriber('/board_state', BoardState, board_state_callback)
    move_pub = rospy.Publisher('/ai_move', Move, queue_size=10)  # Define the publisher
    rospy.loginfo("Move Decision Node Started")
    rospy.spin()

if __name__ == "__main__":
    main()
