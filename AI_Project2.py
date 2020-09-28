import os.path
from os import path
from Board import Board
groupName = "Sigmoid"

def main():
    board = Board()
    result = playGame(board) #0 for tie, 1 for AI player wins, 2 for opposing player wins

#Function which will play the Gomoku game until completion
#board: An array represetnation of the game board
def playGame(board):
    while not path.exists(groupName+".go"): #waits until it is the player's move
       pass
    if path.exists("endgame"):
        #end of game
        print("End of game")
        return 0
    else:
        #read opponent's move here
        f = open("move_file", "rw")

        #make move here
        playGame() #repeats until game completion

def MiniMax(position, depth, alpha, deta, maximizingPlayer):
    """
    if depth == 0 or game over in position then
        return static evaluation of position
    if maximizingPlayer then
        maxEval = −∞
        each child in position
        eval = Minimax(child, depth-1, false)
        maxEval = max(maxEval, eval)
        return maxEval
    else
        minEval = +∞
        each child in position
        eval = Minimax(child, depth-1, true)
        minEval = min(minEval, eval)
        return minEval
    """
    return 1
   

def AlphaBetaPruning():
    """
    if depth == 0 or game over in position then
        return static evaluation of position
    if maximizingPlayer then
        each child in position
        eval = Minimax(child, depth-1, false)
        maxEval = max(maxEval, eval) alpha= max(alpha, eval)
        if beta ≤ alpha break
            return maxEval
    else
        each child in position
        eval = Minimax(child, depth-1, true)
        minEval = min(minEval, eval) beta= max(beta, eval)
    if beta ≤ alpha break
        return minEval
    """
    return 1

#------------------------------------------------------------------
#Heuristics that limit the depth to which the game tree is expanded

def CuttingOffSearch():
    return 1

def IterativeDeepening():
    return 1

def HeuristicContinuation():
    return 1


#------------------------------------------------------------------
#Heuristics that limit the branching factor of the game tree
def TaperedSearch():
    return 1

#------------------------------------------------------------------

##function to determine if its our agents turn
def isOurTurn():
    return 1

##function to read in move_file to determind moves made from opposing agent 
def readFile():
    return 1

##function to output file with the move of our agent
#format: <groupname> <column> <row>
def outputFile():
    return 1

main()