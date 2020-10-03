import os.path
from os import path
from Board import Board
from Board import BoardConfiguration
from Board import Vector
import ConfigsEnum
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
        board.currentGameState.boardList[0][0] = 1
        board.currentGameState.boardList[1][1] = 1
        print(str(PerformSpiral(board, 15, 15, 1)))
        print("Turn "+str(moveNum)+" completed.")
        moveNum += 1
        input("Press any key to continue . . .")
        return PlayGame(board) #repeats until game completion

def getDistance(x2, x1, y2, y1):
    dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

    return dist

def PerformSpiral(boardConfig, inputBoardDimensionX, inputBoardDimensionY, inputPlayerTurn):
    X = inputBoardDimensionX
    Y = inputBoardDimensionY
    turn = inputPlayerTurn
    oppTurn = 2 if turn == 1 else 1 #assigns opponent turn to opposite of current turn

    totalUtil = 0 #the utility value to return

    NumOfFives = 0 # the number of five-in-row
    NumOfFours = 0 # the number of fours
    NumOfThrees = 0 # the number of threes
    NumOfTwos = 0 # the number of twos
    NumOfOnes = 0 # the number of ones


    x = 0
    y = 0
    dx = 0
    dy = -1
    adjX = 0
    adjY = 0

    stoneArrForOpp = []
    stoneCounterForOpp = 0

    stoneArrForSelf = []
    stoneCounterForSelf = 0

    for i in range(max(X, Y)**2):
        if (int(-X/2) < x <= int(X/2)) and (int(-Y/2) < y <= int(Y/2)):
            location = []
            adjX = x+7
            adjY = y+7
            location.append(adjX)
            location.append(adjY)

            print("X: "+str(adjX)+", Y: "+str(adjY))

            spot = boardConfig.currentGameState.boardList[x][y]

            if spot == 1:

                if not stoneArrForSelf:
                    stoneArrForSelf = location
                elif stoneArrForSelf:
                    dist = getDistance(stoneArrForSelf[0], location[0], stoneArrForSelf[1], location[1])

                    if dist < 2:
                        stoneCounterForSelf = stoneCounterForSelf + 1
                        #add the utility for the current player and subtract the utility for the opposing player
                        totalUtil += calcPathUtil(boardConfig.currentGameState.boardList, Vector(stoneArrForSelf[0], stoneArrForSelf[1]), getVector(location[0], stoneArrForSelf[0], location[1], stoneArrForSelf[1]), turn)
                        totalUtil -= calcPathUtil(boardConfig.currentGameState.boardList, Vector(stoneArrForSelf[0], stoneArrForSelf[1]), getVector(location[0], stoneArrForSelf[0], location[1], stoneArrForSelf[1]), oppTurn)
                        print(totalUtil)
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
            dx, dy = -dy, dx
        x, y = x+dx, y+dy

    return totalUtil

#Calculates the utility value for a given path
def calcPathUtil (boardState, startPos, dir, player):
    currentPos = Vector(startPos.x + dir.x, startPos.y + dir.y); #represents the current position in the search
    pathLength = 1 #represents the length of the path
    block = 0 #0 if path is not obstructed on either side, 1 if obstructed on 1 side, 2 if obstructed on both sides
    gap = False #bool representing if there is a gap

    #search in the positive direction
    while currentPos.x < len(boardState) and currentPos.y < len(boardState[0]) and pathLength < 5: #makes sure the coords are within the bounds of the board
        if boardState[currentPos.x][currentPos.y] == player:
            pathLength += 1 #add to the running total for the current direction
        elif boardState[currentPos.x][currentPos.y] != 0: #check to see if it is enemy piece
            block += 1
            break;
        else: #no piece present
            if not gap:
                gap = True
            else:
                break #break out of the for loop if >1 gap is found
        currentPos.x += 1;
        currentPos.y += 1;

        #todo implement turns

    currentPos = Vector(startPos.x - dir.x, startPos.y - dir.y); #begin search in other direction

    #search in the positive direction
    while currentPos.x > 0 and currentPos.y > 0 and pathLength < 5: #makes sure the coords are within the bounds of the board
        if boardState[currentPos.x][currentPos.y] == player:
            pathLength += 1 #add to the running total for the current direction
        elif boardState[currentPos.x][currentPos.y] != 0: #check to see if it is enemy piece
            block += 1
            break;
        else: #no piece present
            if not gap:
                gap = True
            else:
                break #break out of the for loop if >1 gap is found
        currentPos.x -= 1;
        currentPos.y -= 1;

    if pathLength == 5:
       return 10
    if block == 2 and not gap: #if the path is obstructed on both sides and there is no gap in the middle, the position is worth nothing
        return 0
    if pathLength == 2:
        return 5

    return 0

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

#Gets the two children of an input position
#inputPosition: The BoardConfiguration to generate moves from
def getChildren(inputPosition):
    return None

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

def getVector(x2, x1, y2, y1):
    xCoord = x2 - x1
    yCoord = y2 - y1
    orderedPair = Vector(x = xCoord, y = yCoord)

    return orderedPair

main()