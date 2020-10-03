#Class representing a possible board state
class BoardConfiguration:
    boardSize = 15
    boardList: list
    def __init__(self):
        self.boardList = [[0 for x in range(self.boardSize)] for y in range(self.boardSize)]

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
    def placePiece(self, row, col, utility, player, moveNum):
        if self.currentGameState.boardList[row][col] != 0 and moveNum != 1: #if the spot on the board is taken and it is not the second
            #move of the game (where placing a piece over another is a legal move)
            return False
        self.currentGameState.boardList[row][col] = player
        if player == 1:
            self.savedMovesSelf.append(Move(player, row, col, utility, self.currentGameState, 0))
        if player == 2:
            self.savedMovesOpp.append(Move(player, row, col, utility, self.currentGameState, 0))
        return True
s
class Move: #class representing a move made by either player
    player: int #the player that made the move
    row: int #the row the piece was placed in
    col: int #the column the piece was placed in
    utility: float #the utility represented by the move
    moveXBoardConfig : BoardConfiguration #the board configuration after the move has been made
    moveNum: int #the move number in the game

    def __init__(self, player, row, col, utility, board, moveNum):
        self.player = player
        self.row = row
        self.col = col
        self.utility = utility
        self.moveXBoardConfig = board
        self.moveNum = moveNum

#Class representing a direction
class Vector:
    x: int #horizontal offset
    y: int #vertical offset

    def __init__(self, x, y):
        self.x = x
        self.y = y