#Class representing a possible board state
class BoardConfiguration:
    boardSize = 15
    boardList: list
    def __init__(self):
        self.boardList = [[0 for x in range(self.boardSize)] for y in range(self.boardSize)]

#Represents the current board state of the game
class Board:
    boardConfiguration : BoardConfiguration
    selfMoves = [] #list representing moves made by the AI player (self)
    oppMoves = [] #list representing moves made by the opposing player
    def __init__(self):
        self.boardConfiguration = BoardConfiguration()

    #Places a piece on the board
    #row: The row
    #col: The column
    #Player: 1 if AI player, 2 if opponent
    def placePiece(self, row, col, utility, player):
        self.boardConfiguration.boardList[row][col] = player
        if player == 1:
            self.selfMoves.append(Move(player, row, col, utility, self.boardConfiguration))
        if player == 2:
            self.oppMoves.append(Move(player, row, col, utility, self.boardConfiguration))

class Move: #class representing a move made by either player
    player: int #the player that made the move
    row: int #the row the piece was placed in
    col: int #the column the piece was placed in
    utility: float #the utility represented by the move
    board : BoardConfiguration #the board configuration after the move has been made

    def __init__(self, player, row, col, utility, board):
        self.player = player
        self.row = row
        self.col = col
        self.utility = utility
        self.board = board