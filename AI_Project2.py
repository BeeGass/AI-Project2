from os import path
import math, paths, copy, sys, time
from Board import Board, Vector, BoardConfiguration, pathEvalValues, Move, MiniMaxNode
#import numpy as np
groupName = "Sigmoid"
moveNum = 0 #The move number in the game
decisionTree: MiniMaxNode #the decision tree for Minimax

#Base game functions
#------------------------------------------------------------------

def main():
    global groupName
    if len(sys.argv) > 1:
        groupName = str(sys.argv[1]) #gets the command line argument and sets the groupname if applicable
    print("Gomoku AI")
    print("---------")
    print("Team name: "+groupName)
    PlayGame(Board()) #0 for tie, 1 for AI player wins, 2 for opposing player wins

#Function which will play the Gomoku game until completion
#board1: An array represetnation of the game board
def PlayGame(board):
    #exit(0)
    global moveNum
    
    print("Waiting for other player. . .")
    while not path.exists(groupName + ".go"): #waits until it is the player's move
        pass
    if path.exists(paths.endgame): #end of game
        print("End of game")
        exit(code=0)
    else:
        #read opponent's move here
        if path.exists(paths.move_file):
            f = open(paths.move_file).read()
            lines = f.split()
            if not lines == []:
                if (lines[0] != groupName):
                    col = LetterToNumber(lines[1])
                    row = int(lines[2]) - 1
                    board.placeStone(col, row, 2, moveNum) #makes opponent move
                    print("Read opponent's move "+str(moveNum))
                    print(lines[1]+" "+lines[2]);
                    moveNum += 1
    #make move here
    makeMove(board)
    print("Turn "+str(moveNum)+" completed.")
    time.sleep(1) #wait 100 ms to make sure the go file has been deleted before continuing
    board = PlayGame(board) #repeats until game completion

#Gets the optimal move using the minimax algorithm with alpha-beta pruning and performs the move
#board: The current game board
def makeMove(board : Board):
    global moveNum
    print("Making move " + str(moveNum))
    if moveNum == 0 or moveNum == 1:
        makefirstMove(board)
    else:
        time1 = time.clock()
        startingNode = MakeStartingNode(board)
        theMove = miniMax(startingNode, 2, math.inf, -math.inf, True).currentMove #TODO: implement function that will dynamically determine input depth based off time left and moveNum
        print("Made move "+str(theMove.col)+" "+str(theMove.row))
        print("Made move in "+str(time.clock() - time1)+"seconds")
        board.placeStone(theMove.col, theMove.row, 1, moveNum)
        OutputFile(theMove.col, theMove.row)

    moveNum += 1
    return board

def makefirstMove(board: Board):
    board.placeStone(7, 7, 1, moveNum)
    OutputFile(7, 7) #puts the stone in the center of the board
    print("Made the first move")
#------------------------------------------------------------------

#Tree creation functions
#------------------------------------------------------------------
#initializes move into a node
#input node
#output MinimaxNode
def MakeStartingNode(inputBoard: Board):
    global moveNum
    firstNode: MiniMaxNode

    if not inputBoard.savedMovesOpp:
        theMove = Move(player = 2, col = -1, row = -1, board = inputBoard.currentGameState, moveNum = moveNum)
    else:
        theMove = inputBoard.savedMovesOpp[-1]

    firstNode = MiniMaxNode(currentVal = -1, currentMove = theMove)
    return firstNode

## genPossibleMoves will iterate through an entire board and find all possible moves that are within 2 spaces of any given piece
def genPossibleMoves(inputMove: Move, player: int):
    newPlayer = 1 if player == 2 else 2

    inputXBoard = inputMove.moveXBoardConfig
    theNumber = inputMove.moveNum + 1

    #Creation of the list that will hold all possible moves on the current board
    ListOfAllPossibleMoves = []

    for position in inputMove.moveXBoardConfig.occupiedSpaces :
        #xPlaceOnBoard and yPlaceOnBoard will be referenced within spiral()
        xPlaceOnBoard = position.x
        yPlaceOnBoard = position.y

        #get current value at cell (i, j)
        theSpot = inputXBoard.boardList[position.x][position.y]

        ListOfMovesForPiece = localSpiral(inputXBoard, xPlaceOnBoard, yPlaceOnBoard) #returns a list of possible moves given the piece found at (i, j)
        #ListOfMovesForPiece = localSpiralReplacement(xPlaceOnBoard, yPlaceOnBoard, inputXBoard)

        for move in ListOfMovesForPiece: #if the move from list of moves found at (i, j) is not within the total list of all possible moves, given the boardstate inputted, add to the list
            newBoard = BoardConfiguration()
            newBoard.boardList = copy.deepcopy(inputXBoard.boardList)
            newBoard.occupiedSpaces = copy.deepcopy(inputXBoard.occupiedSpaces)
            newBoard.placeStone(move.x, move.y, player) 
            ListOfAllPossibleMoves.append(Move(player, col = move.x, row = move.y, board = newBoard, moveNum = theNumber))
    return ListOfAllPossibleMoves #returns all possible moves

def genPossibleMoves2(inputMove: Move, player: int):
    possibleMoves = []
    board = inputMove.moveXBoardConfig
    boundaryList = [(1,0),(0,1),(1,1),(-1,1)]
    for vector in boundaryList:
        posMove = (inputMove.col+vector[0],inputMove.row+vector[1])
        negMove = (inputMove.col-vector[0],inputMove.row-vector[1])
        if inRange(posMove[0], posMove[1]):
            if board.boardList[posMove[0]][posMove[1]] == 0:
                newBoard = BoardConfiguration()
                newBoard.boardList = copy.deepcopy(board.boardList)
                newBoard.occupiedSpaces = copy.deepcopy(board.occupiedSpaces)
                newBoard.placeStone(posMove[0], posMove[1], player)
                possibleMoves.append(Move(player = player, col = posMove[0], row = posMove[1], board = newBoard, moveNum = -1))
        if inRange(negMove[0], negMove[1]):
            if board.boardList[negMove[0]][negMove[1]] == 0:
                newBoard = BoardConfiguration()
                newBoard.boardList = copy.deepcopy(board.boardList)
                newBoard.occupiedSpaces = copy.deepcopy(board.occupiedSpaces)
                newBoard.placeStone(negMove[0], negMove[1], player)
                possibleMoves.append(Move(player = player, col = negMove[0], row = negMove[1], board = newBoard, moveNum = -1))
    return possibleMoves


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
def BoardEval(board: BoardConfiguration, inputPlayerTurn: int):
    oppTurn = 2 if inputPlayerTurn == 1 else 1 #assigns opponent turn to opposite of current turn
    totalUtil = 0
    directions = {Vector(1,0), Vector(0,1), Vector(1,1), Vector(-1,1)}

    for move in board.occupiedSpaces:
        for direction in directions:
            totalUtil += calcPathUtil(board = board, startPos = move, dir = direction, player = inputPlayerTurn)
            totalUtil -= calcPathUtil(board = board, startPos = move, dir = direction, player = oppTurn)

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
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                        2  |   |   |   |   |   |
# 5 |   |   |   |   | X | O |   |   | X |   |   |   |   |   |   |                           +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                 \      1  |   | X |   |   |   |
# 6 |   |   |   |   |   |   | O | X |   |   |   |   |   |   |   |     -------------\        +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                   >    0  |   |   | O | X |   |
# 7 |   |   |   |   |   |   | O | X |   |   |   |   |   |   |   |     -------------/        +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                 /     -1  |   |   | X | O |   |
# 8 |   |   |   |   |   |   | O | X |   |   |   |   |   |   |   |                           +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                       -2  |   |   |   |   | O |
# 9 |   |   |   |   |   |   | X | O |   |   |   |   |   |   |   |                           +---+---+---+---+---+
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
#10 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                            -2  -1   0   1   2
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                           +---+---+---+---+---+
#11 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                        2  |END|10→|11→|12→|13↓|
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                           +---+---+---+---+---+
#12 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                 \      1  |24↑| 9↑| 2→| 3↓|14↓|
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+     -------------\        +---+---+---+---+---+
#13 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                   >    0  |23↑| 8↑| 1↑| 4↓|15↓|
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+     -------------/        +---+---+---+---+---+
#14 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |                 /     -1  |22↑| 7↑| 6←| 5←|16↓|
#   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+                           +---+---+---+---+---+
#                                                                                       -2  |21↑|20←|19←|18←|17←|
#                                                                                           +---+---+---+---+---+
def localSpiral(inputXBoard: Board, inputXPlaceOnBoard: int, inputYPlaceOnBoard: int):

    X = 3#WERE BOTH 3
    Y = 3

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
    ListOfPreviousPossibleMoves = set()
    tempCoordList = []

    for i in range(max(X, Y)**2):
        vecX = x
        vecY = y

        # adjusts the spiral board so that the center of the spiral board is in the correct coordinate system as the board where the piece lies on.
        #this means that we need to adjust the coordinates and the range the coordinates can fall under aswell
        XNegativeLimit = int((-X/2) + trueX)
        #XNegativeLimit = XNegativeLimit - 1

        XPositiveLimit = int((X/2) + trueX)
        #XPositiveLimit = XPositiveLimit - 1


        YNegativeLimit = int((-Y/2) + trueY)
        #YNegativeLimit = YNegativeLimit - 1

        YPositiveLimit = int((Y/2) + trueY)
        #YPositiveLimit = YPositiveLimit - 1

        #adjusts the coordinates aswell
        adjustedX = int(trueX + x)
        adjustedY = int(trueY - y)

        tempCoordList.append(Vector(adjustedX, adjustedY))

        if (-X/2 < x <= X/2) and (-Y/2 < y <= Y/2):
            if inRange(adjustedX, adjustedY):
                theSpot = inputXBoard.boardList[adjustedX][adjustedY] #the true dimension inputted to find the value of the board at that cell
                if theSpot != 1 and theSpot != 2 and theSpot not in ListOfPreviousPossibleMoves: #if the spot is equal to an open space then add that to possible moves, if not move on to next potential cell
                    ListOfPreviousPossibleMoves.add(Vector(x = adjustedX, y = adjustedY)) #add the vector to the list

                else:
                    pass

        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy

    return ListOfPreviousPossibleMoves

def localSpiralReplacement (col: int, row: int, board: BoardConfiguration):
    possibleMoves = []
    dists = {Vector(-2, 2),Vector(-1,2),Vector(0,2),Vector(1,2),Vector(2,2),Vector(-2,1),Vector(-1,1),Vector(0,1),Vector(1,1),Vector(2,1),Vector(-2,0),Vector(-1,0),Vector(1,0),Vector(2,0),Vector(-2,-1),Vector(-1,-1),Vector(0,-1),Vector(1,-1),Vector(2,-1),Vector(-2,-2),Vector(-1,-2),Vector(0,-2),Vector(1,-2),Vector(2,-2)}
    for dist in dists:
        newPos = Vector(col+dist.x,row+dist.y)
        if inRange(newPos.x, newPos.y):
            if board.boardList[newPos.x][newPos.y] == 0:
                possibleMoves.append(newPos)
    return possibleMoves

#Calculates the utility value for a given path
#boardState: The board configuration
#startPos: The vector indicating the path's starting location
#dir: The direction of the path
#player: The player to calculate the util for
def calcPathUtil (board: BoardConfiguration, startPos: Vector, dir: Vector, player: int):
    currentPos = Vector(startPos.x + dir.x, startPos.y + dir.y) #represents the current position in the search
    pathLength = 0 #represents the length of the path
    block = 0 #0 if path is not obstructed on either side, 1 if obstructed on 1 side, 2 if obstructed on both sides
    gap = False #bool representing if there is a gap
    boardState = board.boardList

    #search in the positive direction
    while inRange(currentPos.x, currentPos.y) and pathLength < 5: #makes sure the coords are within the bounds of the board
        if board.boardList[currentPos.x][currentPos.y] == player:
            pathLength += 1 #add to the running total for the current direction
        elif board.boardList[currentPos.x][currentPos.y] != 0: #check to see if it is enemy piece
            block += 1
            break;
        elif board.boardList[currentPos.x][currentPos.y] == 0: #no piece present
            if not gap:
                gap = True
            else:
                gap = False
                break #break out of the for loop if >1 gap is found
        currentPos.x += dir.x
        currentPos.y += dir.y
        #print("first while: " + str(dir.x) + ", " + str(dir.y))

        #todo implement turns

    currentPos = Vector(startPos.x - dir.x, startPos.y - dir.y); #begin search in other direction

    #search in the negative direction
    while inRange(currentPos.x, currentPos.y) and pathLength < 5: #makes sure the coords are within the bounds of the board
        if boardState[currentPos.x][currentPos.y] == player:
            pathLength += 1 #add to the running total for the current direction
        elif boardState[currentPos.x][currentPos.y] != 0: #check to see if it is enemy piece
            block += 1
            break;
        else: #no piece present
            if not gap:
                gap = True
            else:
                gap = False
                break #break out of the for loop if >1 gap is found
        currentPos.x -= dir.x
        currentPos.y -= dir.y

    pathLength += 1 #path length is incremented because all adjacent stones to the starting stone are counted, but the starting stone itself is not

    #return the appropriate eval values based on the path
    if pathLength == 5:
       return pathEvalValues.FIVE.value
    if block >= 2 and not gap: #if the path is obstructed on both sides and there is no gap in the middle, the position is worth nothing
        return 0

    live: bool #indicates if the path is being evaluated as live or not
    live = (gap and block < 2) or (not gap and block < 1)
    #explanation:
    #if there is a gap in the path, it can be blocked on at most 1 side and still be live
    #if no gap exists, it can only be live if there is no block on either side

    if pathLength == 4:
        return pathEvalValues.LIVEFOUR.value if live else pathEvalValues.DEADFOUR.value #ternary to check if the path is live or not
    elif pathLength == 3:
        return pathEvalValues.LIVETHREE.value if live else pathEvalValues.DEADTHREE.value
    elif pathLength == 2:
        return pathEvalValues.LIVETWO.value if live else pathEvalValues.DEADTWO.value
    elif pathLength <= 1: #any path <= 1 in length is not worth anything
        return 0
    return 0

def IsGameOver(inputBoardState: BoardConfiguration):
    boardConfig = inputBoardState.boardList
    for i in range(len(boardConfig)):
        for j in range(len(boardConfig[i])):
            if boardConfig[i][j] != 0:
                currentVal = boardConfig[i][j]
                directions = {Vector(1,0), Vector(0,1), Vector(1,1), Vector(-1,0), Vector(-1,1), Vector(0,-1), Vector(-1,-1), Vector(1,-1)}
                for direction in directions:
                    newPos = Vector(i+direction.x,j+direction.y)
                    if inRange(newPos.x,newPos.y):
                        if boardConfig[newPos.x][newPos.y] == currentVal:
                            if calcPathUtil(inputBoardState, Vector(i,j), direction, currentVal) == pathEvalValues.FIVE.value:
                                return True

    return False

#------------------------------------------------------------------

#Algorithms
#------------------------------------------------------------------

#function that ensures an ordered pair is within the bounds of the board
def inRange(col, row):
    return col >= 0 and col < 15 and row >= 0 and row < 15

def alphaBetaPruning(inputNode: MiniMaxNode, inputDepth: int, alpha: int, beta: int, inputPlayerTurn: bool):
    #stupid problem requires stupid solution
    if type(inputNode) is list:
        inputNode = inputNode[0]

    currentTurn = 1 if inputPlayerTurn else 2 #ternary baby

    gameOver = IsGameOver(inputBoardState = inputNode.currentMove.moveXBoardConfig)
    
    #check if leaf node
    if inputDepth == 0 or gameOver:
        return inputNode

    time0 = time.clock()
    validMoves = genPossibleMoves2(inputMove = inputNode.currentMove, player = currentTurn)
    print("genPossibleMoves ran in "+str(time.clock()-time0)+" seconds")

    if inputPlayerTurn:
        maxNode = MiniMaxNode(currentVal = -math.inf, currentMove = None)
        for move in validMoves:
            currentNode = alphaBetaPruning(inputNode = MiniMaxNode(-1, move), inputDepth = inputDepth-1, alpha = alpha, beta = beta, inputPlayerTurn = False)
            time0 = time.clock()
            currentNode.currentVal = BoardEval(currentNode.currentMove.moveXBoardConfig, currentTurn)
            print("BoardEval ran in "+str(time.clock()-time0)+" seconds")
            if (currentNode.currentVal > maxNode.currentVal):
                maxNode = currentNode
            alpha = max(maxNode.currentVal, alpha)
            if beta <= alpha:
                break
        return maxNode
    else:
        minNode = MiniMaxNode(currentVal = math.inf, currentMove = None)
        for move in validMoves:
            currentNode = alphaBetaPruning(inputNode = MiniMaxNode(-1, move), inputDepth = inputDepth-1, alpha = alpha, beta = beta, inputPlayerTurn = True)
            currentNode.currentVal = BoardEval(currentNode.currentMove.moveXBoardConfig, currentTurn)
            if (currentNode.currentVal < minNode.currentVal):
                minNode = currentNode
            beta = min(minNode.currentVal, beta)
            if beta <= alpha:
                break
        return minNode

def miniMax(inputNode: MiniMaxNode, inputDepth: int, alpha, beta, inputPlayerTurn: bool):
    currentTurn = 1 if inputPlayerTurn else 2 #ternary baby
    validMoves = genPossibleMoves2(inputMove = inputNode.currentMove, player = currentTurn)

    maxNode = MiniMaxNode(currentVal = -math.inf, currentMove = None)
    for move in validMoves:
        currentNode = alphaBetaPruning(inputNode = MiniMaxNode(-1, move), inputDepth = inputDepth, alpha = -math.inf, beta = math.inf, inputPlayerTurn = True)
        if (currentNode.currentVal > maxNode.currentVal):
            maxNode = currentNode
    return maxNode

    ##if maximizing player
    #if inputPlayerTurn and inputDepth >= 0:
    #    maxNode = MiniMaxNode(parent = None, children = None, currentVal = -math.inf, currentMove = None)
    #    #for child in inputNode.children:
    #    #    if type(child) is list:
    #    #        child = child[0]
    #    #    aNode = miniMax(child, inputDepth - 1, alpha, beta, False)
    #    #    #theNode = getNextMoveNode(aNode)
    #    #    if aNode.currentVal > maxNode.currentVal:
    #    #        maxNode = aNode

    #    #    if maxNode.currentVal > alpha.currentVal:
    #    #        alpha = maxNode

    #    #    if beta.currentVal <= alpha.currentVal:
    #    #        break
            

    #    return maxNode

    ##if minimizing player
    #elif not inputPlayerTurn and inputDepth >= 0:
    #    minNode = MiniMaxNode(parent = None, children = None, currentVal = infinity, currentMove = None)
    #    for child in inputNode.children:

    #        if type(child) is list:
    #            child = child[0]
    #        aNode = miniMax(child, inputDepth - 1, alpha, beta, True)
    #        #theNode = getNextMoveNode(aNode)

    #        if aNode.currentVal < minNode.currentVal:
    #            minNode = aNode

    #        if minNode.currentVal < beta.currentVal:
    #            beta = minNode

    #        if beta.currentVal <= alpha.currentVal:
    #            break
    #    # print(minNode)
    #    # print('minNode')
    #    # return minNode
#------------------------------------------------------------------

##function to output file with the move of our agent
#format: <groupname> <column> <row>
def OutputFile(inputCol: int, inputRow: int):
    colLetter = NumberToLetter(inputCol)
    rowNumber = inputRow + 1
    f = open(paths.move_file, "w")
    strToWrite = groupName + " " + colLetter + " " + str(rowNumber)
    f.write(strToWrite)
    f.close()

    return f

##inputCol is the number associated with the column
#that the agent gives which NumberToLetter translates
#into a capital letter associated with the number
#example: 1->A
#         2->B
#         3->C
def NumberToLetter(inputColAsNumber: int):
    theLetter = chr(97 + inputColAsNumber)
    theLetter = theLetter.upper()
    return theLetter

##The opposite of NumberToLetter. It takes in a letter and converts it
#into a number
def LetterToNumber(inputColAsLetter: chr):
    inputColAsLetter = inputColAsLetter.lower()
    theNumber = ord(inputColAsLetter) - 97
    return theNumber

#------------------------------------------------------------------

#Run the program
if __name__ == '__main__':
    main()
