class Board:
    boardSize = 15
    board: list
    selfMoves: list #list representing moves made by the AI player (self)
    oppMoves: list #list representing moves made by the opposing player
    def __init__(self):
        self.board = [[0 for x in range(self.boardSize)] for y in range(self.boardSize)]
        #initializes a 15x15 board
        #0 represents an empty space, 1 represents a space occupied by the AI player, and 2 represents a space occupied by the
        #opposing player

    #Places a piece on the board
    #row: The row
    #col: The column
    #Player: 1 if AI player, 2 if opponent
    def placePiece(row, col, utility, player):
        global selfMoves
        board[row,col] = player
        if player == 1:
            selfMoves.append(Move(player, row, col, 0))
        if player == 2:
            oppMoves.append(Move(player, row, col, 0))

class Move: #class representing a move made by either player
    player: int #the player that made the move
    row: int #the row the piece was placed in
    col: int #the column the piece was placed in
    utility: float #the utility represented by the move
    def __init__(self, player, row, col, utility):
        self.player = player
        self.row = row
        self.col = col
        self.utility = utility