from os import path
from Board import Board, Vector, BoardConfiguration
import ConfigsEnum, math, paths
groupName = "Sigmoid"

moveNum = 0 #The move number in the game

def main():
    board = Board()
    PlayGame(board) #0 for tie, 1 for AI player wins, 2 for opposing player wins

#Function which will play the Gomoku game until completion
#board: An array represetnation of the game board
def PlayGame(board):
    global moveNum
    #while not path.exists(groupName+".go"): #waits until it is the player's move
    #   pass
    if path.exists(paths.goFile):
        if path.exists(paths.endgame):
            #end of game
            print("End of game")
            exit(code=0)
        else:
            #read opponent's move here
            if path.exists(paths.move_file):
                f = open(paths.move_file).read()
                lines = f.split()
                row = LetterToNumber(lines[1])
                col = int(lines[2])
                board.placePiece(row, col, 0, 2, moveNum) #makes opponent move
                moveNum += 1
                ######TODO This was not indented before, however I think it should be. I commmented this in case Im wrong and we get a bug
                #make move here
                board.currentGameState.boardList[0][0] = 1
                board.currentGameState.boardList[1][1] = 1
                print(str(PerformSpiral(board, 15, 15, 1)))
                print("Turn "+str(moveNum)+" completed.")
                moveNum += 1
                input("Press any key to continue . . .")
                PlayGame(board) #repeats until game completion

#distance formula
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

def PerformSpiral(board, inputBoardDimensionX, inputBoardDimensionY, inputPlayerTurn):
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
            #TODO shoudnt adjX and adjY be lists containing a coordinate? Given that the board is a 2d array
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

def MakeStartingNode(inputStartingMove):
    theMove = inputStartingMove
    firstNode = MiniMaxNode(parent = None, children = None, currentVal = theMove.utility, currentMove = theMove)

    return firstNode

def CreateTree(inputStartingMove, depthLimit):
    rootNode = firstNode = MiniMaxNode(parent = None, children = None, currentVal = inputStartingMove.utility, currentMove = inputStartingNode)
    rootNode.children = CreateChildren(rootNode.currentMove, depthLimit, 0)

def CreateChildren(prevMove, depthLimit, currentDepth):
    children = []
    currentTurn = currentDepth % 2 + 1
    childMoves = genPossibleMoves(prevMove, currentDepth % 2 + 1)

    if (currentDepth >= depthLimit):
        lastChild = []
        return lastChild

    currentDepth += 1
    for move in childMoves:
        children.append(MiniMaxNode(parent  = prevMove, children = CreateChildren(move, depthLimit, currentDepth), currentVal = -1, currentMove = move, evalForNextMove = -1))

    return children


##spiral() will perform a spiraling search from the point that was found at (inputXPlaceOnBoard, inputYPlaceOnBoard).
#The search will search up 2 cells away from the center point and will stop if it finds nothing
#in the event it does find an empty place to potentially put a stone it will add it to the ListOfPreviousPossibleMoves to avoid any potential duplicated moves
#     0   1   2   3   4   5   6   7   8   9  10  11  12  13  14
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
# 0 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
# 1 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
# 2 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
# 3 |   |   |   | X |   |   |   |   |   |   |   |   |   |   |   |
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                            -2  -1   0   1   2
# 4 |   |   |   |   | O | X |   |   |   | O |   |   |   |   |   |                           +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                       -2  |   |   |   |   |   |
# 5 |   |   |   |   | X | O |   |   | X |   |   |   |   |   |   |                           +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                 \     -1  |   | X |   |   |   |
# 6 |   |   |   |   |   |   | O | X |   |   |   |   |   |   |   |     -------------\        +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                   >    0  |   |   | O | X |   |
# 7 |   |   |   |   |   |   | O | X |   |   |   |   |   |   |   |     -------------/        +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                 /      1  |   |   | X | O |   |
# 8 |   |   |   |   |   |   | O | X |   |   |   |   |   |   |   |                           +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                        2  |   |   |   |   | O |
# 9 |   |   |   |   |   |   | X | O |   |   |   |   |   |   |   |                           +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
#10 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                            -2  -1   0   1   2
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                           +---+---+---+---+---+
#11 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                       -2  |END|10→|11→|12→|13↓|
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                           +---+---+---+---+---+
#12 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                 \     -1  |24↑| 9↑| 2→| 3↓|14↓|
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+     -------------\        +---+---+---+---+---+
#13 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                   >    0  |23↑| 8↑| 1↑| 4↓|15↓|
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+     -------------/        +---+---+---+---+---+
#14 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                 /      1  |22↑| 7↑| 6←| 5←|16↓|
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                           +---+---+---+---+---+
#                                                                                        2  |21↑|20←|19←|18←|17←|
#                                                                                           +---+---+---+---+---+
def spiral(X, Y, listOfPreviousMoves, inputXBoard, inputXPlaceOnBoard, inputYPlaceOnBoard):

    # trueX and trueY are the x and y values associated with the real game board
    #this is because it can be thought of that spiral() analyzes a the game board a zoomed in manner
    #treating the inputXPlaceOnBoard, inputYPlaceOnBoard as the center and only viewing 2 cells around it in each axis
    trueX = inputXPlaceOnBoard
    trueY = inputYPlaceOnBoard

    #these are to initialize values associated with performing the spiral function
    x = 0
    y = 0
    dx = 0
    dy = -1

    #List of all possible moves around the piece in question
    ListOfPreviousPossibleMoves = []

    for i in range(max(X, Y)**2):
        vecX = x
        vecY = y

        # adjusts the spiral board so that the center of the spiral board is in the correct coordinate system as the board where the piece lies on.
        #this means that we need to adjust the coordinates and the range the coordinates can fall under aswell
        NegativeXLimit = int((-X/2) + (trueX - 1))
        PositiveXLimit = int((X/2) + (trueX - 1))

        NegativeYLimit = int((-Y/2) + (trueY - 1))
        PositiveYLimit = int((Y/2) + (trueY - 1))

        #adjusts the coordinates aswell
        adjustedX = int(trueX + x)
        adjustedY = int(trueY - y)

        if (NegativeXLimit < adjustedX <= PositiveXLimit) and (NegativeYLimit < adjustedY <= PositiveYLimit):
            theSpot = inputXBoard.boardList[trueX + vecX][trueY - vecY] #the true dimension inputted to find the value of the board at that cell

            if theSpot != 1 and theSpot != 2 and theSpot not in ListOfPreviousPossibleMoves: #if the spot is equal to an open space then add that to possible moves, if not move on to next potential cell
                ListOfPreviousPossibleMoves.append(Vector(x = adjustedX, y = adjustedY)) #add the vector to the list

            else:
                pass

        if adjustedX == adjustedY or (adjustedX < 0 and adjustedX == -adjustedY) or (adjustedX > 0 and adjustedX == 1-adjustedY):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy

    return ListOfPreviousPossibleMoves


## genPossibleMoves will iterate through an entire board and find all possible moves that are within 2 spaces of any given piece
def genPossibleMoves(inputMove, player):l

    inputMove.moveXBoardConfig = inputXBoard
    theNumber = inputMove.moveNum + 1

    #this two define the search space of a given piece should be within 2 blocks of it
    widthOfSearch = 4
    lengthOfSearch = 4

    #Creation of the list that will hold all possible moves on the current board
    ListOfAllPossibleMoves = []

    for i,j in range(len(inputXBoard.boardList[i][j])): #iterate through the board
        #xPlaceOnBoard and yPlaceOnBoard will be referenced within spiral()
        xPlaceOnBoard = i
        yPlaceOnBoard = j

        #get current value at cell (i, j)
        theSpot = inputXBoard.boardList[i][j]

        if theSpot == 1 or theSpot == 2: #if the cell is either a "1" or "2" player search for a possible move
            ListOfMovesForPiece = spiral(widthOfSearch, lengthOfSearch, inputXBoard, xPlaceOnBoard, yPlaceOnBoard) #returns a list of possible moves given the piece found at (i, j)

            for move in ListOfMovesForPiece: #if the move from list of moves found at (i, j) is not within the total list of all possible moves, given the boardstate inputted, add to the list
                if not move in ListOfAllPossibleMoves:
                    ListOfAllPossibleMoves.append(Move(player, row = move.x, col = move.y, utility = -1, board = inputXBoard.boardList.append(move), moveNum = theNumber))

    if ListOfAllPossibleMoves == []: #if the list is empty then no moves have been made and we need to perform the first move
        PerformFirstMove() #TODO: implement this function

    return ListOfAllPossibleMoves #returns all possible moves


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

#TODO add list of moves
def MiniMax(inputPosition, inputDepth, inputMaximizingPlayer):
    #if the input depth is met or the game is over out put the evaluation of how good the move last made was
    if inputDepth == 0 or gameOver:
        positionEval = CalculateSelfUtility()
        return positionEval #nodes associated with evals

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

##getVector will take in two different points and find the vector associated with the two to create a
#sense of direction to search for a potential continuation of connected stones
def getVector(x2, x1, y2, y1):
    xCoord = x2 - x1
    yCoord = y2 - y1
    orderedPair = Vector(x = xCoord, y = yCoord)

    return orderedPair

if __name__ == '__main__':
    main()
