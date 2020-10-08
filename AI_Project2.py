#from PIL import Image #this is meme, dont kill me pls
from os import path
import math, paths
from Board import Board, Vector, BoardConfiguration, pathEvalValues, Move, MiniMaxNode
import math, paths
#import numpy as np
groupName = "Sigmoid"
moveNum = 0 #The move number in the game
decisionTree: MiniMaxNode #the decision tree for Minimax

#Base game functions
#------------------------------------------------------------------

def main():
    board = Board()
    PlayGame(board) #0 for tie, 1 for AI player wins, 2 for opposing player wins

#Function which will play the Gomoku game until completion
#board: An array represetnation of the game board
def PlayGame(board):
    #exit(0)
    global moveNum
    while not path.exists(paths.goFile): #waits until it is the player's move
        pass
    if path.exists(paths.endgame):
        #end of game
        print("End of game")
        im = Image.open('img.jpg') #this is meme, dont kill me pls
        im.show('image',im) #this is meme, dont kill me pls
        exit(code=0)
    else:
        #read opponent's move here
        if path.exists(paths.move_file):
            print("Here")
            f = open(paths.move_file).read()
            lines = f.split()
            moveNum += 1
            if not lines == []:
                row = LetterToNumber(lines[1])
                col = int(lines[2])
                board.placePiece(row, col, -1, 2, moveNum) #makes opponent move
    #make move here
    makeMove(board)
    print("Turn "+str(moveNum)+" completed.")
    moveNum += 1
    PlayGame(board) #repeats until game completion

#Gets the optimal move using the minimax algorithm with alpha-beta pruning and performs the move
#board: The current game board
def makeMove(board : Board):
    global moveNum, decisionTree

    ##########
    #first move shit that im not sure of. Pseudo code
    if moveNum == 0 or moveNum == 1:
        startingMove = makefirstMove(board) #TODO create me father
        OutputFile(7, 7)
        startingNode = MakeStartingNode(startingMove)
        #MakeStartingNode(startingMove) #TODO god left me unfinished
        return -69
    #########

    #Minimax doing its thing bruv
    newTree = MiniMaxConAlphaBetaPruning(MinimaxNode(decisionTree, 10, math.INF, math.INF, Move))
    theMove = newTree.currentMove
    decisionTree = newTree
    #the submission spinoff
    board.placePiece(theMove.row, theMove.col, theMove.utility, 1, moveNum)
    OutputFile(theMove.row, theMove.col)

def makefirstMove(board: Board):
    # if moveNum is 0:
    board.placePiece(7, 7, -1, 1, moveNum) #TODO how do i get the utility for the first move and why is this stored
    # else:
        # board.placePiece() #TODO place on top of enemy move if its a good m11
#------------------------------------------------------------------

#Tree creation functions
#------------------------------------------------------------------
#initializes move into a node
#input node
#output MinimaxNode
def MakeStartingNode(inputStartingMove: Move):
    theMove = inputStartingMove
    firstNode = MiniMaxNode(parent = None, children = None, currentVal = theMove.utility, currentMove = theMove)

    return firstNode

#Creates the tree for minimax algorithm to running
#input starting move, depthlimit
def CreateTree(inputCurrentRootNode: MiniMaxNode, depthLimit: int):
    rootNode = inputCurrentRootNode
    rootNode.children = CreateChildrenForTree(inputCurrentRootNode.currentMove, depthLimit, 0)

    return rootNode

def CreateChildrenForTree(prevMove: Move, depthLimit: int, currentDepth: int):
    children = []
    currentTurn = currentDepth % 2 + 1
    childMoves = genPossibleMoves(prevMove, currentTurn)
    emptyChild = []

    if (currentDepth >= depthLimit):
        children.append(MiniMaxNode(parent  = prevMove, children = emptyChild, currentVal = -1, currentMove = move, evalForNextMove = -1))

    else:
        currentDepth += 1
        for move in childMoves:
            children.append(MiniMaxNode(parent  = prevMove, children = CreateChildrenForTree(move, depthLimit, currentDepth), currentVal = -1, currentMove = move, evalForNextMove = -1))

    return children

## genPossibleMoves will iterate through an entire board and find all possible moves that are within 2 spaces of any given piece
def genPossibleMoves(inputMove: Move, player: int):

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
            ListOfMovesForPiece = localSpiral(widthOfSearch, lengthOfSearch, inputXBoard, xPlaceOnBoard, yPlaceOnBoard) #returns a list of possible moves given the piece found at (i, j)

            for move in ListOfMovesForPiece: #if the move from list of moves found at (i, j) is not within the total list of all possible moves, given the boardstate inputted, add to the list
                if not move in ListOfAllPossibleMoves:
                    ListOfAllPossibleMoves.append(Move(player, row = move.x, col = move.y, utility = -1, board = inputXBoard.boardList.append(move), moveNum = theNumber))

    if ListOfAllPossibleMoves == []: #if the list is empty then no moves have been made and we need to perform the first move
        PerformFirstMove() #TODO: implement this function

    return ListOfAllPossibleMoves #returns all possible moves
#------------------------------------------------------------------

#Math helper functions
#------------------------------------------------------------------
#distance formula
def getDistance(x2: int, x1: int, y2: int, y1: int):
    dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

    return dist

##getVector will take in two different points and find the vector associated with the two to create a
#sense of direction to search for a potential continuation of connected stones
def getVector(x2: int, x1: int, y2: int, y1: int):
    xCoord = x2 - x1
    yCoord = y2 - y1
    orderedPair = Vector(x = xCoord, y = yCoord)

    return orderedPair
#------------------------------------------------------------------

#Board evaluation functions
#------------------------------------------------------------------
def BoardEval(board: Board, inputPlayerTurn: int):
    X = 15
    Y = 15

    turn = inputPlayerTurn
    oppTurn = 2 if turn == 1 else 1 #assigns opponent turn to opposite of current turn
    totalUtil = 0 #the utility value to return

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

            if spot != 0:
                if not stoneArrForSelf:
                    stoneArrForSelf = location
                elif stoneArrForSelf:
                    dist = getDistance(stoneArrForSelf[0], location[0], stoneArrForSelf[1], location[1])
                    if dist < 2:
                        stoneCounterForSelf = stoneCounterForSelf + 1
                        #add the utility for the current player and subtract the utility for the opposing player
                        if spot == turn:
                            totalUtil += calcPathUtil(boardConfig.currentGameState.boardList, Vector(stoneArrForSelf[0], stoneArrForSelf[1]), getVector(location[0], stoneArrForSelf[0], location[1], stoneArrForSelf[1]), turn)
                        if spot == oppTurn:
                            totalUtil -= calcPathUtil(boardConfig.currentGameState.boardList, Vector(stoneArrForSelf[0], stoneArrForSelf[1]), getVector(location[0], stoneArrForSelf[0], location[1], stoneArrForSelf[1]), oppTurn)
                        stoneArrForSelf = []
                        stoneArrForSelf = location
                    elif dist > 1:
                        stoneCounterForSelf = 0
                        stoneArrForSelf = []
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy

    return totalUtil

##localSpiral() will perform a spiraling search from the point that was found at (inputXPlaceOnBoard, inputYPlaceOnBoard).
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

def localSpiral(X: int, Y: int, listOfPreviousMoves: list, inputXBoard: Board, inputXPlaceOnBoard: int, inputYPlaceOnBoard: int):

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

#Calculates the utility value for a given path
#boardState: The board configuration
#startPos: The vector indicating the path's starting location
#dir: The direction of the path
#player: The player to calculate the util for
def calcPathUtil (Board: BoardConfiguration, startPos: Vector, dir: Vector, player: int):
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

    #search in the negative direction
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
        currentPos.x -= 1
        currentPos.y -= 1

    #return the appropriate eval values based on the path
    if pathLength == 5:
       return pathEvalValues.FIVE
    if block == 2 and not gap: #if the path is obstructed on both sides and there is no gap in the middle, the position is worth nothing
        return 0

    live: bool #indicates if the path is being evaluated as live or not
    live = (gap and block < 2) or (not gap and block < 1)
    #explanation:
    #if there is a gap in the path, it can be blocked on at most 1 side and still be live
    #if no gap exists, it can only be live if there is no block on either side

    if pathLength == 4:
        return pathEvalValues.LIVEFOUR if live else pathEvalValues.DEADFOUR #ternary to check if the path is live or not
    elif pathLength == 3:
        return pathEvalValues.LIVETHREE if live else pathEvalValues.DEADTHREE
    elif pathLength == 2:
        return pathEvalValues.LIVETWO if live else pathEvalValues.DEADTWO
    elif pathLength <= 1: #any path <= 1 in length is not worth anything
        return 0
    return 0

def IsGameOver(inputBoardState: Board, inputCurrentpathEvalValues: pathEvalValues):
    theGame =  inputBoardState
    pointState = inputBoardState.utility
    gameOver = None
    currentPointVals = inputCurrentpathEvalValues

    if pointState <= 0:
        gameOver = False

    if currentPointVals.FIVE == someValueRepresentingEvalAssociatedWithWinning: #input value here that represents when we win
        gameOver = True

    return gameOver
#------------------------------------------------------------------

#Algorithms
#------------------------------------------------------------------
def MiniMaxConAlphaBetaPruning(inputNode: MiniMaxNode, inputDepth: int, inputAlpha, inputBeta, inputPlayerTurn: bool):
    global decisionTree
    gameOver = IsGameOver(inputNode.move.moveXBoardConfig, eval) #TODO: implement that beh Bryan pls explain purpose of eval
    alpha = inputAlpha
    beta = inputBeta
    infinity = math.INF
    negInfinity = -math.INF

    CreateTree(inputNode, inputDepth)

    if inputDepth == 0 or gameOver:
        inputNode.move.currentVal = BoardEval(inputNode.move.moveXBoardConfig)

        return inputNode

    if inputPlayerTurn:
        maxEval = negInfinity

        for child in startingNode.children:
            aNode = MiniMaxConAlphaBetaPruning(inputNode, inputDepth - 1, inputAlpha, inputBeta, False)

            if aNode.currentVal > maxEval:
                maxEval = aNode.currentVal
                maxNode = aNode

            alpha = max(alpha, aNode.currentVal)
            if beta <= alpha:
                break

        return maxNode

    else:
        minEval = inifinity

        for child in startingNode.children:
            aNode = Minimax(inputNode, inputDepth - 1, inputAlpha, inputBeta, True)

            if aNode.currentVal < minEval:
                minEval = aNode.currentVal
                minNode = aNode

            beta = min(beta, aNode.currentVal)
            if beta <= alpha:
                break

        return minNode
#------------------------------------------------------------------

#------------------------------------------------------------------
#Heuristics that limit the depth to which the game tree is expanded

def IterativeDeepening():
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

"""
#montecarlo Helper
def UCB1(node):
    vi = None #mean of utility nodes beneath this ones
    N = None # number of times parent node was visited
    ni = None #number of times child node was visited
    ucb = vi + 2*math.sqrt((np.log(N))/ni)

    return ucb
"""
#------------------------------------------------------------------

#File helper functions
#------------------------------------------------------------------

##function to output file with the move of our agent
#format: <groupname> <column> <row>
def OutputFile(inputRow: chr, inputCol: int):
    f = open(paths.move_file, "w")
    f.write("Sigmoid {} {}\n".format(inputCol, inputRow))
    f.close

    return f

##inputCol is the number associated with the column
#that the agent gives which NumberToLetter translates
#into a capital letter associated with the number
#example: 1->A
#         2->B
#         3->C
def NumberToLetter(inputColAsNumber: int):
    theLetter = chr(ord('@') + inputColAsNumber)
    return theLetter

##The opposite of NumberToLetter. It takes in a letter and converts it
#into a number
def LetterToNumber(inputColAsLetter: chr):
    theNumber = ord(inputColAsLetter) - ord('@')
    return theNumber

#------------------------------------------------------------------

#Run the program
if __name__ == '__main__':
    main()
