#!/usr/bin/env python2

import rospy
import numpy as np
import time
from board_detection.msg import BoardState
from move_decision.msg import Move  # Import the custom Move message

Rows = 6
Columns = 7
Grid = np.zeros((Rows, Columns), dtype=int)
last_board_state = None  # Track the last board state to detect changes
TurnCounter = 0
winner = 0
player = None
next_move = 0

def print_grid(grid):
    for row in range(Rows):
        print(grid[row])
    print("")

def OpposingPlayer(Player):
    if Player == 1:
        return 2
    else:
        return 1

def Turn(Column, Player):
    if 0 <= Column < Columns:
        for Row in range(Rows-1, -1, -1):  # Looping from the last row down to the first
            if Grid[Row, Column] == 0:
                Grid[Row, Column] = Player
                return 1
    return 0

def UndoTurn(Column):
    for Row in range(Rows):
        if Grid[Row, Column] != 0:
            Grid[Row, Column] = 0
            return 1
    return 0

def CheckForWinner(Grid, Player):
    for Row in range(Rows):
        for Column in range(Columns):
            if Grid[Row, Column] == Player:
                if Column + 3 < Columns:
                    if ((Grid[Row, Column + 1] == Player) and (Grid[Row, Column + 2] == Player) and (Grid[Row, Column + 3] == Player)):
                        return 1
                if Row + 3 < Rows:
                    if ((Grid[Row + 1, Column] == Player) and (Grid[Row + 2, Column] == Player) and (Grid[Row + 3, Column] == Player)):
                        return 1
                if Column + 3 < Columns and Row + 3 < Rows:
                    if ((Grid[Row + 1, Column + 1] == Player) and (Grid[Row + 2, Column + 2] == Player) and (Grid[Row + 3, Column + 3] == Player)):
                        return 1
                if Column - 3 >= 0 and Row + 3 < Rows:
                    if ((Grid[Row + 1, Column - 1] == Player) and (Grid[Row + 2, Column - 2] == Player) and (Grid[Row + 3, Column - 3] == Player)):
                        return 1
    return 0

def Defense(Grid, Player):
    target = OpposingPlayer(Player)
    for column in range(Columns):
        if Turn(column, target):
            if CheckForWinner(Grid, target):
                UndoTurn(column)
                rospy.loginfo("Threat identified on column {}".format(column + 1))
                return column
            UndoTurn(column)
    return 0

def Offense(Grid, Player):
    for column in range(Columns):
        if Turn(column, Player):
            if CheckForWinner(Grid, Player):
                UndoTurn(column)
                rospy.loginfo("Win opportunity identified on column {}".format(column + 1))
                return column
            UndoTurn(column)
    return 0

def EvalPos(Grid, Player):
    score = 0
    for row in range(Rows):
        for column in range(Columns):
            if Grid[row, column] == Player: #score based on position
                score += 4 - abs(3 - column)
                if row >= 3:
                    score += (6 - row)
                else:
                    score += row + 1
            if row > 0:#trap hunter
                if Grid[row, column] == 0:
                    Grid[row, column] = OpposingPlayer(Player)
                    if CheckForWinner(Grid, OpposingPlayer(Player)):
                        score -= 100
                        Grid[row - 1, column] = OpposingPlayer(Player)
                        if CheckForWinner(Grid, OpposingPlayer(Player)):
                            score -= 10000
                        Grid[row - 1, column] = 0
                    Grid[row, column] = 0
    if CheckForWinner(Grid, Player):
        score += 100000
    if CheckForWinner(Grid, OpposingPlayer(Player)):
        score -= 1000000
    return score

def MiniMaxRecursion(Grid, Player, Depth):
    if Depth == 0:
        return None, (EvalPos(Grid, 2))
    if Player == 2:
        BestScore = -np.inf
        Depth -= 1
        for column in range(Columns):
            if Turn(column, Player):
                choice, score = MiniMaxRecursion(Grid, 1, Depth)
                if score > BestScore:
                    BestScore = score
                    BestChoice = column
                UndoTurn(column)
        return BestChoice, BestScore
    if Player == 1:
        WorstScore = np.inf
        Depth -= 1
        for column in range(Columns):
            if Turn(column, Player):
                choice, score = MiniMaxRecursion(Grid, 2, Depth)
                if score < WorstScore:
                    WorstScore = score
                    WorstChoice = column
                UndoTurn(column)
        return WorstChoice, WorstScore

def MiniMaxAI(Grid, Player):
    MaxDepth = 0 #test changing this to: MaxDepth = np.count_nonzero(Grid==0) and delete for loop 
    for row in range(Rows):
        for column in range(Columns):
            if Grid[row, column] == 0:
                MaxDepth += 1
    Depth = 5
    if MaxDepth < Depth:
        Depth = MaxDepth
    choice = Offense(Grid, Player)
    if choice:
        return choice
    choice = Defense(Grid, Player)
    if choice:
        return choice    
    choice, score = MiniMaxRecursion(Grid, Player, Depth)
    return choice

def board_state_callback(msg):
    global Grid, last_board_state, TurnCounter, winner, player
    Grid = np.array(msg.state).reshape((Rows, Columns))

    rospy.loginfo("Current Board State:\n{}".format(Grid))

    if CheckForWinner(Grid, 1):
        rospy.loginfo("Player 1 wins!")
        winner =  1
        
    if CheckForWinner(Grid, 2):
        rospy.loginfo("Player 2 wins!")
        winner = 2


    if np.sum(Grid) % 3 != 0 or winner != 0:  # AI's turn (after human move)
        rospy.loginfo("My turn")
        player = 2
        if last_board_state is None or not np.array_equal(Grid, last_board_state) or winner != 0:
            start = time.time()
            rospy.loginfo("Thinking...")
            next_move = MiniMaxAI(Grid, 2)
            end = time.time()
            TurnCounter += 1

            rospy.loginfo("TIAGo chooses column: {} in {} seconds. Turn #: {}".format(next_move + 1, str(round((end - start), 2)), TurnCounter))
    else:
        player = 1
        next_move = 0
            
    move_msg = Move()
    move_msg.player = player
    move_msg.column = next_move
    move_msg.TurnCounter = TurnCounter
    move_msg.winner =  winner
    move_pub.publish(move_msg)

    last_board_state = Grid.copy()  # Update the last board state to the current one

def main():
    global move_pub
    rospy.init_node('move_decision_node')
    rospy.Subscriber('/board_state', BoardState, board_state_callback)
    move_pub = rospy.Publisher('/ai_move', Move, queue_size=10)
    rospy.loginfo("Move Decision Node Started")
    rospy.spin()

if __name__ == "__main__":
    main()
