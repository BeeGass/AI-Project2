from os import path
from Board import Board, Vector, BoardConfiguration
import ConfigsEnum, math, paths
import numpy as np
groupName = "Sigmoid"
moveNum = 0 #The move number in the game

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
    print("Waiting for other player. . .")
    while not path.exists(paths.goFile): #waits until it is the player's move
        pass
    if path.exists(paths.endgame):
        #end of game
        print("End of game")
        exit(code=0)
    else:
        #read opponent's move here
        if path.exists(paths.move_file):
            print("Here")
            f = open(paths.move_file).read()
            lines = f.split()
            if not lines == []:
                row = LetterToNumber(lines[1])
                col = int(lines[2])
                board.placePiece(row, col, -1, 2, moveNum) #makes opponent move
                moveNum += 1
            #make move here
            board.currentGameState.boardList[0][0] = 1
            board.currentGameState.boardList[1][1] = 1
            print(str(BoardEval(board, 15, 15, 1)))#TODO same as comment on line 44
            print("Turn "+str(moveNum)+" completed.")#TODO same as comment on line 44
            moveNum += 1 #TODO why are we adding moveNum here again, we already did one time above for the enemy turn
            input("Press any key to continue . . .") #TODO we should probably get rid of this, the 10 second counter starts the moment the referee makes the new file for us, plus running headless will make it faster
        #make move here
        makeMove(board)
        print("Turn "+str(moveNum)+" completed.")
        moveNum += 1
        PlayGame(board) #repeats until game completion

#Gets the optimal move using the minimax algorithm with alpha-beta pruning and performs the move
#board: The current game board
def makeMoveV2(board : Board):
    global moveNum
    ##########
    #first move shit that im not sure of. Pseudo code
    if moveNum is 0 or 1:
        startingMove = makefirstMove(board) #TODO create me father
        #MakeStartingNode(startingMove) #TODO god left me unfinished
        pass
    #########

    #Tree birth: Origins Part 1, the start
    localSpiral(X, Y, listOfPreviousMoves, inputXBoard, inputXPlaceOnBoard, inputYPlaceOnBoard)
    CreateTree(board.currentGameState, depthLimit) #TODO what is the purpose of depthLimit

    #the tree opitimization Saga
    BoardEval(board, inputBoardDimensionX, inputBoardDimensionY, inputPlayerTurn) #TODO is inputPlayerTurn pointless? We are never going to get to run this on an active enemy turn because of the while loop checking for the .go file
    inputMove, inputDepth = AlphaBetaPruning(inputMove, inputDepth, inputAlpha, inputBeta, inputMaximizingPlayer)

    #The minimax and final choice conclusion
    inputRow, inputCol = MiniMax(inputMove, inputDepth, inputMaximizingPlayer) #should produce inputRow and inputCol
    #the submission spinoff
    OutputFile(inputRow, inputCol)

def makeMove(board: Board):
    global moveNum
    global groupName
    r = 0
    c = 0
    utility = 0
    #TODO: implement actual r and c values
    board.placePiece(0, 0, 0, 1, moveNum) #place piece on board
    #write to the file here
    strToWrite = groupName + " " + NumberToLetter(r) + " " + str(c)
    f = open("move_file", "w") #open file to write over
    f.write(strToWrite) #write the inputted move
    f.close()

def makefirstMove(board: board):
    if moveNum is 0:
        board.placePiece(7, 7, utility, 1, moveNum) #TODO how do i get the utility for the first move and why is this stored
    else:
        board.placePiece() #TODO place on top of enemy move if its a good move
#------------------------------------------------------------------

#Tree creation functions
#------------------------------------------------------------------
def MakeStartingNode(inputStartingMove):
    theMove = inputStartingMove
    firstNode = MiniMaxNode(parent = None, children = None, currentVal = theMove.utility, currentMove = theMove)

    return firstNode

def CreateTree(inputStartingMove, depthLimit):
    rootNode = firstNode = MiniMaxNode(parent = None, children = None, currentVal = inputStartingMove.utility, currentMove = inputStartingNode)
    rootNode.children = CreateChildren(rootNode.currentMove, depthLimit, 0)

    return rootNode

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

## genPossibleMoves will iterate through an entire board and find all possible moves that are within 2 spaces of any given piece
def genPossibleMoves(inputMove, player):

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
def getDistance(x2, x1, y2, y1):
    dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

    return dist

##getVector will take in two different points and find the vector associated with the two to create a
#sense of direction to search for a potential continuation of connected stones
def getVector(x2, x1, y2, y1):
    xCoord = x2 - x1
    yCoord = y2 - y1
    orderedPair = Vector(x = xCoord, y = yCoord)

    return orderedPair
#------------------------------------------------------------------

#Board evaluation functions
#------------------------------------------------------------------
def BoardEval(board, inputBoardDimensionX, inputBoardDimensionY, inputPlayerTurn):
    X = inputBoardDimensionX
    Y = inputBoardDimensionY
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
def localSpiral(X, Y, listOfPreviousMoves, inputXBoard, inputXPlaceOnBoard, inputYPlaceOnBoard):

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
        currentPos.x -= 1
        currentPos.y -= 1

    if pathLength == 5:
       return 10
    if block == 2 and not gap: #if the path is obstructed on both sides and there is no gap in the middle, the position is worth nothing
        return 0
    if pathLength == 2:
        return 5

    return 0
#------------------------------------------------------------------



#Algorithms
#------------------------------------------------------------------
#TODO add list of moves
def MiniMax(inputMove, inputDepth, inputMaximizingPlayer):
    #if the input depth is met or the game is over out put the evaluation of how good the move last made was
    if inputDepth == 0 or gameOver:
        positionEval = CalculateSelfUtility()
        return positionEval #nodes associated with evals

    if inputMaximizingPlayer: #this is a boolean value
        maxEval = -math.INF

        for child in inputMove:
            eval = MiniMax(child, inputDepth - 1, false)
            maxEval = max(maxEval, eval)
            return maxEval
    else:
        minEval = math.inf
        for child in inputMove:
            eval = MiniMax(child, depth - 1, true)
            minEval = min(minEval, eval)
            return minEval

#ripped from geek4geeks, returns a single value tho, worth a look
def MinimaxABprune(depth, nodeIndex, maximizingPlayer, values, alpha, beta):
    # Terminating condition. i.e
    # leaf node is reached
    if depth == 3:
        return values[nodeIndex]
    if maximizingPlayer:
        best = MIN
        # Recur for left and right children
        for i in range(0, 2):
            val = MinimaxABprune(depth + 1, nodeIndex * 2 + i, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)
            # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best
    else:
        best = MAX
        # Recur for left and
        # right children
        for i in range(0, 2):
            val = MinimaxABprune(depth + 1, nodeIndex * 2 + i, True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)
            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best
def AlphaBetaPruning(inputMove, inputDepth, inputAlpha, inputBeta, inputMaximizingPlayer):
    if inputDepth == 0 or gameOver:
        positionEval = CalculateSelfUtility()
        return positionEval

    if inputMaximizingPlayer:
        for child in inputMove:
            eval = Minimax(child, inputDepth - 1, inputAlpha, inputBeta, false)
            maxEval = max(maxEval, eval)

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

            return maxEval
    else:
        for child in inputMove:
            eval = Minimax(child, inputDepth - 1, inputAlpha, inputBeta, true)
            minEval = min(minEval, eval)

            beta = min(beta, eval)
            if beta <= alpha:
                break
            return minEval
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

#montecarlo Helper
def UCB1(node):
    vi = None #mean of utility nodes beneath this ones
    N = None # number of times parent node was visited
    ni = None #number of times child node was visited
    ucb = vi + 2*math.sqrt((np.log(N))/ni)

    return ucb

#------------------------------------------------------------------

#File helper functions
#------------------------------------------------------------------

##function to output file with the move of our agent
#format: <groupname> <column> <row>
def OutputFile(inputRow, inputCol):
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
def NumberToLetter(inputColAsNumber):
    theLetter = chr(ord('@') + inputColAsNumber)
    return theLetter

##The opposite of NumberToLetter. It takes in a letter and converts it
#into a number
def LetterToNumber(inputColAsLetter):
    theNumber = ord(inputColAsLetter) - ord('@')
    return theNumber

#------------------------------------------------------------------

#Run the program
if __name__ == '__main__':
    main()
