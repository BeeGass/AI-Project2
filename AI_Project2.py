import os.path
from os import path
from Board import Board
from Board import BoardConfiguration
from Board import Vector
from Board import Move

import math
groupName = "Sigmoid"

moveNum = 0 #The move number in the game

def main():
    board = Board()
    result = PlayGame(board) #0 for tie, 1 for AI player wins, 2 for opposing player wins

#Function which will play the Gomoku game until completion
#board: An array represetnation of the game board
def PlayGame(board):
    global moveNum
    #while not path.exists(groupName+".go"): #waits until it is the player's move
    #   pass
    if path.exists("endgame"):
        #end of game
        print("End of game")
        return 0
    else:
        #read opponent's move here
        if path.exists("move_file"):
            f = open("move_file").read()
            lines = f.split()
            row = LetterToNumber(lines[1])
            col = int(lines[2])
            board.placePiece(row, col, 0, 2, moveNum) #makes opponent move
            moveNum += 1
        #make move here
        print("Turn "+str(moveNum)+" completed.")
        moveNum += 1
        input("Press any key to continue . . .")
        PlayGame(board) #repeats until game completion

#Evaluation function that returns the utility value of a given board configuration
#boardConfig: BoardConfiguration, the board config to evaluate
#player: int, the player to evaluate the utility for
def BoardEval(boardConfig, player):
    #ints representing weights for possible stone configurations
    #fiveWeight, liveFourWeight, deadFourWeight, liveThreeWeight, deadThree, liveTwo, deadTwo: int
    #ints representing the counts for each configuration
    fiveCnt, liveFourCnt, deadFourCnt, liveThreeCnt, deadThreeCnt, liveTwoCnt, deadTwoCnt = 0
    eval = 0 #the return value for the function
    #-------------------------
    #scenario for finding a direction of movement
    r = 0
    c = 0
    movementDir = Dir(0,0) #dummy direction for implementation's sake
    successiveCount = 0 #count of successive stones for current player
    totalCount = 0 #count of the total number of stones for current player in the direction the search is looking
    block = False #bool representing if there is a piece blocking on any side
    gap = False #bool representing if there is a gap
    currentPos = Dir(r, c) #represents the current position
    while currentPos.h < len(boardConfig) and currentPos.v < len(boardConfig[0]): #makes sure the coords are within the bounds of the board
        if boardConfig[r+movementDir.h][c+movementDir.v] == player:
            totalCount += 1 #add to the running total for the current direction
            if not gap: successiveCount += 1 #if no gap, add to successive count
        elif boardConfig[r+movementDir.h][c+movementDir.v] != 0: #check to see if it is enemy piece
            if not block:
                block = True
            else:
                break #break out of the for loop once >1 block has been found
        else: #no piece present
            if not gap:
                gap = True
                successiveCount = 0
            else:
                break #break out of the for loop if >1 gap is found

    if totalCount == 5: fiveCnt += 1
    if totalCount == 4:
        if block: deadFourCnt += 1 #if the move is blocked on one side, it is dead
        else: liveFourCnt += 1 #if it is not blocked, it is live
    if totalCount == 3:
        if block: deadThreeCnt += 1
        else: liveThreeCnt
    if totalCount == 2:
        if block: deadTwoCnt += 1
        else: liveTwoCnt += 1
    
    #------------------------------------

    if player == 1:
        eval -= BoardEval(boardConfig, 2) #subtract the opponent's eval score

#------------------------------------------------------------------
def getDistance(x2, x1, y2, y1):
    dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

    return dist

def getVector(x2, x1, y2, y1):
    xCoord = x2 - x1
    yCoord = y2 - y1
    orderedPair = Vector(x = xCoord, y = yCoord)

    return orderedPair
#------------------------------------------------------------------

def isAdjacentCell():
    dist = getDistance()

    if dist > 1: 
        #DO SOME SHIT
        print()
    elif dist == 1:
        #DO SOME SHIT
        print()
    elif dist == 0:
        #YOU GOT A PROBLEM BECAUSE THE DISTANCE SHOULDNT BE 0
        print("Error: distance shouldnt be 0")
    else: 
        print("Error: issue in the isAdjacentCell() function")

def CalculateBoardState():

    return 1

def PerformSpiral(inputBoardDimensionX, inputBoardDimensionY, inputPlayerTurn):
    X = inputBoardDimensionX
    Y = inputBoardDimensionY
    turn = inputPlayerTurn

    NumOfFives = 0 # the number of five-in-row
    NumOfFours = 0 # the number of fours
    NumOfThrees = 0 # the number of threes
    NumOfTwos = 0 # the number of twos
    NumOfOnes = 0 # the number of ones


    x = 0
    y = 0
    dx = 0
    dy = -1

    stoneArrForOpp = []
    stoneCounterForOpp = 0

    stoneArrForSelf = []
    stoneCounterForSelf = 0

    for i in range(max(X, Y)**2):
        if (int(-X/2) < x <= int(X/2)) and (int(-Y/2) < y <= int(Y/2)):
            location = []
            location.append(x)
            location.append(y)

            spot = Board.currentGameState.boardList[x][y]

            if spot == 1:
                if not stoneArrForSelf:
                    stoneArrForSelf = location
                elif stoneArrForSelf:
                    dist = getDistance(stoneArrForSelf[0], location[0], stoneArrForSelf[1], location[1])

                    if dist < 2:
                        stoneCounterForSelf = stoneCounterForSelf + 1
                        stoneArrForSelf = []
                        stoneArrForSelf = location
                    elif dist > 1:
                        if stoneCounterForSelf == 1:
                            NumOfOnes = NumOfOnes + 1

                        elif stoneCounterForSelf == 2:
                            NumOfTwos = NumOfTwos + 1

                        elif stoneCounterForSelf == 3:
                            NumOfThrees = NumOfThrees + 1

                        elif stoneCounterForSelf == 4:
                            NumOfFours = NumOfFours + 1

                        elif stoneCounterForSelf == 5:
                            NumOfFives = NumOfFives + 1

                        else:
                            print("error in the distance portion of PerformSpiral()")

                        stoneCounterForSelf = 0 
                        stoneArrForSelf = []

            elif spot == 2:
                if not stoneArrForSelf:
                    stoneArrForSelf = location
                elif stoneArrForSelf:
                    dist = getDistance(stoneArrForSelf[0], location[0], stoneArrForSelf[1], location[1])

                    if dist < 2:
                        stoneCounterForSelf = stoneCounterForSelf + 1
                        stoneArrForSelf = []
                        stoneArrForSelf = location
                    elif dist > 1:
                        if stoneCounterForSelf == 1:
                            NumOfOnes = NumOfOnes + 1

                        elif stoneCounterForSelf == 2:
                            NumOfTwos = NumOfTwos + 1

                        elif stoneCounterForSelf == 3:
                            NumOfThrees = NumOfThrees + 1

                        elif stoneCounterForSelf == 4:
                            NumOfFours = NumOfFours + 1

                        elif stoneCounterForSelf == 5:
                            NumOfFives = NumOfFives + 1

                        else:
                            print("error in the distance portion of PerformSpiral()")

                        stoneCounterForSelf = 0 
                        stoneArrForSelf = []

        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx = -dy 
            dy = dx
        x = x+dx 
        y = y+dy

def CalculateBoardValue():
    widthOfBoard = 15
    heightOfBoard = 15

    for i in 1:
        if i == 0:
            PerformSpiral(widthOfBoard, heightOfBoard, i)
        elif i == 1: 
            PerformSpiral(widthOfBoard, heightOfBoard, i)
        else: 
            print("error in CalculateBoardValue()")




##Calcultes the utility for home team agent
def CalculateSelfUtility(inputCol, inputRow):
    CalculateBoardValue() 

    """
    w1 × the number of five-in-row
    w2 × the number of live-fours
    w3 × the number of dead-fours
    w4 × the number of live-threes
    w5 × the number of dead-threes
    w6 × the number of live-twos
    w7 × the number of dead-twos
    w8 x the number of live-ones
    w9 x the number of dead-ones
    """

    return 1

##Calcultes the utility for away team agent
def CalculateOpposingUtility():

    return 1

def MiniMax(inputPosition, inputDepth, inputMaximizingPlayer):

    #if the input depth is met or the game is over out put the evaluation of how good the move last made was
    if inputDepth == 0 or gameOver:
        positionEval = CalculateSelfUtility()
        return positionEval

    if inputMaximizingPlayer: #this is a boolean value
        maxEval = -math.INF

        for child in inputPosition:
            eval = MiniMax(child, inputDepth - 1, false)
            maxEval = max(maxEval, eval)
            return maxEval
    else:
        minEval = math.inf
        for child in inputPosition:
            eval = MiniMax(child, depth - 1, true)
            minEval = min(minEval, eval)
            return minEval
   

def AlphaBetaPruning(inputPosition, inputDepth, inputAlpha, inputBeta, inputMaximizingPlayer):
    if inputDepth == 0 or gameOver:
        positionEval = CalculateSelfUtility()
        return positionEval

    if inputMaximizingPlayer: 
        for child in inputPosition:
            eval = Minimax(child, inputDepth - 1, inputAlpha, inputBeta, false)
            maxEval = max(maxEval, eval) 

            alpha = max(alpha, eval)
            if beta <= alpha: 
                break

            return maxEval
    else:
        for child in inputPosition:
            eval = Minimax(child, inputDepth - 1, inputAlpha, inputBeta, true)
            minEval = min(minEval, eval) 

            beta = min(beta, eval)
            if beta <= alpha: 
                break
            return minEval

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
#Big Boi Algorithm 
#https://en.wikipedia.org/wiki/Monte_Carlo_tree_search

def MonteCarloTreeSearch():

    return 1

#------------------------------------------------------------------
##function to read in move_file to determind moves made from opposing agent 
def ReadFile():
    return 1

##inputCol is the number associated with the column 
#that the agent gives which NumberToLetter translates 
#into a capital letter associated with the number
#example: 1->A 
#         2->B
#         3->C
def NumberToLetter(inputColAsNumber):
    theLetter = chr(ord('@') + inputColAsNumber)
    return theLetter

##The opposite of NumberToLetter. It takes in a letter and converts it 
#into a number
def LetterToNumber(inputColAsLetter):
    theNumber = ord(inputColAsLetter) - ord('@')
    return theNumber

##function to output file with the move of our agent
#format: <groupname> <column> <row>
def OutputFile(inputRow, inputCol):
    f = open("move_file", "w")
    f.write("Sigmoid {} {}\n".format(inputCol, inputRow))
    f.close

    return f

#Evaluates the board and returns the utility value
#config: The board configuration
def boardConfigEval(config):
    return 1

main()
