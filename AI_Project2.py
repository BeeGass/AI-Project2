import os.path
from os import path
groupName = "Sigmoid"

def main():
    playGame()

def playGame():
    while not path.exists(groupName+".txt"): #Waits until it is the player's move
        #Make move here

"""
Psuedo code for MiniMax

function Minimax(position, depth, maximizingPlayer)
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


Psuedo code for alpha beta pruning

function Minimax(position, depth, alpha, deta, maximizingPlayer)
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

def MiniMax():
    return 1

def AlphaBetaPruning():
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

def main():
    return 1
