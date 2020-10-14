from enum import Enum

#Class representing a possible board state
class BoardConfiguration:
    boardSize = 15
    boardList: list
    occupiedSpaces = [] #list of spaces occupied on the board
    def __init__(self):
        self.boardList = [[0 for x in range(self.boardSize)] for y in range(self.boardSize)]
    def placeStone(self, col: int, row: int, player: int):
        self.boardList[col][row] = player
        self.occupiedSpaces.append(Vector(col, row))
        return self

#Represents the current board state of the game
class Board:
    currentGameState : BoardConfiguration
    savedMovesSelf = [] #list representing moves made by the AI player (self)
    savedMovesOpp = [] #list representing moves made by the opposing player
    def __init__(self):
        self.currentGameState = BoardConfiguration()

    #Places a piece on the board
    #row: The row
    #col: The column
    #Player: 1 if AI player, 2 if opponent
    #Returns true if move was successful, false otherwise
    def placeStone(self, col, row, utility, player, moveNum):
        if self.currentGameState.boardList[col][row] != 0 and moveNum != 1: #if the spot on the board is taken and it is not the second
            #move of the game (where placing a piece over another is a legal move)
            return False
        self.currentGameState.placeStone(col, row, player)
        if player == 1:
            self.savedMovesSelf.append(Move(player, col, row, utility, self.currentGameState, 0))
        if player == 2:
            self.savedMovesOpp.append(Move(player, col, row, utility, self.currentGameState, 0))
        return True

class Move: #class representing a move made by either player
    player: int #the player that made the move
    col: int #the row the piece was placed in
    row: int #the column the piece was placed in
    utility: float #the utility represented by the move
    moveXBoardConfig : BoardConfiguration #the board configuration after the move has been made
    moveNum: int #the move number in the game

    def __init__(self, player, col, row, utility, board, moveNum):
        self.player = player
        self.col = col
        self.row = row
        self.utility = utility
        self.moveXBoardConfig = board
        self.moveNum = moveNum

#Class representing a direction
class Vector:
    x: int #x coordinate
    y: int #y coordinate

    def __init__(self, x, y):
        self.x = x
        self.y = y


class MiniMaxNode:
    parent : 'MiniMaxNode' #collection of arbitrary moves to current aribitrary point
    children: list #collection of arbitrary moves representing arbitrary amount of children
    currentVal: int #the metric for utility
    currentMove: Move #the move so as to reference the board state later on

    def __init__(self, parent, children, currentVal, currentMove):
        self.parent = parent
        self.children = children
        self.currentVal = currentVal
        self.currentMove = currentMove

#Enum representing the evaluation values for each path type for calcPathUtil
class pathEvalValues(Enum):
    FIVE = 10 #five in a row
    #TODO fill values
    LIVEFOUR = 9
    DEADFOUR = 8
    LIVETHREE = 7
    DEADTHREE = 6
    LIVETWO = 5
    DEADTWO = 4

class monteNode:
    parent : 'monteNode'
    currentMove: Move
    children: list #
    t: int #keeps track of the value to terminal state
    n: int  #number of times node has been visited

    def __init__(self, parent, children, currentVal, currentMove, currentBoard, t):
        self.parent = parent
        self.children = children
        self.t = 0
        self.n = math.inf
        self.currentMove = Move
